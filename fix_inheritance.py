#!/usr/bin/env python3
"""
[IN]  Dependencies/Inputs:
 - multidim_audit.json (1940 records with research_tier, inherited_from, skipped, etc.)
 - dedup_results.json (1940 records with uniqueness, duplicate_group, canonical_repo)
[OUT] Outputs:
 - multidim_audit.json (updated: inheritance failures fixed, garbage flagged)
 - Backup: multidim_audit.json.bak.phase1a
[POS] Position in the system:
 - Phase 1a post-processing fix. Repairs the canonical_lookup bug in
   audit_multidim.py (line 524-534) where only uniqueness=="canonical" entries
   were indexed, causing 59 fork_copies pointing to variant repos to fail
   inheritance. Also flags 38 entries that inherited garbage data from
   skipped/failed canonicals.

 Change warning: once you modify this file's logic, you must update this
 comment block, and check/update the module doc (README/CLAUDE) in the
 containing folder; update the root global map if necessary.
"""

import json
import shutil
import sys
from collections import Counter
from pathlib import Path

# ─────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────
BASE = Path(__file__).parent
MULTIDIM_FILE = BASE / "multidim_audit.json"
DEDUP_FILE = BASE / "dedup_results.json"
BACKUP_SUFFIX = ".bak.phase1a"

# Fields to copy during inheritance
INHERIT_FIELDS = [
    "research_tier", "research_tier_reason", "research_stages",
    "domain", "added_value", "added_value_reason", "doc_completeness",
]

# Default values that indicate a failed/garbage audit
DEFAULT_TIER_REASON = "No canonical audit available"


def load_json(filepath):
    """Load JSON file with UTF-8 encoding."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    """Save JSON file with UTF-8 encoding, indented for readability."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_dedup_lookup(dedup_results):
    """Build lookup: (skill_name, repo, theme) -> dedup entry."""
    lookup = {}
    for entry in dedup_results:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        lookup[key] = entry
    return lookup


def build_expanded_source_lookup(multidim_results, dedup_results):
    """Build lookup: (skill_name_lower, repo) -> multidim_entry.

    Includes all non-fork_copy entries (original, canonical, variant).
    canonical entries overwrite variant entries for the same key.
    """
    dedup_lookup = build_dedup_lookup(dedup_results)
    lookup = {}

    # First pass: add variant and original entries
    for entry in multidim_results:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        dedup_entry = dedup_lookup.get(key)
        if dedup_entry is None:
            continue
        uniqueness = dedup_entry.get("uniqueness", "")
        if uniqueness == "fork_copy":
            continue
        lkey = (entry["skill_name"].lower(), entry["repo"])
        if uniqueness in ("variant", "original"):
            lookup[lkey] = entry

    # Second pass: canonical overwrites (higher priority)
    for entry in multidim_results:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        dedup_entry = dedup_lookup.get(key)
        if dedup_entry is None:
            continue
        if dedup_entry.get("uniqueness") == "canonical":
            lkey = (entry["skill_name"].lower(), entry["repo"])
            lookup[lkey] = entry

    return lookup


def is_garbage_source(source_entry):
    """Check if a source entry contains garbage data (skipped/default)."""
    if source_entry.get("skipped", False):
        return True
    reason = source_entry.get("research_tier_reason", "")
    if reason == DEFAULT_TIER_REASON:
        return True
    return False


def fix_null_inheritances(multidim_data, dedup_data):
    """Fix fork_copy entries where inherited_from is null.

    Returns (updated_results, stats_dict).
    """
    dedup_lookup = build_dedup_lookup(dedup_data["results"])
    source_lookup = build_expanded_source_lookup(
        multidim_data["results"], dedup_data["results"]
    )

    fixed = 0
    unfixable = 0
    tier_changes = Counter()
    unfixable_list = []

    for entry in multidim_data["results"]:
        # Only process entries with inherited_from explicitly set to null
        if "inherited_from" not in entry:
            continue
        if entry["inherited_from"] is not None:
            continue

        # Find dedup entry for this fork_copy
        dkey = (entry["skill_name"], entry["repo"], entry["theme"])
        dedup_entry = dedup_lookup.get(dkey)
        if dedup_entry is None:
            unfixable += 1
            unfixable_list.append(f"{entry['skill_name']} ({entry['repo']}): no dedup entry")
            continue

        dup_group = dedup_entry.get("duplicate_group", "")
        canon_repo = dedup_entry.get("canonical_repo", "")
        if not dup_group or not canon_repo:
            unfixable += 1
            unfixable_list.append(
                f"{entry['skill_name']} ({entry['repo']}): "
                f"no group={dup_group} or canon={canon_repo}"
            )
            continue

        # Look up source in expanded lookup
        source_key = (dup_group, canon_repo)
        source = source_lookup.get(source_key)
        if source is None:
            unfixable += 1
            unfixable_list.append(
                f"{entry['skill_name']} ({entry['repo']}): "
                f"source not found for ({dup_group}, {canon_repo})"
            )
            continue

        # Copy fields from source
        old_tier = entry.get("research_tier", "D")
        for field in INHERIT_FIELDS:
            if field in source:
                entry[field] = source[field]
        entry["inherited_from"] = canon_repo
        entry["skipped"] = False

        new_tier = entry.get("research_tier", "D")
        if old_tier != new_tier:
            tier_changes[f"{old_tier}->{new_tier}"] += 1
        fixed += 1

    return {
        "fixed": fixed,
        "unfixable": unfixable,
        "unfixable_list": unfixable_list,
        "tier_changes": dict(tier_changes),
    }


def flag_garbage_inheritances(multidim_data, dedup_data):
    """Flag entries that inherited from garbage (skipped/failed) sources.

    Returns (count_flagged, details).
    """
    source_lookup = build_expanded_source_lookup(
        multidim_data["results"], dedup_data["results"]
    )
    dedup_lookup = build_dedup_lookup(dedup_data["results"])

    flagged = 0
    details = []

    for entry in multidim_data["results"]:
        # Only check entries with a non-null inherited_from
        inherited_repo = entry.get("inherited_from")
        if inherited_repo is None or inherited_repo == "":
            continue
        # Already flagged in a previous run
        if entry.get("inherited_quality") == "garbage":
            continue

        # Find the source entry
        source_key = (entry["skill_name"].lower(), inherited_repo)
        source = source_lookup.get(source_key)

        if source is None:
            # Try via dedup group
            dkey = (entry["skill_name"], entry["repo"], entry["theme"])
            dedup_entry = dedup_lookup.get(dkey)
            if dedup_entry:
                dup_group = dedup_entry.get("duplicate_group", "")
                source_key = (dup_group, inherited_repo)
                source = source_lookup.get(source_key)

        if source is not None and is_garbage_source(source):
            entry["inherited_quality"] = "garbage"
            reason = source.get("research_tier_reason", "")
            skipped = source.get("skipped", False)
            details.append({
                "skill": entry["skill_name"],
                "repo": entry["repo"],
                "source_repo": inherited_repo,
                "source_skipped": skipped,
                "source_reason": reason[:80],
            })
            flagged += 1

    return flagged, details


def main():
    """Main entry point for fix_inheritance."""
    print("=" * 60)
    print("Phase 1a: Fix Inheritance Failures & Flag Garbage")
    print("=" * 60)

    # Load data
    print("\n1. Loading data files...")
    multidim_data = load_json(MULTIDIM_FILE)
    dedup_data = load_json(DEDUP_FILE)
    total = len(multidim_data["results"])
    print(f"   Loaded {total} multidim entries, {len(dedup_data['results'])} dedup entries")

    # Pre-fix counts
    null_count = sum(
        1 for e in multidim_data["results"]
        if "inherited_from" in e and e["inherited_from"] is None
    )
    print(f"   inherited_from=null entries: {null_count}")

    # Backup
    print("\n2. Creating backup...")
    backup_path = str(MULTIDIM_FILE) + BACKUP_SUFFIX
    shutil.copy2(MULTIDIM_FILE, backup_path)
    print(f"   Backed up to {backup_path}")

    # Fix null inheritances
    print("\n3. Fixing null inheritances...")
    fix_stats = fix_null_inheritances(multidim_data, dedup_data)
    print(f"   Fixed: {fix_stats['fixed']}")
    print(f"   Unfixable: {fix_stats['unfixable']}")
    if fix_stats["tier_changes"]:
        print("   Tier changes:")
        for change, cnt in sorted(fix_stats["tier_changes"].items()):
            print(f"     {change}: {cnt}")
    if fix_stats["unfixable_list"]:
        print("   Unfixable details:")
        for item in fix_stats["unfixable_list"][:10]:
            print(f"     - {item}")
        if len(fix_stats["unfixable_list"]) > 10:
            print(f"     ... and {len(fix_stats['unfixable_list']) - 10} more")

    # Flag garbage inheritances
    print("\n4. Flagging garbage inheritances...")
    garbage_count, garbage_details = flag_garbage_inheritances(
        multidim_data, dedup_data
    )
    print(f"   Flagged as garbage: {garbage_count}")
    if garbage_details:
        print("   Sample garbage entries:")
        for d in garbage_details[:5]:
            print(f"     - {d['skill']} ({d['repo']}) <- {d['source_repo']}")
            print(f"       source_skipped={d['source_skipped']}, reason={d['source_reason']}")

    # Post-fix verification
    print("\n5. Verification...")
    post_null = sum(
        1 for e in multidim_data["results"]
        if "inherited_from" in e and e["inherited_from"] is None
    )
    post_garbage = sum(
        1 for e in multidim_data["results"]
        if e.get("inherited_quality") == "garbage"
    )
    tier_counts = Counter(e.get("research_tier", "?") for e in multidim_data["results"])
    post_total = len(multidim_data["results"])

    print(f"   inherited_from=null: {null_count} -> {post_null}")
    print(f"   inherited_quality=garbage: {post_garbage}")
    print(f"   Total entries: {post_total} (should be {total})")
    print(f"   Tier distribution: {dict(sorted(tier_counts.items()))}")

    # Validate
    ok = True
    if post_total != total:
        print("   ERROR: Total entry count changed!")
        ok = False
    if post_null > 0 and fix_stats["unfixable"] == 0:
        print("   ERROR: Still have null inheritances but no unfixable reported!")
        ok = False

    # Save
    if ok:
        print("\n6. Saving updated multidim_audit.json...")
        save_json(MULTIDIM_FILE, multidim_data)
        print("   Done!")
    else:
        print("\n6. SKIPPING save due to errors above.")
        sys.exit(1)

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Null inheritances fixed: {fix_stats['fixed']}/{null_count}")
    print(f"  Unfixable: {fix_stats['unfixable']}")
    print(f"  Garbage flagged: {garbage_count}")
    print(f"  Tier changes: {fix_stats['tier_changes']}")
    print("=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
[IN]  Dependencies/Inputs:
 - dedup_results.json (new: after Phase 3a rerun with 0.95 threshold)
 - dedup_results.json.bak.phase3a (old: before Phase 3a)
 - multidim_audit.json (current audit data)
 - audit_results.json (research_relevance, overall_quality for LLM prompt)
 - Final_Research_Skills_Link_Downloads_By_Theme_LATEST/**/SKILL.md
 - API: https://yunwu.ai/v1/chat/completions (claude-haiku-4-5-20251001)
[OUT] Outputs:
 - multidim_audit.json (updated: new variants get independent LLM audit)
 - Backup: multidim_audit.json.bak.phase3b
[POS] Position in the system:
 - Phase 3b repair. After dedup_skills.py raises fork_copy threshold to 0.95,
   ~75 entries change from fork_copy to variant. This script audits those
   new variants via LLM (they previously inherited results, now need independent
   evaluation). Reuses LLM call logic + enhanced JSON extraction from retry_failed.py.

 Change warning: once you modify this file's logic, you must update this
 comment block, and check/update the module doc (README/CLAUDE) in the
 containing folder; update the root global map if necessary.
"""

import json
import os
import shutil
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────
BASE = Path(__file__).parent
MULTIDIM_FILE = BASE / "multidim_audit.json"
DEDUP_FILE = BASE / "dedup_results.json"
OLD_DEDUP_FILE = BASE / "dedup_results.json.bak.phase3a"
AUDIT_FILE = BASE / "audit_results.json"
DOWNLOADS_DIR = BASE / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
BACKUP_SUFFIX = ".bak.phase3b"

# API config (same as audit_multidim.py)
API_URL = os.getenv("BASE_URL", "https://yunwu.ai") + "/v1/chat/completions"
API_KEY = os.getenv("API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"
MAX_RETRIES = 3

# Import shared functions from retry_failed.py
from retry_failed import (
    SYSTEM_PROMPT,
    build_file_index,
    call_llm_enhanced,
    find_skill_file,
    read_skill_content,
)


def load_json(filepath):
    """Load JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    """Save JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_new_variants(old_dedup, new_dedup):
    """Find entries that changed from fork_copy to variant.

    Returns list of (skill_name, repo, theme) tuples.
    """
    old_lookup = {}
    for entry in old_dedup["results"]:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        old_lookup[key] = entry

    new_variants = []
    for entry in new_dedup["results"]:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        old_entry = old_lookup.get(key)
        if old_entry is None:
            continue
        if (old_entry.get("uniqueness") == "fork_copy"
                and entry.get("uniqueness") == "variant"):
            new_variants.append(key)

    return new_variants


def main():
    """Main entry point for audit_new_variants."""
    print("=" * 60)
    print("Phase 3b: Audit New Variants")
    print("=" * 60)

    # Load data
    print("\n1. Loading data files...")
    if not OLD_DEDUP_FILE.exists():
        print(f"   ERROR: Old dedup backup not found: {OLD_DEDUP_FILE}")
        print("   Phase 3a must create this backup before Phase 3b can run.")
        sys.exit(1)

    new_dedup = load_json(DEDUP_FILE)
    old_dedup = load_json(OLD_DEDUP_FILE)
    multidim_data = load_json(MULTIDIM_FILE)
    audit_data = load_json(AUDIT_FILE)
    total = len(multidim_data["results"])
    print(f"   {total} multidim entries loaded")

    # Build audit lookup
    audit_lookup = {}
    for entry in audit_data["results"]:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        audit_lookup[key] = entry

    # Build multidim lookup
    multidim_lookup = {}
    for entry in multidim_data["results"]:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        multidim_lookup[key] = entry

    # Find new variants
    new_variants = find_new_variants(old_dedup, new_dedup)
    print(f"   New variants (fork_copy -> variant): {len(new_variants)}")

    if not new_variants:
        print("   No new variants to audit!")
        return

    # Build file index
    print("\n2. Building file index...")
    build_file_index()

    # Backup
    print("\n3. Creating backup...")
    backup_path = str(MULTIDIM_FILE) + BACKUP_SUFFIX
    shutil.copy2(MULTIDIM_FILE, backup_path)
    print(f"   Backed up to {backup_path}")

    # Audit each new variant
    print(f"\n4. Auditing {len(new_variants)} new variants...")
    audited = 0
    failed = 0
    no_content = 0
    tier_dist = Counter()

    for idx, (skill, repo, theme) in enumerate(new_variants):
        print(f"   [{idx+1}/{len(new_variants)}] {skill} ({repo})...", end=" ")

        # Find SKILL.md
        filepath = find_skill_file(skill, repo)
        content = read_skill_content(filepath)

        if not content:
            print("NO CONTENT")
            no_content += 1
            failed += 1
            # Mark entry as having no content
            entry = multidim_lookup.get((skill, repo, theme))
            if entry:
                entry["skipped"] = True
                entry["research_tier_reason"] = "No SKILL.md content available for evaluation"
                if "inherited_from" in entry:
                    del entry["inherited_from"]
                if "inherited_quality" in entry:
                    del entry["inherited_quality"]
            continue

        # Get audit data for LLM prompt
        audit_entry = audit_lookup.get((skill, repo, theme), {})
        relevance = audit_entry.get("research_relevance", "unknown")
        quality = audit_entry.get("overall_quality", "unknown")

        # Call LLM
        parsed = call_llm_enhanced(skill, repo, relevance, quality, content)

        entry = multidim_lookup.get((skill, repo, theme))
        if entry is None:
            print("ENTRY NOT FOUND")
            failed += 1
            continue

        if parsed is None:
            print("LLM FAILED")
            entry["skipped"] = True
            entry["research_tier_reason"] = "LLM evaluation failed"
            if "inherited_from" in entry:
                del entry["inherited_from"]
            if "inherited_quality" in entry:
                del entry["inherited_quality"]
            failed += 1
            continue

        # Update entry with parsed results
        entry["research_tier"] = parsed.get("research_tier", "D")
        entry["research_tier_reason"] = parsed.get("research_tier_reason", "")
        entry["research_stages"] = parsed.get("research_stages", [])
        if "domain_original" not in entry:
            entry["domain_original"] = entry.get("domain", "")
        entry["domain"] = parsed.get("domain", "unknown")
        entry["added_value"] = parsed.get("added_value", "low")
        entry["added_value_reason"] = parsed.get("added_value_reason", "")
        entry["doc_completeness"] = parsed.get("doc_completeness", {})
        entry["skipped"] = False
        # Remove inheritance markers — now independently audited
        if "inherited_from" in entry:
            del entry["inherited_from"]
        if "inherited_quality" in entry:
            del entry["inherited_quality"]

        tier_dist[entry["research_tier"]] += 1
        audited += 1
        print(f"OK -> tier={entry['research_tier']}")

        # Rate limiting
        if idx < len(new_variants) - 1:
            time.sleep(0.5)

    print(f"\n   Results: {audited} audited, {failed} failed")
    print(f"   ({no_content} had no content)")
    print(f"   Tier distribution: {dict(tier_dist)}")

    # Verification
    print("\n5. Verification...")
    post_total = len(multidim_data["results"])
    print(f"   Total entries: {post_total} (should be {total})")

    ok = True
    if post_total != total:
        print("   ERROR: Total entry count changed!")
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
    print(f"  New variants found: {len(new_variants)}")
    print(f"  Successfully audited: {audited}")
    print(f"  Failed: {failed}")
    print(f"  Tier distribution: {dict(tier_dist)}")
    print("=" * 60)


if __name__ == "__main__":
    main()

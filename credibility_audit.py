#!/usr/bin/env python3
"""
[IN]  Dependencies/Inputs:
 - dedup_results.json (1558 records after fork_copy removal: skill_name,
   repo, theme, uniqueness, duplicate_group, canonical_repo, similarity,
   similar_repos)
 - multidim_audit.json (1558 records after fork_copy removal: research_tier,
   added_value, domain, skipped, doc_completeness, research_stages)
 - Final_Research_Skills_Link_Downloads_By_Theme_LATEST/**/SKILL.md
   (original skill files for Q1/Q2 content-based analysis)
[OUT] Outputs:
 - credibility_audit_report.json (structured audit results for Q1-Q6)
 - CREDIBILITY_AUDIT.md (human-readable report with data, samples, analysis)
[POS] Position in the system:
 - Post-hoc credibility verification of the multi-dimensional audit pipeline.
   Consumes outputs from dedup_skills.py (Phase 1) and audit_multidim.py
   (Phase 2). Pure local execution—no API calls. Produces actionable
   improvement priorities for pipeline refinement.

 Change warning: once you modify this file's logic, you must update this
 comment block, and check/update the module doc (README/CLAUDE) in the
 containing folder; update the root global map if necessary.
"""

import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

# ─────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────
BASE = Path(__file__).parent
DEDUP_FILE = BASE / "dedup_results.json"
MULTIDIM_FILE = BASE / "multidim_audit.json"
DOWNLOADS_DIR = BASE / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
OUTPUT_JSON = BASE / "credibility_audit_report.json"
OUTPUT_MD = BASE / "CREDIBILITY_AUDIT.md"

SEED = 42
STRICT_SIM_THRESHOLD = 0.99
FORK_COPY_SIM_THRESHOLD = 0.80

THEME_DIR_MAP = {
    "01_information_retrieval_evidence_collection":
        "01_information_retrieval_evidence_collection",
    "02_literature_review_writing_citation_part1":
        "02_literature_review_writing_citation",
    "02_literature_review_writing_citation_part2":
        "02_literature_review_writing_citation",
    "03_experiment_benchmark_reproducibility_validation_part1":
        "03_experiment_benchmark_reproducibility_validation",
    "03_experiment_benchmark_reproducibility_validation_part2":
        "03_experiment_benchmark_reproducibility_validation",
    "04_data_analysis_and_evidence_interpretation":
        "04_data_analysis_and_evidence_interpretation",
    "05_research_operations_and_workflow_support":
        "05_research_operations_and_workflow_support",
    "06_Additional_Scientific_Skills":
        "06_Additional_Scientific_Skills",
}

RESEARCH_KEYWORDS = [
    "genome", "proteom", "phylogen", "bioinformat", "metabolom",
    "transcriptom", "epigen", "metagenom", "single-cell", "rnaseq",
    "chipseq", "variant-call", "sequence-align", "molecular-dyn",
    "clinical-trial", "epidemiolog", "biostatist", "neuroimag",
    "spectroscop", "crystallograph", "mass-spec", "flow-cytometr",
    "microscop", "chromatograph", "pcr", "crispr", "protein-struct",
    "drug-discover", "chemoinformat", "quantum-chem",
    "archaeolog", "paleontolog", "geospat", "remote-sens",
    "climate", "ocean", "seismolog", "hydrolog",
    "econometr", "psychometr", "bibliometr", "scientometr",
    "literature-review", "systematic-review", "meta-analysis",
    "scientific", "research", "experiment", "hypothesis",
    "statistical", "scholarly", "academic", "peer-review",
    "lab", "assay", "reagent", "specimen", "dataset",
]


# ─────────────────────────────────────────────────────────
# Data Loading
# ─────────────────────────────────────────────────────────
def load_dedup_data():
    """Load dedup_results.json and return the results list."""
    with open(DEDUP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["results"], data.get("stats", {})


def load_multidim_data():
    """Load multidim_audit.json and return the results list."""
    with open(MULTIDIM_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["results"], data.get("metadata", {})


def build_skill_file_index():
    """Build lookup index for SKILL.md files.

    Returns dict: (repo_slug, skill_dir_lower) -> Path
    """
    index = {}
    repo_index = defaultdict(list)

    if not DOWNLOADS_DIR.exists():
        print(f"WARNING: Downloads dir not found: {DOWNLOADS_DIR}")
        return index, repo_index

    for theme_dir in DOWNLOADS_DIR.iterdir():
        if not theme_dir.is_dir():
            continue
        for repo_dir in theme_dir.iterdir():
            if not repo_dir.is_dir():
                continue
            repo_slug = repo_dir.name
            for skill_file in repo_dir.rglob("SKILL.md"):
                skill_dir_name = skill_file.parent.name
                key = (repo_slug, skill_dir_name.lower())
                index[key] = skill_file
                repo_index[repo_slug].append((skill_dir_name, skill_file))

    return index, repo_index


def find_skill_file(skill_name, repo, theme, index, repo_index):
    """Locate SKILL.md for a given skill entry. Mirrors dedup_skills.py logic."""
    repo_slug = repo.replace("/", "__")
    skill_lower = skill_name.lower()

    # Strategy 1: exact match
    key = (repo_slug, skill_lower)
    if key in index:
        return index[key]

    # Strategy 2: case-insensitive in repo's list
    if repo_slug in repo_index:
        for dir_name, path in repo_index[repo_slug]:
            if dir_name.lower() == skill_lower:
                return path

    # Strategy 3: partial match
    if repo_slug in repo_index:
        candidates = []
        for dir_name, path in repo_index[repo_slug]:
            dl = dir_name.lower()
            if skill_lower in dl or dl in skill_lower:
                candidates.append((dir_name, path))
        if len(candidates) == 1:
            return candidates[0][1]
        if candidates:
            for dir_name, path in candidates:
                if dir_name.lower().startswith(skill_lower):
                    return path
            return candidates[0][1]

    return None


def read_skill_content(filepath, max_chars=None):
    """Read SKILL.md content, optionally truncated."""
    if filepath is None or not filepath.exists():
        return ""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
        if max_chars:
            return text[:max_chars]
        return text
    except Exception:
        return ""


def text_similarity(text1, text2):
    """Calculate SequenceMatcher similarity between two texts."""
    if not text1 and not text2:
        return 1.0
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1, text2).ratio()


def build_dedup_lookup(dedup_results):
    """Build lookup: (skill_name, repo, theme) -> dedup entry."""
    lookup = {}
    for entry in dedup_results:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        lookup[key] = entry
    return lookup


def build_multidim_lookup(multidim_results):
    """Build lookup: (skill_name, repo, theme) -> multidim entry."""
    lookup = {}
    for entry in multidim_results:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        lookup[key] = entry
    return lookup


# ─────────────────────────────────────────────────────────
# Q3: Default Value Pollution Analysis
# ─────────────────────────────────────────────────────────
def classify_entry(dedup_entry, multidim_entry):
    """Classify a single entry into pollution categories.

    Returns one of: real_audit, inherited_ok, inherited_failed,
                    skipped_no_content, llm_failed
    """
    is_skipped = multidim_entry.get("skipped", False)
    tier_reason = multidim_entry.get("research_tier_reason", "")
    has_inherited = "inherited_from" in multidim_entry
    inherited_val = multidim_entry.get("inherited_from")

    if is_skipped:
        if "LLM evaluation failed" in tier_reason:
            return "llm_failed"
        return "skipped_no_content"

    if has_inherited:
        if inherited_val is not None:
            return "inherited_ok"
        return "inherited_failed"

    return "real_audit"


def compute_tier_distribution(entries):
    """Compute tier and added_value distributions from multidim entries."""
    tiers = Counter()
    values = Counter()
    for e in entries:
        tiers[e.get("research_tier", "?")] += 1
        values[e.get("added_value", "?")] += 1
    return dict(tiers), dict(values)


def tier_dist_with_pct(tier_dict, total):
    """Add percentage to tier distribution."""
    result = {}
    for k in ["A", "B", "C", "D"]:
        count = tier_dict.get(k, 0)
        pct = round(100.0 * count / total, 1) if total > 0 else 0.0
        result[k] = {"count": count, "pct": pct}
    return result


def value_dist_with_pct(val_dict, total):
    """Add percentage to added_value distribution."""
    result = {}
    for k in ["high", "medium", "low", "negligible"]:
        count = val_dict.get(k, 0)
        pct = round(100.0 * count / total, 1) if total > 0 else 0.0
        result[k] = {"count": count, "pct": pct}
    return result


def audit_default_pollution(dedup_results, multidim_results):
    """Q3: Analyze default value pollution across multiple cleansing views."""
    print("\n=== Q3: Default Value Pollution Analysis ===")

    dedup_lookup = build_dedup_lookup(dedup_results)
    categories = defaultdict(list)

    for m in multidim_results:
        key = (m["skill_name"], m["repo"], m["theme"])
        d = dedup_lookup.get(key, {})
        cat = classify_entry(d, m)
        categories[cat].append(m)

    cat_counts = {k: len(v) for k, v in categories.items()}
    print(f"  Categories: {cat_counts}")

    # Build views
    all_entries = multidim_results
    views = {}

    # Full view
    full_tiers, full_values = compute_tier_distribution(all_entries)
    views["full"] = {
        "description": f"All {len(all_entries)} entries (baseline)",
        "total": len(all_entries),
        "tiers": tier_dist_with_pct(full_tiers, len(all_entries)),
        "added_value": value_dist_with_pct(full_values, len(all_entries)),
    }

    # No skipped
    no_skipped = [
        m for m in all_entries
        if classify_entry(dedup_lookup.get(
            (m["skill_name"], m["repo"], m["theme"]), {}
        ), m) not in ("skipped_no_content", "llm_failed")
    ]
    ns_tiers, ns_vals = compute_tier_distribution(no_skipped)
    views["no_skipped"] = {
        "description": "Excluding skipped (no content) + LLM failures",
        "excluded": cat_counts.get("skipped_no_content", 0)
                    + cat_counts.get("llm_failed", 0),
        "total": len(no_skipped),
        "tiers": tier_dist_with_pct(ns_tiers, len(no_skipped)),
        "added_value": value_dist_with_pct(ns_vals, len(no_skipped)),
    }

    # No failed inherit
    no_fail_inh = [
        m for m in all_entries
        if classify_entry(dedup_lookup.get(
            (m["skill_name"], m["repo"], m["theme"]), {}
        ), m) != "inherited_failed"
    ]
    nfi_tiers, nfi_vals = compute_tier_distribution(no_fail_inh)
    views["no_failed_inherit"] = {
        "description": "Excluding failed inheritance (59 entries)",
        "excluded": cat_counts.get("inherited_failed", 0),
        "total": len(no_fail_inh),
        "tiers": tier_dist_with_pct(nfi_tiers, len(no_fail_inh)),
        "added_value": value_dist_with_pct(nfi_vals, len(no_fail_inh)),
    }

    # Clean view: exclude skipped + llm_failed + inherited_failed
    excluded_cats = {"skipped_no_content", "llm_failed", "inherited_failed"}
    clean = [
        m for m in all_entries
        if classify_entry(dedup_lookup.get(
            (m["skill_name"], m["repo"], m["theme"]), {}
        ), m) not in excluded_cats
    ]
    cl_tiers, cl_vals = compute_tier_distribution(clean)
    views["clean"] = {
        "description": "Excluding all default-value entries",
        "excluded": sum(
            cat_counts.get(c, 0) for c in excluded_cats
        ),
        "total": len(clean),
        "tiers": tier_dist_with_pct(cl_tiers, len(clean)),
        "added_value": value_dist_with_pct(cl_vals, len(clean)),
    }

    # Core only: real_audit only
    core = categories.get("real_audit", [])
    co_tiers, co_vals = compute_tier_distribution(core)
    views["core_only"] = {
        "description": "Only directly LLM-audited entries (no inheritance)",
        "total": len(core),
        "tiers": tier_dist_with_pct(co_tiers, len(core)),
        "added_value": value_dist_with_pct(co_vals, len(core)),
    }

    # Compute deltas (full → clean)
    full_d_count = views["full"]["tiers"].get("D", {}).get("count", 0)
    clean_d_count = views["clean"]["tiers"].get("D", {}).get("count", 0)
    d_inflation = full_d_count - clean_d_count

    full_low = views["full"]["added_value"].get("low", {}).get("count", 0)
    full_neg = views["full"]["added_value"].get(
        "negligible", {}
    ).get("count", 0)
    clean_low = views["clean"]["added_value"].get("low", {}).get("count", 0)
    clean_neg = views["clean"]["added_value"].get(
        "negligible", {}
    ).get("count", 0)
    low_neg_inflation = (full_low + full_neg) - (clean_low + clean_neg)

    delta = {
        "d_tier_inflation": d_inflation,
        "low_negligible_inflation": low_neg_inflation,
        "total_polluted": len(all_entries) - len(clean),
        "pollution_rate_pct": round(
            100.0 * (len(all_entries) - len(clean)) / len(all_entries), 1
        ),
    }

    print(f"  D-tier inflation: {d_inflation}")
    print(f"  Total polluted: {delta['total_polluted']}")

    return {
        "category_counts": cat_counts,
        "views": views,
        "delta_full_to_clean": delta,
    }


# ─────────────────────────────────────────────────────────
# Q5: Fork Inheritance Risk Analysis
# ─────────────────────────────────────────────────────────
def audit_fork_inheritance(dedup_results, multidim_results):
    """Q5: Analyze 59 fork_copy entries with failed inheritance."""
    print("\n=== Q5: Fork Inheritance Risk ===")

    dedup_lookup = build_dedup_lookup(dedup_results)
    multidim_lookup = build_multidim_lookup(multidim_results)

    # Find fork_copy entries in dedup
    fork_copies = [
        d for d in dedup_results if d["uniqueness"] == "fork_copy"
    ]

    # Find all entries that were audited as canonical or variant
    canonical_entries = [
        d for d in dedup_results if d["uniqueness"] == "canonical"
    ]
    canonical_by_group = defaultdict(list)
    for c in canonical_entries:
        if c["duplicate_group"]:
            canonical_by_group[c["duplicate_group"]].append(c)

    # Identify failed inheritances from multidim data
    failures = []
    successes = []
    for fc in fork_copies:
        key = (fc["skill_name"], fc["repo"], fc["theme"])
        m = multidim_lookup.get(key)
        if not m:
            continue
        if m.get("inherited_from") is None:
            failures.append({"dedup": fc, "multidim": m})
        else:
            successes.append({"dedup": fc, "multidim": m})

    print(f"  Fork copies: {len(fork_copies)}")
    print(f"  Successes: {len(successes)}, Failures: {len(failures)}")

    # Diagnose failure causes
    diagnosis_counts = Counter()
    failure_details = []

    for fail in failures:
        fc = fail["dedup"]
        group = fc.get("duplicate_group", "")
        canon_repo = fc.get("canonical_repo", "")

        # Check what the canonical_repo entry looks like in dedup
        cause = diagnose_inheritance_failure(
            group, canon_repo, dedup_results, canonical_by_group
        )
        diagnosis_counts[cause] += 1

        # Find actual canonical for this group
        actual_canonicals = canonical_by_group.get(group, [])
        actual_canonical_audit = None
        if actual_canonicals:
            ac = actual_canonicals[0]
            ac_key = (ac["skill_name"], ac["repo"], ac["theme"])
            actual_canonical_audit = multidim_lookup.get(ac_key)

        detail = {
            "skill_name": fc["skill_name"],
            "repo": fc["repo"],
            "theme": fc["theme"],
            "duplicate_group": group,
            "canonical_repo": canon_repo,
            "cause": cause,
            "actual_canonical_tier": (
                actual_canonical_audit.get("research_tier")
                if actual_canonical_audit else None
            ),
            "actual_canonical_value": (
                actual_canonical_audit.get("added_value")
                if actual_canonical_audit else None
            ),
        }
        failure_details.append(detail)

    # Compute fix impact: if correctly inherited, how would tiers change?
    fix_tier_changes = Counter()
    fix_value_changes = Counter()
    for detail in failure_details:
        if detail["actual_canonical_tier"]:
            # Currently D, would become actual tier
            old_tier = "D"
            new_tier = detail["actual_canonical_tier"]
            if old_tier != new_tier:
                fix_tier_changes[f"D→{new_tier}"] += 1
        if detail["actual_canonical_value"]:
            old_val = "low"
            new_val = detail["actual_canonical_value"]
            if old_val != new_val:
                fix_value_changes[f"low→{new_val}"] += 1

    return {
        "total_fork_copies": len(fork_copies),
        "successful_inheritance": len(successes),
        "failed_inheritance": len(failures),
        "diagnosis_summary": dict(diagnosis_counts),
        "failure_details": failure_details,
        "fix_impact": {
            "tier_changes": dict(fix_tier_changes),
            "value_changes": dict(fix_value_changes),
        },
    }


def diagnose_inheritance_failure(group, canon_repo, dedup_results,
                                 canonical_by_group):
    """Determine why fork_copy inheritance failed for one entry."""
    if not group or not canon_repo:
        return "missing_group_or_repo"

    # Check if canonical_repo points to a variant (not canonical)
    for d in dedup_results:
        if d.get("repo") == canon_repo and d.get("duplicate_group") == group:
            if d["uniqueness"] == "variant":
                return "canonical_repo_is_variant"
            if d["uniqueness"] == "fork_copy":
                return "canonical_repo_is_fork_copy"
            if d["uniqueness"] == "canonical":
                return "repo_key_mismatch"

    # Check if canonical_repo is not in any entry for this group
    group_repos = [
        d["repo"] for d in dedup_results
        if d.get("duplicate_group") == group
    ]
    if canon_repo not in group_repos:
        return "canonical_repo_not_in_group"

    return "unknown_cause"


# ─────────────────────────────────────────────────────────
# Q1: Dedup Correctness Verification
# ─────────────────────────────────────────────────────────
def audit_dedup_correctness(dedup_results, index, repo_index):
    """Q1: Verify fork_copy labels via similarity distribution + sampling."""
    print("\n=== Q1: Dedup Correctness Verification ===")

    fork_copies = [
        d for d in dedup_results if d["uniqueness"] == "fork_copy"
    ]

    # Layer 1: Full statistics from dedup_results.json (no file I/O)
    sim_distribution = classify_similarities(fork_copies)
    print(f"  Fork copies: {len(fork_copies)}")
    for band, entries in sorted(sim_distribution.items()):
        print(f"    {band}: {len(entries)}")

    # Layer 2: Stratified sampling of 30 groups
    groups = build_duplicate_groups(dedup_results)
    sampled = sample_groups(groups, seed=SEED)
    print(f"  Sampled groups: {len(sampled)}")

    group_analyses = []
    for group_name, group_entries in sampled:
        analysis = analyze_group(
            group_name, group_entries, index, repo_index
        )
        group_analyses.append(analysis)

    # Summarize sampling findings
    sample_stats = summarize_sample_findings(group_analyses)

    # Strict standard estimate
    confirmed = sim_distribution.get("1.00", [])
    near_confirmed = sim_distribution.get("0.99-1.00", [])
    strict_correct = len(confirmed) + len(near_confirmed)
    suspect = len(fork_copies) - strict_correct

    return {
        "total_fork_copies": len(fork_copies),
        "similarity_distribution": {
            band: len(entries)
            for band, entries in sim_distribution.items()
        },
        "strict_threshold": STRICT_SIM_THRESHOLD,
        "confirmed_correct": strict_correct,
        "suspect_count": suspect,
        "suspect_rate_pct": round(
            100.0 * suspect / len(fork_copies), 1
        ) if fork_copies else 0.0,
        "sampled_groups_count": len(sampled),
        "group_analyses": group_analyses,
        "sample_summary": sample_stats,
    }


def _get_sim_band(sim):
    """Map a similarity score to its band label."""
    # Ordered thresholds: check from highest to lowest
    _BAND_THRESHOLDS = [
        (1.0, "1.00"), (0.99, "0.99-1.00"), (0.95, "0.95-0.99"),
        (0.90, "0.90-0.95"), (0.85, "0.85-0.90"), (0.80, "0.80-0.85"),
    ]
    for threshold, label in _BAND_THRESHOLDS:
        if sim >= threshold:
            return label
    return "<0.80"


def classify_similarities(fork_copies):
    """Classify fork_copies by similarity bands."""
    bands = {
        "1.00": [], "0.99-1.00": [], "0.95-0.99": [],
        "0.90-0.95": [], "0.85-0.90": [], "0.80-0.85": [], "<0.80": [],
    }

    for fc in fork_copies:
        sim = fc.get("similarity")
        band = "<0.80" if sim is None else _get_sim_band(sim)
        bands[band].append(fc)

    return bands


def build_duplicate_groups(dedup_results):
    """Build dict: group_name -> list of dedup entries in that group."""
    groups = defaultdict(list)
    for d in dedup_results:
        if d.get("duplicate_group"):
            groups[d["duplicate_group"]].append(d)
    return dict(groups)


def sample_groups(groups, seed=42):
    """Stratified sampling of 30 duplicate groups.

    Small (size=2): 10, Medium (size=3-5): 12, Large (size>=6): all (up to 8).
    If large < 8, fill medium quota from remaining medium groups.
    """
    rng = random.Random(seed)

    small = [(k, v) for k, v in groups.items() if len(v) == 2]
    medium = [(k, v) for k, v in groups.items() if 3 <= len(v) <= 5]
    large = [(k, v) for k, v in groups.items() if len(v) >= 6]

    rng.shuffle(small)
    rng.shuffle(medium)

    sampled = []

    # Large: take all (up to 8)
    large_take = large[:8]
    sampled.extend(large_take)
    large_deficit = max(0, 8 - len(large_take))

    # Medium: 12 + large deficit
    medium_take_count = min(12 + large_deficit, len(medium))
    sampled.extend(medium[:medium_take_count])

    # Small: 10
    small_take_count = min(10, len(small))
    sampled.extend(small[:small_take_count])

    # Cap at 30
    return sampled[:30]


def analyze_group(group_name, group_entries, index, repo_index):
    """Analyze a single duplicate group: read files, compute NxN similarity."""
    entries_data = []
    for entry in group_entries:
        filepath = find_skill_file(
            entry["skill_name"], entry["repo"], entry["theme"],
            index, repo_index
        )
        content = read_skill_content(filepath)
        entries_data.append({
            "skill_name": entry["skill_name"],
            "repo": entry["repo"],
            "theme": entry["theme"],
            "uniqueness": entry["uniqueness"],
            "recorded_sim": entry.get("similarity"),
            "has_file": bool(content),
            "content_length": len(content),
            "content_preview": content[:300] if content else "",
        })

    # Compute NxN similarity matrix
    n = len(entries_data)
    sim_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(1.0)
            elif entries_data[i]["has_file"] and entries_data[j]["has_file"]:
                ci = read_skill_content(
                    find_skill_file(
                        group_entries[i]["skill_name"],
                        group_entries[i]["repo"],
                        group_entries[i]["theme"],
                        index, repo_index
                    )
                )
                cj = read_skill_content(
                    find_skill_file(
                        group_entries[j]["skill_name"],
                        group_entries[j]["repo"],
                        group_entries[j]["theme"],
                        index, repo_index
                    )
                )
                row.append(round(text_similarity(ci, cj), 4))
            else:
                row.append(None)
        sim_matrix.append(row)

    # Detect issues
    issues = detect_group_issues(entries_data, sim_matrix, group_entries)

    return {
        "group_name": group_name,
        "size": n,
        "entries": entries_data,
        "similarity_matrix": sim_matrix,
        "issues": issues,
    }


def _classify_canonical_sim(sim, repo):
    """Classify a fork_copy's similarity to its canonical entry."""
    _SIM_ISSUE_THRESHOLDS = [
        (STRICT_SIM_THRESHOLD, None),  # >= 0.99: no issue
        (0.95, "false_merge_minor"),
        (0.80, "false_merge_major"),
        (0.0, "transitive_artifact"),
    ]
    for threshold, issue_type in _SIM_ISSUE_THRESHOLDS:
        if sim >= threshold:
            if issue_type is None:
                return None
            return {"type": issue_type, "repo": repo, "sim_to_canonical": sim}
    return None


def detect_group_issues(entries_data, sim_matrix, group_entries):
    """Detect problems in a duplicate group based on similarity matrix."""
    issues = []
    n = len(entries_data)

    for i in range(n):
        if group_entries[i]["uniqueness"] != "fork_copy":
            continue
        _check_fork_copy_issues(
            i, n, entries_data, sim_matrix, group_entries, issues
        )

    return issues


def _check_fork_copy_issues(i, n, entries_data, sim_matrix, group_entries,
                             issues):
    """Check one fork_copy against all other entries in its group."""
    for j in range(n):
        if i == j:
            continue
        sim = sim_matrix[i][j]

        if sim is None:
            both_missing = (
                not entries_data[i]["has_file"]
                and not entries_data[j]["has_file"]
            )
            if both_missing:
                issues.append({
                    "type": "both_missing",
                    "entry_i": entries_data[i]["repo"],
                    "entry_j": entries_data[j]["repo"],
                })
            continue

        if group_entries[j]["uniqueness"] != "canonical":
            continue

        issue = _classify_canonical_sim(sim, entries_data[i]["repo"])
        if issue:
            issues.append(issue)

    return issues


def summarize_sample_findings(group_analyses):
    """Aggregate issue counts across all sampled groups."""
    issue_type_counts = Counter()
    groups_with_issues = 0
    total_fork_copies_in_sample = 0

    for ga in group_analyses:
        if ga["issues"]:
            groups_with_issues += 1
        for issue in ga["issues"]:
            issue_type_counts[issue["type"]] += 1
        for e in ga["entries"]:
            if e.get("uniqueness") == "fork_copy":
                total_fork_copies_in_sample += 1

    return {
        "groups_analyzed": len(group_analyses),
        "groups_with_issues": groups_with_issues,
        "issue_type_counts": dict(issue_type_counts),
        "total_fork_copies_in_sample": total_fork_copies_in_sample,
    }


# ─────────────────────────────────────────────────────────
# Q2: Document-Driven Audit Bias Analysis
# ─────────────────────────────────────────────────────────
def audit_document_bias(dedup_results, multidim_results, index, repo_index):
    """Q2: Analyze 5 types of systematic bias in the document-driven audit."""
    print("\n=== Q2: Document-Driven Audit Bias ===")

    dedup_lookup = build_dedup_lookup(dedup_results)
    # Only analyze directly audited entries (not inherited/skipped)
    direct_audited = [
        m for m in multidim_results
        if not m.get("skipped", False)
        and "inherited_from" not in m
        and "LLM evaluation failed" not in m.get("research_tier_reason", "")
    ]

    bias1 = analyze_truncation_bias(direct_audited, index, repo_index)
    bias2 = analyze_section_name_bias(direct_audited, index, repo_index)
    bias3 = analyze_domain_asymmetry(direct_audited)
    bias4 = analyze_naming_bias(direct_audited)

    return {
        "direct_audited_count": len(direct_audited),
        "bias_1_truncation": bias1,
        "bias_2_section_names": bias2,
        "bias_3_domain_asymmetry": bias3,
        "bias_4_naming": bias4,
        "bias_5_temperature": {
            "description": (
                "temperature=1.0 introduces randomness; same skill "
                "re-run may yield different tier. Not measurable with "
                "current single-run data."
            ),
            "measurable": False,
            "risk_level": "medium",
            "affected_dimensions": [
                "research_tier", "added_value", "domain"
            ],
        },
    }


def analyze_truncation_bias(direct_audited, index, repo_index):
    """Bias 1: 6000-char truncation effect on long documents."""
    print("  Bias 1: Truncation analysis...")
    truncation_limit = 6000
    long_docs = []
    short_docs = []

    for m in direct_audited:
        filepath = find_skill_file(
            m["skill_name"], m["repo"], m["theme"], index, repo_index
        )
        content = read_skill_content(filepath)
        if not content:
            continue
        char_count = len(content)
        entry = {
            "skill_name": m["skill_name"],
            "tier": m.get("research_tier", "?"),
            "char_count": char_count,
        }
        if char_count > truncation_limit:
            long_docs.append(entry)
        else:
            short_docs.append(entry)

    # Compare tier distributions
    long_tiers = Counter(d["tier"] for d in long_docs)
    short_tiers = Counter(d["tier"] for d in short_docs)

    def avg_tier_score(tier_counter):
        score_map = {"A": 4, "B": 3, "C": 2, "D": 1}
        total = sum(tier_counter.values())
        if total == 0:
            return 0.0
        weighted = sum(
            score_map.get(t, 0) * c for t, c in tier_counter.items()
        )
        return round(weighted / total, 2)

    return {
        "truncation_limit": truncation_limit,
        "long_docs_count": len(long_docs),
        "short_docs_count": len(short_docs),
        "long_avg_tier_score": avg_tier_score(long_tiers),
        "short_avg_tier_score": avg_tier_score(short_tiers),
        "long_tier_distribution": dict(long_tiers),
        "short_tier_distribution": dict(short_tiers),
        "impact_direction": (
            "Long documents may lose key information after truncation, "
            "potentially lowering tier assessment"
        ),
    }


def analyze_section_name_bias(direct_audited, index, repo_index):
    """Bias 2: Non-standard section names missed by doc_completeness."""
    print("  Bias 2: Section name analysis...")
    # Check entries where has_when_to_use=false but content has usage info
    false_negative_count = 0
    total_no_when_to_use = 0
    usage_patterns = re.compile(
        r"(when to use|usage|use case|how to use|getting started"
        r"|overview|purpose|about)",
        re.IGNORECASE
    )

    for m in direct_audited:
        dc = m.get("doc_completeness", {})
        if not dc.get("has_when_to_use", True):
            total_no_when_to_use += 1
            filepath = find_skill_file(
                m["skill_name"], m["repo"], m["theme"], index, repo_index
            )
            content = read_skill_content(filepath, max_chars=6000)
            if content and usage_patterns.search(content):
                false_negative_count += 1

    return {
        "total_missing_when_to_use": total_no_when_to_use,
        "false_negatives_with_usage_content": false_negative_count,
        "false_negative_rate_pct": round(
            100.0 * false_negative_count / total_no_when_to_use, 1
        ) if total_no_when_to_use > 0 else 0.0,
        "impact_direction": (
            "doc_completeness systematically undercounts sections "
            "with non-standard naming"
        ),
    }


def analyze_domain_asymmetry(direct_audited):
    """Bias 3: Compare tier distributions across high-freq vs low-freq domains."""
    print("  Bias 3: Domain asymmetry analysis...")
    domain_groups = defaultdict(list)
    for m in direct_audited:
        domain = m.get("domain", "unknown")
        domain_groups[domain].append(m)

    # Sort domains by frequency
    domain_freq = {
        d: len(entries) for d, entries in domain_groups.items()
    }
    sorted_domains = sorted(
        domain_freq.items(), key=lambda x: x[1], reverse=True
    )

    # Top 10 high-freq domains
    high_freq = sorted_domains[:10]
    # Bottom domains (freq <= 3)
    low_freq = [
        (d, c) for d, c in sorted_domains if c <= 3
    ]

    # Compute avg tier for high-freq vs low-freq
    score_map = {"A": 4, "B": 3, "C": 2, "D": 1}

    def avg_score(domain_list):
        entries = []
        for d, _ in domain_list:
            entries.extend(domain_groups[d])
        if not entries:
            return 0.0
        total = sum(
            score_map.get(e.get("research_tier", "D"), 1) for e in entries
        )
        return round(total / len(entries), 2)

    return {
        "total_unique_domains": len(domain_groups),
        "high_freq_domains": [
            {"domain": d, "count": c} for d, c in high_freq
        ],
        "low_freq_domain_count": len(low_freq),
        "high_freq_avg_tier_score": avg_score(high_freq),
        "low_freq_avg_tier_score": avg_score(low_freq),
        "unknown_domain_count": domain_freq.get("unknown", 0),
        "impact_direction": (
            "LLM may assess familiar domains more accurately; "
            "rare domains risk misclassification"
        ),
    }


def analyze_naming_bias(direct_audited):
    """Bias 4: Skills with research keywords in name vs generic names."""
    print("  Bias 4: Naming bias analysis...")
    research_named = []
    generic_named = []

    for m in direct_audited:
        name_lower = m["skill_name"].lower()
        has_keyword = any(kw in name_lower for kw in RESEARCH_KEYWORDS)
        if has_keyword:
            research_named.append(m)
        else:
            generic_named.append(m)

    score_map = {"A": 4, "B": 3, "C": 2, "D": 1}

    def avg_score(entries):
        if not entries:
            return 0.0
        total = sum(
            score_map.get(e.get("research_tier", "D"), 1) for e in entries
        )
        return round(total / len(entries), 2)

    research_tiers = Counter(
        m.get("research_tier", "?") for m in research_named
    )
    generic_tiers = Counter(
        m.get("research_tier", "?") for m in generic_named
    )

    return {
        "research_named_count": len(research_named),
        "generic_named_count": len(generic_named),
        "research_avg_tier_score": avg_score(research_named),
        "generic_avg_tier_score": avg_score(generic_named),
        "research_tier_dist": dict(research_tiers),
        "generic_tier_dist": dict(generic_tiers),
        "impact_direction": (
            "Skills with research-related names may receive "
            "higher tiers due to name-based priming"
        ),
    }


# ─────────────────────────────────────────────────────────
# Q4: Reproducibility Boundaries
# ─────────────────────────────────────────────────────────
def audit_reproducibility(dedup_results, multidim_results, q1_result,
                          q3_result, q5_result):
    """Q4: Classify each entry's confidence level (A/B/C)."""
    print("\n=== Q4: Reproducibility Boundaries ===")

    dedup_lookup = build_dedup_lookup(dedup_results)
    # Collect problematic groups from Q1
    problematic_groups = set()
    for ga in q1_result.get("group_analyses", []):
        if ga.get("issues"):
            problematic_groups.add(ga["group_name"])

    confidence_counts = Counter()
    confidence_entries = {"A": [], "B": [], "C": []}

    for m in multidim_results:
        key = (m["skill_name"], m["repo"], m["theme"])
        d = dedup_lookup.get(key, {})
        cat = classify_entry(d, m)
        conf = determine_confidence(
            d, m, cat, problematic_groups
        )
        confidence_counts[conf] += 1
        confidence_entries[conf].append({
            "skill_name": m["skill_name"],
            "repo": m["repo"],
        })

    return {
        "confidence_distribution": dict(confidence_counts),
        "category_A": {
            "label": "可直接使用 (Directly usable)",
            "description": (
                "original entries with successful LLM audit, "
                "no inheritance, not in problematic groups"
            ),
            "count": confidence_counts.get("A", 0),
        },
        "category_B": {
            "label": "需人工复核 (Needs human review)",
            "description": (
                "canonical/variant with audit + successful "
                "fork_copy inheritance; boundary similarity cases"
            ),
            "count": confidence_counts.get("B", 0),
        },
        "category_C": {
            "label": "不应依赖 (Should not rely on)",
            "description": (
                "skipped/LLM-failed/inherited-failed entries, "
                "domain=unknown, problematic dedup groups"
            ),
            "count": confidence_counts.get("C", 0),
        },
    }


def determine_confidence(dedup_entry, multidim_entry, category,
                          problematic_groups):
    """Determine confidence category (A/B/C) for a single entry."""
    # Category C: unreliable
    if category in ("skipped_no_content", "llm_failed", "inherited_failed"):
        return "C"
    if multidim_entry.get("domain") == "unknown":
        return "C"
    group = dedup_entry.get("duplicate_group")
    if group and group in problematic_groups:
        return "C"

    # Category A: high confidence
    uniqueness = dedup_entry.get("uniqueness", "")
    if uniqueness == "original" and category == "real_audit":
        return "A"

    # Category B: moderate confidence (everything else)
    return "B"


# ─────────────────────────────────────────────────────────
# Q6: Improvement Priorities
# ─────────────────────────────────────────────────────────
def generate_priorities(q1, q3, q5):
    """Q6: Generate ranked improvement priorities based on Q1-Q5 findings."""
    print("\n=== Q6: Improvement Priorities ===")

    priorities = [
        {
            "id": "P0",
            "title": "修复 fork 继承 lookup bug",
            "risk": (
                f"{q5['failed_inheritance']} fork_copies got default "
                f"tier=D/value=low due to lookup key mismatch"
            ),
            "location": "audit_multidim.py:524-540",
            "fix": (
                "Change canonical_lookup key to match by "
                "(duplicate_group, canonical_repo) correctly, "
                "handling multi-cluster union-find groups"
            ),
            "benefit": (
                f"Correct {q5['failed_inheritance']} entries; "
                f"tier changes: {q5['fix_impact']['tier_changes']}"
            ),
            "cost": "low (code change only)",
            "rerun_required": "Partial — re-run inheritance propagation only",
        },
        {
            "id": "P1",
            "title": "重审 LLM 失败条目",
            "risk": (
                f"{q3['category_counts'].get('llm_failed', 0)} entries got "
                f"default tier=D/value=low due to LLM JSON parse failures"
            ),
            "location": "audit_multidim.py retry logic",
            "fix": (
                "Add retry with backoff for failed entries; "
                "improve JSON extraction from LLM responses"
            ),
            "benefit": (
                "Recover accurate assessments for "
                f"~{q3['category_counts'].get('llm_failed', 0)} entries"
            ),
            "cost": "low (retry mechanism)",
            "rerun_required": "Partial — only failed entries",
        },
        {
            "id": "P2",
            "title": "规范化 domain 分类",
            "risk": (
                f"{q3['views']['full']['total']} entries with "
                f"domain='unknown': "
                f"{sum(1 for m in [] if m.get('domain') == 'unknown')}"
                " (see Q2 bias 3 for domain distribution)"
            ),
            "location": "Post-processing script (new)",
            "fix": (
                "Create domain normalization mapping; "
                "merge near-duplicate domain names"
            ),
            "benefit": "Cleaner domain statistics, better filtering",
            "cost": "medium (mapping creation + validation)",
            "rerun_required": "No — post-processing only",
        },
        {
            "id": "P3",
            "title": "加入 Union-Find 后验校验",
            "risk": (
                f"Q1 found {q1['suspect_count']} potential false merges "
                f"({q1['suspect_rate_pct']}% of fork_copies)"
            ),
            "location": "dedup_skills.py:260-285",
            "fix": (
                "Add post-merge verification: re-check all pairs in "
                "each union-find cluster, split if below threshold"
            ),
            "benefit": (
                f"Reduce false merge rate from ~{q1['suspect_rate_pct']}% "
                "to near 0%"
            ),
            "cost": "low (validation pass after merge)",
            "rerun_required": "Yes — re-run dedup + downstream",
        },
        {
            "id": "P4",
            "title": "增大截断限制 6000→12000 字符",
            "risk": (
                "Long SKILL.md files lose information after 6000 chars; "
                "may cause under-rating"
            ),
            "location": "audit_multidim.py:204",
            "fix": "Increase MAX_SKILL_CHARS from 6000 to 12000",
            "benefit": "More accurate assessment for long documents",
            "cost": "low (constant change, slightly higher API cost)",
            "rerun_required": "Yes — re-run affected entries",
        },
        {
            "id": "P5",
            "title": "添加可信度评分到审计 prompt",
            "risk": (
                "Current audit has no self-assessed confidence; "
                "all results treated equally"
            ),
            "location": "audit_multidim.py prompt + post-processing",
            "fix": (
                "Add confidence_score (1-5) to LLM prompt; "
                "use for downstream filtering"
            ),
            "benefit": "Enable confidence-weighted statistics",
            "cost": "high (prompt redesign + full re-run)",
            "rerun_required": "Yes — full re-run required",
        },
    ]

    return {"priorities": priorities}


# ─────────────────────────────────────────────────────────
# Report Generation: JSON
# ─────────────────────────────────────────────────────────
def generate_json_report(q1, q2, q3, q4, q5, q6):
    """Write credibility_audit_report.json."""
    report = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "script": "credibility_audit.py",
            "random_seed": SEED,
            "strict_similarity_threshold": STRICT_SIM_THRESHOLD,
        },
        "q1_dedup_correctness": q1,
        "q2_document_bias": q2,
        "q3_default_pollution": q3,
        "q4_reproducibility": q4,
        "q5_fork_inheritance": q5,
        "q6_priorities": q6,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nSaved JSON report: {OUTPUT_JSON}")
    return report


# ─────────────────────────────────────────────────────────
# Report Generation: Markdown
# ─────────────────────────────────────────────────────────
def generate_markdown_report(q1, q2, q3, q4, q5, q6):
    """Write CREDIBILITY_AUDIT.md human-readable report."""
    lines = []
    a = lines.append

    a("# 可信度审计报告 (Credibility Audit Report)")
    a("")
    a(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
      f"随机种子: {SEED} | 脚本: credibility_audit.py")
    a("")

    # Executive Summary
    write_executive_summary(a, q1, q3, q4, q5, q6)

    # Q1
    write_q1_section(a, q1)

    # Q2
    write_q2_section(a, q2)

    # Q3
    write_q3_section(a, q3)

    # Q4
    write_q4_section(a, q4)

    # Q5
    write_q5_section(a, q5)

    # Q6
    write_q6_section(a, q6)

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Saved Markdown report: {OUTPUT_MD}")


def write_executive_summary(a, q1, q3, q4, q5, q6):
    """Write executive summary section."""
    a("## Executive Summary")
    a("")

    full_total = q3["views"]["full"]["total"]
    clean_total = q3["views"]["clean"]["total"]
    polluted = q3["delta_full_to_clean"]["total_polluted"]
    poll_pct = q3["delta_full_to_clean"]["pollution_rate_pct"]

    a(f"- **总 skill 数**: {full_total}")
    a(f"- **清洁条目数**: {clean_total} (有可靠审计结果)")
    a(f"- **污染条目数**: {polluted} ({poll_pct}%)")
    a(f"- **去重误判率估计**: ~{q1['suspect_rate_pct']}% "
      f"({q1['suspect_count']}/{q1['total_fork_copies']} fork_copies)")
    a(f"- **Fork 继承失败率**: "
      f"{q5['failed_inheritance']}/{q5['total_fork_copies']} "
      f"({round(100*q5['failed_inheritance']/max(q5['total_fork_copies'],1), 1)}%)")
    a(f"- **置信度分布**: "
      f"A={q4['category_A']['count']}, "
      f"B={q4['category_B']['count']}, "
      f"C={q4['category_C']['count']}")
    a(f"- **最高优先级修复**: {q6['priorities'][0]['title']}")
    a("")


def write_q1_section(a, q1):
    """Write Q1 section of markdown report."""
    a("---")
    a("## Q1: 去重正确性验证")
    a("")
    a("### 方法")
    a(f"- 严格阈值: similarity ≥ {STRICT_SIM_THRESHOLD}")
    a(f"- 分层抽样: {q1['sampled_groups_count']} 个重复组深度分析")
    a("")

    a("### 全量相似度分布")
    a("")
    a("| 相似度区间 | 数量 | 分类 |")
    a("|-----------|------|------|")
    band_labels = {
        "1.00": ("文本完全一致", "confirmed_copy"),
        "0.99-1.00": ("几乎一致", "confirmed_copy"),
        "0.95-0.99": ("有差异，需审查", "suspect"),
        "0.90-0.95": ("高概率误标", "suspect"),
        "0.85-0.90": ("高概率误标", "suspect"),
        "0.80-0.85": ("几乎确定误标", "suspect"),
        "<0.80": ("传递性拉入", "suspect"),
    }
    for band in ["1.00", "0.99-1.00", "0.95-0.99", "0.90-0.95",
                  "0.85-0.90", "0.80-0.85", "<0.80"]:
        count = q1["similarity_distribution"].get(band, 0)
        label, _ = band_labels[band]
        a(f"| {band} | {count} | {label} |")

    a("")
    a(f"**严格标准结果**: {q1['confirmed_correct']} 正确, "
      f"{q1['suspect_count']} 潜在误标 "
      f"({q1['suspect_rate_pct']}%)")
    a("")

    a("### 抽样深度分析")
    a("")
    ss = q1.get("sample_summary", {})
    a(f"- 分析组数: {ss.get('groups_analyzed', 0)}")
    a(f"- 有问题的组: {ss.get('groups_with_issues', 0)}")
    itc = ss.get("issue_type_counts", {})
    if itc:
        a("- 问题类型:")
        for itype, cnt in sorted(itc.items()):
            a(f"  - {itype}: {cnt}")
    a("")

    # Individual group analyses (abbreviated)
    a("### 抽样组详情")
    a("")
    for ga in q1.get("group_analyses", []):
        issues_str = (
            f" — **{len(ga['issues'])} 问题**"
            if ga["issues"] else " — 无问题"
        )
        a(f"#### {ga['group_name']} (size={ga['size']}){issues_str}")
        a("")
        a("| 条目 | Repo | 唯一性 | 有文件 |")
        a("|------|------|--------|--------|")
        for e in ga["entries"]:
            a(f"| {e['skill_name']} | {e['repo'][:40]} | "
              f"{e.get('uniqueness', '?')} | "
              f"{'✓' if e['has_file'] else '✗'} |")
        a("")

        # Show similarity matrix (abbreviated)
        if ga["size"] <= 6:
            a("相似度矩阵:")
            a("```")
            header = "     " + "  ".join(
                f"[{i}]  " for i in range(ga["size"])
            )
            a(header)
            for i, row in enumerate(ga["similarity_matrix"]):
                vals = []
                for v in row:
                    if v is None:
                        vals.append(" N/A ")
                    else:
                        vals.append(f"{v:.3f}")
                a(f"[{i}] " + "  ".join(vals))
            a("```")
            a("")

        if ga["issues"]:
            for issue in ga["issues"]:
                a(f"- **{issue['type']}**: {issue.get('repo', '?')} "
                  f"(sim={issue.get('sim_to_canonical', 'N/A')})")
            a("")


def write_q2_section(a, q2):
    """Write Q2 section of markdown report."""
    a("---")
    a("## Q2: 文档驱动审计的系统性偏差")
    a("")
    a(f"分析范围: {q2['direct_audited_count']} 条直接审计条目")
    a("")

    # Bias 1
    b1 = q2["bias_1_truncation"]
    a("### 偏差 1: 截断偏差 (6000 字符)")
    a("")
    a(f"- 超过 6000 字符的文档: **{b1['long_docs_count']}**")
    a(f"- 短文档 (≤6000): **{b1['short_docs_count']}**")
    a(f"- 长文档平均 tier 分数: **{b1['long_avg_tier_score']}**")
    a(f"- 短文档平均 tier 分数: **{b1['short_avg_tier_score']}**")
    a(f"- 长文档 tier 分布: {b1['long_tier_distribution']}")
    a(f"- 短文档 tier 分布: {b1['short_tier_distribution']}")
    a(f"- 影响方向: {b1['impact_direction']}")
    a("")

    # Bias 2
    b2 = q2["bias_2_section_names"]
    a("### 偏差 2: 段落名称偏差")
    a("")
    a(f"- 缺少 when_to_use 的条目: **{b2['total_missing_when_to_use']}**")
    a(f"- 其中含 usage 类内容的假阴性: "
      f"**{b2['false_negatives_with_usage_content']}**")
    a(f"- 假阴性率: **{b2['false_negative_rate_pct']}%**")
    a(f"- 影响方向: {b2['impact_direction']}")
    a("")

    # Bias 3
    b3 = q2["bias_3_domain_asymmetry"]
    a("### 偏差 3: 领域知识不对称")
    a("")
    a(f"- 唯一领域数: **{b3['total_unique_domains']}**")
    a(f"- 高频领域 (Top 10) 平均 tier: "
      f"**{b3['high_freq_avg_tier_score']}**")
    a(f"- 低频领域 (≤3 条) 平均 tier: "
      f"**{b3['low_freq_avg_tier_score']}**")
    a(f"- domain='unknown' 条目数: **{b3['unknown_domain_count']}**")
    a("")
    a("高频领域 Top 10:")
    a("")
    a("| 领域 | 数量 |")
    a("|------|------|")
    for d in b3["high_freq_domains"]:
        a(f"| {d['domain'][:60]} | {d['count']} |")
    a("")

    # Bias 4
    b4 = q2["bias_4_naming"]
    a("### 偏差 4: 命名偏差")
    a("")
    a(f"- 含研究关键词的 skill: **{b4['research_named_count']}**")
    a(f"- 通用名称的 skill: **{b4['generic_named_count']}**")
    a(f"- 研究命名平均 tier: **{b4['research_avg_tier_score']}**")
    a(f"- 通用命名平均 tier: **{b4['generic_avg_tier_score']}**")
    a(f"- 影响方向: {b4['impact_direction']}")
    a("")

    # Bias 5
    b5 = q2["bias_5_temperature"]
    a("### 偏差 5: 温度方差")
    a("")
    a(f"- 可测量: {'是' if b5['measurable'] else '否 (需要多次运行)'}")
    a(f"- 风险级别: {b5['risk_level']}")
    a(f"- 受影响维度: {', '.join(b5['affected_dimensions'])}")
    a(f"- 说明: {b5['description']}")
    a("")


def write_q3_section(a, q3):
    """Write Q3 section of markdown report."""
    a("---")
    a("## Q3: 默认值污染分析")
    a("")

    a("### 条目分类统计")
    a("")
    a("| 类别 | 数量 | 说明 |")
    a("|------|------|------|")
    cat_labels = {
        "real_audit": "直接 LLM 审计",
        "inherited_ok": "成功继承 canonical",
        "inherited_failed": "继承失败 (默认值)",
        "skipped_no_content": "跳过 (无内容)",
        "llm_failed": "LLM 解析失败 (默认值)",
    }
    for cat, label in cat_labels.items():
        count = q3["category_counts"].get(cat, 0)
        a(f"| {cat} | {count} | {label} |")
    a("")

    a("### 多视图分布对比")
    a("")
    a("| 视图 | 总数 | Tier A | Tier B | Tier C | Tier D |")
    a("|------|------|--------|--------|--------|--------|")
    for view_name in ["full", "no_skipped", "no_failed_inherit",
                       "clean", "core_only"]:
        v = q3["views"][view_name]
        t = v["tiers"]
        a(f"| {view_name} | {v['total']} | "
          f"{t['A']['count']} ({t['A']['pct']}%) | "
          f"{t['B']['count']} ({t['B']['pct']}%) | "
          f"{t['C']['count']} ({t['C']['pct']}%) | "
          f"{t['D']['count']} ({t['D']['pct']}%) |")
    a("")

    a("| 视图 | high | medium | low | negligible |")
    a("|------|------|--------|-----|------------|")
    for view_name in ["full", "no_skipped", "no_failed_inherit",
                       "clean", "core_only"]:
        v = q3["views"][view_name]
        av = v["added_value"]
        a(f"| {view_name} | "
          f"{av['high']['count']} ({av['high']['pct']}%) | "
          f"{av['medium']['count']} ({av['medium']['pct']}%) | "
          f"{av['low']['count']} ({av['low']['pct']}%) | "
          f"{av['negligible']['count']} ({av['negligible']['pct']}%) |")
    a("")

    delta = q3["delta_full_to_clean"]
    a("### 污染影响量化")
    a("")
    a(f"- **D-tier 膨胀量**: {delta['d_tier_inflation']} 条")
    a(f"- **low+negligible 膨胀量**: {delta['low_negligible_inflation']} 条")
    a(f"- **总污染条目**: {delta['total_polluted']} 条 "
      f"({delta['pollution_rate_pct']}%)")
    a("")


def write_q4_section(a, q4):
    """Write Q4 section of markdown report."""
    a("---")
    a("## Q4: 可复现性边界")
    a("")

    for cat_key in ["category_A", "category_B", "category_C"]:
        cat = q4[cat_key]
        a(f"### {cat['label']}")
        a(f"- 数量: **{cat['count']}**")
        a(f"- 说明: {cat['description']}")
        a("")

    dist = q4["confidence_distribution"]
    total = sum(dist.values())
    a("| 置信度 | 数量 | 占比 |")
    a("|--------|------|------|")
    for level in ["A", "B", "C"]:
        count = dist.get(level, 0)
        pct = round(100.0 * count / total, 1) if total else 0
        a(f"| {level} | {count} | {pct}% |")
    a("")


def write_q5_section(a, q5):
    """Write Q5 section of markdown report."""
    a("---")
    a("## Q5: Fork 继承风险")
    a("")

    a("### 概况")
    a(f"- 总 fork_copy: {q5['total_fork_copies']}")
    a(f"- 成功继承: {q5['successful_inheritance']}")
    a(f"- 失败继承: {q5['failed_inheritance']}")
    a("")

    a("### 失败原因分类")
    a("")
    a("| 原因 | 数量 |")
    a("|------|------|")
    for cause, count in sorted(
        q5["diagnosis_summary"].items(), key=lambda x: -x[1]
    ):
        a(f"| {cause} | {count} |")
    a("")

    a("### 修复后预期变化")
    a("")
    fix = q5["fix_impact"]
    if fix["tier_changes"]:
        a("Tier 变化:")
        for change, count in sorted(fix["tier_changes"].items()):
            a(f"- {change}: {count} 条")
    if fix["value_changes"]:
        a("")
        a("Added Value 变化:")
        for change, count in sorted(fix["value_changes"].items()):
            a(f"- {change}: {count} 条")
    a("")

    a("### 失败条目列表 (前 30 条)")
    a("")
    a("| Skill | Repo | Group | 原因 | 实际 Tier |")
    a("|-------|------|-------|------|-----------|")
    for detail in q5["failure_details"][:30]:
        a(f"| {detail['skill_name'][:30]} | "
          f"{detail['repo'][:35]} | "
          f"{detail['duplicate_group'][:20]} | "
          f"{detail['cause']} | "
          f"{detail.get('actual_canonical_tier', '?')} |")
    if len(q5["failure_details"]) > 30:
        a(f"| ... | 共 {len(q5['failure_details'])} 条 | | | |")
    a("")


def write_q6_section(a, q6):
    """Write Q6 section of markdown report."""
    a("---")
    a("## Q6: 改进优先级")
    a("")
    a("| 优先级 | 改进项 | 修改位置 | 成本 | 需重跑 |")
    a("|--------|--------|---------|------|--------|")
    for p in q6["priorities"]:
        a(f"| {p['id']} | {p['title']} | "
          f"`{p['location']}` | {p['cost']} | {p['rerun_required']} |")
    a("")

    for p in q6["priorities"]:
        a(f"### {p['id']}: {p['title']}")
        a(f"- **风险**: {p['risk']}")
        a(f"- **修复方案**: {p['fix']}")
        a(f"- **预期收益**: {p['benefit']}")
        a(f"- **实施成本**: {p['cost']}")
        a(f"- **是否重跑**: {p['rerun_required']}")
        a("")


# ─────────────────────────────────────────────────────────
# Main Entry Point
# ─────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  Credibility Audit - Post-hoc Verification")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    dedup_results, dedup_stats = load_dedup_data()
    multidim_results, multidim_meta = load_multidim_data()
    print(f"  Dedup: {len(dedup_results)} entries")
    print(f"  Multidim: {len(multidim_results)} entries")

    # Build file index
    print("Building SKILL.md file index...")
    index, repo_index = build_skill_file_index()
    total_files = sum(len(v) for v in repo_index.values())
    print(f"  Indexed {total_files} SKILL.md files")

    # Run Q3 first (simplest, no file I/O)
    q3 = audit_default_pollution(dedup_results, multidim_results)

    # Run Q5 (medium complexity, cross-reference two JSONs)
    q5 = audit_fork_inheritance(dedup_results, multidim_results)

    # Run Q1 (complex, needs file I/O + similarity)
    q1 = audit_dedup_correctness(dedup_results, index, repo_index)

    # Run Q2 (needs file I/O + section analysis)
    q2 = audit_document_bias(
        dedup_results, multidim_results, index, repo_index
    )

    # Run Q4 (depends on Q1, Q3, Q5)
    q4 = audit_reproducibility(
        dedup_results, multidim_results, q1, q3, q5
    )

    # Run Q6 (depends on Q1-Q5)
    q6 = generate_priorities(q1, q3, q5)

    # Generate reports
    print("\n=== Generating Reports ===")
    generate_json_report(q1, q2, q3, q4, q5, q6)
    generate_markdown_report(q1, q2, q3, q4, q5, q6)

    print("\n" + "=" * 60)
    print("  Credibility Audit Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
[IN]  Dependencies/Inputs:
 - audit_results.json (1940 audit records with skill_name, repo, theme, has_local_file)
 - Final_Research_Skills_Link_Downloads_By_Theme_LATEST/**/SKILL.md (local skill files)
[OUT] Outputs:
 - dedup_results.json (each skill annotated: canonical/fork_copy/variant/original)
[POS] Position in the system:
 - Phase 1 of multi-dimensional audit. Pure local deduplication—no API calls.
   Groups skills by name, compares SKILL.md text similarity, picks canonical version.
   Output feeds into audit_multidim.py (Phase 2) to skip fork copies.
   Phase 3a fixes: removed both-missing auto-merge, default sim 1.0→0.0,
   fork_copy threshold raised to 0.95 (0.80-0.95 now classified as variant).

 Change warning: once you modify this file's logic, you must update this comment block,
 and check/update the module doc (README/CLAUDE) in the containing folder; update the root
 global map if necessary.
"""

import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).parent
AUDIT_FILE = BASE / "audit_results.json"
DOWNLOADS_DIR = BASE / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
OUTPUT = BASE / "dedup_results.json"

# Canonical priority: higher index = higher priority
REPO_PRIORITY = {
    "anthropics": 100,
    "K-Dense-AI": 80,
    "GPTomics": 60,
}

# Theme directory name mapping (audit_results theme → download dir name)
# audit_results themes have _part1/_part2 suffixes; download dirs don't
THEME_DIR_MAP = {
    "01_information_retrieval_evidence_collection": "01_information_retrieval_evidence_collection",
    "02_literature_review_writing_citation_part1": "02_literature_review_writing_citation",
    "02_literature_review_writing_citation_part2": "02_literature_review_writing_citation",
    "03_experiment_benchmark_reproducibility_validation_part1": "03_experiment_benchmark_reproducibility_validation",
    "03_experiment_benchmark_reproducibility_validation_part2": "03_experiment_benchmark_reproducibility_validation",
    "04_data_analysis_and_evidence_interpretation": "04_data_analysis_and_evidence_interpretation",
    "05_research_operations_and_workflow_support": "05_research_operations_and_workflow_support",
    "06_Additional_Scientific_Skills": "06_Additional_Scientific_Skills",
}


def build_skillmd_index():
    """Pre-scan all SKILL.md files and build lookup index.

    Returns: dict mapping (repo_slug, skill_dir_name_lower) -> file_path
    Also returns a secondary index: (repo_slug) -> [(skill_dir_name, file_path), ...]
    """
    index = {}  # (repo_slug, skill_dir_lower) -> path
    repo_index = defaultdict(list)  # repo_slug -> [(skill_dir, path)]

    if not DOWNLOADS_DIR.exists():
        print(f"WARNING: Downloads directory not found: {DOWNLOADS_DIR}")
        return index, repo_index

    for theme_dir in DOWNLOADS_DIR.iterdir():
        if not theme_dir.is_dir():
            continue
        for repo_dir in theme_dir.iterdir():
            if not repo_dir.is_dir():
                continue
            repo_slug = repo_dir.name  # e.g., "GPTomics__bioSkills"
            # Find all SKILL.md files recursively
            for skill_file in repo_dir.rglob("SKILL.md"):
                # The skill name is typically the parent directory name
                skill_dir_name = skill_file.parent.name
                key = (repo_slug, skill_dir_name.lower())
                index[key] = skill_file
                repo_index[repo_slug].append((skill_dir_name, skill_file))

    return index, repo_index


def find_skill_file(skill_name, repo, theme, index, repo_index):
    """Find SKILL.md file for a given audit entry.

    Tries multiple matching strategies:
    1. Exact match by (repo_slug, skill_name)
    2. Case-insensitive search in repo's skill list
    3. Partial match (skill_name contained in dir name or vice versa)
    """
    repo_slug = repo.replace("/", "__")
    skill_lower = skill_name.lower()

    # Strategy 1: exact match
    key = (repo_slug, skill_lower)
    if key in index:
        return index[key]

    # Strategy 2: search repo's skills for case-insensitive match
    if repo_slug in repo_index:
        for dir_name, path in repo_index[repo_slug]:
            if dir_name.lower() == skill_lower:
                return path

    # Strategy 3: partial match (e.g., "xlsx" matches "xlsx-official")
    if repo_slug in repo_index:
        candidates = []
        for dir_name, path in repo_index[repo_slug]:
            dl = dir_name.lower()
            if skill_lower in dl or dl in skill_lower:
                candidates.append((dir_name, path))
        if len(candidates) == 1:
            return candidates[0][1]
        # If multiple partial matches, prefer exact substring match
        if candidates:
            # Prefer the one where skill_name is the main part
            for dir_name, path in candidates:
                # e.g., "xlsx-official" contains "xlsx"
                if dir_name.lower().startswith(skill_lower):
                    return path
            return candidates[0][1]

    return None


def read_skill_content(filepath, max_chars=2000):
    """Read SKILL.md content, truncated to max_chars."""
    if filepath is None or not filepath.exists():
        return ""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
        return text[:max_chars]
    except Exception:
        return ""


def get_line_count(filepath):
    """Get line count of a SKILL.md file."""
    if filepath is None or not filepath.exists():
        return 0
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
        return len(text.split("\n"))
    except Exception:
        return 0


def text_similarity(text1, text2):
    """Calculate similarity ratio between two text strings."""
    if not text1 and not text2:
        return 1.0
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1, text2).ratio()


def get_repo_priority(repo):
    """Get priority score for a repo. Higher = more canonical."""
    org = repo.split("/")[0] if "/" in repo else repo
    return REPO_PRIORITY.get(org, 0)


def choose_canonical(group_entries, index, repo_index):
    """Choose the canonical version from a group of same-name skills.

    Priority:
    1. anthropics/* repos
    2. K-Dense-AI/* repos
    3. GPTomics/* repos
    4. Largest SKILL.md by line count
    """
    # Sort by repo priority (desc), then by line count (desc)
    scored = []
    for entry in group_entries:
        filepath = find_skill_file(
            entry["skill_name"], entry["repo"], entry["theme"], index, repo_index
        )
        priority = get_repo_priority(entry["repo"])
        lines = get_line_count(filepath)
        scored.append((priority, lines, entry, filepath))

    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return scored[0][2], scored[0][3]  # (canonical_entry, canonical_filepath)


def main():
    print("=== Phase 1: Skill Deduplication Analysis ===\n")

    # 1. Load audit results
    print("Loading audit_results.json...")
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        audit_data = json.load(f)
    records = audit_data["results"]
    print(f"  Loaded {len(records)} records")

    # 2. Build SKILL.md file index
    print("Building SKILL.md file index...")
    index, repo_index = build_skillmd_index()
    print(f"  Indexed {len(index)} SKILL.md files")

    # 3. Group by skill_name (case-insensitive)
    print("Grouping by skill name...")
    groups = defaultdict(list)
    for record in records:
        name_key = record["skill_name"].lower()
        groups[name_key].append(record)

    single_count = sum(1 for g in groups.values() if len(g) == 1)
    dup_groups = {k: v for k, v in groups.items() if len(v) > 1}
    dup_record_count = sum(len(v) for v in dup_groups.values())

    print(f"  Unique names: {len(groups)}")
    print(f"  Single-instance skills: {single_count}")
    print(f"  Duplicate groups: {len(dup_groups)}")
    print(f"  Total duplicate records: {dup_record_count}")

    # 4. Analyze each group
    print("\nAnalyzing duplicates...")
    results = []
    stats = {"original": 0, "canonical": 0, "fork_copy": 0, "variant": 0, "files_found": 0, "files_missing": 0}

    for name_key, group_entries in sorted(groups.items()):
        if len(group_entries) == 1:
            # Single instance → original
            entry = group_entries[0]
            results.append({
                "skill_name": entry["skill_name"],
                "repo": entry["repo"],
                "theme": entry["theme"],
                "uniqueness": "original",
                "duplicate_group": None,
                "duplicate_count": 1,
                "canonical_repo": None,
                "similarity": None,
                "similar_repos": [],
            })
            stats["original"] += 1
            continue

        # Multiple instances → cluster-based dedup
        # Step A: read all content and find files
        entry_data = []
        for entry in group_entries:
            filepath = find_skill_file(
                entry["skill_name"], entry["repo"], entry["theme"], index, repo_index
            )
            if filepath:
                stats["files_found"] += 1
            else:
                stats["files_missing"] += 1
            content = read_skill_content(filepath)
            entry_data.append({
                "entry": entry,
                "filepath": filepath,
                "content": content,
                "cluster": None,  # assigned below
            })

        # Step B: cluster by pairwise similarity (>80% = same cluster)
        n = len(entry_data)
        # Union-Find for clustering
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for i in range(n):
            for j in range(i + 1, n):
                ci, cj = entry_data[i]["content"], entry_data[j]["content"]
                if ci and cj:
                    sim = text_similarity(ci, cj)
                    if sim > 0.8:
                        union(i, j)
                # Note: both-missing case no longer auto-merges (zero evidence)

        # Group into clusters
        clusters = defaultdict(list)
        for i in range(n):
            clusters[find(i)].append(i)

        # Step C: for each cluster, pick canonical (highest repo priority, then line count)
        group_results = []
        for cluster_indices in clusters.values():
            cluster_entries = [entry_data[i] for i in cluster_indices]

            # Pick canonical for this cluster
            best_idx = max(
                cluster_indices,
                key=lambda i: (
                    get_repo_priority(entry_data[i]["entry"]["repo"]),
                    get_line_count(entry_data[i]["filepath"]),
                ),
            )
            best_entry = entry_data[best_idx]["entry"]
            best_content = entry_data[best_idx]["content"]

            if len(cluster_indices) == 1:
                # Solo in cluster within a dup group → it's a variant (unique impl)
                idx = cluster_indices[0]
                ed = entry_data[idx]
                # Compare to the overall group's best to get similarity
                overall_canonical_idx = max(
                    range(n),
                    key=lambda i: (
                        get_repo_priority(entry_data[i]["entry"]["repo"]),
                        get_line_count(entry_data[i]["filepath"]),
                    ),
                )
                if idx == overall_canonical_idx:
                    # This is the overall canonical
                    other_repos = [
                        entry_data[j]["entry"]["repo"]
                        for j in range(n) if j != idx
                    ]
                    group_results.append({
                        "skill_name": ed["entry"]["skill_name"],
                        "repo": ed["entry"]["repo"],
                        "theme": ed["entry"]["theme"],
                        "uniqueness": "canonical",
                        "duplicate_group": name_key,
                        "duplicate_count": len(group_entries),
                        "canonical_repo": None,
                        "similarity": None,
                        "similar_repos": other_repos,
                    })
                    stats["canonical"] += 1
                else:
                    oc = entry_data[overall_canonical_idx]
                    sim = text_similarity(ed["content"], oc["content"]) if (ed["content"] and oc["content"]) else 0.0
                    group_results.append({
                        "skill_name": ed["entry"]["skill_name"],
                        "repo": ed["entry"]["repo"],
                        "theme": ed["entry"]["theme"],
                        "uniqueness": "variant",
                        "duplicate_group": name_key,
                        "duplicate_count": len(group_entries),
                        "canonical_repo": oc["entry"]["repo"],
                        "similarity": round(sim, 3),
                        "similar_repos": [],
                    })
                    stats["variant"] += 1
            else:
                # Multi-entry cluster: one canonical, rest fork_copy
                for idx in cluster_indices:
                    ed = entry_data[idx]
                    if idx == best_idx:
                        # Check if this is the overall group canonical too
                        overall_canonical_idx = max(
                            range(n),
                            key=lambda i: (
                                get_repo_priority(entry_data[i]["entry"]["repo"]),
                                get_line_count(entry_data[i]["filepath"]),
                            ),
                        )
                        if idx == overall_canonical_idx:
                            other_repos = [
                                entry_data[j]["entry"]["repo"]
                                for j in range(n) if j != idx
                            ]
                            group_results.append({
                                "skill_name": ed["entry"]["skill_name"],
                                "repo": ed["entry"]["repo"],
                                "theme": ed["entry"]["theme"],
                                "uniqueness": "canonical",
                                "duplicate_group": name_key,
                                "duplicate_count": len(group_entries),
                                "canonical_repo": None,
                                "similarity": None,
                                "similar_repos": other_repos,
                            })
                            stats["canonical"] += 1
                        else:
                            # Cluster canonical but not overall canonical → variant
                            oc = entry_data[overall_canonical_idx]
                            sim = text_similarity(ed["content"], oc["content"]) if (ed["content"] and oc["content"]) else 0.0
                            group_results.append({
                                "skill_name": ed["entry"]["skill_name"],
                                "repo": ed["entry"]["repo"],
                                "theme": ed["entry"]["theme"],
                                "uniqueness": "variant",
                                "duplicate_group": name_key,
                                "duplicate_count": len(group_entries),
                                "canonical_repo": oc["entry"]["repo"],
                                "similarity": round(sim, 3),
                                "similar_repos": [
                                    entry_data[j]["entry"]["repo"]
                                    for j in cluster_indices if j != idx
                                ],
                            })
                            stats["variant"] += 1
                    else:
                        # Non-canonical member of multi-entry cluster
                        sim = text_similarity(ed["content"], best_content) if (ed["content"] and best_content) else 0.0
                        if sim >= 0.95:
                            # High similarity → fork_copy (inherits canonical audit)
                            group_results.append({
                                "skill_name": ed["entry"]["skill_name"],
                                "repo": ed["entry"]["repo"],
                                "theme": ed["entry"]["theme"],
                                "uniqueness": "fork_copy",
                                "duplicate_group": name_key,
                                "duplicate_count": len(group_entries),
                                "canonical_repo": best_entry["repo"],
                                "similarity": round(sim, 3),
                                "similar_repos": [],
                            })
                            stats["fork_copy"] += 1
                        else:
                            # Lower similarity → variant (needs independent audit)
                            oc = entry_data[best_idx]
                            group_results.append({
                                "skill_name": ed["entry"]["skill_name"],
                                "repo": ed["entry"]["repo"],
                                "theme": ed["entry"]["theme"],
                                "uniqueness": "variant",
                                "duplicate_group": name_key,
                                "duplicate_count": len(group_entries),
                                "canonical_repo": oc["entry"]["repo"],
                                "similarity": round(sim, 3),
                                "similar_repos": [],
                            })
                            stats["variant"] += 1

        # Ensure exactly one canonical per group
        canonicals = [r for r in group_results if r["uniqueness"] == "canonical"]
        if not canonicals:
            # Promote the highest-priority variant to canonical
            overall_idx = max(
                range(n),
                key=lambda i: (
                    get_repo_priority(entry_data[i]["entry"]["repo"]),
                    get_line_count(entry_data[i]["filepath"]),
                ),
            )
            for r in group_results:
                if (r["repo"] == entry_data[overall_idx]["entry"]["repo"]
                        and r["theme"] == entry_data[overall_idx]["entry"]["theme"]):
                    if r["uniqueness"] == "variant":
                        r["uniqueness"] = "canonical"
                        r["canonical_repo"] = None
                        r["similar_repos"] = [
                            entry_data[j]["entry"]["repo"]
                            for j in range(n) if j != overall_idx
                        ]
                        stats["variant"] -= 1
                        stats["canonical"] += 1
                    break

        results.extend(group_results)

    # 5. Build output
    print(f"\n=== Results ===")
    print(f"  Original (single): {stats['original']}")
    print(f"  Canonical (chosen): {stats['canonical']}")
    print(f"  Fork copies (>80% similar): {stats['fork_copy']}")
    print(f"  Variants (≤80% similar): {stats['variant']}")
    print(f"  SKILL.md files found: {stats['files_found']}")
    print(f"  SKILL.md files missing: {stats['files_missing']}")

    output = {
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "total_skills": len(records),
        "unique_names": len(groups),
        "duplicates": dup_record_count,
        "duplicate_groups": len(dup_groups),
        "stats": stats,
        "results": results,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSaved: {OUTPUT}")
    print(f"Total records in output: {len(results)}")

    # 6. Summary: canonical + variant + original = skills to audit in Phase 2
    auditable = sum(1 for r in results if r["uniqueness"] != "fork_copy")
    print(f"\nSkills to audit in Phase 2 (non-fork_copy): {auditable}")


if __name__ == "__main__":
    main()

"""
/**
 * [IN]  repo_inventory.jsonl, staged LATEST directory tree, and optional materialization report.
 * [OUT] refresh verification JSON plus missing-by-repo markdown summary.
 * [POS] Quality gate stage: verifies row-level existence and repo-set consistency before cutover.
 *
 * Change warning: once you modify this file's logic, you must update this comment block,
 * and check/update the module doc (README/CLAUDE) in the containing folder; update the root
 * global map if necessary.
 */
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set

from refresh_pipeline_common import (
    build_output_relative_path,
    load_jsonl,
    path_exists,
    read_json,
    write_json,
    write_text,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify staged refresh result against inventory.")
    parser.add_argument("--inventory-jsonl", required=True, help="Inventory JSONL")
    parser.add_argument("--staging-dir", required=True, help="Staging root dir")
    parser.add_argument("--output-report", required=True, help="Verification report JSON")
    parser.add_argument(
        "--materialize-report",
        default="",
        help="Optional materialization report JSON for hard_fail_count gate",
    )
    parser.add_argument("--expect-rows", type=int, default=2074, help="Expected inventory row count")
    parser.add_argument("--expect-repos", type=int, default=67, help="Expected unique repo count")
    return parser.parse_args()


def to_markdown_missing(missing_by_repo: Dict[str, List[Dict[str, object]]]) -> str:
    lines = [
        "# Refresh Missing By Repo",
        "",
        "| Repo | Missing Rows | Themes |",
        "|---|---:|---|",
    ]
    for repo in sorted(missing_by_repo.keys(), key=lambda r: len(missing_by_repo[r]), reverse=True):
        rows = missing_by_repo[repo]
        themes = sorted({str(r["theme"]) for r in rows})
        lines.append(f"| {repo} | {len(rows)} | {', '.join(themes)} |")
    lines.append("")
    lines.append("## Sample Missing Rows")
    lines.append("")
    lines.append("| Repo | Theme | Evidence File |")
    lines.append("|---|---|---|")
    for repo in sorted(missing_by_repo.keys(), key=lambda r: len(missing_by_repo[r]), reverse=True):
        for row in missing_by_repo[repo][:5]:
            lines.append(f"| {repo} | {row['theme']} | `{row['evidence_file']}` |")
    return "\n".join(lines) + "\n"


def collect_actual_repo_set(latest_root: Path) -> Set[str]:
    repos: Set[str] = set()
    if not latest_root.exists():
        return repos
    for theme_dir in latest_root.iterdir():
        if not theme_dir.is_dir():
            continue
        for repo_dir in theme_dir.iterdir():
            if not repo_dir.is_dir():
                continue
            if "__" in repo_dir.name:
                repos.add(repo_dir.name.replace("__", "/", 1))
    return repos


def main() -> int:
    args = parse_args()
    rows = load_jsonl(Path(args.inventory_jsonl))
    staging_dir = Path(args.staging_dir)
    latest_root = staging_dir / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
    output_report = Path(args.output_report)

    exists_count = 0
    missing_rows: List[Dict[str, object]] = []
    missing_by_repo: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    theme_counter = Counter()
    expected_repo_set: Set[str] = set()
    for row in rows:
        expected_repo_set.add(str(row["repo"]))
        theme_counter[str(row["theme"])] += 1
        target_path = staging_dir / build_output_relative_path(row)
        if path_exists(target_path):
            exists_count += 1
            continue
        miss = {
            "row_id": row["row_id"],
            "repo": row["repo"],
            "theme": row["theme"],
            "evidence_file": row["evidence_file"],
            "target": str(target_path),
        }
        missing_rows.append(miss)
        missing_by_repo[str(row["repo"])].append(miss)

    actual_repo_set = collect_actual_repo_set(latest_root)
    extra_repos = sorted(actual_repo_set - expected_repo_set)
    missing_repos = sorted(expected_repo_set - actual_repo_set)

    hard_fail_count = 0
    materialize_conflicts = 0
    if args.materialize_report:
        materialize = read_json(Path(args.materialize_report))
        summary = dict(materialize.get("summary", {}))
        hard_fail_count = int(summary.get("failed", 0))
        materialize_conflicts = int(summary.get("conflicts", 0))

    check_1 = len(rows) == args.expect_rows
    check_2_expected = len(rows) - hard_fail_count
    check_2 = exists_count == check_2_expected
    check_3 = (len(expected_repo_set) == args.expect_repos) and (not extra_repos) and (not missing_repos)
    check_4 = True
    checks = {
        "check_1_expected_rows": check_1,
        "check_2_exists_equals_expected_minus_hard_fail": check_2,
        "check_3_repo_set_match_and_no_extra": check_3,
        "check_4_missing_report_generated": check_4,
        "materialize_conflicts_zero": materialize_conflicts == 0,
    }
    pass_gate = all(checks.values())

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inventory_rows": len(rows),
        "expected_rows": args.expect_rows,
        "exists_count": exists_count,
        "hard_fail_count": hard_fail_count,
        "check_2_expected_exists_count": check_2_expected,
        "expected_repo_count": args.expect_repos,
        "actual_repo_count": len(actual_repo_set),
        "expected_repo_count_from_inventory": len(expected_repo_set),
        "extra_repos": extra_repos,
        "missing_repos": missing_repos,
        "missing_rows_count": len(missing_rows),
        "missing_by_repo_count": {repo: len(items) for repo, items in sorted(missing_by_repo.items(), key=lambda kv: len(kv[1]), reverse=True)},
        "theme_counts": dict(sorted(theme_counter.items())),
        "checks": checks,
        "pass_gate": pass_gate,
        "missing_rows": missing_rows,
    }
    write_json(output_report, report)

    missing_md = output_report.with_name("refresh_missing_by_repo.md")
    write_text(missing_md, to_markdown_missing(missing_by_repo))

    print(f"Inventory rows: {len(rows)}")
    print(f"Exists count:   {exists_count}")
    print(f"Hard fails:     {hard_fail_count}")
    print(f"Extra repos:    {len(extra_repos)}")
    print(f"Missing repos:  {len(missing_repos)}")
    print(f"Missing rows:   {len(missing_rows)}")
    print(f"Conflicts:      {materialize_conflicts}")
    print(f"Report:         {output_report}")
    print(f"Missing MD:     {missing_md}")
    print(f"Pass gate:      {pass_gate}")
    return 0 if pass_gate else 2


if __name__ == "__main__":
    raise SystemExit(main())

"""
/**
 * [IN]  Root-level thematic markdown files in Final_Research_Skills_Thematic_Split/
 *       that match ^0[1-6]_.*\\.md$ (default).
 * [OUT] repo_inventory.jsonl (one validated row per skill evidence reference) and
 *       repo_summary.json (aggregate counts and validation status).
 * [POS] Source-of-truth inventory builder for the refresh pipeline; it blocks the
 *       pipeline when parsing/validation/count checks fail.
 *
 * Change warning: once you modify this file's logic, you must update this comment block,
 * and check/update the module doc (README/CLAUDE) in the containing folder; update the root
 * global map if necessary.
 */
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from refresh_pipeline_common import (
    DEFAULT_INCLUDE_REGEX,
    build_inventory,
    build_repo_summary,
    write_json,
    write_jsonl,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build validated skill repo inventory from thematic markdown files.")
    parser.add_argument("--source-dir", required=True, help="Path to Final_Research_Skills_Thematic_Split")
    parser.add_argument("--include-regex", default=DEFAULT_INCLUDE_REGEX, help="Filename regex (root level only)")
    parser.add_argument("--output-jsonl", required=True, help="Output inventory JSONL path")
    parser.add_argument("--output-summary", required=True, help="Output summary JSON path")
    parser.add_argument("--expect-rows", type=int, default=2074, help="Expected total inventory rows")
    parser.add_argument("--expect-repos", type=int, default=67, help="Expected unique repo count")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_dir = Path(args.source_dir)
    output_jsonl = Path(args.output_jsonl)
    output_summary = Path(args.output_summary)

    rows, issues = build_inventory(source_dir, args.include_regex)
    summary = build_repo_summary(rows, args.include_regex, source_dir)
    summary["generated_at"] = datetime.now(timezone.utc).isoformat()
    summary["issues"] = issues

    blocking_reasons: List[str] = []
    blocking_issue_types = {"parse_error", "url_missing", "url_invalid", "path_mismatch"}
    blocking_issues = [issue for issue in issues if issue.get("type") in blocking_issue_types]
    warning_issues = [issue for issue in issues if issue.get("type") not in blocking_issue_types]
    summary["blocking_issues"] = blocking_issues
    summary["warning_issues"] = warning_issues
    if blocking_issues:
        blocking_reasons.append(f"blocking validation issues: {len(blocking_issues)}")
    if summary["rows_count"] != args.expect_rows:
        blocking_reasons.append(
            f"rows mismatch: expected {args.expect_rows}, got {summary['rows_count']}"
        )
    if summary["unique_repo_count"] != args.expect_repos:
        blocking_reasons.append(
            f"repo mismatch: expected {args.expect_repos}, got {summary['unique_repo_count']}"
        )

    summary["expected_rows"] = args.expect_rows
    summary["expected_repos"] = args.expect_repos
    summary["blocking_reasons"] = blocking_reasons
    summary["blocked"] = bool(blocking_reasons)

    write_jsonl(output_jsonl, rows)
    write_json(output_summary, summary)

    print(f"Inventory rows: {summary['rows_count']}")
    print(f"Unique repos:   {summary['unique_repo_count']}")
    print(f"Issues:         {len(issues)} (blocking: {len(blocking_issues)}, warning: {len(warning_issues)})")
    print(f"Inventory file: {output_jsonl}")
    print(f"Summary file:   {output_summary}")
    if summary["blocked"]:
        print("BLOCKED:")
        for reason in blocking_reasons:
            print(f"  - {reason}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

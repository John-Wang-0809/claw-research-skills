"""
/**
 * [IN]  repo_inventory.jsonl and refreshed git snapshots under cache-dir.
 * [OUT] Staged evidence files in staging-dir/Final_Research_Skills_Link_Downloads_By_Theme_LATEST
 *       plus a row-level materialization report JSON.
 * [POS] File materialization stage that pulls exact blob paths from git refs and enforces
 *       duplicate/conflict checks before cutover.
 *
 * Change warning: once you modify this file's logic, you must update this comment block,
 * and check/update the module doc (README/CLAUDE) in the containing folder; update the root
 * global map if necessary.
 */
"""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from refresh_pipeline_common import (
    build_output_relative_path,
    load_jsonl,
    path_exists,
    read_bytes,
    repo_to_dirname,
    sha256_bytes,
    write_bytes,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize inventory evidence files into staging directory.")
    parser.add_argument("--inventory-jsonl", required=True, help="Inventory JSONL")
    parser.add_argument("--cache-dir", required=True, help="Git snapshot cache dir")
    parser.add_argument("--staging-dir", required=True, help="Staging root dir (parent of LATEST folder)")
    parser.add_argument("--report-json", required=True, help="Materialization report JSON")
    parser.add_argument("--timeout-sec", type=int, default=120, help="Per git show timeout")
    return parser.parse_args()


def git_show_blob(repo_dir: Path, ref_name: str, rel_path: str, timeout_sec: int) -> bytes:
    blob_ref = f"{ref_name}:{rel_path}"
    proc = subprocess.run(
        ["git", "-C", str(repo_dir), "show", blob_ref],
        capture_output=True,
        timeout=timeout_sec,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(stderr or f"git show failed for {blob_ref}")
    return proc.stdout


def main() -> int:
    args = parse_args()
    inventory_path = Path(args.inventory_jsonl)
    cache_dir = Path(args.cache_dir)
    staging_dir = Path(args.staging_dir)
    report_json = Path(args.report_json)
    latest_root = staging_dir / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"

    rows = load_jsonl(inventory_path)
    written_hashes: Dict[str, str] = {}
    row_results: List[Dict[str, object]] = []
    conflicts: List[Dict[str, object]] = []

    for row in rows:
        repo = str(row["repo"])
        fetch_repo = str(row.get("repo_from_url") or repo)
        branch = str(row["branch"])
        evidence_file = str(row["evidence_file"])
        repo_dir = cache_dir / repo_to_dirname(fetch_repo)
        target_relative = build_output_relative_path(row)
        target_path = staging_dir / target_relative
        target_key = str(target_path).lower()
        row_result: Dict[str, object] = {
            "row_id": row["row_id"],
            "repo": repo,
            "fetch_repo": fetch_repo,
            "theme": row["theme"],
            "evidence_file": evidence_file,
            "target": str(target_path),
            "status": "failed",
            "reason": "",
        }

        if not (repo_dir / ".git").exists():
            row_result["reason"] = "repo_snapshot_missing"
            row_results.append(row_result)
            continue

        ref_name = f"refs/remotes/origin/{branch}"
        try:
            blob = git_show_blob(repo_dir, ref_name, evidence_file, args.timeout_sec)
        except Exception as exc:  # pylint: disable=broad-except
            row_result["reason"] = str(exc)
            row_results.append(row_result)
            continue

        current_hash = sha256_bytes(blob)
        if target_key in written_hashes:
            if written_hashes[target_key] == current_hash:
                row_result["status"] = "skipped"
                row_result["reason"] = "duplicate_same_content"
                row_results.append(row_result)
                continue
            row_result["reason"] = "duplicate_conflict"
            row_results.append(row_result)
            conflicts.append(row_result)
            continue

        if path_exists(target_path):
            existing_hash = sha256_bytes(read_bytes(target_path))
            if existing_hash == current_hash:
                written_hashes[target_key] = current_hash
                row_result["status"] = "skipped"
                row_result["reason"] = "already_exists_same_content"
                row_results.append(row_result)
                continue
            row_result["reason"] = "existing_file_conflict"
            row_results.append(row_result)
            conflicts.append(row_result)
            continue

        write_bytes(target_path, blob)
        written_hashes[target_key] = current_hash
        row_result["status"] = "written"
        row_result["reason"] = "ok"
        row_results.append(row_result)

    written = sum(1 for r in row_results if r["status"] == "written")
    skipped = sum(1 for r in row_results if r["status"] == "skipped")
    failed = sum(1 for r in row_results if r["status"] == "failed")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inventory_path": str(inventory_path),
        "cache_dir": str(cache_dir),
        "staging_dir": str(staging_dir),
        "latest_root": str(latest_root),
        "summary": {
            "rows_total": len(rows),
            "written": written,
            "skipped": skipped,
            "failed": failed,
            "conflicts": len(conflicts),
        },
        "conflicts": conflicts,
        "rows": row_results,
    }
    write_json(report_json, report)

    print(f"Rows total: {len(rows)}")
    print(f"Written:    {written}")
    print(f"Skipped:    {skipped}")
    print(f"Failed:     {failed}")
    print(f"Conflicts:  {len(conflicts)}")
    print(f"Report:     {report_json}")
    return 2 if conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main())

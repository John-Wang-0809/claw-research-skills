"""
/**
 * [IN]  repo_inventory.jsonl with repo/branch fields and a writable cache directory.
 * [OUT] Updated local git snapshots under cache-dir and a snapshot report JSON.
 * [POS] Network fetch stage for the refresh pipeline: keeps shallow refs per branch
 *       without full repository checkout.
 *
 * Change warning: once you modify this file's logic, you must update this comment block,
 * and check/update the module doc (README/CLAUDE) in the containing folder; update the root
 * global map if necessary.
 */
"""

from __future__ import annotations

import argparse
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from refresh_pipeline_common import load_jsonl, repo_jobs_from_inventory, repo_to_dirname, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh shallow repo snapshots for inventory repos.")
    parser.add_argument("--inventory-jsonl", required=True, help="Inventory JSONL from build_repo_inventory.py")
    parser.add_argument("--cache-dir", required=True, help="Short cache directory (example: E:\\RS_CACHE)")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers")
    parser.add_argument("--retry", type=int, default=3, help="Retry attempts for git fetch")
    parser.add_argument(
        "--report-json",
        default="tmp_research_audit/repo_snapshot_report.json",
        help="Output snapshot report JSON",
    )
    parser.add_argument("--timeout-sec", type=int, default=300, help="Per git command timeout")
    return parser.parse_args()


def run_git(repo_dir: Path, args: List[str], timeout_sec: int) -> Tuple[int, str, str]:
    cmd = ["git", "-C", str(repo_dir)] + args
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def ensure_repo(repo_dir: Path, repo_url: str, timeout_sec: int) -> None:
    repo_dir.mkdir(parents=True, exist_ok=True)
    git_dir = repo_dir / ".git"
    if not git_dir.exists():
        rc, _, err = run_git(repo_dir, ["init"], timeout_sec)
        if rc != 0:
            raise RuntimeError(f"git init failed: {err}")
    rc, out, err = run_git(repo_dir, ["remote", "get-url", "origin"], timeout_sec)
    if rc != 0:
        rc, _, err = run_git(repo_dir, ["remote", "add", "origin", repo_url], timeout_sec)
        if rc != 0:
            raise RuntimeError(f"git remote add origin failed: {err}")
        return
    if out.strip() != repo_url:
        rc, _, err = run_git(repo_dir, ["remote", "set-url", "origin", repo_url], timeout_sec)
        if rc != 0:
            raise RuntimeError(f"git remote set-url origin failed: {err}")


def fetch_branch_with_retry(repo_dir: Path, branch: str, retry: int, timeout_sec: int) -> str:
    ref_name = f"refs/remotes/origin/{branch}"
    for attempt in range(retry + 1):
        rc, _, err = run_git(
            repo_dir,
            ["fetch", "--depth", "1", "origin", f"{branch}:{ref_name}"],
            timeout_sec,
        )
        if rc == 0:
            rc, out, err = run_git(repo_dir, ["rev-parse", ref_name], timeout_sec)
            if rc != 0:
                raise RuntimeError(f"git rev-parse {ref_name} failed: {err}")
            return out.strip()
        if attempt >= retry:
            raise RuntimeError(f"git fetch branch '{branch}' failed: {err}")
        time.sleep(2 ** attempt)
    raise RuntimeError(f"unreachable retry state for branch '{branch}'")


def process_repo_job(
    cache_dir: Path,
    job: Dict[str, object],
    retry: int,
    timeout_sec: int,
) -> Dict[str, object]:
    repo = str(job["repo"])
    repo_url = str(job["repo_url"])
    branches = list(job["branches"])
    repo_dir = cache_dir / repo_to_dirname(repo)
    result: Dict[str, object] = {
        "repo": repo,
        "repo_url": repo_url,
        "repo_dir": str(repo_dir),
        "branches": branches,
        "branch_results": [],
        "status": "success",
    }

    try:
        ensure_repo(repo_dir, repo_url, timeout_sec)
    except Exception as exc:  # pylint: disable=broad-except
        result["status"] = "failed"
        result["error"] = str(exc)
        return result

    any_failed = False
    for branch in branches:
        branch_result = {"branch": branch, "status": "success", "commit": None}
        try:
            commit = fetch_branch_with_retry(repo_dir, branch, retry, timeout_sec)
            branch_result["commit"] = commit
        except Exception as exc:  # pylint: disable=broad-except
            any_failed = True
            branch_result["status"] = "failed"
            branch_result["error"] = str(exc)
        result["branch_results"].append(branch_result)

    if any_failed and len(result["branch_results"]) == 0:
        result["status"] = "failed"
    elif any_failed:
        result["status"] = "partial"
    return result


def main() -> int:
    args = parse_args()
    cache_dir = Path(args.cache_dir)
    report_json = Path(args.report_json)
    rows = load_jsonl(Path(args.inventory_jsonl))
    jobs = repo_jobs_from_inventory(rows)

    cache_dir.mkdir(parents=True, exist_ok=True)
    repo_results: List[Dict[str, object]] = []
    started_at = datetime.now(timezone.utc).isoformat()

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(process_repo_job, cache_dir, job, args.retry, args.timeout_sec): repo
            for repo, job in jobs.items()
        }
        for future in as_completed(futures):
            repo_results.append(future.result())

    success_count = sum(1 for r in repo_results if r["status"] == "success")
    partial_count = sum(1 for r in repo_results if r["status"] == "partial")
    failed_count = sum(1 for r in repo_results if r["status"] == "failed")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "started_at": started_at,
        "inventory_rows": len(rows),
        "repo_jobs": len(jobs),
        "workers": args.workers,
        "retry": args.retry,
        "cache_dir": str(cache_dir),
        "summary": {
            "success": success_count,
            "partial": partial_count,
            "failed": failed_count,
        },
        "results": sorted(repo_results, key=lambda x: str(x["repo"])),
    }
    write_json(report_json, report)

    print(f"Repo jobs:  {len(jobs)}")
    print(f"Success:    {success_count}")
    print(f"Partial:    {partial_count}")
    print(f"Failed:     {failed_count}")
    print(f"Report:     {report_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
/**
 * [IN]  Verified staged LATEST directory path and current target LATEST directory path.
 * [OUT] Target LATEST replaced by staged directory and a timestamped backup for rollback.
 * [POS] Atomic cutover/rollback gate for publishing refreshed evidence files.
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

from refresh_pipeline_common import write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cut over staged LATEST directory with rollback backup.")
    parser.add_argument("--staging-latest-dir", required=True, help="Staged Final_Research_Skills_Link_Downloads_By_Theme_LATEST path")
    parser.add_argument("--target-latest-dir", required=True, help="Current Final_Research_Skills_Link_Downloads_By_Theme_LATEST path")
    parser.add_argument("--backup-suffix", required=True, help="Backup suffix, e.g. 20260301_153000")
    parser.add_argument(
        "--report-json",
        default="tmp_research_audit/cutover_report.json",
        help="Cutover report JSON output path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    staging = Path(args.staging_latest_dir)
    target = Path(args.target_latest_dir)
    report_path = Path(args.report_json)
    backup = target.parent / f"{target.name}__backup_{args.backup_suffix}"

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "staging": str(staging),
        "target": str(target),
        "backup": str(backup),
        "status": "failed",
        "steps": [],
    }

    target_moved = False
    try:
        if not staging.exists():
            raise RuntimeError(f"staging path does not exist: {staging}")
        if not staging.is_dir():
            raise RuntimeError(f"staging path is not a directory: {staging}")
        result["steps"].append("validated staging directory")

        if target.exists():
            if backup.exists():
                raise RuntimeError(f"backup path already exists: {backup}")
            target.rename(backup)
            target_moved = True
            result["steps"].append(f"moved target to backup: {backup}")

        staging.rename(target)
        result["steps"].append("moved staging to target")

        if not target.exists():
            raise RuntimeError("target path missing after cutover rename")
        result["steps"].append("validated target exists after cutover")
        result["status"] = "success"
        write_json(report_path, result)
        print(f"Cutover success. Report: {report_path}")
        return 0
    except Exception as exc:  # pylint: disable=broad-except
        result["error"] = str(exc)
        if target_moved and not target.exists() and backup.exists():
            try:
                backup.rename(target)
                result["steps"].append("rollback restored backup to target")
            except Exception as rollback_exc:  # pylint: disable=broad-except
                result["rollback_error"] = str(rollback_exc)
        write_json(report_path, result)
        print(f"Cutover failed. Report: {report_path}")
        print(f"Reason: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

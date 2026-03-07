"""
/**
 * [IN]  materialize_report.json failed rows, repo_inventory.jsonl, local git snapshots,
 *       and current Final_Research_Skills_Link_Downloads_By_Theme_LATEST target tree.
 * [OUT] Recovered evidence files written to expected target paths and a recovery report
 *       describing strategy used per row, plus unresolved rows.
 * [POS] Post-materialization recovery stage for stale/renamed upstream paths using
 *       deterministic multi-strategy lookup (branch fallback, mappings, suffix matching).
 *
 * Change warning: once you modify this file's logic, you must update this comment block,
 * and check/update the module doc (README/CLAUDE) in the containing folder; update the root
 * global map if necessary.
 */
"""

from __future__ import annotations

import argparse
import re
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from refresh_pipeline_common import (
    build_output_relative_path,
    load_jsonl,
    path_exists,
    read_json,
    repo_to_dirname,
    sha256_bytes,
    write_bytes,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recover unresolved evidence paths with multiple heuristics.")
    parser.add_argument("--inventory-jsonl", required=True, help="Inventory JSONL path")
    parser.add_argument("--materialize-report", required=True, help="materialize_report.json path")
    parser.add_argument("--cache-dir", required=True, help="Snapshot cache dir")
    parser.add_argument("--target-root", required=True, help="Workspace root that contains Final_..._LATEST")
    parser.add_argument("--report-json", required=True, help="Recovery report output JSON")
    parser.add_argument("--timeout-sec", type=int, default=120, help="Per git command timeout")
    return parser.parse_args()


def git_lines(repo_dir: Path, args: List[str], timeout_sec: int) -> List[str]:
    proc = subprocess.run(
        ["git", "-C", str(repo_dir)] + args,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        raise RuntimeError(stderr or f"git command failed: {' '.join(args)}")
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def git_blob(repo_dir: Path, ref_name: str, rel_path: str, timeout_sec: int) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo_dir), "show", f"{ref_name}:{rel_path}"],
        capture_output=True,
        timeout=timeout_sec,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(stderr or f"git show failed for {ref_name}:{rel_path}")
    return proc.stdout


def release_version_tuple(path_text: str) -> Tuple[int, int, int, int]:
    # Prefer newest release paths when multiple matches exist.
    m = re.match(r"^Releases/v(\d+)(?:\.(\d+))?(?:\.(\d+))?/", path_text)
    if not m:
        return (0, 0, 0, 0)
    a = int(m.group(1) or 0)
    b = int(m.group(2) or 0)
    c = int(m.group(3) or 0)
    return (1, a, b, c)


def candidate_score(path_text: str, skill_dir: str) -> Tuple[int, int, int, int, int]:
    release = release_version_tuple(path_text)
    claude_pref = 1 if "/.claude/skills/" in path_text else 0
    exact_skill_suffix = 1 if path_text.endswith(f"/{skill_dir}/SKILL.md") else 0
    neg_depth = -path_text.count("/")
    return (exact_skill_suffix, claude_pref, release[1], release[2], release[3] + (neg_depth // 1000))


def choose_best_candidate(candidates: List[str], skill_dir: str) -> str:
    if len(candidates) == 1:
        return candidates[0]
    return sorted(candidates, key=lambda p: candidate_score(p, skill_dir), reverse=True)[0]


def build_mapped_candidates(evidence_file: str) -> List[str]:
    candidates: List[str] = []
    if evidence_file.startswith(".cursor/skills/"):
        suffix = evidence_file[len(".cursor/skills/"):]
        candidates.extend([
            f"skills/{suffix}",
            f".agents/skills/{suffix}",
            f".claude/skills/{suffix}",
            f"docs/zh-CN/skills/{suffix}",
            f"docs/ja-JP/skills/{suffix}",
            f"docs/zh-TW/skills/{suffix}",
        ])
    if evidence_file.endswith("-automation/SKILL.md") and "/" not in evidence_file:
        candidates.append(f"composio-skills/{evidence_file}")
    return candidates


class RepoContext:
    def __init__(self, repo_dir: Path, timeout_sec: int):
        self.repo_dir = repo_dir
        self.timeout_sec = timeout_sec
        self.refs = self._load_refs()
        self.files_by_ref: Dict[str, List[str]] = {}
        self.lower_index_by_ref: Dict[str, Dict[str, str]] = {}

    def _load_refs(self) -> List[str]:
        refs = git_lines(self.repo_dir, ["for-each-ref", "--format=%(refname:short)", "refs/remotes/origin"], self.timeout_sec)
        return refs

    def ensure_files(self, ref_name: str) -> None:
        if ref_name in self.files_by_ref:
            return
        files = git_lines(self.repo_dir, ["ls-tree", "-r", "--name-only", ref_name], self.timeout_sec)
        self.files_by_ref[ref_name] = files
        self.lower_index_by_ref[ref_name] = {p.lower(): p for p in files}

    def existing_case_path(self, ref_name: str, rel_path: str) -> Optional[str]:
        self.ensure_files(ref_name)
        return self.lower_index_by_ref[ref_name].get(rel_path.lower())

    def find_suffix_matches(self, ref_name: str, suffix: str) -> List[str]:
        self.ensure_files(ref_name)
        suffix_l = suffix.lower()
        return [p for p in self.files_by_ref[ref_name] if p.lower().endswith(suffix_l)]


def recover_one_row(
    row: Dict[str, object],
    inv: Dict[str, object],
    ctx: RepoContext,
    target_root: Path,
    timeout_sec: int,
) -> Dict[str, object]:
    repo = str(inv.get("repo_from_url") or inv["repo"])
    branch = str(inv["branch"])
    evidence_file = str(inv["evidence_file"])
    skill_dir = Path(evidence_file).parent.name
    target_path = target_root / build_output_relative_path(inv)
    main_ref = f"refs/remotes/origin/{branch}"
    fallback_refs = [ref for ref in ctx.refs if ref != main_ref]

    attempts: List[Tuple[str, str, str]] = []

    def try_path(ref_name: str, rel_path: str, method: str) -> Optional[Dict[str, object]]:
        matched_case = ctx.existing_case_path(ref_name, rel_path)
        if not matched_case:
            attempts.append((method, ref_name, rel_path))
            return None
        blob = git_blob(ctx.repo_dir, ref_name, matched_case, timeout_sec)
        # If file already exists with same content, mark as already fixed.
        if path_exists(target_path):
            existing = target_path.read_bytes()
            if sha256_bytes(existing) == sha256_bytes(blob):
                return {
                    "status": "skipped",
                    "method": method,
                    "source_ref": ref_name,
                    "source_path": matched_case,
                    "target": str(target_path),
                    "reason": "already_exists_same_content",
                }
        write_bytes(target_path, blob)
        return {
            "status": "recovered",
            "method": method,
            "source_ref": ref_name,
            "source_path": matched_case,
            "target": str(target_path),
            "reason": "ok",
        }

    # Method 1: exact path in primary/fallback branches (handles branch drift).
    for ref_name in [main_ref] + fallback_refs:
        out = try_path(ref_name, evidence_file, "exact_or_branch_fallback")
        if out:
            return out

    # Method 2: deterministic path mapping rules.
    mapped = build_mapped_candidates(evidence_file)
    for rel_path in mapped:
        for ref_name in [main_ref] + fallback_refs:
            out = try_path(ref_name, rel_path, "path_mapping")
            if out:
                out["mapped_from"] = evidence_file
                return out

    # Method 3: case-insensitive exact suffix match by "<skill_dir>/SKILL.md".
    suffix = f"/{skill_dir}/SKILL.md"
    for ref_name in [main_ref] + fallback_refs:
        matches = ctx.find_suffix_matches(ref_name, suffix)
        if not matches:
            continue
        chosen = choose_best_candidate(matches, skill_dir)
        out = try_path(ref_name, chosen, "skill_dir_suffix_match")
        if out:
            out["candidate_count"] = len(matches)
            return out

    # Method 4: pack-style broad fallback for danielmiessler style paths.
    # Search by exact filename and nearest directory token.
    file_name = Path(evidence_file).name
    dir_token = skill_dir.lower()
    for ref_name in [main_ref] + fallback_refs:
        ctx.ensure_files(ref_name)
        broad = [
            p for p in ctx.files_by_ref[ref_name]
            if p.lower().endswith("/" + file_name.lower()) and f"/{dir_token}/" in p.lower()
        ]
        if not broad:
            continue
        chosen = choose_best_candidate(broad, skill_dir)
        out = try_path(ref_name, chosen, "broad_token_match")
        if out:
            out["candidate_count"] = len(broad)
            return out

    return {
        "status": "unresolved",
        "method": "none",
        "target": str(target_path),
        "repo": repo,
        "evidence_file": evidence_file,
        "attempts": [{"method": m, "ref": r, "path": p} for m, r, p in attempts[:50]],
    }


def main() -> int:
    args = parse_args()
    inventory_rows = load_jsonl(Path(args.inventory_jsonl))
    inventory_by_row = {str(row["row_id"]): row for row in inventory_rows}
    materialize = read_json(Path(args.materialize_report))
    failed_rows = [r for r in materialize.get("rows", []) if r.get("status") == "failed"]
    target_root = Path(args.target_root)

    repo_contexts: Dict[str, RepoContext] = {}
    recovered: List[Dict[str, object]] = []
    unresolved: List[Dict[str, object]] = []
    by_method = defaultdict(int)

    for failed in failed_rows:
        row_id = str(failed["row_id"])
        inv = inventory_by_row.get(row_id)
        if not inv:
            unresolved.append({
                "status": "unresolved",
                "method": "missing_inventory_row",
                "row_id": row_id,
                "repo": failed.get("repo"),
                "evidence_file": failed.get("evidence_file"),
            })
            by_method["missing_inventory_row"] += 1
            continue

        fetch_repo = str(inv.get("repo_from_url") or inv["repo"])
        repo_dir = Path(args.cache_dir) / repo_to_dirname(fetch_repo)
        if fetch_repo not in repo_contexts:
            try:
                repo_contexts[fetch_repo] = RepoContext(repo_dir, args.timeout_sec)
            except Exception as exc:  # pylint: disable=broad-except
                unresolved.append({
                    "status": "unresolved",
                    "method": "repo_context_error",
                    "row_id": row_id,
                    "repo": fetch_repo,
                    "evidence_file": inv["evidence_file"],
                    "error": str(exc),
                })
                by_method["repo_context_error"] += 1
                continue

        result = recover_one_row(failed, inv, repo_contexts[fetch_repo], target_root, args.timeout_sec)
        result["row_id"] = row_id
        result["repo"] = str(inv["repo"])
        result["fetch_repo"] = fetch_repo
        result["evidence_file"] = str(inv["evidence_file"])
        result["theme"] = str(inv["theme"])
        by_method[str(result["method"])] += 1
        if result["status"] in {"recovered", "skipped"}:
            recovered.append(result)
        else:
            unresolved.append(result)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "materialize_report": args.materialize_report,
        "inventory_jsonl": args.inventory_jsonl,
        "target_root": args.target_root,
        "failed_input_count": len(failed_rows),
        "recovered_count": len([r for r in recovered if r["status"] == "recovered"]),
        "skipped_count": len([r for r in recovered if r["status"] == "skipped"]),
        "unresolved_count": len(unresolved),
        "method_counts": dict(sorted(by_method.items())),
        "recovered": recovered,
        "unresolved": unresolved,
    }
    write_json(Path(args.report_json), report)

    print(f"Input failed rows: {len(failed_rows)}")
    print(f"Recovered:         {report['recovered_count']}")
    print(f"Skipped:           {report['skipped_count']}")
    print(f"Unresolved:        {report['unresolved_count']}")
    print(f"Report:            {args.report_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

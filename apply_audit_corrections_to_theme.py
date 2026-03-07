#!/usr/bin/env python3
"""
Apply corrected_text fields from audit_results.jsonl back to one theme markdown file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Tuple


AUDIT_FIELDS = [
    "why_research_related",
    "function_explanation",
    "execution_flow",
    "evidence",
]


def normalize_text(v: str) -> str:
    return re.sub(r"\s+", " ", (v or "").strip())


def normalize_for_compare(v: str) -> str:
    """
    Semantic normalization for markdown table cells.
    Treat escaped/unescaped pipe variants as equivalent when comparing updates.
    """
    s = str(v or "")
    s = re.sub(r"\\+\|", "|", s)
    return normalize_text(s)


def sha1_text(v: str) -> str:
    return hashlib.sha1(v.encode("utf-8", errors="ignore")).hexdigest()


def extract_skill_and_url(row_line: str) -> Tuple[str, str]:
    skill_match = re.search(r"^\|\s*([^|]+?)\s*\|", row_line)
    url_match = re.search(r"\[[^\]]*\]\((https?://[^)\s]+)\)", row_line)
    skill = normalize_text(skill_match.group(1)) if skill_match else ""
    url = normalize_text(url_match.group(1)) if url_match else ""
    return skill, url


def split_row_by_unescaped_pipes(row_line: str) -> List[str]:
    cols: List[str] = []
    buf: List[str] = []
    escaped = False
    for ch in row_line:
        if escaped:
            buf.append(ch)
            escaped = False
            continue
        if ch == "\\":
            buf.append(ch)
            escaped = True
            continue
        if ch == "|":
            cols.append("".join(buf))
            buf = []
            continue
        buf.append(ch)
    cols.append("".join(buf))
    return cols


def parse_row_best_effort(row_line: str) -> Dict[str, str]:
    result = {
        "skill": "",
        "evidence_file": "",
        "skill_url_cell": "",
        "why_research_related": "",
        "function_explanation": "",
        "execution_flow": "",
        "evidence": "",
    }

    parts = split_row_by_unescaped_pipes(row_line)
    if parts and row_line.lstrip().startswith("|") and not parts[0].strip():
        parts = parts[1:]
    if parts and row_line.rstrip().endswith("|") and not parts[-1].strip():
        parts = parts[:-1]

    if len(parts) < 7:
        skill, _ = extract_skill_and_url(row_line)
        result["skill"] = skill
        return result

    # If malformed rows contain extra unescaped pipes, merge overflow into evidence.
    if len(parts) > 7:
        parts = parts[:6] + ["|".join(parts[6:])]

    result["skill"] = normalize_text(parts[0])
    result["evidence_file"] = normalize_text(parts[1])
    result["skill_url_cell"] = normalize_text(parts[2])
    result["why_research_related"] = normalize_text(parts[3])
    result["function_explanation"] = normalize_text(parts[4])
    result["execution_flow"] = normalize_text(parts[5])
    result["evidence"] = normalize_text(parts[6])
    return result


def escape_unescaped_pipes(v: str) -> str:
    s = str(v or "")
    # Collapse repeated escape levels to a single markdown escape first.
    s = re.sub(r"\\+\|", r"\|", s)

    out: List[str] = []
    escaped = False
    for ch in s:
        if escaped:
            out.append(ch)
            escaped = False
            continue
        if ch == "\\":
            out.append(ch)
            escaped = True
            continue
        if ch == "|":
            out.append(r"\|")
            continue
        out.append(ch)
    return "".join(out).strip()


def sanitize_cell(v: str) -> str:
    # Keep markdown table valid when replacement text contains a literal pipe.
    return escape_unescaped_pipes(v)


def build_row_line(fields: Dict[str, str]) -> str:
    return (
        f"| {sanitize_cell(fields['skill'])} | "
        f"{sanitize_cell(fields['evidence_file'])} | "
        f"{sanitize_cell(fields['skill_url_cell'])} | "
        f"{sanitize_cell(fields['why_research_related'])} | "
        f"{sanitize_cell(fields['function_explanation'])} | "
        f"{sanitize_cell(fields['execution_flow'])} | "
        f"{sanitize_cell(fields['evidence'])} |"
    )


GITHUB_BLOB_RE = re.compile(
    r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/blob/(?P<branch>[^/]+)/(?P<path>.+)$",
    re.IGNORECASE,
)


def parse_github_blob_url(url: str) -> Tuple[str, str, str, str]:
    m = GITHUB_BLOB_RE.match(str(url or "").strip())
    if not m:
        return "", "", "", ""
    return (
        m.group("owner"),
        m.group("repo"),
        m.group("branch"),
        m.group("path"),
    )


def github_blob_url(owner: str, repo: str, branch: str, rel_path: str) -> str:
    return f"https://github.com/{owner}/{repo}/blob/{branch}/{rel_path}"


def url_is_reachable(url: str, cache: Dict[str, bool], timeout: int = 8) -> bool:
    cached = cache.get(url)
    if cached is not None:
        return cached

    ok = False
    try:
        req = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "research-skills-audit/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = getattr(resp, "status", 0) or 0
            ok = 200 <= int(code) < 400
    except urllib.error.HTTPError as exc:
        code = int(getattr(exc, "code", 0) or 0)
        # Some endpoints disallow HEAD; fallback to GET.
        if code in {403, 405}:
            try:
                req = urllib.request.Request(
                    url,
                    method="GET",
                    headers={"User-Agent": "research-skills-audit/1.0"},
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    status = getattr(resp, "status", 0) or 0
                    ok = 200 <= int(status) < 400
            except Exception:
                ok = False
        else:
            ok = False
    except Exception:
        ok = False

    cache[url] = ok
    return ok


def maybe_rewrite_skill_url(url: str, cache: Dict[str, bool]) -> str:
    """
    Repair known moved skill paths while preserving branch.
    Current scoped fix: ComposioHQ/awesome-claude-skills moved many skills under composio-skills/.
    """
    owner, repo, branch, rel_path = parse_github_blob_url(url)
    if not owner:
        return url

    if owner.lower() == "composiohq" and repo.lower() == "awesome-claude-skills":
        if not rel_path.lower().startswith("composio-skills/"):
            candidate_path = f"composio-skills/{rel_path}"
            candidate_url = github_blob_url(owner, repo, branch, candidate_path)
            old_ok = url_is_reachable(url, cache)
            new_ok = url_is_reachable(candidate_url, cache)
            if (not old_ok) and new_ok:
                return candidate_url

    return url


def url_to_repo_path(url: str) -> str:
    _, _, _, rel_path = parse_github_blob_url(url)
    return rel_path


def load_audit_rows(audit_jsonl: Path, theme: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    with audit_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except Exception:
                continue
            if row.get("theme") != theme:
                continue
            if not row.get("ok", False):
                continue
            row_id = row.get("row_id")
            if isinstance(row_id, str) and row_id.strip():
                out[row_id] = row
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply audit corrected_text values to a single theme markdown file."
    )
    parser.add_argument(
        "--theme-doc",
        required=True,
        help="Path to one theme markdown file, e.g. Final_Research_Skills_Thematic_Split/01_xxx.md",
    )
    parser.add_argument(
        "--audit-jsonl",
        required=True,
        help="Path to run-*/audit_results.jsonl",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional output markdown path. If omitted, overwrite --theme-doc.",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        default=True,
        help="Create a timestamped backup when overwriting source file (default: true).",
    )
    parser.add_argument(
        "--no-backup",
        dest="backup",
        action="store_false",
        help="Disable backup creation.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    theme_doc = Path(args.theme_doc)
    audit_jsonl = Path(args.audit_jsonl)
    output_path = Path(args.output) if args.output else theme_doc
    theme = theme_doc.stem

    if not theme_doc.exists():
        raise SystemExit(f"theme doc not found: {theme_doc}")
    if not audit_jsonl.exists():
        raise SystemExit(f"audit jsonl not found: {audit_jsonl}")

    audit_map = load_audit_rows(audit_jsonl, theme)
    if not audit_map:
        raise SystemExit(f"no usable audit rows found for theme '{theme}' in {audit_jsonl}")

    lines = theme_doc.read_text(encoding="utf-8", errors="replace").splitlines()
    current_repo = ""
    total_rows = 0
    matched_rows = 0
    updated_rows = 0
    updated_fields = 0
    updated_urls = 0
    url_health_cache: Dict[str, bool] = {}

    for i, line in enumerate(lines, start=1):
        if line.startswith("### "):
            current_repo = normalize_text(line[4:])
            continue
        if not line.startswith("|"):
            continue
        if line.startswith("| Skill |") or line.startswith("|---"):
            continue
        if "[link](" not in line:
            continue

        parsed = parse_row_best_effort(line)
        skill, url = extract_skill_and_url(line)
        if not skill or not url:
            continue

        total_rows += 1
        seed = f"{theme}|{current_repo}|{i}|{skill}|{url}"
        row_id = sha1_text(seed)
        audit_row = audit_map.get(row_id)
        if not audit_row:
            continue

        matched_rows += 1
        checks = ((audit_row.get("parsed_result") or {}).get("field_checks") or {})
        if not isinstance(checks, dict):
            continue

        new_fields = dict(parsed)
        row_changed = False

        # URL/path maintenance: keep existing behavior unless URL is stale and known rewrite is reachable.
        repaired_url = maybe_rewrite_skill_url(url, url_health_cache)
        if repaired_url != url:
            new_fields["skill_url_cell"] = f"[link]({repaired_url})"
            path_from_url = url_to_repo_path(repaired_url)
            if path_from_url:
                new_fields["evidence_file"] = f"`{path_from_url}`"
            row_changed = True
            updated_urls += 1

        for field in AUDIT_FIELDS:
            item = checks.get(field) or {}
            if not isinstance(item, dict):
                continue
            corrected = normalize_text(str(item.get("corrected_text", "") or ""))
            if corrected and normalize_for_compare(corrected) != normalize_for_compare(parsed.get(field, "")):
                new_fields[field] = corrected
                row_changed = True
                updated_fields += 1

        if row_changed:
            lines[i - 1] = build_row_line(new_fields)
            updated_rows += 1

    if output_path == theme_doc and args.backup:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        backup_path = theme_doc.with_name(f"{theme_doc.name}.bak.{stamp}")
        backup_path.write_text(theme_doc.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        print(f"Backup created: {backup_path}")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(f"Theme doc       : {theme_doc}")
    print(f"Audit jsonl     : {audit_jsonl}")
    print(f"Rows scanned    : {total_rows}")
    print(f"Rows matched    : {matched_rows}")
    print(f"Rows updated    : {updated_rows}")
    print(f"Fields updated  : {updated_fields}")
    print(f"URLs updated    : {updated_urls}")
    print(f"Output          : {output_path}")


if __name__ == "__main__":
    main()

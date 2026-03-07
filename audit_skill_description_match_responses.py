#!/usr/bin/env python3
"""
Audit skill-row descriptions against downloaded SKILL.md source files via Responses API.

What this script does:
1) Parse all skill rows from Final_Research_Skills_Thematic_Split/*.md
2) Map each skill URL to downloaded local content via download_manifest.json
3) Call /v1/responses for each skill row + source document pair
4) Save per-row audit result JSONL + summary + mismatch-only markdown report
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import threading
import time
import unicodedata
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
from dotenv import load_dotenv

load_dotenv()


# =========================
# Explicit API Configuration
# =========================
API_KEY = os.getenv("API_KEY", "")
API_BASE_URL = os.getenv("BASE_URL", "https://yunwu.ai")
API_ENDPOINT = f"{API_BASE_URL}/v1/responses"
MODEL_NAME = "gpt-5.2"

# Request controls
REQUEST_TIMEOUT_SECONDS = 120
MAX_RETRIES = 3
RETRY_SLEEP_SECONDS = 2.0


SYSTEM_PROMPT = """You are a strict source-grounded content auditor and corrector.
Goal: ensure corrected table text aligns with source SKILL content.

Hard rules:
- Use ONLY the provided source text; do not invent facts.
- Corrections must be extractive-first (reuse source wording whenever possible).
- Do NOT inject generic research boilerplate unless explicitly present in source.
- If status is accurate, corrected_text MUST equal original_text exactly.
- If status is partial/mismatch, corrected_text must be directly replaceable in the table.
- Provide field-level supporting_quotes as exact snippets copied from source.
- Each supporting quote must be a contiguous substring from source (no stitched fragments).
- Prefer 1-2 short quotes per field (avoid oversized table-block quotes).
- Output JSON only. No markdown, no extra text.
"""


EXPECTED_REASONS = [
    "Supports systematic information retrieval and evidence collection for research tasks.",
    "Supports literature review, paper drafting, and citation management in academic workflows.",
    "Supports experiment design, benchmarking, reproducibility, and quantitative validation.",
    "Supports data-centric investigation, statistical analysis, and evidence interpretation.",
    "Related to research operations (evidence gathering, analysis, validation, or reporting).",
]


USER_PROMPT_TEMPLATE = """Please audit the match quality between the table row and the source SKILL file.

Context:
- Theme: {theme}
- Repository: {repo}
- Skill name: {skill}
- Skill URL: {url}
- Source file path: {local_path}

Raw markdown table row:
{row_raw}

Column meanings (for strict auditing):
- Skill: the skill identifier/name being audited.
- Evidence File: the repository-relative file path where the skill evidence is located.
- Skill URL: the canonical source link for this skill entry.
- Why Research-Related: explains whether and why this skill is related to research work.
- Function Explanation (2-3 sentences): concise summary of the skill's real core functionality.
- Execution Flow: ordered workflow steps that the skill actually follows (not a generic feature list).
- Evidence: source-grounded proof text (prefer exact quote) supporting the row's claims.

**Original table row fields (parsed by Python):**

1. Why Research-Related:
   {why_research_related}

2. Function Explanation (2-3 sentences):
   {function_explanation}

3. Execution Flow:
   {execution_flow}

4. Evidence:
   {evidence}

**Source SKILL document content:**
----- BEGIN SOURCE -----
{source_excerpt}
----- END SOURCE -----

**Your correction task:**
For each field above, compare it against the source document and:

1. If the field is "accurate" (matches source well):
   - Set corrected_text = original_text (copy it exactly)
   - Set correction_applied = false

2. If the field is "partial" (somewhat matches but incomplete) or "mismatch" (doesn't match):
   - Generate a COMPLETE corrected version based strictly on source document
   - The corrected_text must be ready to directly replace the original in the table
   - Ensure corrected_text is verifiable from supporting_quotes (exact source snippets)
   - Set correction_applied = true

3. Format requirements:
   - why_research_related: one sentence, strictly grounded in source
   - function_explanation: 2-3 complete sentences describing actual functionality from source
   - execution_flow: brief step-by-step flow using " -> " separator and only explicit source steps
   - evidence: exact quote preferred (not a path string)
   - avoid unsupported generic phrases such as "cross-verification", "structured insights", "evidence collection" unless source explicitly states them
   - supporting_quotes must be copied exactly from source as contiguous snippets (no merging non-adjacent lines)
   - keep supporting_quotes concise (prefer <=220 chars each, max 2 per field)

4. If parsed fields and source conflict, source is authoritative.

Return JSON with this exact schema:
{{
  "overall_match": "high|medium|low",
  "field_checks": {{
    "why_research_related": {{
      "status": "accurate|partial|mismatch",
      "reason": "string explaining the assessment",
      "original_text": "{why_research_related}",
      "corrected_text": "complete corrected text ready for replacement",
      "correction_applied": true|false,
      "supporting_quotes": ["exact snippet from source", "exact snippet from source"]
    }},
    "function_explanation": {{
      "status": "accurate|partial|mismatch",
      "reason": "string explaining the assessment",
      "original_text": "{function_explanation}",
      "corrected_text": "complete corrected text ready for replacement",
      "correction_applied": true|false,
      "supporting_quotes": ["exact snippet from source", "exact snippet from source"]
    }},
    "execution_flow": {{
      "status": "accurate|partial|mismatch",
      "reason": "string explaining the assessment",
      "original_text": "{execution_flow}",
      "corrected_text": "complete corrected text ready for replacement",
      "correction_applied": true|false,
      "supporting_quotes": ["exact snippet from source", "exact snippet from source"]
    }},
    "evidence": {{
      "status": "accurate|partial|mismatch",
      "reason": "string explaining the assessment",
      "original_text": "{evidence}",
      "corrected_text": "complete corrected text ready for replacement",
      "correction_applied": true|false,
      "supporting_quotes": ["exact snippet from source", "exact snippet from source"]
    }}
  }},
  "critical_issues": ["string"],
  "confidence": 0.0,
  "source_citations": ["short quote/snippet from source used as correction basis"]
}}
"""


AUDIT_FIELDS = [
    "why_research_related",
    "function_explanation",
    "execution_flow",
    "evidence",
]

@dataclass
class SkillRow:
    row_id: str
    theme: str
    source_doc: str
    repo: str
    line_no: int
    skill: str
    url: str
    row_raw: str
    parsed_fields: Dict[str, str]
    local_path: Optional[str] = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit skill descriptions with Responses API against downloaded source files."
    )
    parser.add_argument(
        "--theme-dir",
        default=r"E:\LLM\EDU+LLM\1\Good_Tools\research-skills\Final_Research_Skills_Thematic_Split",
        help="Directory containing thematic markdown files.",
    )
    parser.add_argument(
        "--manifest",
        default=r"E:\LLM\EDU+LLM\1\Good_Tools\research-skills\Final_Research_Skills_Link_Downloads_By_Theme\download_manifest.json",
        help="download_manifest.json path.",
    )
    parser.add_argument(
        "--output-dir",
        default=r"E:\LLM\EDU+LLM\1\Good_Tools\research-skills\skill_description_audit_results",
        help="Output directory for audit artifacts.",
    )
    parser.add_argument("--theme", action="append", default=[], help="Theme filename stem filter (repeatable).")
    parser.add_argument("--limit", type=int, default=0, help="Only process first N rows (0 = all).")
    parser.add_argument("--workers", type=int, default=4, help="Concurrent API workers.")
    parser.add_argument("--max-source-chars", type=int, default=18000, help="Max chars from source file.")
    parser.add_argument("--resume", action="store_true", default=True, help="Resume from existing results.")
    parser.add_argument("--no-resume", dest="resume", action="store_false", help="Disable resume mode.")
    parser.add_argument("--dry-run", action="store_true", help="Parse and map rows only, no API call.")
    return parser.parse_args()


def normalize_text(v: str) -> str:
    return re.sub(r"\s+", " ", (v or "").strip())


def normalize_for_match(v: str) -> str:
    s = str(v or "")
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("\r\n", "\n").replace("\r", "\n")

    # Treat markdown/escaped pipe variants as equivalent.
    s = re.sub(r"\\+\|", "|", s)

    # Ignore common markdown formatting wrappers for matching.
    s = s.replace("**", "")
    s = s.replace("__", "")
    s = s.replace("`", "")

    # Normalize common arrow variants.
    s = re.sub(r"[→⇒➜⟶⟹➔↦↣↪↝⇢➡]+", " -> ", s)
    s = s.replace("->", " -> ")

    s = re.sub(r"\s+", " ", s).strip()
    return s


def simplify_for_match(v: str) -> str:
    s = normalize_for_match(v)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def contains_source_snippet(source_text: str, snippet: str) -> bool:
    source_n = normalize_for_match(source_text)
    snippet_n = normalize_for_match(snippet)
    if not snippet_n:
        return False
    if snippet_n in source_n:
        return True

    # Fallback for harmless formatting/encoding noise.
    snippet_s = simplify_for_match(snippet)
    source_s = simplify_for_match(source_text)
    if snippet_s and len(snippet_s) >= 24 and snippet_s in source_s:
        return True
    return False


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
    """
    Best-effort parser for 7-column markdown row.
    It is intentionally tolerant to extra unescaped '|' in later columns.
    """
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
        for reason in EXPECTED_REASONS:
            if reason in row_line:
                result["why_research_related"] = reason
                break
        return result

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


def parse_theme_markdown(md_path: Path) -> List[SkillRow]:
    lines = md_path.read_text(encoding="utf-8", errors="replace").splitlines()
    theme = md_path.stem
    rows: List[SkillRow] = []
    current_repo = ""

    for idx, line in enumerate(lines, start=1):
        if line.startswith("### "):
            current_repo = normalize_text(line[4:])
            continue
        if not line.startswith("|"):
            continue
        if line.startswith("| Skill |") or line.startswith("|---"):
            continue
        if "[link](" not in line:
            continue

        skill, url = extract_skill_and_url(line)
        if not skill or not url:
            continue

        parsed_fields = parse_row_best_effort(line)
        row_id_seed = f"{theme}|{current_repo}|{idx}|{skill}|{url}"
        row_id = sha1_text(row_id_seed)
        rows.append(
            SkillRow(
                row_id=row_id,
                theme=theme,
                source_doc=md_path.name,
                repo=current_repo,
                line_no=idx,
                skill=skill,
                url=url,
                row_raw=line,
                parsed_fields=parsed_fields,
            )
        )

    return rows


def load_manifest_map(manifest_path: Path) -> Dict[str, str]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    out: Dict[str, str] = {}
    for item in data:
        url = item.get("url", "")
        output_path = item.get("output_path", "")
        ok = bool(item.get("download_ok", False))
        if not url or not output_path or not ok:
            continue
        if url not in out:
            out[url] = output_path
    return out


def excerpt_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    head = int(max_chars * 0.75)
    tail = max_chars - head - 32
    return text[:head] + "\n\n...[TRUNCATED]...\n\n" + text[-tail:]


def extract_response_text(resp_json: Dict[str, Any]) -> str:
    output_text = resp_json.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    collected: List[str] = []
    for item in resp_json.get("output", []):
        if item.get("type") != "message":
            continue
        for part in item.get("content", []):
            p_type = part.get("type")
            if p_type in {"output_text", "text"}:
                txt = part.get("text")
                if isinstance(txt, dict):
                    txt = txt.get("value", "")
                if isinstance(txt, str) and txt.strip():
                    collected.append(txt.strip())
    if collected:
        return "\n".join(collected).strip()

    # Backward compatibility fallback
    choices = resp_json.get("choices", [])
    if choices:
        msg = choices[0].get("message", {})
        content = msg.get("content")
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts = []
            for c in content:
                if isinstance(c, dict):
                    t = c.get("text") or c.get("content")
                    if isinstance(t, str):
                        parts.append(t)
            if parts:
                return "\n".join(parts).strip()
    return ""


def extract_first_json_object(text: str) -> Optional[Dict[str, Any]]:
    def _repair_json_like(v: str) -> str:
        t = (v or "").strip()
        if not t:
            return t

        # Remove optional markdown fences.
        t = re.sub(r"^\s*```(?:json)?\s*", "", t, flags=re.IGNORECASE)
        t = re.sub(r"\s*```\s*$", "", t)

        # Some responses contain over-escaped standalone JSON string lines:
        #     \"foo\"
        # Convert only when the whole line is a single JSON string token.
        t = re.sub(r'(?m)^(\s*)\\"(.*)\\"(\s*[,}\]])$', r'\1"\2"\3', t)
        return t

    text = text.strip()
    if not text:
        return None
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    repaired_text = _repair_json_like(text)
    if repaired_text != text:
        try:
            data = json.loads(repaired_text)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    # Best effort: find first balanced {...}
    start = text.find("{")
    if start < 0:
        return None

    in_str = False
    esc = False
    depth = 0
    end = -1
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue

        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i
                break

    if end < 0:
        return None
    chunk = text[start : end + 1]
    try:
        data = json.loads(chunk)
        if isinstance(data, dict):
            return data
    except Exception:
        repaired_chunk = _repair_json_like(chunk)
        try:
            data = json.loads(repaired_chunk)
            if isinstance(data, dict):
                return data
        except Exception:
            return None
    return None


def postprocess_parsed_result(parsed: Dict[str, Any], source_text: str) -> Dict[str, Any]:
    """
    Normalize parsed result for deterministic validation and replacement.
    """
    checks = parsed.get("field_checks")
    if not isinstance(checks, dict):
        return parsed

    for field in AUDIT_FIELDS:
        item = checks.get(field)
        if not isinstance(item, dict):
            continue

        status = str(item.get("status", "") or "").strip().lower()
        original_text = str(item.get("original_text", "") or "")
        corrected_text = str(item.get("corrected_text", "") or "")

        # Accurate rows must remain byte-for-byte with original column text.
        if status == "accurate":
            item["corrected_text"] = original_text
            item["correction_applied"] = False
            corrected_text = original_text
        else:
            item["correction_applied"] = bool(item.get("correction_applied", False))

        quotes = item.get("supporting_quotes", [])
        if not isinstance(quotes, list):
            quotes = []
        quotes = [q for q in quotes if isinstance(q, str) and q.strip()]
        matched_quotes = [q for q in quotes if contains_source_snippet(source_text, q)]

        # If a long block quote is not contiguous in source, salvage line-level matches.
        if not matched_quotes and quotes:
            line_matches: List[str] = []
            seen = set()
            for q in quotes:
                for ln in str(q).splitlines():
                    cand = ln.strip()
                    if not cand or cand.startswith("```"):
                        continue
                    if len(cand) < 8:
                        continue
                    if contains_source_snippet(source_text, cand):
                        key = normalize_for_match(cand)
                        if key and key not in seen:
                            seen.add(key)
                            line_matches.append(cand)
                if len(line_matches) >= 2:
                    break
            if line_matches:
                matched_quotes = line_matches

        if not matched_quotes and field == "execution_flow":
            step_matches: List[str] = []
            seen_steps = set()
            for raw_flow in (corrected_text, original_text):
                for step in re.split(r"\s*->\s*|[→⇒➜⟶⟹➔↦↣↪↝⇢➡]+\s*", str(raw_flow or "")):
                    cand = step.strip()
                    if len(cand) < 6:
                        continue
                    if contains_source_snippet(source_text, cand):
                        key = normalize_for_match(cand)
                        if key and key not in seen_steps:
                            seen_steps.add(key)
                            step_matches.append(cand)
                    if len(step_matches) >= 2:
                        break
                if len(step_matches) >= 2:
                    break
            if step_matches:
                matched_quotes = step_matches

        # Keep compact, source-grounded quotes.
        if matched_quotes:
            item["supporting_quotes"] = matched_quotes[:2]
        else:
            fallback = ""
            if corrected_text and contains_source_snippet(source_text, corrected_text):
                fallback = corrected_text
            elif original_text and contains_source_snippet(source_text, original_text):
                fallback = original_text

            if fallback:
                item["supporting_quotes"] = [fallback]
            elif field in {"why_research_related", "function_explanation", "evidence"}:
                m = re.search(r"(?im)^description:\s*(.+)$", source_text)
                if m:
                    item["supporting_quotes"] = [f"description: {m.group(1).strip()}"]
                elif status == "accurate":
                    item["supporting_quotes"] = []
                else:
                    item["supporting_quotes"] = quotes[:2]
            elif status == "accurate":
                item["supporting_quotes"] = []
            else:
                item["supporting_quotes"] = quotes[:2]

        if field == "evidence":
            # Keep evidence extractive when possible.
            ct = str(item.get("corrected_text", "") or "")
            if ct and not contains_source_snippet(source_text, ct):
                sq = item.get("supporting_quotes", [])
                if not isinstance(sq, list):
                    sq = []
                matched_sq = [q for q in sq if isinstance(q, str) and contains_source_snippet(source_text, q)]
                if matched_sq:
                    item["supporting_quotes"] = matched_sq[:2]
                    item["corrected_text"] = str(matched_sq[0])
                elif original_text and contains_source_snippet(source_text, original_text):
                    item["supporting_quotes"] = [original_text]
                    item["corrected_text"] = original_text
                else:
                    m = re.search(r"(?im)^description:\s*(.+)$", source_text)
                    if m:
                        desc = f"description: {m.group(1).strip()}"
                        item["supporting_quotes"] = [desc]
                        item["corrected_text"] = desc

        # Enforce accurate invariants after any evidence fallback.
        if status == "accurate":
            item["corrected_text"] = original_text
            item["correction_applied"] = False

    return parsed


def validate_alignment(parsed: Optional[Dict[str, Any]], source_text: str) -> Dict[str, Any]:
    """
    Lightweight post-check to ensure model corrections are source-grounded.
    """
    per_field: Dict[str, Dict[str, Any]] = {}
    all_passed = True

    if not isinstance(parsed, dict):
        return {
            "passed": False,
            "reason": "parsed_result is not a dict",
            "fields": {},
        }

    checks = parsed.get("field_checks")
    if not isinstance(checks, dict):
        return {
            "passed": False,
            "reason": "field_checks missing or invalid",
            "fields": {},
        }

    for field in AUDIT_FIELDS:
        item = checks.get(field) if isinstance(checks, dict) else None
        if not isinstance(item, dict):
            per_field[field] = {
                "passed": False,
                "issues": ["field payload missing"],
                "quotes_present": 0,
                "quotes_matched": 0,
            }
            all_passed = False
            continue

        original_text = str(item.get("original_text", "") or "")
        corrected_text = str(item.get("corrected_text", "") or "")
        correction_applied = bool(item.get("correction_applied", False))
        status = str(item.get("status", "") or "")
        quotes = item.get("supporting_quotes", [])
        if not isinstance(quotes, list):
            quotes = []
        quotes = [q for q in quotes if isinstance(q, str) and q.strip()]

        matched_quotes = [q for q in quotes if contains_source_snippet(source_text, q)]
        issues: List[str] = []
        warnings: List[str] = []

        if status == "accurate" and corrected_text != original_text:
            issues.append("status=accurate but corrected_text != original_text")
        if correction_applied and not quotes:
            issues.append("correction_applied=true but no supporting_quotes")
        if quotes and len(matched_quotes) == 0:
            issues.append("no supporting_quotes found in source")
        elif quotes and len(matched_quotes) < len(quotes):
            warnings.append("some supporting_quotes not found in source")
        if field == "evidence" and corrected_text and not contains_source_snippet(source_text, corrected_text):
            # Allow evidence to be supported by quote list even if corrected_text itself is condensed.
            if not matched_quotes:
                issues.append("evidence corrected_text not found in source and no matched quotes")
        if field == "execution_flow" and " -> " not in corrected_text and correction_applied:
            issues.append('execution_flow corrected_text should use " -> " separator')

        passed = len(issues) == 0
        if not passed:
            all_passed = False

        per_field[field] = {
            "passed": passed,
            "issues": issues,
            "warnings": warnings,
            "quotes_present": len(quotes),
            "quotes_matched": len(matched_quotes),
        }

    return {
        "passed": all_passed,
        "reason": None if all_passed else "One or more fields failed source-grounding checks",
        "fields": per_field,
    }


class ResponsesClient:
    def __init__(self, api_key: str, endpoint: str, model: str, timeout: int):
        self.api_key = api_key
        self.endpoint = endpoint
        self.model = model
        self.timeout = timeout
        self.local = threading.local()

    def _session(self) -> requests.Session:
        if not hasattr(self.local, "session"):
            self.local.session = requests.Session()
        return self.local.session

    def call(self, user_prompt: str) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "input": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.1,
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        last_error: Optional[str] = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self._session().post(
                    self.endpoint,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout,
                )
                if resp.status_code >= 500:
                    last_error = f"HTTP {resp.status_code}: {resp.text[:300]}"
                else:
                    resp.raise_for_status()
                    return {"ok": True, "response_json": resp.json(), "error": None}
            except Exception as exc:
                last_error = f"{type(exc).__name__}: {exc}"

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_SLEEP_SECONDS * attempt)

        return {"ok": False, "response_json": None, "error": last_error or "Unknown API error"}


def load_processed_ids(results_jsonl: Path) -> set:
    if not results_jsonl.exists():
        return set()
    processed = set()
    with results_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            row_id = obj.get("row_id")
            if isinstance(row_id, str) and row_id:
                processed.add(row_id)
    return processed


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_prompt(record: SkillRow, source_text: str) -> str:
    # Extract the four key fields from parsed_fields
    why_research_related = record.parsed_fields.get("why_research_related", "")
    function_explanation = record.parsed_fields.get("function_explanation", "")
    execution_flow = record.parsed_fields.get("execution_flow", "")
    evidence = record.parsed_fields.get("evidence", "")

    return USER_PROMPT_TEMPLATE.format(
        theme=record.theme,
        repo=record.repo or "unknown",
        skill=record.skill,
        url=record.url,
        local_path=record.local_path or "",
        row_raw=record.row_raw,
        why_research_related=why_research_related,
        function_explanation=function_explanation,
        execution_flow=execution_flow,
        evidence=evidence,
        source_excerpt=source_text,
    )


def audit_one_record(client: ResponsesClient, record: SkillRow, max_source_chars: int) -> Dict[str, Any]:
    t0 = time.time()
    local_path = Path(record.local_path or "")
    if not local_path.exists():
        return {
            "row_id": record.row_id,
            "theme": record.theme,
            "source_doc": record.source_doc,
            "repo": record.repo,
            "line_no": record.line_no,
            "skill": record.skill,
            "url": record.url,
            "local_path": record.local_path,
            "ok": False,
            "error": "Local source file not found",
            "elapsed_seconds": round(time.time() - t0, 3),
        }

    source_raw = local_path.read_text(encoding="utf-8", errors="replace")
    source_excerpt = excerpt_text(source_raw, max_source_chars)
    prompt = build_prompt(record, source_excerpt)

    api_result = client.call(prompt)
    if not api_result["ok"]:
        return {
            "row_id": record.row_id,
            "theme": record.theme,
            "source_doc": record.source_doc,
            "repo": record.repo,
            "line_no": record.line_no,
            "skill": record.skill,
            "url": record.url,
            "local_path": record.local_path,
            "ok": False,
            "error": api_result["error"],
            "elapsed_seconds": round(time.time() - t0, 3),
        }

    resp_json = api_result["response_json"]
    resp_text = extract_response_text(resp_json)
    parsed = extract_first_json_object(resp_text)
    if isinstance(parsed, dict):
        parsed = postprocess_parsed_result(parsed, source_raw)
    alignment_validation = validate_alignment(parsed, source_raw) if parsed is not None else None

    return {
        "row_id": record.row_id,
        "theme": record.theme,
        "source_doc": record.source_doc,
        "repo": record.repo,
        "line_no": record.line_no,
        "skill": record.skill,
        "url": record.url,
        "local_path": record.local_path,
        "ok": parsed is not None,
        "error": None if parsed is not None else "Model output is not valid JSON",
        "aligned_with_source": bool(alignment_validation and alignment_validation.get("passed")),
        "alignment_validation": alignment_validation,
        "parsed_result": parsed,
        "model_output_text": resp_text,
        "api_response_id": resp_json.get("id"),
        "usage": resp_json.get("usage"),
        "elapsed_seconds": round(time.time() - t0, 3),
    }


def build_mismatch_report(results: List[Dict[str, Any]], output_path: Path) -> None:
    lines = ["# Skill Description Mismatch Report", ""]
    mismatch_count = 0
    for row in results:
        parsed = row.get("parsed_result") or {}
        checks = (parsed.get("field_checks") or {}) if isinstance(parsed, dict) else {}
        alignment = row.get("alignment_validation") or {}
        alignment_fields = alignment.get("fields", {}) if isinstance(alignment, dict) else {}

        statuses = []
        for k in AUDIT_FIELDS:
            status = ((checks.get(k) or {}) if isinstance(checks, dict) else {}).get("status")
            statuses.append(status)

        has_problem = any(s in {"partial", "mismatch"} for s in statuses) or not bool(row.get("aligned_with_source", False))
        if not has_problem:
            continue
        mismatch_count += 1

        lines.append(f"## {row.get('skill', '')} ({row.get('repo', '')})")
        lines.append(f"- Theme: `{row.get('theme', '')}`")
        lines.append(f"- URL: {row.get('url', '')}")
        lines.append(f"- Row ID: `{row.get('row_id', '')}`")
        lines.append(f"- Aligned With Source: **{row.get('aligned_with_source', False)}**")
        lines.append("")

        for k in AUDIT_FIELDS:
            item = checks.get(k) or {}
            lines.append(f"- {k}: **{item.get('status', 'unknown')}**")
            reason = (item.get("reason") or "").strip()
            if reason:
                lines.append(f"  - reason: {reason}")
            corrected = (item.get("corrected_text") or "").strip()
            if corrected:
                lines.append(f"  - corrected_text: {corrected}")
            quotes = item.get("supporting_quotes")
            if isinstance(quotes, list) and quotes:
                lines.append(f"  - supporting_quotes: {len([q for q in quotes if isinstance(q, str) and q.strip()])}")

            aitem = alignment_fields.get(k) if isinstance(alignment_fields, dict) else None
            if isinstance(aitem, dict) and not aitem.get("passed", False):
                issues = aitem.get("issues", [])
                if isinstance(issues, list) and issues:
                    lines.append(f"  - alignment_issues: {'; '.join(str(x) for x in issues)}")
        lines.append("")

    lines.insert(2, f"- Total mismatch/partial rows: **{mismatch_count}**")
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def summarize_results(all_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(all_rows)
    ok = sum(1 for r in all_rows if r.get("ok"))
    fail = total - ok
    aligned = sum(1 for r in all_rows if r.get("aligned_with_source") is True)
    unaligned = sum(1 for r in all_rows if r.get("ok") and r.get("aligned_with_source") is False)

    status_counter = {field: {"accurate": 0, "partial": 0, "mismatch": 0} for field in AUDIT_FIELDS}
    overall_counter: Dict[str, int] = {}

    for row in all_rows:
        parsed = row.get("parsed_result")
        if not isinstance(parsed, dict):
            continue
        overall = parsed.get("overall_match")
        if isinstance(overall, str):
            overall_counter[overall] = overall_counter.get(overall, 0) + 1

        checks = parsed.get("field_checks")
        if not isinstance(checks, dict):
            continue
        for field in AUDIT_FIELDS:
            status = (checks.get(field) or {}).get("status")
            if status in status_counter[field]:
                status_counter[field][status] += 1

    by_theme: Dict[str, int] = {}
    for row in all_rows:
        theme = row.get("theme", "unknown")
        by_theme[theme] = by_theme.get(theme, 0) + 1

    return {
        "total_rows": total,
        "ok_rows": ok,
        "failed_rows": fail,
        "aligned_rows": aligned,
        "unaligned_rows": unaligned,
        "overall_match_counts": overall_counter,
        "field_status_counts": status_counter,
        "theme_counts": by_theme,
    }


def main() -> None:
    args = parse_args()

    if API_KEY == "REPLACE_WITH_YOUR_API_KEY" and not args.dry_run:
        raise SystemExit("Please edit API_KEY in script before running (or run with --dry-run).")

    theme_dir = Path(args.theme_dir)
    manifest_path = Path(args.manifest)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_ts = time.strftime("%Y%m%d-%H%M%S")
    run_dir = output_dir / f"run-{run_ts}"
    run_dir.mkdir(parents=True, exist_ok=True)

    theme_files = sorted(
        p for p in theme_dir.glob("*.md") if p.name.lower() != "readme.md"
    )
    if args.theme:
        wanted = {x.strip() for x in args.theme if x.strip()}
        theme_files = [p for p in theme_files if p.stem in wanted or p.name in wanted]
    if not theme_files:
        raise SystemExit(f"No theme markdown files found in {theme_dir}")

    rows: List[SkillRow] = []
    for md in theme_files:
        rows.extend(parse_theme_markdown(md))

    manifest_map = load_manifest_map(manifest_path)
    missing_local = 0
    for row in rows:
        local_path = manifest_map.get(row.url)
        row.local_path = local_path
        if not local_path:
            missing_local += 1

    rows = [r for r in rows if r.local_path]

    if args.limit and args.limit > 0:
        rows = rows[: args.limit]

    input_rows_path = run_dir / "input_rows.jsonl"
    write_jsonl(input_rows_path, [asdict(r) for r in rows])

    summary_init = {
        "api_endpoint": API_ENDPOINT,
        "model": MODEL_NAME,
        "theme_dir": str(theme_dir),
        "manifest": str(manifest_path),
        "theme_docs": [p.name for p in theme_files],
        "rows_parsed": len(rows),
        "rows_missing_local_source": missing_local,
        "workers": args.workers,
        "max_source_chars": args.max_source_chars,
        "dry_run": args.dry_run,
        "started_at": run_ts,
    }
    (run_dir / "run_config.json").write_text(
        json.dumps(summary_init, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if args.dry_run:
        print(json.dumps(summary_init, ensure_ascii=False, indent=2))
        print(f"Dry-run completed. Output: {run_dir}")
        return

    results_jsonl = run_dir / "audit_results.jsonl"
    processed_ids = load_processed_ids(results_jsonl) if args.resume else set()
    pending_rows = [r for r in rows if r.row_id not in processed_ids]

    print(f"Total rows: {len(rows)}")
    print(f"Already processed (resume): {len(processed_ids)}")
    print(f"Pending rows: {len(pending_rows)}")

    client = ResponsesClient(
        api_key=API_KEY,
        endpoint=API_ENDPOINT,
        model=MODEL_NAME,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    all_results: List[Dict[str, Any]] = []
    lock = threading.Lock()

    def _run_one(rec: SkillRow) -> Dict[str, Any]:
        return audit_one_record(client, rec, max_source_chars=args.max_source_chars)

    done = 0
    total = len(pending_rows)
    progress_every = 1 if args.workers <= 1 else 20
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        future_map = {pool.submit(_run_one, rec): rec for rec in pending_rows}
        for fut in concurrent.futures.as_completed(future_map):
            result = fut.result()
            with lock:
                write_jsonl(results_jsonl, [result])
                all_results.append(result)
                done += 1
                if done % progress_every == 0 or done == total:
                    ok_count = sum(1 for x in all_results if x.get("ok"))
                    print(f"Progress: {done}/{total} (ok={ok_count})")

    # Reload complete result file (includes resumed records + new records)
    merged_results: List[Dict[str, Any]] = []
    with results_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                merged_results.append(json.loads(line))
            except Exception:
                continue

    summary = summarize_results(merged_results)
    summary["completed_at"] = time.strftime("%Y%m%d-%H%M%S")
    summary["result_file"] = str(results_jsonl)
    (run_dir / "audit_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    mismatch_path = run_dir / "audit_mismatch_only.md"
    build_mismatch_report(merged_results, mismatch_path)

    print("Done.")
    print(f"Run directory: {run_dir}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()



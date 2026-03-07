"""
audit_all_skills.py
[IN]  Final_Research_Skills_Thematic_Split/0*.md (8 theme documents)
      Final_Research_Skills_Link_Downloads_By_Theme_LATEST/ (local SKILL.md files)
      API: https://yunwu.ai/v1 (gpt-5.2)
[OUT] audit_results.json (per-skill structured audit)
      audit_summary.md (human-readable report)
      audit_failed_cases.json / audit_failed_cases.md (failed execution cases and report)
      audit_results_debug.json / audit_summary_debug.md / audit_failed_cases_debug.* (debug-mode outputs)
[POS] Full audit of ~2,074 research skill descriptions using LLM API batch calls.
      Evaluates: Function Explanation accuracy, Research Relevance quality, Overall Quality (1-5).
      Supports concurrent batch processing via --concurrency flag (default 5).
"""

import argparse
import json
import os
import re
import sys
import time
import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -- Configuration --
API_KEY = os.getenv("API_KEY", "")
API_BASE = os.getenv("BASE_URL", "https://yunwu.ai") + "/v1"
MODEL = "gpt-5.2"
BATCH_SIZE = 15
CHECKPOINT_EVERY = 5
MAX_RETRIES = 3
RETRY_BASE_SLEEP = 3.0
SKILLMD_TRUNCATE = 8000

BASE_DIR = Path(__file__).resolve().parent
THEME_DIR = BASE_DIR / "Final_Research_Skills_Thematic_Split"
DOWNLOAD_DIR = BASE_DIR / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
OUTPUT_DIR = BASE_DIR
CHECKPOINT_PATH = OUTPUT_DIR / "audit_checkpoint.json"
RESULTS_PATH = OUTPUT_DIR / "audit_results.json"
SUMMARY_PATH = OUTPUT_DIR / "audit_summary.md"
FAILED_CASES_JSON_PATH = OUTPUT_DIR / "audit_failed_cases.json"
FAILED_CASES_MD_PATH = OUTPUT_DIR / "audit_failed_cases.md"

DEBUG_RESULTS_PATH = OUTPUT_DIR / "audit_results_debug.json"
DEBUG_SUMMARY_PATH = OUTPUT_DIR / "audit_summary_debug.md"
DEBUG_FAILED_CASES_JSON_PATH = OUTPUT_DIR / "audit_failed_cases_debug.json"
DEBUG_FAILED_CASES_MD_PATH = OUTPUT_DIR / "audit_failed_cases_debug.md"

THEME_FILES = [
    "01_information_retrieval_evidence_collection.md",
    "02_literature_review_writing_citation_part1.md",
    "02_literature_review_writing_citation_part2.md",
    "03_experiment_benchmark_reproducibility_validation_part1.md",
    "03_experiment_benchmark_reproducibility_validation_part2.md",
    "04_data_analysis_and_evidence_interpretation.md",
    "05_research_operations_and_workflow_support.md",
    "06_Additional_Scientific_Skills.md",
]

SYSTEM_PROMPT = (
    "You are a research skill quality auditor. Evaluate each skill and return a JSON array.\n\n"
    "## Core Rules\n"
    "- Base judgments ONLY on the provided data. Do not fabricate information.\n"
    "- If SKILL.md description is provided, compare Function Explanation against it.\n"
    "- If SKILL.md is not available, set function_accuracy to \"cannot_verify\".\n"
    "- Output ONLY a valid JSON array. No markdown fences, no extra text.\n\n"
    "## Calibration for function_accuracy\n"
    "Function Explanation is a HIGH-LEVEL SUMMARY (typically 2-5 sentences). "
    "It is NOT expected to list every feature from SKILL.md.\n"
    "- \"accurate\": Correctly captures the MAIN PURPOSE and KEY CAPABILITIES. "
    "Rewording, paraphrasing, or omitting minor/secondary features is acceptable.\n"
    "- \"partial\": Misses a MAJOR capability (e.g., skill does both X and Y but summary only mentions X), "
    "OR introduces claims not supported by SKILL.md (hallucination).\n"
    "- \"inaccurate\": Fundamentally misrepresents what the skill does.\n"
    "- \"cannot_verify\": No SKILL.md available.\n\n"
    "## What counts as \"key details\"\n"
    "Key details = PRIMARY PURPOSE + MAJOR CAPABILITIES (top 1-3 things it does). "
    "Minor features, implementation specifics, version numbers, edge-case behaviors, "
    "and secondary options are NOT key details. Omitting them should NOT downgrade the rating.\n\n"
    "## Examples\n"
    "ACCURATE: Summary says \"PDF extraction, creation, merge/split, forms, and scalable processing\" "
    "— SKILL.md describes the same capabilities. Faithfully mirrors the source.\n"
    "ACCURATE: Summary says \"semantic code search with orchestrated reader/indexer agents\" "
    "— SKILL.md lists same purpose with additional operational details. Captures the essence.\n"
    "PARTIAL: Summary mentions only \"fingerprint-based similarity\" but SKILL.md describes "
    "BOTH similarity search AND Butina clustering as co-equal major features. A major capability missing.\n"
    "PARTIAL: Summary adds \"auto-load at session start\" not stated anywhere in SKILL.md. "
    "Introduces unsupported claims."
)


# -- Data Loading --

def build_repo_dir_map():
    repo_map = {}
    for theme_dir in os.listdir(DOWNLOAD_DIR):
        theme_path = DOWNLOAD_DIR / theme_dir
        if not theme_path.is_dir():
            continue
        for repo_dir in os.listdir(theme_path):
            repo_path = theme_path / repo_dir
            if not repo_path.is_dir():
                continue
            if '__' in repo_dir:
                owner, repo = repo_dir.split('__', 1)
                key = f"{owner}/{repo}"
                if key not in repo_map:
                    repo_map[key] = []
                repo_map[key].append(str(repo_path))
    return repo_map


def extract_yaml_description(content):
    if not content.startswith('---'):
        return None
    end = content.find('\n---', 3)
    if end == -1:
        return None
    frontmatter = content[3:end]
    m = re.search(r'^description:\s*(.+?)(?=\n\w|\Z)', frontmatter, re.MULTILINE | re.DOTALL)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def parse_theme_markdown(md_path):
    content = open(md_path, encoding='utf-8').read()
    lines = content.split('\n')
    theme = Path(md_path).stem
    skills = []
    current_repo = ""

    for line in lines:
        line = line.rstrip('\r')
        if line.startswith('### '):
            current_repo = line[4:].strip()
            continue
        if not line.startswith('|') or line.startswith('| Skill |') or line.startswith('|---|'):
            continue
        if '[link](' not in line:
            continue

        parts = line.split('|')
        if parts and not parts[0].strip():
            parts = parts[1:]
        if parts and not parts[-1].strip():
            parts = parts[:-1]
        if len(parts) < 7:
            continue
        if len(parts) > 7:
            parts = parts[:6] + ['|'.join(parts[6:])]

        url_m = re.search(r'\[link\]\((https?://[^)\s]+)\)', parts[2])
        row_id = hashlib.sha1(
            f"{theme}:{current_repo}:{parts[0].strip()}:{parts[1].strip()}".encode()
        ).hexdigest()[:12]

        skills.append({
            "row_id": row_id,
            "theme": theme,
            "repo": current_repo,
            "skill_name": parts[0].strip().strip('`'),
            "evidence_file": parts[1].strip().strip('`'),
            "skill_url": url_m.group(1) if url_m else "",
            "why_research_related": parts[3].strip(),
            "function_explanation": parts[4].strip(),
            "execution_flow": parts[5].strip(),
            "evidence": parts[6].strip(),
        })
    return skills


def load_all_skills():
    all_skills = []
    for tf in THEME_FILES:
        path = THEME_DIR / tf
        if not path.exists():
            print(f"WARNING: {tf} not found")
            continue
        skills = parse_theme_markdown(path)
        all_skills.extend(skills)
        print(f"  {tf}: {len(skills)} skills")
    return all_skills


def resolve_local_descriptions(skills, repo_map, debug=False):
    found = 0
    for s in skills:
        repo_dirs = repo_map.get(s["repo"], [])
        desc = None
        tried_paths = []
        for rd in repo_dirs:
            skill_path = os.path.join(rd, s["evidence_file"])
            tried_paths.append(skill_path)
            if os.path.exists(skill_path):
                try:
                    desc = open(skill_path, encoding='utf-8').read()
                except Exception:
                    pass
                break
        s["local_description"] = desc
        if desc:
            found += 1
        if debug:
            status = "FOUND" if desc else "MISSING"
            print(f"    [{status}] {s['skill_name']}")
            for p in tried_paths:
                print(f"      path: {p}")
            if desc:
                print(f"      description: {desc[:150]}...")
    print(f"  Local SKILL.md resolved: {found}/{len(skills)}")
    return skills


# -- Prompt Building --

def build_user_prompt(batch):
    parts = []
    for i, s in enumerate(batch, 1):
        lines = [f"### Skill {i}: `{s['skill_name']}` ({s['repo']})"]
        lines.append(f"- Theme: {s['theme']}")
        lines.append(f"- Why Research-Related: {s['why_research_related']}")
        lines.append(f"- Function Explanation: {s['function_explanation']}")
        lines.append(f"- Evidence: {s['evidence']}")
        if s.get("local_description"):
            desc = s["local_description"][:SKILLMD_TRUNCATE]
            lines.append(f"- SKILL.md full content:\n{desc}")
        else:
            lines.append("- SKILL.md: Not available")
        parts.append('\n'.join(lines))

    skills_text = '\n\n'.join(parts)
    n = len(batch)

    response_schema = (
        '[{"index":1,"skill_name":"...","function_accuracy":"accurate|partial|inaccurate|cannot_verify",'
        '"function_accuracy_reason":"brief","research_relevance":"valid|weak|invalid",'
        '"research_relevance_reason":"brief","overall_quality":4,"issues":[]}]'
    )

    return (
        f"Evaluate these {n} research skills:\n\n"
        f"{skills_text}\n\n"
        "For each skill, assess:\n\n"
        "1. function_accuracy: Compare Function Explanation (a high-level summary) against SKILL.md.\n"
        "   The summary is NOT expected to cover every detail — judge by main purpose and key capabilities.\n"
        '   - "accurate": correctly captures main purpose and key capabilities\n'
        '   - "partial": misses a MAJOR capability or introduces unsupported claims\n'
        '   - "inaccurate": fundamentally misrepresents the skill\n'
        '   - "cannot_verify": no SKILL.md available\n\n'
        "2. research_relevance: is the Why Research-Related rationale valid?\n"
        '   - "valid": convincing, specific reasoning\n'
        '   - "weak": generic or tangential\n'
        '   - "invalid": no real research connection\n\n'
        "3. overall_quality: 1-5 (5=excellent, 4=good, 3=acceptable, 2=poor, 1=unacceptable)\n\n"
        f"Return a JSON array (same order, one object per skill):\n{response_schema}"
    )


# -- API --

def call_api(client, user_prompt):
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.0,
                max_tokens=4096,
            )
            return resp.choices[0].message.content
        except Exception as e:
            sleep_time = RETRY_BASE_SLEEP * (2 ** attempt)
            print(f"\n    API error (attempt {attempt+1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(sleep_time)
            else:
                raise


def parse_response(text, expected_count):
    if not text:
        return None
    text = text.strip()
    # Remove markdown fences
    if text.startswith('```'):
        text = re.sub(r'^```\w*\n?', '', text)
        text = re.sub(r'\n?```$', '', text)
        text = text.strip()
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass
    # Try to find JSON array in text
    m = re.search(r'\[.*\]', text, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group())
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return None


def get_output_paths(debug=False):
    if debug:
        return {
            "results": DEBUG_RESULTS_PATH,
            "summary": DEBUG_SUMMARY_PATH,
            "failed_json": DEBUG_FAILED_CASES_JSON_PATH,
            "failed_md": DEBUG_FAILED_CASES_MD_PATH,
        }
    return {
        "results": RESULTS_PATH,
        "summary": SUMMARY_PATH,
        "failed_json": FAILED_CASES_JSON_PATH,
        "failed_md": FAILED_CASES_MD_PATH,
    }


def make_error_entry(skill, error_type, error_detail, stage="", batch_index=-1):
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "row_id": skill.get("row_id", ""),
        "skill_name": skill.get("skill_name", ""),
        "repo": skill.get("repo", ""),
        "theme": skill.get("theme", ""),
        "evidence_file": skill.get("evidence_file", ""),
        "stage": stage,
        "batch_index": batch_index,
        "error_type": error_type,
        "error": str(error_detail)[:500],
    }


# -- Checkpoint --

def save_checkpoint(results, errors, batch_idx, total_batches):
    checkpoint = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "batches_completed": batch_idx + 1,
        "batches_total": total_batches,
        "skills_completed": len(results),
        "errors_count": len(errors),
        "completed_row_ids": [r["row_id"] for r in results],
        "results": results,
        "errors": errors,
    }
    with open(CHECKPOINT_PATH, 'w', encoding='utf-8') as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)


def load_checkpoint():
    if not CHECKPOINT_PATH.exists():
        return set(), [], []
    try:
        data = json.load(open(CHECKPOINT_PATH, encoding='utf-8'))
        completed = set(data.get("completed_row_ids", []))
        print(f"  Loaded: {len(completed)} skills done")
        return completed, data.get("results", []), data.get("errors", [])
    except Exception:
        return set(), [], []


# -- Output --

def write_results(results, errors, started_at, output_path):
    output = {
        "metadata": {
            "model": MODEL,
            "started_at": started_at,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "total_audited": len(results),
            "error_count": len(errors),
        },
        "results": results,
        "errors": errors,
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Results: {output_path}")


def write_summary(results, errors, output_path):
    total = len(results)
    if total == 0:
        return

    acc_dist = {}
    rel_dist = {}
    qual_dist = {}
    theme_stats = {}

    for r in results:
        fa = r.get("function_accuracy", "unknown")
        acc_dist[fa] = acc_dist.get(fa, 0) + 1
        rr = r.get("research_relevance", "unknown")
        rel_dist[rr] = rel_dist.get(rr, 0) + 1
        oq = r.get("overall_quality", 0)
        qual_dist[oq] = qual_dist.get(oq, 0) + 1
        theme = r.get("theme", "unknown")
        if theme not in theme_stats:
            theme_stats[theme] = {"count": 0, "sum_quality": 0, "invalid": 0}
        theme_stats[theme]["count"] += 1
        theme_stats[theme]["sum_quality"] += oq
        if rr == "invalid":
            theme_stats[theme]["invalid"] += 1

    flagged = [r for r in results
               if r.get("overall_quality", 5) <= 2 or r.get("research_relevance") == "invalid"]

    lines = [
        "# Research Skills Full Audit Summary",
        "",
        f"- Date: {datetime.now().strftime('%Y-%m-%d')}",
        f"- Model: {MODEL}",
        f"- Total Audited: {total}",
        f"- Errors: {len(errors)}",
        "",
        "## Function Explanation Accuracy",
        "",
        "| Rating | Count | % |",
        "|--------|------:|--:|",
    ]
    for rating in ["accurate", "partial", "inaccurate", "cannot_verify"]:
        c = acc_dist.get(rating, 0)
        lines.append(f"| {rating} | {c} | {c*100/total:.1f}% |")

    lines += ["", "## Research Relevance", "", "| Rating | Count | % |", "|--------|------:|--:|"]
    for rating in ["valid", "weak", "invalid"]:
        c = rel_dist.get(rating, 0)
        lines.append(f"| {rating} | {c} | {c*100/total:.1f}% |")

    lines += ["", "## Quality Score", "", "| Score | Count | % |", "|------:|------:|--:|"]
    for score in [5, 4, 3, 2, 1]:
        c = qual_dist.get(score, 0)
        lines.append(f"| {score} | {c} | {c*100/total:.1f}% |")

    lines += ["", "## By Theme", "", "| Theme | Total | Avg | Invalid |", "|-------|------:|----:|--------:|"]
    for theme in sorted(theme_stats.keys()):
        ts = theme_stats[theme]
        avg = ts["sum_quality"] / ts["count"] if ts["count"] else 0
        lines.append(f"| {theme[:50]} | {ts['count']} | {avg:.1f} | {ts['invalid']} |")

    lines += ["", f"## Flagged ({len(flagged)})", ""]
    if flagged:
        lines += ["| Skill | Repo | Score | Relevance | Issues |", "|-------|------|------:|-----------|--------|"]
        for r in flagged[:100]:
            iss = '; '.join(r.get("issues", []))[:60]
            lines.append(f"| {r.get('skill_name','')} | {r.get('repo','')} | {r.get('overall_quality','')} | {r.get('research_relevance','')} | {iss} |")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Summary: {output_path}")


def write_failed_cases(errors, results, started_at, json_path, md_path):
    error_type_dist = {}
    stage_dist = {}
    for e in errors:
        et = e.get("error_type", "unknown")
        st = e.get("stage", "unknown")
        error_type_dist[et] = error_type_dist.get(et, 0) + 1
        stage_dist[st] = stage_dist.get(st, 0) + 1

    failed_output = {
        "metadata": {
            "model": MODEL,
            "started_at": started_at,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "total_audited_results": len(results),
            "failed_case_count": len(errors),
        },
        "error_type_distribution": error_type_dist,
        "stage_distribution": stage_dist,
        "failed_cases": errors,
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(failed_output, f, ensure_ascii=False, indent=2)
    print(f"Failed cases JSON: {json_path}")

    lines = [
        "# Audit Failed Cases Report",
        "",
        f"- Date: {datetime.now().strftime('%Y-%m-%d')}",
        f"- Model: {MODEL}",
        f"- Total Failed Cases: {len(errors)}",
        "",
        "## Error Type Distribution",
        "",
        "| Error Type | Count |",
        "|---|---:|",
    ]
    for error_type, count in sorted(error_type_dist.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {error_type} | {count} |")

    lines += ["", "## Stage Distribution", "", "| Stage | Count |", "|---|---:|"]
    for stage, count in sorted(stage_dist.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {stage} | {count} |")

    lines += [
        "",
        "## Failed Case Details (Top 300)",
        "",
        "| Time | Skill | Repo | Theme | Stage | Type | Error |",
        "|---|---|---|---|---|---|---|",
    ]
    for e in errors[:300]:
        err_txt = str(e.get("error", "")).replace("\n", " ").replace("|", "\\|")
        lines.append(
            f"| {e.get('timestamp','')} | {e.get('skill_name','')} | "
            f"{e.get('repo','')} | {e.get('theme','')} | {e.get('stage','')} | "
            f"{e.get('error_type','')} | {err_txt[:120]} |"
        )

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Failed cases MD: {md_path}")


# -- Main --

def main():
    parser = argparse.ArgumentParser(description="Full audit of research skill descriptions")
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Debug mode: verbose output, checkpoint writes disabled, outputs saved to *_debug files',
    )
    parser.add_argument('--count', type=int, default=0, help='Only audit first N skills (use with --debug)')
    parser.add_argument('--skill-name', type=str, default='', help='Only audit skills matching this name (use with --debug)')
    parser.add_argument('--concurrency', type=int, default=5, help='Number of concurrent batch workers (default: 5)')
    args = parser.parse_args()

    debug = args.debug
    output_paths = get_output_paths(debug=debug)
    if debug:
        sys.stdout.reconfigure(encoding='utf-8')

    started_at = datetime.now(timezone.utc).isoformat()
    print("=" * 60)
    print("Research Skills Full Audit" + (" [DEBUG MODE]" if debug else ""))
    print("=" * 60)

    print("\n[1/4] Loading skills...")
    all_skills = load_all_skills()
    print(f"  Total: {len(all_skills)}")

    # Filter skills in debug mode
    if args.skill_name:
        all_skills = [s for s in all_skills if args.skill_name.lower() in s["skill_name"].lower()]
        print(f"  Filtered by name '{args.skill_name}': {len(all_skills)} skills")
    if args.count > 0:
        all_skills = all_skills[:args.count]
        print(f"  Limited to first {args.count}: {len(all_skills)} skills")

    if debug:
        print("\n  --- Parsed skill data ---")
        for i, s in enumerate(all_skills, 1):
            print(f"\n  [{i}] {s['skill_name']}  ({s['repo']})")
            print(f"      theme:           {s['theme']}")
            print(f"      evidence_file:   {s['evidence_file']}")
            print(f"      why_research:    {s['why_research_related'][:120]}...")
            print(f"      func_explanation:{s['function_explanation'][:120]}...")
            print(f"      evidence:        {s['evidence'][:120]}...")

    print("\n[2/4] Resolving local SKILL.md...")
    repo_map = build_repo_dir_map()
    all_skills = resolve_local_descriptions(all_skills, repo_map, debug=debug)

    if not debug:
        print("\n[3/4] Checkpoint...")
        completed_ids, results, errors = load_checkpoint()
        remaining = [s for s in all_skills if s["row_id"] not in completed_ids]
        print(f"  Remaining: {len(remaining)}")
    else:
        print("\n[3/4] Checkpoint... SKIPPED (debug mode)")
        completed_ids = set()
        results = []
        errors = []
        remaining = all_skills

    total_batches = 0
    if remaining:
        batch_list = [remaining[i:i+BATCH_SIZE] for i in range(0, len(remaining), BATCH_SIZE)]
        total_batches = len(batch_list)
        concurrency = args.concurrency
        print(f"  Batches: {total_batches}  (concurrency: {concurrency})")

        client = OpenAI(api_key=API_KEY, base_url=API_BASE)

        # Thread-safe state for concurrent processing
        lock = threading.Lock()
        batches_done = [0]  # mutable counter for progress

        def process_batch(bi, batch):
            """Process a single batch: build prompt, call API, parse response.
            Returns (batch_results, batch_errors) for the caller to merge."""
            batch_results = []
            batch_errors = []
            try:
                prompt = build_user_prompt(batch)

                if debug:
                    with lock:
                        print(f"\n  --- PROMPT SENT TO API (batch {bi+1}) ---")
                        print(f"  System: {SYSTEM_PROMPT[:200]}...")
                        print(f"\n  User ({len(prompt)} chars):")
                        print("  " + prompt.replace("\n", "\n  "))
                        print("  --- END PROMPT ---\n")

                resp_text = call_api(client, prompt)

                if debug:
                    with lock:
                        print(f"  --- RAW API RESPONSE (batch {bi+1}) ---")
                        print("  " + (resp_text or "(empty)").replace("\n", "\n  "))
                        print("  --- END RESPONSE ---\n")

                parsed = parse_response(resp_text, len(batch))

                if parsed:
                    for i, skill in enumerate(batch):
                        r = parsed[i] if i < len(parsed) else {}
                        if i >= len(parsed):
                            batch_errors.append(
                                make_error_entry(
                                    skill,
                                    error_type="response_item_missing",
                                    error_detail=f"missing item in parsed response; parsed={len(parsed)} expected={len(batch)}",
                                    stage="parse_response",
                                    batch_index=bi + 1,
                                )
                            )
                        result = {
                            "row_id": skill["row_id"],
                            "skill_name": skill["skill_name"],
                            "repo": skill["repo"],
                            "theme": skill["theme"],
                            "has_local_file": skill.get("local_description") is not None,
                            "function_accuracy": r.get("function_accuracy", "unknown"),
                            "function_accuracy_reason": r.get("function_accuracy_reason", ""),
                            "research_relevance": r.get("research_relevance", "unknown"),
                            "research_relevance_reason": r.get("research_relevance_reason", ""),
                            "overall_quality": r.get("overall_quality", 0),
                            "issues": r.get("issues", []),
                        }
                        batch_results.append(result)

                        if debug:
                            with lock:
                                print(f"  --- RESULT [{i+1}] {skill['skill_name']} (batch {bi+1}) ---")
                                for k, v in result.items():
                                    if k == "row_id":
                                        continue
                                    print(f"    {k}: {v}")

                    with lock:
                        batches_done[0] += 1
                        print(f"  Batch {bi+1}/{total_batches} OK ({len(parsed)} results)  [{batches_done[0]}/{total_batches} done]")
                else:
                    resp_excerpt = (resp_text or "").strip().replace("\n", " ")[:300]
                    for s in batch:
                        batch_errors.append(
                            make_error_entry(
                                s,
                                error_type="parse_failed",
                                error_detail=f"parse failed. response excerpt: {resp_excerpt}",
                                stage="parse_response",
                                batch_index=bi + 1,
                            )
                        )
                    with lock:
                        batches_done[0] += 1
                        print(f"  Batch {bi+1}/{total_batches} FAILED (parse)  [{batches_done[0]}/{total_batches} done]")
            except Exception as e:
                for s in batch:
                    batch_errors.append(
                        make_error_entry(
                            s,
                            error_type="api_or_runtime_error",
                            error_detail=str(e),
                            stage="call_api",
                            batch_index=bi + 1,
                        )
                    )
                with lock:
                    batches_done[0] += 1
                    print(f"  Batch {bi+1}/{total_batches} ERROR: {e}  [{batches_done[0]}/{total_batches} done]")

            return batch_results, batch_errors

        print(f"\n[4/4] Processing ({concurrency} concurrent workers)...")

        if concurrency <= 1:
            # Sequential fallback (original behavior)
            for bi, batch in enumerate(batch_list):
                print(f"\n  Batch {bi+1}/{total_batches} ({len(batch)} skills)...")
                br, be = process_batch(bi, batch)
                results.extend(br)
                errors.extend(be)
                for r in br:
                    completed_ids.add(r["row_id"])
                if not debug and (bi + 1) % CHECKPOINT_EVERY == 0:
                    save_checkpoint(results, errors, bi, total_batches)
                    print(f"  [Checkpoint: {len(results)} done]")
                time.sleep(0.5)
        else:
            # Concurrent execution
            checkpoint_counter = [0]
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = {executor.submit(process_batch, bi, batch): bi
                           for bi, batch in enumerate(batch_list)}
                for future in as_completed(futures):
                    bi = futures[future]
                    try:
                        br, be = future.result()
                    except Exception as e:
                        print(f"  Batch {bi+1} unexpected executor error: {e}")
                        br, be = [], []
                    with lock:
                        results.extend(br)
                        errors.extend(be)
                        for r in br:
                            completed_ids.add(r["row_id"])
                        checkpoint_counter[0] += 1
                        if not debug and checkpoint_counter[0] % CHECKPOINT_EVERY == 0:
                            save_checkpoint(results, errors, bi, total_batches)
                            print(f"  [Checkpoint: {len(results)} done]")
    else:
        print("  All skills already audited!")

    if not debug:
        save_checkpoint(results, errors, total_batches - 1 if total_batches else 0, total_batches)
    print("\n" + "=" * 60)
    write_results(results, errors, started_at, output_paths["results"])
    write_summary(results, errors, output_paths["summary"])
    write_failed_cases(
        errors,
        results,
        started_at,
        output_paths["failed_json"],
        output_paths["failed_md"],
    )

    print(f"\nDone! {len(results)} audited, {len(errors)} errors.")


if __name__ == '__main__':
    main()

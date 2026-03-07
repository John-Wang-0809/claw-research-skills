"""
fix_descriptions.py
[IN]  audit_results.json (审核结果)
      Final_Research_Skills_Thematic_Split/*.md (8 theme docs)
      Final_Research_Skills_Link_Downloads_By_Theme_LATEST/ (SKILL.md 文件)
      API: https://yunwu.ai/v1 (gpt-5.2)
[OUT] 修改后的 theme docs (原地更新)
      fix_checkpoint.json (断点续传)
      fix_report.json (修正报告)
[POS] 根据审核结果调用 API 修正不精确的 Function Explanation 和 Why Research-Related。
      A 类 (func partial/inaccurate + relevance valid): 只修正 Function Explanation
      B 类 (func accurate + relevance weak): 只修正 Why Research-Related
      C 类 (两者都有问题): 修正两列
      Supports concurrent batch processing via --concurrency flag (default 5).
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
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
BATCH_SIZE = 10
CHECKPOINT_EVERY = 5
MAX_RETRIES = 3
RETRY_BASE_SLEEP = 3.0
SKILLMD_TRUNCATE = 8000

BASE_DIR = Path(__file__).resolve().parent
THEME_DIR = BASE_DIR / "Final_Research_Skills_Thematic_Split"
DOWNLOAD_DIR = BASE_DIR / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
AUDIT_RESULTS_PATH = BASE_DIR / "audit_results.json"
CHECKPOINT_PATH = BASE_DIR / "fix_checkpoint.json"
REPORT_PATH = BASE_DIR / "fix_report.json"

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
    "You are a research skill description editor. Apply MINIMAL, SURGICAL edits to fix specific audit issues.\n\n"
    "## Core Principle: Minimal Edit\n"
    "Do NOT rewrite the entire description. Only change the specific words/phrases/sentences that the audit flagged. "
    "Keep all correct parts of the original text UNCHANGED. The less you change, the better.\n\n"
    "## Fix Strategies by fix_strategy field\n"
    "Each skill has a fix_strategy that tells you exactly what to do:\n\n"
    "- **REMOVE_HALLUCINATION**: The description contains claims not in SKILL.md. "
    "DELETE the unsupported sentences/phrases. Do NOT add new content. Do NOT rephrase remaining text. "
    "If removal leaves a short description (even 1-2 sentences), that is fine — accuracy > length.\n\n"
    "- **ADD_MISSING**: The description omits a major capability that IS in SKILL.md. "
    "APPEND 1 sentence describing the missing capability. Do NOT modify existing correct sentences.\n\n"
    "- **REMOVE_AND_ADD**: Both issues. First remove unsupported claims, then append missing capability.\n\n"
    "- **GENERAL_FIX**: Reason unclear. Make minimal corrections based on audit feedback.\n\n"
    "## Constraints\n"
    "- Every claim MUST be traceable to the provided SKILL.md text.\n"
    "- If SKILL.md is vague, keep your output equally vague. Never fill gaps with guesses.\n"
    "- No marketing language. No pipe characters (|).\n"
    "- Output ONLY a valid JSON array. No markdown fences, no extra text."
)


# -- Data Loading (reused from audit_all_skills.py) --

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


def load_skillmd_content(repo, evidence_file, repo_map):
    """Load full SKILL.md content for a skill."""
    repo_dirs = repo_map.get(repo, [])
    for rd in repo_dirs:
        skill_path = os.path.join(rd, evidence_file)
        if os.path.exists(skill_path):
            try:
                return open(skill_path, encoding='utf-8').read()
            except Exception:
                pass
    return None


def compute_row_id(theme, repo, skill_col, evidence_col):
    """Same row_id computation as audit_all_skills.py."""
    return hashlib.sha1(
        f"{theme}:{repo}:{skill_col}:{evidence_col}".encode()
    ).hexdigest()[:12]


# -- Load & Classify Audit Results --

def load_audit_results():
    data = json.load(open(AUDIT_RESULTS_PATH, encoding='utf-8'))
    return data.get("results", [])


def classify_skills(results):
    """Classify skills into fix categories A/B/C."""
    categories = {"A": [], "B": [], "C": []}
    for r in results:
        fa = r.get("function_accuracy", "")
        rr = r.get("research_relevance", "")
        func_bad = fa in ("partial", "inaccurate")
        rel_bad = rr in ("weak", "invalid")

        if func_bad and rel_bad:
            r["fix_category"] = "C"
            categories["C"].append(r)
        elif func_bad and rr == "valid":
            r["fix_category"] = "A"
            categories["A"].append(r)
        elif not func_bad and rel_bad:
            r["fix_category"] = "B"
            categories["B"].append(r)
    return categories


# -- Prompt Building --

HALLUC_KEYWORDS = [
    'not supported', 'not stated', 'not present', 'not confirmed',
    'not mentioned in skill', 'adds ', 'added ', 'introduces',
    'unsupported', 'not in skill', 'fabricat', 'not found in',
]
MISSING_KEYWORDS = [
    'miss', 'omit', 'lacks', 'does not mention', 'not captured',
    'absent', 'fails to mention', 'no mention of', 'does not cover',
    'not address',
]


def detect_fix_strategy(item):
    """Detect whether the audit issue is hallucination, missing, or both."""
    reason = item.get("function_accuracy_reason", "").lower()
    has_halluc = any(k in reason for k in HALLUC_KEYWORDS)
    has_miss = any(k in reason for k in MISSING_KEYWORDS)
    if has_halluc and has_miss:
        return "REMOVE_AND_ADD"
    elif has_halluc:
        return "REMOVE_HALLUCINATION"
    elif has_miss:
        return "ADD_MISSING"
    else:
        return "GENERAL_FIX"


def build_fix_prompt(batch, skillmd_map):
    parts = []
    for i, item in enumerate(batch, 1):
        cat = item["fix_category"]
        row_id = item["row_id"]
        skill_name = item["skill_name"]
        repo = item["repo"]

        lines = [f"### Skill {i}: `{skill_name}` ({repo})"]
        lines.append(f"- Fix type: {cat}")

        if cat in ("A", "C"):
            strategy = detect_fix_strategy(item)
            lines.append(f"- fix_strategy: {strategy}")
            lines.append(f"- Current Function Explanation: {item.get('current_func', '')}")
        if cat in ("B", "C"):
            lines.append(f"- Current Why Research-Related: {item.get('current_why', '')}")

        lines.append(f"- Audit function_accuracy: {item.get('function_accuracy', '')}")
        lines.append(f"- Audit function_accuracy_reason: {item.get('function_accuracy_reason', '')}")
        lines.append(f"- Audit research_relevance: {item.get('research_relevance', '')}")
        lines.append(f"- Audit research_relevance_reason: {item.get('research_relevance_reason', '')}")
        issues = item.get("issues", [])
        if issues:
            lines.append(f"- Issues: {'; '.join(issues)}")

        skillmd = skillmd_map.get(row_id, "")
        if skillmd:
            lines.append(f"- SKILL.md content:\n{skillmd[:SKILLMD_TRUNCATE]}")
        else:
            lines.append("- SKILL.md: Not available")

        parts.append('\n'.join(lines))

    skills_text = '\n\n'.join(parts)
    n = len(batch)

    fix_instructions = (
        "For each skill, apply MINIMAL edits based on fix_strategy and audit feedback.\n\n"
        "Fix type rules:\n"
        "- Type A: Only produce corrected function_explanation\n"
        "- Type B: Only produce corrected why_research_related\n"
        "- Type C: Produce both corrected function_explanation and why_research_related\n\n"
        "CRITICAL: Follow the fix_strategy exactly:\n"
        "- REMOVE_HALLUCINATION → Delete unsupported claims, keep everything else verbatim\n"
        "- ADD_MISSING → Keep current text, append 1 sentence for the missing capability\n"
        "- REMOVE_AND_ADD → Delete unsupported claims, then append missing capability\n"
        "- GENERAL_FIX → Minimal correction based on audit reason\n\n"
    )

    response_schema = (
        '[{"index":1,"function_explanation":"corrected text or empty if not fixing",'
        '"why_research_related":"corrected text or empty if not fixing"}]'
    )

    return (
        f"Correct these {n} research skill descriptions:\n\n"
        f"{skills_text}\n\n"
        f"{fix_instructions}"
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
                max_tokens=8192,
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
    m = re.search(r'\[.*\]', text, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group())
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return None


# -- Checkpoint --

def save_checkpoint(fixes, errors, batch_idx, total_batches):
    checkpoint = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "batches_completed": batch_idx + 1,
        "batches_total": total_batches,
        "fixes_completed": len(fixes),
        "errors_count": len(errors),
        "completed_row_ids": list(set(f["row_id"] for f in fixes)),
        "fixes": fixes,
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
        print(f"  Loaded checkpoint: {len(completed)} fixes done")
        return completed, data.get("fixes", []), data.get("errors", [])
    except Exception:
        return set(), [], []


# -- Theme Doc Rewriting --

def apply_fixes_to_theme_docs(fixes_map, dry_run=False):
    """Apply fixes to theme markdown files. fixes_map: {row_id: {func_exp, why_research}}"""
    applied = 0
    for tf in THEME_FILES:
        path = THEME_DIR / tf
        if not path.exists():
            continue
        content = open(path, encoding='utf-8').read()
        lines = content.split('\n')
        theme = path.stem
        current_repo = ""
        new_lines = []
        file_applied = 0

        for line in lines:
            stripped = line.rstrip('\r')
            if stripped.startswith('### '):
                current_repo = stripped[4:].strip()
                new_lines.append(line)
                continue

            if not stripped.startswith('|') or stripped.startswith('| Skill |') or stripped.startswith('|---|'):
                new_lines.append(line)
                continue
            if '[link](' not in stripped:
                new_lines.append(line)
                continue

            parts = stripped.split('|')
            raw_parts = list(parts)
            if parts and not parts[0].strip():
                parts = parts[1:]
            if parts and not parts[-1].strip():
                parts = parts[:-1]
            if len(parts) < 7:
                new_lines.append(line)
                continue

            row_id = compute_row_id(theme, current_repo, parts[0].strip(), parts[1].strip())

            if row_id not in fixes_map:
                new_lines.append(line)
                continue

            fix = fixes_map[row_id]
            new_func = fix.get("function_explanation", "").strip()
            new_why = fix.get("why_research_related", "").strip()

            # Rebuild the line using raw_parts to preserve leading/trailing empty segments
            # raw_parts[0] is empty (before first |), raw_parts[-1] is empty (after last |)
            # Content columns are raw_parts[1..7] corresponding to parts[0..6]
            # parts[3] = Why Research-Related (raw_parts[4])
            # parts[4] = Function Explanation (raw_parts[5])
            offset = 1 if raw_parts[0].strip() == '' else 0

            if new_why:
                raw_parts[offset + 3] = f" {new_why} "
            if new_func:
                raw_parts[offset + 4] = f" {new_func} "

            new_line = '|'.join(raw_parts)
            new_lines.append(new_line)
            file_applied += 1

        if file_applied > 0 and not dry_run:
            with open(path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
        applied += file_applied
        if file_applied > 0:
            print(f"  {tf}: {file_applied} fixes" + (" (dry-run)" if dry_run else ""))

    return applied


# -- Main --

def main():
    parser = argparse.ArgumentParser(description="Fix skill descriptions based on audit results")
    parser.add_argument('--debug', action='store_true', help='Debug mode: verbose output')
    parser.add_argument('--count', type=int, default=0, help='Only fix first N skills')
    parser.add_argument('--skill-name', type=str, default='', help='Only fix skills matching this name')
    parser.add_argument('--dry-run', action='store_true', help='Generate fixes but do not write to theme docs')
    parser.add_argument('--category', type=str, default='', help='Only fix category A, B, or C')
    parser.add_argument('--concurrency', type=int, default=5, help='Number of concurrent batch workers (default: 5)')
    args = parser.parse_args()

    debug = args.debug
    if debug or args.dry_run:
        sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 60)
    mode_label = " [DEBUG]" if debug else (" [DRY-RUN]" if args.dry_run else "")
    print(f"Fix Descriptions Based on Audit{mode_label}")
    print("=" * 60)

    # 1. Load audit results
    print("\n[1/6] Loading audit results...")
    audit_results = load_audit_results()
    print(f"  Total audit results: {len(audit_results)}")

    # 2. Classify
    print("\n[2/6] Classifying skills...")
    categories = classify_skills(audit_results)
    print(f"  A (func fix only):      {len(categories['A'])}")
    print(f"  B (relevance fix only): {len(categories['B'])}")
    print(f"  C (both fix):           {len(categories['C'])}")

    # Build fix list
    to_fix = []
    if args.category:
        cats = [c.upper() for c in args.category.split(',')]
        for c in cats:
            to_fix.extend(categories.get(c, []))
    else:
        to_fix = categories["A"] + categories["B"] + categories["C"]
    print(f"  Total to fix: {len(to_fix)}")

    if args.skill_name:
        to_fix = [s for s in to_fix if args.skill_name.lower() in s["skill_name"].lower()]
        print(f"  Filtered by name '{args.skill_name}': {len(to_fix)}")
    if args.count > 0:
        to_fix = to_fix[:args.count]
        print(f"  Limited to first {args.count}: {len(to_fix)}")

    if not to_fix:
        print("  Nothing to fix!")
        return

    # 3. Load current theme doc values + SKILL.md content
    print("\n[3/6] Loading SKILL.md content and current values...")
    repo_map = build_repo_dir_map()

    # Load current values from theme docs
    current_values = {}
    for tf in THEME_FILES:
        path = THEME_DIR / tf
        if not path.exists():
            continue
        content = open(path, encoding='utf-8').read()
        theme = path.stem
        current_repo = ""
        for line in content.split('\n'):
            line = line.rstrip('\r')
            if line.startswith('### '):
                current_repo = line[4:].strip()
                continue
            if not line.startswith('|') or '| Skill |' in line or '|---|' in line:
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
            row_id = compute_row_id(theme, current_repo, parts[0].strip(), parts[1].strip())
            current_values[row_id] = {
                "why_research_related": parts[3].strip(),
                "function_explanation": parts[4].strip(),
                "evidence_file": parts[1].strip().strip('`'),
                "repo": current_repo,
            }

    # Enrich to_fix with current values and SKILL.md
    skillmd_map = {}
    for item in to_fix:
        rid = item["row_id"]
        cv = current_values.get(rid, {})
        item["current_func"] = cv.get("function_explanation", item.get("function_explanation", ""))
        item["current_why"] = cv.get("why_research_related", item.get("why_research_related", ""))
        evidence_file = cv.get("evidence_file", "")
        repo = item.get("repo", cv.get("repo", ""))
        if evidence_file and repo:
            md_content = load_skillmd_content(repo, evidence_file, repo_map)
            if md_content:
                skillmd_map[rid] = md_content

    print(f"  SKILL.md loaded: {len(skillmd_map)}/{len(to_fix)}")

    if debug:
        print("\n  --- Skills to fix ---")
        for i, item in enumerate(to_fix, 1):
            print(f"\n  [{i}] {item['skill_name']} ({item['repo']}) [Cat {item['fix_category']}]")
            print(f"      func_accuracy:  {item.get('function_accuracy','')}")
            print(f"      func_reason:    {item.get('function_accuracy_reason','')[:150]}")
            print(f"      relevance:      {item.get('research_relevance','')}")
            print(f"      rel_reason:     {item.get('research_relevance_reason','')[:150]}")
            print(f"      has SKILL.md:   {item['row_id'] in skillmd_map}")

    # 4. Checkpoint
    if not debug:
        print("\n[4/6] Checkpoint...")
        completed_ids, fixes, errors = load_checkpoint()
        remaining = [s for s in to_fix if s["row_id"] not in completed_ids]
        print(f"  Remaining: {len(remaining)}")
    else:
        print("\n[4/6] Checkpoint... SKIPPED (debug)")
        completed_ids = set()
        fixes = []
        errors = []
        remaining = to_fix

    # 5. Process batches
    total_batches = 0
    if remaining:
        batch_list = [remaining[i:i+BATCH_SIZE] for i in range(0, len(remaining), BATCH_SIZE)]
        total_batches = len(batch_list)
        concurrency = args.concurrency
        print(f"  Batches: {total_batches}  (concurrency: {concurrency})")

        client = OpenAI(api_key=API_KEY, base_url=API_BASE)

        # Thread-safe state
        lock = threading.Lock()
        batches_done = [0]

        def process_batch(bi, batch):
            """Process a single fix batch. Returns (batch_fixes, batch_errors)."""
            batch_fixes = []
            batch_errors = []
            try:
                prompt = build_fix_prompt(batch, skillmd_map)

                if debug:
                    with lock:
                        print(f"\n  --- PROMPT (batch {bi+1}) ---")
                        print(f"  System: {SYSTEM_PROMPT[:200]}...")
                        print(f"\n  User ({len(prompt)} chars):")
                        print("  " + prompt[:3000].replace("\n", "\n  "))
                        if len(prompt) > 3000:
                            print(f"  ... ({len(prompt) - 3000} more chars)")
                        print("  --- END PROMPT ---\n")

                resp_text = call_api(client, prompt)

                if debug:
                    with lock:
                        print(f"  --- RAW RESPONSE (batch {bi+1}) ---")
                        print("  " + (resp_text or "(empty)").replace("\n", "\n  "))
                        print("  --- END RESPONSE ---\n")

                parsed = parse_response(resp_text, len(batch))

                if parsed:
                    for i, item in enumerate(batch):
                        r = parsed[i] if i < len(parsed) else {}
                        fix_entry = {
                            "row_id": item["row_id"],
                            "skill_name": item["skill_name"],
                            "repo": item["repo"],
                            "theme": item["theme"],
                            "fix_category": item["fix_category"],
                        }

                        cat = item["fix_category"]
                        if cat in ("A", "C"):
                            new_func = r.get("function_explanation", "").strip()
                            new_func = new_func.replace("|", "/")
                            fix_entry["old_function_explanation"] = item.get("current_func", "")[:200]
                            fix_entry["new_function_explanation"] = new_func
                        if cat in ("B", "C"):
                            new_why = r.get("why_research_related", "").strip()
                            new_why = new_why.replace("|", "/")
                            fix_entry["old_why_research_related"] = item.get("current_why", "")[:200]
                            fix_entry["new_why_research_related"] = new_why

                        batch_fixes.append(fix_entry)

                        if debug:
                            with lock:
                                print(f"  --- FIX [{i+1}] {item['skill_name']} (Cat {cat}, batch {bi+1}) ---")
                                if cat in ("A", "C"):
                                    print(f"    OLD func: {fix_entry.get('old_function_explanation','')[:120]}...")
                                    print(f"    NEW func: {fix_entry.get('new_function_explanation','')[:120]}...")
                                if cat in ("B", "C"):
                                    print(f"    OLD why:  {fix_entry.get('old_why_research_related','')[:120]}...")
                                    print(f"    NEW why:  {fix_entry.get('new_why_research_related','')[:120]}...")

                    with lock:
                        batches_done[0] += 1
                        print(f"  Batch {bi+1}/{total_batches} OK ({len(parsed)} fixes)  [{batches_done[0]}/{total_batches} done]")
                else:
                    for s in batch:
                        batch_errors.append({
                            "row_id": s["row_id"],
                            "skill_name": s["skill_name"],
                            "error": "parse_failed",
                        })
                    with lock:
                        batches_done[0] += 1
                        print(f"  Batch {bi+1}/{total_batches} FAILED (parse)  [{batches_done[0]}/{total_batches} done]")
            except Exception as e:
                for s in batch:
                    batch_errors.append({
                        "row_id": s["row_id"],
                        "skill_name": s["skill_name"],
                        "error": str(e)[:200],
                    })
                with lock:
                    batches_done[0] += 1
                    print(f"  Batch {bi+1}/{total_batches} ERROR: {e}  [{batches_done[0]}/{total_batches} done]")

            return batch_fixes, batch_errors

        print(f"\n[5/6] Calling API for corrections ({concurrency} concurrent workers)...")

        if concurrency <= 1:
            # Sequential fallback
            for bi, batch in enumerate(batch_list):
                print(f"\n  Batch {bi+1}/{total_batches} ({len(batch)} skills)...")
                bf, be = process_batch(bi, batch)
                fixes.extend(bf)
                errors.extend(be)
                for f in bf:
                    completed_ids.add(f["row_id"])
                if not debug and (bi + 1) % CHECKPOINT_EVERY == 0:
                    save_checkpoint(fixes, errors, bi, total_batches)
                    print(f"  [Checkpoint: {len(fixes)} done]")
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
                        bf, be = future.result()
                    except Exception as e:
                        print(f"  Batch {bi+1} unexpected executor error: {e}")
                        bf, be = [], []
                    with lock:
                        fixes.extend(bf)
                        errors.extend(be)
                        for f in bf:
                            completed_ids.add(f["row_id"])
                        checkpoint_counter[0] += 1
                        if not debug and checkpoint_counter[0] % CHECKPOINT_EVERY == 0:
                            save_checkpoint(fixes, errors, bi, total_batches)
                            print(f"  [Checkpoint: {len(fixes)} done]")

        if not debug:
            save_checkpoint(fixes, errors, total_batches - 1, total_batches)
    else:
        print("\n[5/6] All skills already fixed!")

    # 6. Apply fixes to theme docs
    print(f"\n[6/6] Applying {len(fixes)} fixes to theme docs...")
    fixes_map = {}
    for f in fixes:
        entry = {}
        if f.get("new_function_explanation"):
            entry["function_explanation"] = f["new_function_explanation"]
        if f.get("new_why_research_related"):
            entry["why_research_related"] = f["new_why_research_related"]
        if entry:
            fixes_map[f["row_id"]] = entry

    applied = apply_fixes_to_theme_docs(fixes_map, dry_run=args.dry_run or debug)

    # Write report
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_fixes": len(fixes),
        "applied_to_docs": applied,
        "errors": len(errors),
        "dry_run": args.dry_run or debug,
        "category_counts": {
            "A": sum(1 for f in fixes if f.get("fix_category") == "A"),
            "B": sum(1 for f in fixes if f.get("fix_category") == "B"),
            "C": sum(1 for f in fixes if f.get("fix_category") == "C"),
        },
        "fixes": fixes,
        "errors_list": errors,
    }
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  Report: {REPORT_PATH}")

    print(f"\nDone! {len(fixes)} fixes generated, {applied} applied, {len(errors)} errors.")


if __name__ == '__main__':
    main()

"""
fix_invalid_skills.py
[IN]  audit_results.json (审核结果)
      x_class_row_ids.json (X 类 skill 列表)
      Final_Research_Skills_Thematic_Split/*.md (8 theme docs)
      Final_Research_Skills_Link_Downloads_By_Theme_LATEST/ (SKILL.md 文件)
      API: https://yunwu.ai/v1 (gpt-5.2)
[OUT] 修改后的 theme docs (原地更新)
      fix_invalid_checkpoint.json (断点续传)
      fix_invalid_report.json (修正报告)
[POS] 修正被错误标记为 invalid 的研究技能。
      这些 skill 实际与科研高度相关（生物信息学、科学数据库、AI/ML 研究工具等），
      但 theme doc 中的 Why Research-Related 字段写错了（标 NOT_RESEARCH 或理由不匹配）。
      基于 SKILL.md 内容重新生成正确的 Why Research-Related，
      同时修正 function_accuracy 为 partial 的 Function Explanation。
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
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
MAX_RETRIES = 3
RETRY_BASE_SLEEP = 3.0
SKILLMD_TRUNCATE = 2000

BASE_DIR = Path(__file__).resolve().parent
THEME_DIR = BASE_DIR / "Final_Research_Skills_Thematic_Split"
DOWNLOAD_DIR = BASE_DIR / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
AUDIT_RESULTS_PATH = BASE_DIR / "audit_results.json"
X_CLASS_PATH = BASE_DIR / "x_class_row_ids.json"
CHECKPOINT_PATH = BASE_DIR / "fix_invalid_checkpoint.json"
REPORT_PATH = BASE_DIR / "fix_invalid_report.json"

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
    "You are a research skill description editor specializing in scientific tools. "
    "These skills were incorrectly marked as NOT research-relevant. "
    "Your job is to write CORRECT Why Research-Related rationale and, if needed, fix the Function Explanation.\n\n"
    "Rules:\n"
    "- Base corrections ONLY on the provided SKILL.md content. Do not fabricate details.\n"
    "- Why Research-Related: 1-2 sentences explaining the SPECIFIC research value. "
    "Be concrete: name the research domain (bioinformatics, cheminformatics, ML research, etc.) "
    "and the specific research activity (data retrieval, analysis, model training, visualization, etc.). "
    "Do NOT use generic phrases like 'supports research workflows'. Be specific.\n"
    "- Function Explanation (only if fix_func is true): 2-3 concise sentences capturing core purpose, "
    "key capabilities, and important limitations. Must faithfully represent the SKILL.md.\n"
    "- Keep text concise. No marketing language. No pipe characters (|).\n"
    "- Output ONLY a valid JSON array. No markdown fences, no extra text."
)


# -- Data Loading (reused from fix_descriptions.py) --

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
    return hashlib.sha1(
        f"{theme}:{repo}:{skill_col}:{evidence_col}".encode()
    ).hexdigest()[:12]


# -- Load X-class skills --

def load_x_class_skills():
    x_data = json.load(open(X_CLASS_PATH, encoding='utf-8'))
    x_row_ids = set(x_data['row_ids'])

    audit_data = json.load(open(AUDIT_RESULTS_PATH, encoding='utf-8'))
    audit_results = audit_data.get("results", [])

    # Build lookup from audit results
    audit_map = {r['row_id']: r for r in audit_results}

    skills = []
    for rid in x_row_ids:
        r = audit_map.get(rid)
        if r:
            r['fix_func'] = r.get('function_accuracy') in ('partial', 'inaccurate')
            skills.append(r)
    return skills


# -- Prompt Building --

def build_fix_prompt(batch, skillmd_map):
    parts = []
    for i, item in enumerate(batch, 1):
        row_id = item["row_id"]
        skill_name = item["skill_name"]
        repo = item["repo"]
        fix_func = item.get("fix_func", False)

        lines = [f"### Skill {i}: `{skill_name}` ({repo})"]
        lines.append(f"- fix_func: {fix_func}")
        lines.append(f"- Current research_relevance_reason: {item.get('research_relevance_reason', '')[:300]}")

        if fix_func:
            lines.append(f"- Current function_accuracy: {item.get('function_accuracy', '')}")
            lines.append(f"- function_accuracy_reason: {item.get('function_accuracy_reason', '')[:300]}")

        issues = item.get("issues", [])
        if issues:
            lines.append(f"- Issues: {'; '.join(issues)[:300]}")

        skillmd = skillmd_map.get(row_id, "")
        if skillmd:
            lines.append(f"- SKILL.md content:\n{skillmd[:SKILLMD_TRUNCATE]}")
        else:
            lines.append("- SKILL.md: Not available")

        parts.append('\n'.join(lines))

    skills_text = '\n\n'.join(parts)
    n = len(batch)

    response_schema = (
        '[{"index":1,"why_research_related":"corrected research rationale",'
        '"function_explanation":"corrected text or empty string if fix_func is false"}]'
    )

    return (
        f"Fix these {n} research skill descriptions. "
        f"Each was incorrectly marked as NOT research-relevant. "
        f"Write a correct Why Research-Related for ALL skills. "
        f"Only fix Function Explanation if fix_func is true.\n\n"
        f"{skills_text}\n\n"
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
                temperature=0.2,
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

def save_checkpoint(fixes, errors):
    checkpoint = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
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
    parser = argparse.ArgumentParser(description="Fix wrongly-invalid research skills")
    parser.add_argument('--debug', action='store_true', help='Debug mode: verbose output')
    parser.add_argument('--dry-run', action='store_true', help='Generate fixes but do not write to theme docs')
    parser.add_argument('--count', type=int, default=0, help='Only fix first N skills')
    args = parser.parse_args()

    debug = args.debug
    if debug or args.dry_run:
        sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 60)
    mode_label = " [DEBUG]" if debug else (" [DRY-RUN]" if args.dry_run else "")
    print(f"Fix Wrongly-Invalid Research Skills{mode_label}")
    print("=" * 60)

    # 1. Load X-class skills
    print("\n[1/5] Loading X-class skills...")
    to_fix = load_x_class_skills()
    print(f"  Total X-class: {len(to_fix)}")
    func_fix_count = sum(1 for s in to_fix if s.get('fix_func'))
    print(f"  Need func fix: {func_fix_count}")

    if args.count > 0:
        to_fix = to_fix[:args.count]
        print(f"  Limited to first {args.count}")

    if not to_fix:
        print("  Nothing to fix!")
        return

    # 2. Load SKILL.md content + current theme doc values
    print("\n[2/5] Loading SKILL.md content...")
    repo_map = build_repo_dir_map()

    # Get current values from theme docs
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
                "evidence_file": parts[1].strip().strip('`'),
                "repo": current_repo,
            }

    # Load SKILL.md for each skill
    skillmd_map = {}
    for item in to_fix:
        rid = item["row_id"]
        cv = current_values.get(rid, {})
        evidence_file = cv.get("evidence_file", "")
        repo = item.get("repo", cv.get("repo", ""))
        if evidence_file and repo:
            md_content = load_skillmd_content(repo, evidence_file, repo_map)
            if md_content:
                skillmd_map[rid] = md_content

    print(f"  SKILL.md loaded: {len(skillmd_map)}/{len(to_fix)}")

    if debug:
        for i, item in enumerate(to_fix, 1):
            has_md = item['row_id'] in skillmd_map
            print(f"  [{i}] {item['skill_name']:50s} | {item['repo']:40s} | md={has_md} | fix_func={item.get('fix_func')}")

    # 3. Checkpoint
    if not debug:
        print("\n[3/5] Checkpoint...")
        completed_ids, fixes, errors = load_checkpoint()
        remaining = [s for s in to_fix if s["row_id"] not in completed_ids]
        print(f"  Remaining: {len(remaining)}")
    else:
        print("\n[3/5] Checkpoint... SKIPPED (debug)")
        completed_ids = set()
        fixes = []
        errors = []
        remaining = to_fix

    # 4. Process batches
    if remaining:
        batch_list = [remaining[i:i+BATCH_SIZE] for i in range(0, len(remaining), BATCH_SIZE)]
        total_batches = len(batch_list)
        print(f"  Batches: {total_batches}")

        client = OpenAI(api_key=API_KEY, base_url=API_BASE)

        print("\n[4/5] Calling API for corrections...")
        for bi, batch in enumerate(batch_list):
            print(f"\n  Batch {bi+1}/{total_batches} ({len(batch)} skills)...")

            try:
                prompt = build_fix_prompt(batch, skillmd_map)

                if debug:
                    print(f"\n  --- PROMPT ({len(prompt)} chars) ---")
                    print("  " + prompt[:2000].replace("\n", "\n  "))
                    if len(prompt) > 2000:
                        print(f"  ... ({len(prompt) - 2000} more chars)")
                    print("  --- END PROMPT ---\n")

                resp_text = call_api(client, prompt)

                if debug:
                    print("  --- RAW RESPONSE ---")
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
                            "fix_func": item.get("fix_func", False),
                        }

                        new_why = r.get("why_research_related", "").strip()
                        new_why = new_why.replace("|", "/")
                        fix_entry["new_why_research_related"] = new_why

                        if item.get("fix_func"):
                            new_func = r.get("function_explanation", "").strip()
                            new_func = new_func.replace("|", "/")
                            fix_entry["new_function_explanation"] = new_func

                        fixes.append(fix_entry)
                        completed_ids.add(item["row_id"])

                        if debug:
                            print(f"  [{i+1}] {item['skill_name']}")
                            print(f"      NEW why: {new_why[:120]}...")
                            if item.get("fix_func"):
                                print(f"      NEW func: {fix_entry.get('new_function_explanation','')[:120]}...")

                    print(f"  OK ({len(parsed)} fixes)")
                else:
                    print("  FAILED (parse)")
                    for s in batch:
                        errors.append({
                            "row_id": s["row_id"],
                            "skill_name": s["skill_name"],
                            "error": "parse_failed",
                        })
            except Exception as e:
                print(f"  ERROR: {e}")
                for s in batch:
                    errors.append({
                        "row_id": s["row_id"],
                        "skill_name": s["skill_name"],
                        "error": str(e)[:200],
                    })

            if not debug:
                save_checkpoint(fixes, errors)

            time.sleep(1.0)

        if not debug:
            save_checkpoint(fixes, errors)
    else:
        print("\n[4/5] All skills already fixed!")

    # 5. Apply fixes
    print(f"\n[5/5] Applying {len(fixes)} fixes to theme docs...")
    fixes_map = {}
    for f in fixes:
        entry = {}
        if f.get("new_why_research_related"):
            entry["why_research_related"] = f["new_why_research_related"]
        if f.get("new_function_explanation"):
            entry["function_explanation"] = f["new_function_explanation"]
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
        "fixes": fixes,
        "errors_list": errors,
    }
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  Report: {REPORT_PATH}")

    print(f"\nDone! {len(fixes)} fixes generated, {applied} applied, {len(errors)} errors.")


if __name__ == '__main__':
    main()

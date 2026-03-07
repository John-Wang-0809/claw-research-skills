#!/usr/bin/env python3
"""
Targeted re-audit of the 141 fixed skills.
Reuses audit_all_skills.py logic but only audits skills from fix_manifest.json.
"""
import json
import hashlib
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -- Config (same as audit_all_skills.py) --
API_KEY = os.getenv("API_KEY", "")
API_BASE = os.getenv("BASE_URL", "https://yunwu.ai") + "/v1"
MODEL = "gpt-5.2"
BATCH_SIZE = 15
SKILLMD_TRUNCATE = 8000
MAX_RETRIES = 3
RETRY_BASE_SLEEP = 3.0

BASE_DIR = Path(__file__).resolve().parent
THEME_DIR = BASE_DIR / "Final_Research_Skills_Thematic_Split"
DOWNLOAD_DIR = BASE_DIR / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
MANIFEST_PATH = BASE_DIR / "plans" / "fix_manifest.json"

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
    "PARTIAL: Summary mentions only \"fingerprint-based similarity\" but SKILL.md describes "
    "BOTH similarity search AND Butina clustering as co-equal major features.\n"
    "PARTIAL: Summary adds \"auto-load at session start\" not stated anywhere in SKILL.md."
)


def split_row_by_unescaped_pipes(row_line):
    cols = []
    buf = []
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


def parse_theme_for_target_skills(theme_file, target_skill_names):
    """Parse a theme markdown file and return only rows matching target skill names."""
    content = open(theme_file, encoding="utf-8").read()
    lines = content.split("\n")
    theme = Path(theme_file).stem
    skills = []
    current_repo = ""

    for line in lines:
        line = line.rstrip("\r")
        if line.startswith("### "):
            current_repo = line[4:].strip()
            continue
        if not line.startswith("|") or line.startswith("| Skill |") or line.startswith("|---"):
            continue
        if "[link](" not in line:
            continue

        parts = split_row_by_unescaped_pipes(line)
        if parts and not parts[0].strip():
            parts = parts[1:]
        if parts and not parts[-1].strip():
            parts = parts[:-1]
        if len(parts) < 7:
            continue
        if len(parts) > 7:
            parts = parts[:6] + ["|".join(parts[6:])]

        skill_name = parts[0].strip().strip("`")
        if skill_name not in target_skill_names:
            continue

        url_m = re.search(r"\[link\]\((https?://[^)\s]+)\)", parts[2])

        skills.append({
            "theme": theme,
            "repo": current_repo,
            "skill_name": skill_name,
            "evidence_file": parts[1].strip().strip("`"),
            "skill_url": url_m.group(1) if url_m else "",
            "why_research_related": parts[3].strip(),
            "function_explanation": parts[4].strip(),
            "execution_flow": parts[5].strip(),
            "evidence": parts[6].strip(),
        })

    return skills


def resolve_local_description(skill, repo_map):
    repo_dirs = repo_map.get(skill["repo"], [])
    for rd in repo_dirs:
        skill_path = os.path.join(rd, skill["evidence_file"])
        if os.path.exists(skill_path):
            try:
                return open(skill_path, encoding="utf-8").read()
            except Exception:
                pass
    return None


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
            if "__" in repo_dir:
                owner, repo = repo_dir.split("__", 1)
                key = f"{owner}/{repo}"
                if key not in repo_map:
                    repo_map[key] = []
                repo_map[key].append(str(repo_path))
    return repo_map


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
        parts.append("\n".join(lines))

    skills_text = "\n\n".join(parts)
    n = len(batch)

    return (
        f"Evaluate these {n} research skills:\n\n"
        f"{skills_text}\n\n"
        "For each skill, assess:\n\n"
        "1. function_accuracy: Compare Function Explanation against SKILL.md.\n"
        '   - "accurate": correctly captures main purpose and key capabilities\n'
        '   - "partial": misses a MAJOR capability or introduces unsupported claims\n'
        '   - "inaccurate": fundamentally misrepresents the skill\n'
        '   - "cannot_verify": no SKILL.md available\n\n'
        "2. overall_quality: 1-5 scale\n\n"
        "Return a JSON array with one object per skill:\n"
        '[{"index":1,"skill_name":"...","function_accuracy":"accurate|partial|inaccurate|cannot_verify",'
        '"function_accuracy_reason":"brief reason","overall_quality":4,"issues":[]}]'
    )


def call_api(batch, client):
    prompt = build_user_prompt(batch)
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=4000,
            )
            text = resp.choices[0].message.content.strip()
            # Strip markdown fences
            if text.startswith("```"):
                text = re.sub(r"^```\w*\n?", "", text)
                text = re.sub(r"\n?```$", "", text)
            return json.loads(text)
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BASE_SLEEP * (attempt + 1))
            else:
                print(f"  API error after {MAX_RETRIES} retries: {e}")
                return None


def main():
    print("=" * 60)
    print("Targeted Re-Audit of 141 Fixed Skills")
    print("=" * 60)

    # Load manifest
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    target_skills_by_theme = manifest["by_theme"]

    # Build repo map
    print("\n1. Building repo directory map...")
    repo_map = build_repo_dir_map()
    print(f"   Found {len(repo_map)} repos")

    # Parse target skills from theme docs
    print("\n2. Parsing target skills from theme docs...")
    theme_files = [
        "01_information_retrieval_evidence_collection.md",
        "02_literature_review_writing_citation_part1.md",
        "02_literature_review_writing_citation_part2.md",
        "03_experiment_benchmark_reproducibility_validation_part1.md",
        "03_experiment_benchmark_reproducibility_validation_part2.md",
        "04_data_analysis_and_evidence_interpretation.md",
        "05_research_operations_and_workflow_support.md",
        "06_Additional_Scientific_Skills.md",
    ]

    all_skills = []
    for tf in theme_files:
        theme_name = Path(tf).stem
        target_names = {s["skill_name"] for s in target_skills_by_theme.get(theme_name, [])}
        if not target_names:
            continue
        path = THEME_DIR / tf
        if not path.exists():
            print(f"   WARNING: {tf} not found")
            continue
        skills = parse_theme_for_target_skills(path, target_names)
        print(f"   {tf}: {len(skills)}/{len(target_names)} skills found")
        all_skills.extend(skills)

    print(f"\n   Total skills to audit: {len(all_skills)}")

    # Resolve SKILL.md
    print("\n3. Resolving local SKILL.md files...")
    found = 0
    for s in all_skills:
        desc = resolve_local_description(s, repo_map)
        s["local_description"] = desc
        if desc:
            found += 1
    print(f"   Resolved: {found}/{len(all_skills)}")

    # Batch and call API
    print("\n4. Calling audit API...")
    client = OpenAI(api_key=API_KEY, base_url=API_BASE)
    batches = [all_skills[i:i + BATCH_SIZE] for i in range(0, len(all_skills), BATCH_SIZE)]
    results = []
    errors = []

    for bi, batch in enumerate(batches):
        print(f"   Batch {bi+1}/{len(batches)} ({len(batch)} skills)...")
        api_result = call_api(batch, client)
        if api_result and isinstance(api_result, list):
            for j, item in enumerate(api_result):
                if j < len(batch):
                    item["skill_name"] = batch[j]["skill_name"]
                    item["theme"] = batch[j]["theme"]
                    item["repo"] = batch[j]["repo"]
                    results.append(item)
        else:
            for s in batch:
                errors.append({"skill_name": s["skill_name"], "theme": s["theme"], "error": "API call failed"})
        time.sleep(1)  # rate limit

    # Summarize
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)

    counts = {"accurate": 0, "partial": 0, "inaccurate": 0, "cannot_verify": 0}
    for r in results:
        acc = r.get("function_accuracy", "unknown")
        counts[acc] = counts.get(acc, 0) + 1

    total_audited = len(results)
    print(f"Total audited: {total_audited}")
    print(f"  accurate:      {counts.get('accurate', 0)}")
    print(f"  partial:       {counts.get('partial', 0)}")
    print(f"  inaccurate:    {counts.get('inaccurate', 0)}")
    print(f"  cannot_verify: {counts.get('cannot_verify', 0)}")
    print(f"  API errors:    {len(errors)}")

    accurate = counts.get("accurate", 0)
    if total_audited > 0:
        pct = accurate / total_audited * 100
        print(f"\nAccuracy rate: {accurate}/{total_audited} = {pct:.1f}%")
        print(f"Target: >=85% ({int(total_audited * 0.85)}+ accurate)")

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_audited": total_audited,
        "counts": counts,
        "errors": len(errors),
        "results": results,
        "failed": errors,
    }
    out_path = BASE_DIR / "reaudit_results.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nResults saved to: {out_path}")

    # Save partial/inaccurate details
    remaining = [r for r in results if r.get("function_accuracy") in ("partial", "inaccurate")]
    if remaining:
        print(f"\n--- Still problematic ({len(remaining)}) ---")
        for r in remaining:
            print(f"  [{r.get('function_accuracy')}] {r['skill_name']} ({r.get('theme','')})")
            print(f"    Reason: {r.get('function_accuracy_reason', 'N/A')}")

    remaining_path = BASE_DIR / "reaudit_remaining.json"
    remaining_path.write_text(json.dumps(remaining, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nRemaining issues saved to: {remaining_path}")


if __name__ == "__main__":
    main()

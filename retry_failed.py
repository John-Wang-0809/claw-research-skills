#!/usr/bin/env python3
"""
[IN]  Dependencies/Inputs:
 - multidim_audit.json (1940 records, 51 with skipped=true + "LLM evaluation failed")
 - dedup_results.json (for fork_copy inheritance re-propagation)
 - audit_results.json (research_relevance, overall_quality for LLM prompt)
 - Final_Research_Skills_Link_Downloads_By_Theme_LATEST/**/SKILL.md (skill file contents)
 - API: https://yunwu.ai/v1/chat/completions (claude-haiku-4-5-20251001)
[OUT] Outputs:
 - multidim_audit.json (updated: LLM failures retried, inheritance re-propagated)
 - Backup: multidim_audit.json.bak.phase2a
[POS] Position in the system:
 - Phase 2a repair. Retries 51 LLM JSON parse failures from audit_multidim.py
   with enhanced 3-layer JSON extraction (strip fence → regex block → field-by-field).
   After fixing canonicals, re-propagates inheritance to their fork_copies and
   clears garbage flags on affected entries.

 Change warning: once you modify this file's logic, you must update this
 comment block, and check/update the module doc (README/CLAUDE) in the
 containing folder; update the root global map if necessary.
"""

import json
import os
import re
import shutil
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────
BASE = Path(__file__).parent
MULTIDIM_FILE = BASE / "multidim_audit.json"
DEDUP_FILE = BASE / "dedup_results.json"
AUDIT_FILE = BASE / "audit_results.json"
DOWNLOADS_DIR = BASE / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
BACKUP_SUFFIX = ".bak.phase2a"

# API config (same as audit_multidim.py)
API_URL = os.getenv("BASE_URL", "https://yunwu.ai") + "/v1/chat/completions"
API_KEY = os.getenv("API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"
MAX_RETRIES = 3

# Fields to copy during inheritance
INHERIT_FIELDS = [
    "research_tier", "research_tier_reason", "research_stages",
    "domain", "added_value", "added_value_reason", "doc_completeness",
]

REQUIRED_FIELDS = [
    "research_tier", "research_stages", "domain",
    "added_value", "doc_completeness",
]

# Theme directory mapping (same as audit_multidim.py)
THEME_DIR_MAP = {
    "01_information_retrieval_evidence_collection":
        "01_information_retrieval_evidence_collection",
    "02_literature_review_writing_citation_part1":
        "02_literature_review_writing_citation",
    "02_literature_review_writing_citation_part2":
        "02_literature_review_writing_citation",
    "03_experiment_benchmark_reproducibility_validation_part1":
        "03_experiment_benchmark_reproducibility_validation",
    "03_experiment_benchmark_reproducibility_validation_part2":
        "03_experiment_benchmark_reproducibility_validation",
    "04_data_analysis_and_evidence_interpretation":
        "04_data_analysis_and_evidence_interpretation",
    "05_research_operations_and_workflow_support":
        "05_research_operations_and_workflow_support",
    "06_Additional_Scientific_Skills":
        "06_Additional_Scientific_Skills",
}

SYSTEM_PROMPT = """You are a research skills auditor. You evaluate Claude Code Skills (SKILL.md files)
for their value to academic/scientific researchers.

For each skill, evaluate these dimensions and return ONLY valid JSON:

{
  "research_tier": "A|B|C|D",
  "research_tier_reason": "one sentence",
  "research_stages": ["stage1", "stage2"],
  "domain": "primary domain",
  "added_value": "high|medium|low|negligible",
  "added_value_reason": "one sentence",
  "doc_completeness": {
    "has_when_to_use": true|false,
    "has_prerequisites": true|false,
    "has_examples": true|false,
    "instruction_clarity": 1-5
  }
}

Tier definitions:
- A (Core Research Tool): Directly produces research outputs.
- B (Research Infrastructure): Enables reproducible/executable research.
- C (Research Productivity): General tools useful in research contexts.
- D (Tangentially Related): Weak or forced research connection.

Research stages: discovery, literature, experiment, analysis, writing, operations

Added value levels:
- high: Provides domain-specific pipeline/knowledge that LLM cannot reliably generate
- medium: Provides useful structured instructions that improve consistency
- low: Restates common knowledge with minimal structure
- negligible: Empty or near-empty skill with no substantive instructions"""


# ─────────────────────────────────────────────────────────
# File index (reused from audit_multidim.py)
# ─────────────────────────────────────────────────────────
_FILE_INDEX = None
_REPO_INDEX = None


def build_file_index():
    """Pre-scan all SKILL.md files and build lookup index."""
    global _FILE_INDEX, _REPO_INDEX
    _FILE_INDEX = {}
    _REPO_INDEX = defaultdict(list)

    if not DOWNLOADS_DIR.exists():
        print(f"WARNING: Downloads directory not found: {DOWNLOADS_DIR}")
        return

    for theme_dir in DOWNLOADS_DIR.iterdir():
        if not theme_dir.is_dir():
            continue
        for repo_dir in theme_dir.iterdir():
            if not repo_dir.is_dir():
                continue
            repo_slug = repo_dir.name
            for skill_file in repo_dir.rglob("SKILL.md"):
                skill_dir_name = skill_file.parent.name
                key = (repo_slug, skill_dir_name.lower())
                _FILE_INDEX[key] = skill_file
                _REPO_INDEX[repo_slug].append((skill_dir_name, skill_file))

    print(f"  File index: {len(_FILE_INDEX)} SKILL.md files indexed")


def find_skill_file(skill_name, repo):
    """Find SKILL.md file using pre-built index."""
    repo_slug = repo.replace("/", "__")
    skill_lower = skill_name.lower()

    # Exact match
    key = (repo_slug, skill_lower)
    if key in _FILE_INDEX:
        return _FILE_INDEX[key]

    # Case-insensitive and partial match within repo
    if repo_slug in _REPO_INDEX:
        for dir_name, path in _REPO_INDEX[repo_slug]:
            if dir_name.lower() == skill_lower:
                return path

        candidates = []
        for dir_name, path in _REPO_INDEX[repo_slug]:
            dl = dir_name.lower()
            if skill_lower in dl or dl in skill_lower:
                candidates.append((dir_name, path))
        if len(candidates) == 1:
            return candidates[0][1]
        if candidates:
            for dir_name, path in candidates:
                if dir_name.lower().startswith(skill_lower):
                    return path
            return candidates[0][1]

    # Strip common prefixes
    for prefix in ("bio-", "bio_"):
        if skill_lower.startswith(prefix):
            stripped = skill_lower[len(prefix):]
            for rs in _REPO_INDEX:
                if rs == repo_slug or rs.startswith(repo_slug.split("__")[0]):
                    for dir_name, path in _REPO_INDEX[rs]:
                        dl = dir_name.lower()
                        if dl == stripped or stripped in dl:
                            return path

    return None


def read_skill_content(filepath, max_chars=6000):
    """Read SKILL.md content, truncated to max_chars."""
    if filepath is None or not filepath.exists():
        return ""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
        return text[:max_chars]
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────
# Enhanced JSON extraction (3-layer)
# ─────────────────────────────────────────────────────────
def extract_json_layer1(content):
    """Layer 1: Strip markdown fences and parse directly."""
    text = content.strip()
    # Remove markdown code block wrapper
    if text.startswith("```"):
        lines = text.split("\n")
        if len(lines) > 2:
            text = "\n".join(lines[1:-1])
        text = text.strip()
    if text.startswith("```"):
        text = text[3:].strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    # Remove json language tag
    if text.startswith("json"):
        text = text[4:].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def extract_json_layer2(content):
    """Layer 2: Regex extract first balanced {…} block."""
    # Find the first opening brace
    start = content.find("{")
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False
    end = start

    for i in range(start, len(content)):
        ch = content[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    if depth != 0:
        return None

    try:
        return json.loads(content[start:end])
    except json.JSONDecodeError:
        return None


def extract_json_layer3(content):
    """Layer 3: Field-by-field regex extraction."""
    result = {}

    # research_tier
    m = re.search(r'"research_tier"\s*:\s*"([ABCD])"', content)
    if m:
        result["research_tier"] = m.group(1)

    # research_tier_reason
    m = re.search(r'"research_tier_reason"\s*:\s*"([^"]*)"', content)
    if m:
        result["research_tier_reason"] = m.group(1)

    # research_stages - extract array
    m = re.search(r'"research_stages"\s*:\s*\[([^\]]*)\]', content)
    if m:
        stages_str = m.group(1)
        stages = re.findall(r'"(\w+)"', stages_str)
        result["research_stages"] = stages

    # domain
    m = re.search(r'"domain"\s*:\s*"([^"]*)"', content)
    if m:
        result["domain"] = m.group(1)

    # added_value
    m = re.search(r'"added_value"\s*:\s*"(\w+)"', content)
    if m:
        result["added_value"] = m.group(1)

    # added_value_reason
    m = re.search(r'"added_value_reason"\s*:\s*"([^"]*)"', content)
    if m:
        result["added_value_reason"] = m.group(1)

    # doc_completeness - extract sub-object
    dc = {}
    for field in ("has_when_to_use", "has_prerequisites", "has_examples"):
        m = re.search(rf'"{field}"\s*:\s*(true|false)', content)
        if m:
            dc[field] = m.group(1) == "true"
    m = re.search(r'"instruction_clarity"\s*:\s*(\d)', content)
    if m:
        dc["instruction_clarity"] = int(m.group(1))
    if dc:
        result["doc_completeness"] = dc

    # Check if we got enough fields
    if "research_tier" in result and "domain" in result:
        return result
    return None


def extract_json_enhanced(content):
    """Try all 3 layers of JSON extraction. Returns parsed dict or None."""
    if not content:
        return None

    parsed = extract_json_layer1(content)
    if parsed and isinstance(parsed, dict):
        return parsed

    parsed = extract_json_layer2(content)
    if parsed and isinstance(parsed, dict):
        return parsed

    parsed = extract_json_layer3(content)
    if parsed and isinstance(parsed, dict):
        return parsed

    return None


# ─────────────────────────────────────────────────────────
# LLM call with enhanced extraction
# ─────────────────────────────────────────────────────────
def call_llm_enhanced(skill_name, repo, research_relevance, quality, content):
    """Call LLM API with enhanced JSON extraction. Returns parsed dict or None."""
    user_prompt = f"""Evaluate this skill:

Skill: {skill_name}
Repo: {repo}
Current audit: relevance={research_relevance}, quality={quality}

SKILL.md content:
---
{content}
---

Return ONLY the JSON evaluation object. Do NOT wrap in markdown code blocks."""

    payload = {
        "model": MODEL,
        "max_tokens": 2048,
        "thinking": {
            "type": "enabled",
            "budget_tokens": 10240,
        },
        "messages": [
            {"role": "user", "content": SYSTEM_PROMPT + "\n\n" + user_prompt},
        ],
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                API_URL, json=payload, headers=headers, timeout=120
            )
            resp.raise_for_status()
            result = resp.json()

            # Extract text content (skip thinking blocks)
            raw = ""
            choices = result.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                msg_content = message.get("content", "")
                if isinstance(msg_content, list):
                    for block in msg_content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            raw = block.get("text", "")
                            break
                else:
                    raw = msg_content

            if not raw:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** (attempt + 1))
                    continue
                return None

            # Enhanced extraction
            parsed = extract_json_enhanced(raw)
            if parsed:
                return parsed

            print(f"    All extraction layers failed for {skill_name}")
            print(f"    Raw (first 200): {raw[:200]}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** (attempt + 1))
                continue
            return None

        except requests.exceptions.HTTPError:
            if resp.status_code == 429:
                wait = 2 ** (attempt + 2)
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            print(f"    HTTP error for {skill_name}: {resp.status_code}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            return None
        except Exception as e:
            print(f"    Error for {skill_name}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            return None

    return None


# ─────────────────────────────────────────────────────────
# Inheritance re-propagation
# ─────────────────────────────────────────────────────────
def repropagate_inheritance(multidim_data, dedup_data, fixed_skills):
    """Re-propagate inheritance for fork_copies of fixed canonical entries.

    fixed_skills: set of (skill_name, repo, theme) tuples that were fixed.
    Returns count of re-propagated entries.
    """
    dedup_lookup = {}
    for entry in dedup_data["results"]:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        dedup_lookup[key] = entry

    multidim_lookup = {}
    for entry in multidim_data["results"]:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        multidim_lookup[key] = entry

    # Find which fixed entries are canonicals
    fixed_canonicals = {}
    for sk, rp, th in fixed_skills:
        dkey = (sk, rp, th)
        de = dedup_lookup.get(dkey)
        if de and de.get("uniqueness") == "canonical":
            fixed_canonicals[(sk.lower(), rp)] = multidim_lookup.get(dkey)

    if not fixed_canonicals:
        return 0

    # Find fork_copies that point to these canonicals
    propagated = 0
    for entry in multidim_data["results"]:
        dkey = (entry["skill_name"], entry["repo"], entry["theme"])
        de = dedup_lookup.get(dkey)
        if not de or de.get("uniqueness") != "fork_copy":
            continue

        dup_group = de.get("duplicate_group", "")
        canon_repo = de.get("canonical_repo", "")
        source_key = (dup_group, canon_repo)

        if source_key not in fixed_canonicals:
            continue

        source = fixed_canonicals[source_key]
        if source is None:
            continue

        # Re-propagate
        for field in INHERIT_FIELDS:
            if field in source:
                entry[field] = source[field]
        entry["inherited_from"] = canon_repo
        entry["skipped"] = False
        # Clear garbage flag if present
        if "inherited_quality" in entry:
            del entry["inherited_quality"]
        propagated += 1

    return propagated


def load_json(filepath):
    """Load JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    """Save JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    """Main entry point for retry_failed."""
    print("=" * 60)
    print("Phase 2a: Retry LLM Failures")
    print("=" * 60)

    # Load data
    print("\n1. Loading data files...")
    multidim_data = load_json(MULTIDIM_FILE)
    dedup_data = load_json(DEDUP_FILE)
    audit_data = load_json(AUDIT_FILE)
    total = len(multidim_data["results"])
    print(f"   {total} multidim entries loaded")

    # Build audit lookup for LLM prompt data
    audit_lookup = {}
    for entry in audit_data["results"]:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        audit_lookup[key] = entry

    # Find LLM-failed entries
    failed = []
    for i, entry in enumerate(multidim_data["results"]):
        if entry.get("skipped") and "LLM evaluation failed" in entry.get(
            "research_tier_reason", ""
        ):
            failed.append((i, entry))
    print(f"   LLM-failed entries: {len(failed)}")

    if not failed:
        print("   No LLM failures to retry!")
        return

    # Build file index
    print("\n2. Building file index...")
    build_file_index()

    # Backup
    print("\n3. Creating backup...")
    backup_path = str(MULTIDIM_FILE) + BACKUP_SUFFIX
    shutil.copy2(MULTIDIM_FILE, backup_path)
    print(f"   Backed up to {backup_path}")

    # Retry each failed entry
    print(f"\n4. Retrying {len(failed)} LLM failures...")
    fixed_count = 0
    still_failed = 0
    no_content = 0
    fixed_skills = set()
    tier_dist = Counter()

    for idx, (i, entry) in enumerate(failed):
        skill = entry["skill_name"]
        repo = entry["repo"]
        theme = entry["theme"]
        print(f"   [{idx+1}/{len(failed)}] {skill} ({repo})...", end=" ")

        # Find SKILL.md
        filepath = find_skill_file(skill, repo)
        content = read_skill_content(filepath)

        if not content:
            print("NO CONTENT - skipping")
            no_content += 1
            still_failed += 1
            continue

        # Get audit data for LLM prompt
        akey = (skill, repo, theme)
        audit_entry = audit_lookup.get(akey, {})
        relevance = audit_entry.get("research_relevance", "unknown")
        quality = audit_entry.get("overall_quality", "unknown")

        # Call LLM with enhanced extraction
        parsed = call_llm_enhanced(skill, repo, relevance, quality, content)

        if parsed is None:
            print("FAILED again")
            still_failed += 1
            continue

        # Update entry with parsed results
        entry["research_tier"] = parsed.get("research_tier", "D")
        entry["research_tier_reason"] = parsed.get("research_tier_reason", "")
        entry["research_stages"] = parsed.get("research_stages", [])
        # Keep domain_original from Phase 1b if present
        if "domain_original" not in entry:
            entry["domain_original"] = entry.get("domain", "")
        entry["domain"] = parsed.get("domain", "unknown")
        entry["added_value"] = parsed.get("added_value", "low")
        entry["added_value_reason"] = parsed.get("added_value_reason", "")
        entry["doc_completeness"] = parsed.get("doc_completeness", {})
        entry["skipped"] = False
        entry["research_tier_reason"] = parsed.get(
            "research_tier_reason", ""
        )

        tier_dist[entry["research_tier"]] += 1
        fixed_count += 1
        fixed_skills.add((skill, repo, theme))
        print(f"OK -> tier={entry['research_tier']}")

        # Rate limiting
        if idx < len(failed) - 1:
            time.sleep(0.5)

    print(f"\n   Results: {fixed_count} fixed, {still_failed} still failed")
    print(f"   ({no_content} had no content)")
    print(f"   Tier distribution of fixed: {dict(tier_dist)}")

    # Re-propagate inheritance
    print("\n5. Re-propagating inheritance for fixed canonicals...")
    propagated = repropagate_inheritance(multidim_data, dedup_data, fixed_skills)
    print(f"   Re-propagated to {propagated} fork_copies")

    # Verification
    print("\n6. Verification...")
    post_failed = sum(
        1 for e in multidim_data["results"]
        if e.get("skipped") and "LLM evaluation failed" in e.get(
            "research_tier_reason", ""
        )
    )
    post_garbage = sum(
        1 for e in multidim_data["results"]
        if e.get("inherited_quality") == "garbage"
    )
    post_total = len(multidim_data["results"])
    post_tiers = Counter(
        e.get("research_tier", "?") for e in multidim_data["results"]
    )

    print(f"   LLM failures: {len(failed)} -> {post_failed}")
    print(f"   Garbage inherited: {post_garbage}")
    print(f"   Total entries: {post_total} (should be {total})")
    print(f"   Tier distribution: {dict(sorted(post_tiers.items()))}")

    ok = True
    if post_total != total:
        print("   ERROR: Total entry count changed!")
        ok = False

    # Save
    if ok:
        print("\n7. Saving updated multidim_audit.json...")
        save_json(MULTIDIM_FILE, multidim_data)
        print("   Done!")
    else:
        print("\n7. SKIPPING save due to errors above.")
        sys.exit(1)

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  LLM failures retried: {len(failed)}")
    print(f"  Fixed: {fixed_count}")
    print(f"  Still failed: {still_failed} (target: < 10)")
    print(f"  Re-propagated: {propagated} fork_copies")
    print(f"  Garbage remaining: {post_garbage}")
    print("=" * 60)


if __name__ == "__main__":
    main()

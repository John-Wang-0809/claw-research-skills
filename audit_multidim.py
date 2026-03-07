#!/usr/bin/env python3
"""
[IN]  Dependencies/Inputs:
 - dedup_results.json (Phase 1 output: uniqueness labels for each skill)
 - audit_results.json (existing audit data: function_accuracy, research_relevance, quality)
 - Final_Research_Skills_Link_Downloads_By_Theme_LATEST/**/SKILL.md (skill file contents)
 - API: https://yunwu.ai/v1/chat/completions (claude-haiku-4-5-20251001 with thinking)
[OUT] Outputs:
 - multidim_audit.json (5 new LLM-evaluated dimensions per skill)
[POS] Position in the system:
 - Phase 2 of multi-dimensional audit. Calls LLM API to evaluate 5 dimensions
   for each non-fork_copy skill (~1466). Includes checkpoint/resume and concurrent requests.
   Output feeds into build_relevance_page.py (Phase 3) for visualization.
   Fork_copy skills inherit their canonical's audit results.
   find_skill_file() uses 8 strategies (exact, partial, strip-prefix, cross-theme,
   hyphenated, normalized, token-Jaccard, global cross-repo) to locate SKILL.md files.
   _tokenize_for_jaccard() normalizes all separators (hyphens, underscores, spaces)
   to hyphens before splitting, preventing false negatives for space-separated names.

 Change warning: once you modify this file's logic, you must update this comment block,
 and check/update the module doc (README/CLAUDE) in the containing folder; update the root
 global map if necessary.
"""

import json
import os
import re
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from threading import Lock

import requests
from dotenv import load_dotenv

load_dotenv()

BASE = Path(__file__).parent
DEDUP_FILE = BASE / "dedup_results.json"
AUDIT_FILE = BASE / "audit_results.json"
DOWNLOADS_DIR = BASE / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
OUTPUT = BASE / "multidim_audit.json"
CHECKPOINT = BASE / "multidim_checkpoint.json"

# API config
API_URL = os.getenv("BASE_URL", "https://yunwu.ai") + "/v1/chat/completions"
API_KEY = os.getenv("API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"
MAX_CONCURRENT = 5
CHECKPOINT_INTERVAL = 10  # save every N completions

# Theme directory mapping (audit themes → download dir names)
THEME_DIR_MAP = {
    "01_information_retrieval_evidence_collection": "01_information_retrieval_evidence_collection",
    "02_literature_review_writing_citation_part1": "02_literature_review_writing_citation",
    "02_literature_review_writing_citation_part2": "02_literature_review_writing_citation",
    "03_experiment_benchmark_reproducibility_validation_part1": "03_experiment_benchmark_reproducibility_validation",
    "03_experiment_benchmark_reproducibility_validation_part2": "03_experiment_benchmark_reproducibility_validation",
    "04_data_analysis_and_evidence_interpretation": "04_data_analysis_and_evidence_interpretation",
    "05_research_operations_and_workflow_support": "05_research_operations_and_workflow_support",
    "06_Additional_Scientific_Skills": "06_Additional_Scientific_Skills",
}

# Global file index (built once at startup)
_FILE_INDEX = None  # (repo_slug, skill_dir_lower) -> path
_REPO_INDEX = None  # repo_slug -> [(skill_dir_name, path)]


def build_file_index():
    """Pre-scan all SKILL.md files and build lookup index.
    Must be called once at startup.
    """
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
- A (Core Research Tool): Directly produces research outputs. E.g., genome assembly,
  statistical analysis, paper writing, literature search, molecular simulation.
- B (Research Infrastructure): Enables reproducible/executable research. E.g.,
  experiment version control, data pipelines, Docker for reproducibility.
- C (Research Productivity): General tools useful in research contexts. E.g.,
  code review, debugging, documentation, project management.
- D (Tangentially Related): Weak or forced research connection. E.g., Rails style guide,
  frontend UI kit, marketing automation.

Research stages: discovery, literature, experiment, analysis, writing, operations

Added value levels:
- high: Provides domain-specific pipeline/knowledge that LLM cannot reliably generate
  from general knowledge (e.g., complete SPAdes assembly workflow with QC steps)
- medium: Provides useful structured instructions that improve consistency
  (e.g., systematic code review checklist)
- low: Restates common knowledge with minimal structure
  (e.g., "write clean code" guidelines)
- negligible: Empty or near-empty skill with no substantive instructions"""


_JACCARD_STOPWORDS = frozenset({
    "and", "with", "the", "for", "of", "in", "to",
    "features", "plugins", "tools", "reference",
})


def _tokenize_for_jaccard(name):
    """Split a name into tokens for Jaccard matching.

    Normalizes all separators (hyphens, underscores, spaces) to hyphens first,
    then splits. This prevents whole phrases becoming single tokens when the
    input has no hyphens (e.g. "Linux Production Shell Scripts").
    """
    normalized = name.lower().replace("_", "-").replace(" ", "-")
    tokens = set(normalized.split("-"))
    return tokens - _JACCARD_STOPWORDS - {""}


def _jaccard_similarity(set_a, set_b):
    """Jaccard similarity between two sets."""
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def find_skill_file(skill_name, repo, theme):
    """Find SKILL.md file using pre-built index.
    Tries 8 strategies: exact → partial → strip-prefix → cross-theme →
    hyphenated → normalized → token-Jaccard → global cross-repo.
    """
    repo_slug = repo.replace("/", "__")
    skill_lower = skill_name.lower()

    # Strategy 1: exact match by (repo_slug, skill_name)
    key = (repo_slug, skill_lower)
    if key in _FILE_INDEX:
        return _FILE_INDEX[key]

    # Strategy 2: search repo's skills for partial match
    if repo_slug in _REPO_INDEX:
        # Case-insensitive exact
        for dir_name, path in _REPO_INDEX[repo_slug]:
            if dir_name.lower() == skill_lower:
                return path

        # Partial match: skill_name contained in dir or vice versa
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

    # Strategy 3: strip common prefixes (e.g., "bio-" for GPTomics)
    prefixes = ["bio-", "bio_"]
    for prefix in prefixes:
        if skill_lower.startswith(prefix):
            stripped = skill_lower[len(prefix):]
            # Search across all repos matching this org
            for rs in _REPO_INDEX:
                if rs == repo_slug or rs.startswith(repo_slug.split("__")[0]):
                    for dir_name, path in _REPO_INDEX[rs]:
                        dl = dir_name.lower()
                        if dl == stripped or stripped in dl or dl in stripped:
                            return path

    # Strategy 4: cross-theme search (same repo in different theme dirs)
    org_prefix = repo_slug.split("__")[0] + "__"
    for rs in _REPO_INDEX:
        if rs.startswith(org_prefix) and rs.endswith(repo_slug.split("__")[-1]):
            for dir_name, path in _REPO_INDEX[rs]:
                dl = dir_name.lower()
                if dl == skill_lower or skill_lower in dl:
                    return path

    # Strategy 5: hyphenated name variants (e.g., "Agent Development" → "agent-development")
    hyphenated = skill_lower.replace(" ", "-")
    if hyphenated != skill_lower:
        key2 = (repo_slug, hyphenated)
        if key2 in _FILE_INDEX:
            return _FILE_INDEX[key2]
        # Search across the repo
        if repo_slug in _REPO_INDEX:
            for dir_name, path in _REPO_INDEX[repo_slug]:
                if dir_name.lower() == hyphenated:
                    return path

    # Strategy 6: normalize hyphens/underscores
    norm = skill_lower.replace("_", "-").replace(" ", "-")
    norm_key = (repo_slug, norm)
    if norm_key in _FILE_INDEX:
        return _FILE_INDEX[norm_key]

    # Strategy 7: Token-Jaccard fuzzy matching (threshold >= 0.4)
    tokens_skill = _tokenize_for_jaccard(skill_name)
    if tokens_skill and repo_slug in _REPO_INDEX:
        best_score = 0.0
        best_path = None
        for dir_name, path in _REPO_INDEX[repo_slug]:
            tokens_dir = _tokenize_for_jaccard(dir_name)
            score = _jaccard_similarity(tokens_skill, tokens_dir)
            if score > best_score:
                best_score = score
                best_path = path
        if best_score >= 0.4 and best_path:
            return best_path

    # Strategy 8: global cross-repo search (exact name match)
    for rs in _REPO_INDEX:
        if rs == repo_slug:
            continue
        for dir_name, path in _REPO_INDEX[rs]:
            if dir_name.lower() == skill_lower or dir_name.lower() == norm:
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


def call_llm(skill_name, repo, research_relevance, overall_quality, skill_content):
    """Call LLM API to evaluate a single skill. Returns parsed JSON or None."""
    user_prompt = f"""Evaluate this skill:

Skill: {skill_name}
Repo: {repo}
Current audit: relevance={research_relevance}, quality={overall_quality}

SKILL.md content:
---
{skill_content}
---

Return ONLY the JSON evaluation object."""

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

    for attempt in range(3):
        try:
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)
            resp.raise_for_status()
            result = resp.json()

            # Extract text content (skip thinking blocks)
            content = ""
            choices = result.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                msg_content = message.get("content", "")
                # Handle both string and list content formats
                if isinstance(msg_content, list):
                    for block in msg_content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            content = block.get("text", "")
                            break
                else:
                    content = msg_content

            if not content:
                return None

            # Parse JSON from response (handle markdown code blocks)
            content = content.strip()
            if content.startswith("```"):
                # Remove markdown code block wrapper
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
                content = content.strip()
            if content.startswith("```"):
                content = content[3:].strip()
            if content.endswith("```"):
                content = content[:-3].strip()

            parsed = json.loads(content)
            # Validate required fields
            required = ["research_tier", "research_stages", "domain", "added_value", "doc_completeness"]
            if all(k in parsed for k in required):
                return parsed
            else:
                print(f"  WARNING: Missing fields for {skill_name}: {[k for k in required if k not in parsed]}")
                return parsed  # return partial result

        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429:
                wait = 2 ** (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            print(f"  HTTP error for {skill_name}: {e}")
            if attempt < 2:
                time.sleep(1)
                continue
            return None
        except json.JSONDecodeError as e:
            print(f"  JSON parse error for {skill_name}: {e}")
            print(f"  Raw content: {content[:200]}")
            if attempt < 2:
                time.sleep(1)
                continue
            return None
        except Exception as e:
            print(f"  Error for {skill_name}: {e}")
            if attempt < 2:
                time.sleep(1)
                continue
            return None

    return None


def load_checkpoint():
    """Load checkpoint if exists."""
    if CHECKPOINT.exists():
        try:
            with open(CHECKPOINT, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_checkpoint(completed_results, lock=None):
    """Save checkpoint to disk."""
    if lock:
        with lock:
            _do_save_checkpoint(completed_results)
    else:
        _do_save_checkpoint(completed_results)


def _do_save_checkpoint(completed_results):
    with open(CHECKPOINT, "w", encoding="utf-8") as f:
        json.dump(completed_results, f, ensure_ascii=False, indent=None)


def main():
    print("=== Phase 2: Multi-dimensional LLM Audit ===\n")

    # 0. Build file index
    print("Building SKILL.md file index...")
    build_file_index()

    # 1. Load dedup results
    print("Loading dedup_results.json...")
    with open(DEDUP_FILE, "r", encoding="utf-8") as f:
        dedup_data = json.load(f)
    all_skills = dedup_data["results"]
    print(f"  Total skills: {len(all_skills)}")

    # Filter to non-fork_copy skills
    to_audit = [s for s in all_skills if s["uniqueness"] != "fork_copy"]
    fork_copies = [s for s in all_skills if s["uniqueness"] == "fork_copy"]
    print(f"  To audit (non-fork_copy): {len(to_audit)}")
    print(f"  Fork copies (will inherit): {len(fork_copies)}")

    # 2. Load existing audit results for context
    print("Loading audit_results.json...")
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        audit_data = json.load(f)
    audit_index = {}
    for r in audit_data["results"]:
        key = (r["skill_name"], r["repo"])
        audit_index[key] = r

    # 3. Load checkpoint
    checkpoint = load_checkpoint()
    completed_count = len(checkpoint)
    if completed_count > 0:
        print(f"  Resuming from checkpoint: {completed_count} already done")

    # 4. Prepare audit tasks
    tasks = []
    for skill in to_audit:
        key = f"{skill['skill_name']}__{skill['repo']}__{skill['theme']}"
        if key in checkpoint:
            continue  # already done

        # Get existing audit data
        audit_key = (skill["skill_name"], skill["repo"])
        existing = audit_index.get(audit_key, {})
        relevance = existing.get("research_relevance", "unknown")
        quality = existing.get("overall_quality", 0)

        # Find and read SKILL.md
        filepath = find_skill_file(skill["skill_name"], skill["repo"], skill["theme"])
        content = read_skill_content(filepath)

        if not content:
            # No content → skip with default values
            checkpoint[key] = {
                "skill_name": skill["skill_name"],
                "repo": skill["repo"],
                "theme": skill["theme"],
                "research_tier": "D",
                "research_tier_reason": "No SKILL.md content available for evaluation",
                "research_stages": [],
                "domain": "unknown",
                "added_value": "negligible",
                "added_value_reason": "No SKILL.md content available",
                "doc_completeness": {
                    "has_when_to_use": False,
                    "has_prerequisites": False,
                    "has_examples": False,
                    "instruction_clarity": 1,
                },
                "skipped": True,
            }
            continue

        tasks.append({
            "key": key,
            "skill_name": skill["skill_name"],
            "repo": skill["repo"],
            "theme": skill["theme"],
            "relevance": relevance,
            "quality": quality,
            "content": content,
        })

    print(f"  Tasks remaining: {len(tasks)}")
    if not tasks:
        print("  All skills already audited!")
    else:
        # 5. Process with concurrent API calls
        lock = Lock()
        completed_since_save = [0]
        total_done = [completed_count]
        total_tasks = len(to_audit)
        errors = [0]

        def process_skill(task):
            result = call_llm(
                task["skill_name"],
                task["repo"],
                task["relevance"],
                task["quality"],
                task["content"],
            )

            if result:
                entry = {
                    "skill_name": task["skill_name"],
                    "repo": task["repo"],
                    "theme": task["theme"],
                    **result,
                    "skipped": False,
                }
            else:
                errors[0] += 1
                entry = {
                    "skill_name": task["skill_name"],
                    "repo": task["repo"],
                    "theme": task["theme"],
                    "research_tier": "D",
                    "research_tier_reason": "LLM evaluation failed",
                    "research_stages": [],
                    "domain": "unknown",
                    "added_value": "low",
                    "added_value_reason": "LLM evaluation failed",
                    "doc_completeness": {
                        "has_when_to_use": False,
                        "has_prerequisites": False,
                        "has_examples": False,
                        "instruction_clarity": 1,
                    },
                    "skipped": True,
                }

            with lock:
                checkpoint[task["key"]] = entry
                total_done[0] += 1
                completed_since_save[0] += 1

                if completed_since_save[0] >= CHECKPOINT_INTERVAL:
                    _do_save_checkpoint(checkpoint)
                    completed_since_save[0] = 0
                    print(f"  [{total_done[0]}/{total_tasks}] checkpoint saved (errors: {errors[0]})")

            return entry

        print(f"\nStarting audit with {MAX_CONCURRENT} concurrent workers...")
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
            futures = {executor.submit(process_skill, t): t for t in tasks}
            for future in as_completed(futures):
                task = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"  FATAL error processing {task['skill_name']}: {e}")

        # Final checkpoint save
        save_checkpoint(checkpoint)
        elapsed = time.time() - start_time
        print(f"\nAudit complete in {elapsed:.0f}s")
        print(f"  Processed: {len(tasks)}")
        print(f"  Errors: {errors[0]}")

    # 6. Build final results
    print("\nBuilding final results...")

    # Collect all audited results (canonical + variant + original)
    audited_results = []
    for skill in to_audit:
        key = f"{skill['skill_name']}__{skill['repo']}__{skill['theme']}"
        if key in checkpoint:
            audited_results.append(checkpoint[key])
        else:
            # Should not happen after full run
            print(f"  WARNING: Missing result for {key}")

    # 7. Propagate canonical results to fork_copies
    # Build lookup: (skill_name_lower, repo) -> audit result
    # Include both canonical and variant entries (variant first, canonical overwrites)
    canonical_lookup = {}
    for r in audited_results:
        for skill in to_audit:
            if (skill["skill_name"] == r["skill_name"]
                    and skill["repo"] == r["repo"]
                    and skill["theme"] == r["theme"]
                    and skill["uniqueness"] in ("canonical", "variant")):
                key = (skill["skill_name"].lower(), skill["repo"])
                # canonical takes priority over variant
                if skill["uniqueness"] == "canonical" or key not in canonical_lookup:
                    canonical_lookup[key] = r
                break

    propagated_count = 0
    for fc in fork_copies:
        # Find the canonical result for this fork_copy
        canonical_key = (fc["duplicate_group"], fc.get("canonical_repo", ""))
        canonical_result = canonical_lookup.get(canonical_key)

        if canonical_result:
            # Copy audit dimensions from canonical
            fc_result = {
                "skill_name": fc["skill_name"],
                "repo": fc["repo"],
                "theme": fc["theme"],
                "research_tier": canonical_result.get("research_tier", "D"),
                "research_tier_reason": canonical_result.get("research_tier_reason", ""),
                "research_stages": canonical_result.get("research_stages", []),
                "domain": canonical_result.get("domain", "unknown"),
                "added_value": canonical_result.get("added_value", "low"),
                "added_value_reason": canonical_result.get("added_value_reason", ""),
                "doc_completeness": canonical_result.get("doc_completeness", {}),
                "inherited_from": fc.get("canonical_repo", ""),
            }
            audited_results.append(fc_result)
            propagated_count += 1
        else:
            # No canonical found → use defaults
            fc_result = {
                "skill_name": fc["skill_name"],
                "repo": fc["repo"],
                "theme": fc["theme"],
                "research_tier": "D",
                "research_tier_reason": "No canonical audit available",
                "research_stages": [],
                "domain": "unknown",
                "added_value": "low",
                "added_value_reason": "No canonical audit available",
                "doc_completeness": {
                    "has_when_to_use": False,
                    "has_prerequisites": False,
                    "has_examples": False,
                    "instruction_clarity": 1,
                },
                "inherited_from": None,
            }
            audited_results.append(fc_result)

    print(f"  Propagated to fork copies: {propagated_count}")

    # 8. Build output
    output = {
        "metadata": {
            "model": MODEL,
            "total_audited": len(to_audit),
            "total_with_propagation": len(audited_results),
            "started_at": checkpoint.get("__started_at", datetime.now().isoformat()),
            "completed_at": datetime.now().isoformat(),
        },
        "results": audited_results,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSaved: {OUTPUT}")
    print(f"Total results: {len(audited_results)}")

    # 9. Summary stats
    from collections import Counter
    tiers = Counter(r.get("research_tier", "?") for r in audited_results)
    values = Counter(r.get("added_value", "?") for r in audited_results)
    print(f"\nTier distribution: {dict(sorted(tiers.items()))}")
    print(f"Added value: {dict(sorted(values.items()))}")

    # Clean up checkpoint after successful completion
    # (keep it around for reference, but could delete)
    print("\nDone! Checkpoint preserved at multidim_checkpoint.json")


if __name__ == "__main__":
    main()

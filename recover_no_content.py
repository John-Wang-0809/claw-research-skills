#!/usr/bin/env python3
"""
[IN]  Dependencies/Inputs:
 - multidim_audit.json (1940 records; Phase 4a left 21 skipped entries)
 - dedup_results.json (for fork_copy inheritance re-propagation)
 - audit_results.json (research_relevance, overall_quality for LLM prompt)
 - Final_Research_Skills_Link_Downloads_By_Theme_LATEST/**/SKILL.md (skill file contents)
 - API: https://yunwu.ai/v1/chat/completions (claude-haiku-4-5-20251001)
[OUT] Outputs:
 - multidim_audit.json (updated: recovered entries have LLM audit results)
 - Backup: multidim_audit.json.bak.phase4d
 - Console report: recovery stats, confirmed missing list
[POS] Position in the system:
 - Phase 4d of multi-dimensional audit. Recovers remaining 21 "no SKILL.md content"
   entries left after Phase 4a. Uses manual overrides for 14 recoverable entries
   (including 1 non-standard filename) and marks 7 truly unrecoverable entries
   with specific reasons. Fixes _tokenize() bug that caused false negatives
   for names without hyphens.

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
BACKUP_SUFFIX = ".bak.phase4d"

# API config
API_URL = os.getenv("BASE_URL", "https://yunwu.ai") + "/v1/chat/completions"
API_KEY = os.getenv("API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"
MAX_RETRIES = 3

# Fields to copy during inheritance
INHERIT_FIELDS = [
    "research_tier", "research_tier_reason", "research_stages",
    "domain", "added_value", "added_value_reason", "doc_completeness",
]

# ─────────────────────────────────────────────────────────
# Manual overrides: (skill_name, repo) → actual directory name
# Built from manual inspection of disk vs skipped entries.
# "__REPO_ROOT__" means SKILL.md is at the repo root.
# ─────────────────────────────────────────────────────────
MANUAL_OVERRIDES = {
    # paper-visualizer → visual-architect (3 repos)
    ("paper-visualizer", "proyecto26/research-skills"): "visual-architect",
    ("paper-visualizer", "proyecto26/sherlock-ai-plugin"): "visual-architect",
    ("paper-visualizer", "WilsonWukz/paper-visualizer-skill"): "visual-architect",
    # Orchestra-Research renames
    ("evaluating-llms-harness", "Orchestra-Research/AI-Research-SKILLs"):
        "lm-evaluation-harness",
    ("evaluating-code-models", "Orchestra-Research/AI-Research-SKILLs"):
        "bigcode-evaluation-harness",
    ("training-llms-megatron", "Orchestra-Research/AI-Research-SKILLs"):
        "megatron-core",
    ("fine-tuning-with-trl", "Orchestra-Research/AI-Research-SKILLs"):
        "trl-fine-tuning",
    ("optimizing-attention-flash", "Orchestra-Research/AI-Research-SKILLs"):
        "flash-attention",
    ("sparse-autoencoder-training", "Orchestra-Research/AI-Research-SKILLs"):
        "saelens",
    # GPTomics bio- prefix renames
    ("bio-longread-alignment", "GPTomics/bioSkills"): "long-read-alignment",
    ("bio-longread-medaka", "GPTomics/bioSkills"): "medaka-polishing",
    ("bio-longread-qc", "GPTomics/bioSkills"): "long-read-qc",
    ("bio-metagenomics-abundance", "GPTomics/bioSkills"):
        "abundance-estimation",
    ("bio-metagenomics-kraken", "GPTomics/bioSkills"):
        "kraken-classification",
    ("bio-metagenomics-metaphlan", "GPTomics/bioSkills"):
        "metaphlan-profiling",
    ("bio-metagenomics-visualization", "GPTomics/bioSkills"):
        "metagenome-visualization",
    ("bio-methylation-methylkit", "GPTomics/bioSkills"): "methylkit-analysis",
    ("bio-pathway-reactome", "GPTomics/bioSkills"): "reactome-pathways",
    # Repo root SKILL.md
    ("research-before-coding", "anombyte93/claude-research-skill"):
        "__REPO_ROOT__",
    # Renames
    ("update-skill", "ychampion/claude-self-learning"): "self-learning",
    ("frontend-dev-guidelines", "mrgoonie/claudekit-skills"):
        "frontend-development",
    # ── Phase 4d: antigravity forks (natural-language name → directory slug) ──
    ("Linux Production Shell Scripts", "sickn33/antigravity-awesome-skills"):
        "linux-shell-scripting",
    ("Linux Production Shell Scripts", "huysynf/antigravity-awesome-skills"):
        "linux-shell-scripting",
    ("Linux Production Shell Scripts", "hangoclong/skills-antigravity-awesome"):
        "linux-shell-scripting",
    ("Linux Production Shell Scripts", "ForaeFactory/antigravity-skills"):
        "linux-shell-scripting",
    ("Wireshark Network Traffic Analysis", "sickn33/antigravity-awesome-skills"):
        "wireshark-analysis",
    ("Wireshark Network Traffic Analysis", "huysynf/antigravity-awesome-skills"):
        "wireshark-analysis",
    ("Wireshark Network Traffic Analysis", "hangoclong/skills-antigravity-awesome"):
        "wireshark-analysis",
    ("Wireshark Network Traffic Analysis", "ForaeFactory/antigravity-skills"):
        "wireshark-analysis",
    ("Cross-Site Scripting and HTML Injection Testing", "sickn33/antigravity-awesome-skills"):
        "xss-html-injection",
    ("Cross-Site Scripting and HTML Injection Testing", "hangoclong/skills-antigravity-awesome"):
        "xss-html-injection",
    # ── Phase 4d: ComposioHQ CamelCase → hyphen ──
    ("SurveyMonkey Automation", "ComposioHQ/awesome-claude-skills"):
        "survey-monkey-automation",
    # ── Phase 4d: nested/root paths ──
    ("pytd", "treasure-data/td-skills"): "python",
    ("context-engineering-collection", "muratcankoylan/Agent-Skills-for-Context-Engineering"):
        "__REPO_ROOT__",
    # ── Phase 4d: non-standard filename ──
    ("Claude-Metacognitive-Skills", "Dr-AneeshJoseph/Claude-Metacognitive-Skills"):
        "__NONSTANDARD__",
}

# Non-standard SKILL.md filenames (for __NONSTANDARD__ overrides)
NONSTANDARD_FILES = {
    ("Claude-Metacognitive-Skills", "Dr-AneeshJoseph/Claude-Metacognitive-Skills"):
        "CONSCIOUSNESS_EXPLORATION_SKILL.md",
}

# Specific reasons for truly unrecoverable entries (Phase 4d/4e, GitHub-verified)
UNRECOVERABLE_REASONS = {
    ("td-mcp", "treasure-data/td-skills"):
        "Listed in README but directory not created on GitHub",
    ("discover-diagrams", "rand/cc-polymath"):
        "Skill does not exist (conflated with diagrams/ category dir)",
    ("reasoning-trace-optimizer", "muratcankoylan/Agent-Skills-for-Context-Engineering"):
        "Skill does not exist on GitHub (404)",
    ("every-marketplace", "EveryInc/every-marketplace"):
        "Not a skill (plugin marketplace container)",
    ("SkillName", "danielmiessler/Personal_AI_Infrastructure"):
        "Placeholder template variable (from CreateSkill doc)",
    # heal-skill REMOVED in Phase 4e — confirmed recoverable from GitHub
    # Security Scanning Tools REMOVED in Phase 4d — recovered via fixed Jaccard
}

# Token-Jaccard stopwords
STOPWORDS = frozenset({
    "and", "with", "the", "for", "of", "in", "to",
    "features", "plugins", "tools", "reference",
})

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
# File index
# ─────────────────────────────────────────────────────────
_FILE_INDEX = None   # (repo_slug, dir_lower) -> path
_REPO_INDEX = None   # repo_slug -> [(dir_name, path)]
_NORM_INDEX = None   # (repo_slug, normalized_dir) -> path


def build_file_index():
    """Pre-scan all SKILL.md files and build lookup indices."""
    global _FILE_INDEX, _REPO_INDEX, _NORM_INDEX
    _FILE_INDEX = {}
    _REPO_INDEX = defaultdict(list)
    _NORM_INDEX = {}

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
                # Normalized key (underscores → hyphens)
                norm = skill_dir_name.lower().replace("_", "-")
                _NORM_INDEX[(repo_slug, norm)] = skill_file

    print(f"  File index: {len(_FILE_INDEX)} SKILL.md files indexed")


def _tokenize(name):
    """Split a name into tokens for Jaccard matching.

    Normalizes all separators (hyphens, underscores, spaces) to hyphens first,
    then splits. This prevents whole phrases becoming single tokens when the
    input has no hyphens (e.g. "Linux Production Shell Scripts").
    """
    normalized = name.lower().replace("_", "-").replace(" ", "-")
    tokens = set(normalized.split("-"))
    return tokens - STOPWORDS - {""}


def _jaccard(set_a, set_b):
    """Jaccard similarity between two sets."""
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def find_skill_file_enhanced(skill_name, repo):
    """Enhanced find_skill_file with strategies 1-9.

    Returns (filepath, strategy_used) or (None, None).
    """
    repo_slug = repo.replace("/", "__")
    skill_lower = skill_name.lower()

    # Strategy 0: manual override
    override_key = (skill_name, repo)
    if override_key in MANUAL_OVERRIDES:
        target_dir = MANUAL_OVERRIDES[override_key]
        if target_dir == "__NONSTANDARD__":
            # Non-standard filename — search repo for the specific file
            ns_filename = NONSTANDARD_FILES.get(override_key)
            if ns_filename:
                for rs in _REPO_INDEX:
                    if rs == repo_slug or rs.startswith(
                        repo_slug.split("__")[0]
                    ):
                        for dn, path in _REPO_INDEX[rs]:
                            # path points to SKILL.md; check sibling with ns_filename
                            ns_path = path.parent / ns_filename
                            if ns_path.exists():
                                return ns_path, "manual_override(nonstandard)"
                            # Also check repo root
                            repo_root = path.parent.parent
                            ns_root = repo_root / ns_filename
                            if ns_root.exists():
                                return ns_root, "manual_override(nonstandard)"
                # Try direct search in downloads dir
                for theme_dir in DOWNLOADS_DIR.iterdir():
                    if not theme_dir.is_dir():
                        continue
                    for rd in theme_dir.iterdir():
                        if rd.name == repo_slug and rd.is_dir():
                            for f in rd.rglob(ns_filename):
                                return f, "manual_override(nonstandard)"
        elif target_dir == "__REPO_ROOT__":
            # SKILL.md at repo root: parent.name == repo_slug
            key = (repo_slug, repo_slug)
            if key in _FILE_INDEX:
                return _FILE_INDEX[key], "manual_override(repo_root)"
            # Also try slug variants
            for rs in _REPO_INDEX:
                if rs == repo_slug:
                    for dn, path in _REPO_INDEX[rs]:
                        if dn == repo_slug:
                            return path, "manual_override(repo_root)"
        else:
            key = (repo_slug, target_dir.lower())
            if key in _FILE_INDEX:
                return _FILE_INDEX[key], "manual_override"
            # Search across themes for same repo
            for rs in _REPO_INDEX:
                if rs == repo_slug or (
                    rs.startswith(repo_slug.split("__")[0])
                    and rs.endswith(repo_slug.split("__")[-1])
                ):
                    for dn, path in _REPO_INDEX[rs]:
                        if dn.lower() == target_dir.lower():
                            return path, "manual_override(cross_theme)"
        # Override target not found — fall through to other strategies

    # Strategy 1: exact match
    key = (repo_slug, skill_lower)
    if key in _FILE_INDEX:
        return _FILE_INDEX[key], "exact"

    # Strategy 2: case-insensitive + partial within repo
    if repo_slug in _REPO_INDEX:
        for dir_name, path in _REPO_INDEX[repo_slug]:
            if dir_name.lower() == skill_lower:
                return path, "case_insensitive"

        candidates = []
        for dir_name, path in _REPO_INDEX[repo_slug]:
            dl = dir_name.lower()
            if skill_lower in dl or dl in skill_lower:
                candidates.append((dir_name, path))
        if len(candidates) == 1:
            return candidates[0][1], "partial"
        if candidates:
            for dir_name, path in candidates:
                if dir_name.lower().startswith(skill_lower):
                    return path, "partial_prefix"
            return candidates[0][1], "partial_first"

    # Strategy 3: strip bio- prefix
    for prefix in ("bio-", "bio_"):
        if skill_lower.startswith(prefix):
            stripped = skill_lower[len(prefix):]
            for rs in _REPO_INDEX:
                if rs == repo_slug or rs.startswith(
                    repo_slug.split("__")[0]
                ):
                    for dir_name, path in _REPO_INDEX[rs]:
                        dl = dir_name.lower()
                        if dl == stripped or stripped in dl or dl in stripped:
                            return path, "strip_bio_prefix"

    # Strategy 4: cross-theme (same repo, different theme dir)
    org_prefix = repo_slug.split("__")[0] + "__"
    for rs in _REPO_INDEX:
        if rs.startswith(org_prefix) and rs.endswith(
            repo_slug.split("__")[-1]
        ):
            for dir_name, path in _REPO_INDEX[rs]:
                dl = dir_name.lower()
                if dl == skill_lower or skill_lower in dl:
                    return path, "cross_theme"

    # Strategy 5: hyphenated name (spaces → hyphens)
    hyphenated = skill_lower.replace(" ", "-")
    if hyphenated != skill_lower:
        key2 = (repo_slug, hyphenated)
        if key2 in _FILE_INDEX:
            return _FILE_INDEX[key2], "hyphenated"
        if repo_slug in _REPO_INDEX:
            for dir_name, path in _REPO_INDEX[repo_slug]:
                if dir_name.lower() == hyphenated:
                    return path, "hyphenated_search"

    # Strategy 6: normalize hyphens/underscores
    norm = skill_lower.replace("_", "-").replace(" ", "-")
    norm_key = (repo_slug, norm)
    if norm_key in _NORM_INDEX:
        return _NORM_INDEX[norm_key], "normalized"

    # Strategy 7: Token-Jaccard fuzzy matching (threshold ≥ 0.4)
    tokens_skill = _tokenize(skill_name)
    if tokens_skill and repo_slug in _REPO_INDEX:
        best_score = 0.0
        best_path = None
        for dir_name, path in _REPO_INDEX[repo_slug]:
            tokens_dir = _tokenize(dir_name)
            score = _jaccard(tokens_skill, tokens_dir)
            if score > best_score:
                best_score = score
                best_path = path
        if best_score >= 0.4 and best_path:
            return best_path, f"jaccard({best_score:.2f})"

    # Strategy 8: global cross-repo search (exact name match)
    for rs in _REPO_INDEX:
        if rs == repo_slug:
            continue
        for dir_name, path in _REPO_INDEX[rs]:
            if dir_name.lower() == skill_lower or dir_name.lower() == norm:
                return path, f"global({rs})"

    return None, None


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
# JSON extraction (3-layer, from retry_failed.py)
# ─────────────────────────────────────────────────────────
def extract_json_layer1(content):
    """Strip markdown fences and parse."""
    text = content.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if len(lines) > 2:
            text = "\n".join(lines[1:-1])
        text = text.strip()
    if text.startswith("```"):
        text = text[3:].strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    if text.startswith("json"):
        text = text[4:].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def extract_json_layer2(content):
    """Balanced brace extraction."""
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
    """Field-by-field regex extraction."""
    result = {}
    m = re.search(r'"research_tier"\s*:\s*"([ABCD])"', content)
    if m:
        result["research_tier"] = m.group(1)
    m = re.search(r'"research_tier_reason"\s*:\s*"([^"]*)"', content)
    if m:
        result["research_tier_reason"] = m.group(1)
    m = re.search(r'"research_stages"\s*:\s*\[([^\]]*)\]', content)
    if m:
        result["research_stages"] = re.findall(r'"(\w+)"', m.group(1))
    m = re.search(r'"domain"\s*:\s*"([^"]*)"', content)
    if m:
        result["domain"] = m.group(1)
    m = re.search(r'"added_value"\s*:\s*"(\w+)"', content)
    if m:
        result["added_value"] = m.group(1)
    m = re.search(r'"added_value_reason"\s*:\s*"([^"]*)"', content)
    if m:
        result["added_value_reason"] = m.group(1)
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
    if "research_tier" in result and "domain" in result:
        return result
    return None


def extract_json_enhanced(content):
    """Try all 3 layers. Returns parsed dict or None."""
    if not content:
        return None
    for extractor in (extract_json_layer1, extract_json_layer2,
                      extract_json_layer3):
        parsed = extractor(content)
        if parsed and isinstance(parsed, dict):
            return parsed
    return None


# ─────────────────────────────────────────────────────────
# LLM call
# ─────────────────────────────────────────────────────────
def call_llm(skill_name, repo, research_relevance, quality, content):
    """Call LLM API with enhanced JSON extraction."""
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
        "thinking": {"type": "enabled", "budget_tokens": 10240},
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

            raw = ""
            choices = result.get("choices", [])
            if choices:
                msg = choices[0].get("message", {})
                msg_content = msg.get("content", "")
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

            parsed = extract_json_enhanced(raw)
            if parsed:
                return parsed

            print(f"    JSON extraction failed: {raw[:150]}")
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
            print(f"    HTTP {resp.status_code}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            return None
        except Exception as e:
            print(f"    Error: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            return None

    return None


# ─────────────────────────────────────────────────────────
# Inheritance re-propagation (from retry_failed.py)
# ─────────────────────────────────────────────────────────
def repropagate_inheritance(multidim_data, dedup_data, fixed_skills):
    """Re-propagate inheritance for fork_copies of fixed canonical entries."""
    dedup_lookup = {}
    for entry in dedup_data["results"]:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        dedup_lookup[key] = entry

    multidim_lookup = {}
    for entry in multidim_data["results"]:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        multidim_lookup[key] = entry

    fixed_canonicals = {}
    for sk, rp, th in fixed_skills:
        dkey = (sk, rp, th)
        de = dedup_lookup.get(dkey)
        if de and de.get("uniqueness") == "canonical":
            fixed_canonicals[(sk.lower(), rp)] = multidim_lookup.get(dkey)

    if not fixed_canonicals:
        return 0

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

        for field in INHERIT_FIELDS:
            if field in source:
                entry[field] = source[field]
        entry["inherited_from"] = canon_repo
        entry["skipped"] = False
        if "inherited_quality" in entry:
            del entry["inherited_quality"]
        propagated += 1

    return propagated


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Phase 4d: Recover Remaining No-Content Entries")
    print("=" * 60)

    # 1. Load data
    print("\n1. Loading data files...")
    multidim_data = load_json(MULTIDIM_FILE)
    dedup_data = load_json(DEDUP_FILE)
    audit_data = load_json(AUDIT_FILE)
    total = len(multidim_data["results"])
    print(f"   {total} multidim entries loaded")

    # Build audit lookup
    audit_lookup = {}
    for entry in audit_data["results"]:
        key = (entry["skill_name"], entry["repo"], entry["theme"])
        audit_lookup[key] = entry

    # 2. Identify skipped (no-content) entries
    #    Phase 4a looked for "No SKILL.md content"; Phase 4d also recovers
    #    entries that Phase 4a marked as "Confirmed: SKILL.md not on disk"
    NO_CONTENT_MARKERS = (
        "No SKILL.md content",
        "Confirmed: SKILL.md not on disk",
        "SKILL.md not in local clone",
    )
    skipped_entries = []
    for i, entry in enumerate(multidim_data["results"]):
        reason = entry.get("research_tier_reason", "")
        if entry.get("skipped") and any(m in reason for m in NO_CONTENT_MARKERS):
            skipped_entries.append((i, entry))

    print(f"   No-content entries: {len(skipped_entries)}")
    if not skipped_entries:
        print("   Nothing to recover!")
        return

    # 3. Build file index
    print("\n2. Building file index...")
    build_file_index()

    # 4. Backup
    print("\n3. Creating backup...")
    backup_path = str(MULTIDIM_FILE) + BACKUP_SUFFIX
    shutil.copy2(MULTIDIM_FILE, backup_path)
    print(f"   Backed up to {backup_path}")

    # 5. Enhanced matching + LLM audit
    print(f"\n4. Recovering {len(skipped_entries)} entries...")
    recovered = 0
    llm_failed = 0
    confirmed_missing = 0
    fixed_skills = set()
    strategy_stats = Counter()
    tier_dist = Counter()
    missing_list = []

    for idx, (i, entry) in enumerate(skipped_entries):
        skill = entry["skill_name"]
        repo = entry["repo"]
        theme = entry["theme"]
        print(f"   [{idx+1}/{len(skipped_entries)}] {skill} ({repo})...",
              end=" ")

        # Enhanced file search
        filepath, strategy = find_skill_file_enhanced(skill, repo)
        content = read_skill_content(filepath)

        if not content:
            # Check for specific unrecoverable reason
            unrec_key = (skill, repo)
            if unrec_key in UNRECOVERABLE_REASONS:
                specific_reason = UNRECOVERABLE_REASONS[unrec_key]
                entry["research_tier_reason"] = specific_reason
                print(f"UNRECOVERABLE ({specific_reason})")
            else:
                entry["research_tier_reason"] = (
                    "Confirmed: SKILL.md not on disk"
                )
                print("MISSING")
            confirmed_missing += 1
            missing_list.append((skill, repo))
            continue

        strategy_stats[strategy] += 1

        # Get audit data for LLM prompt
        akey = (skill, repo, theme)
        audit_entry = audit_lookup.get(akey, {})
        relevance = audit_entry.get("research_relevance", "unknown")
        quality = audit_entry.get("overall_quality", "unknown")

        # Call LLM
        parsed = call_llm(skill, repo, relevance, quality, content)

        if parsed is None:
            print(f"LLM FAILED (found via {strategy})")
            llm_failed += 1
            entry["research_tier_reason"] = "LLM evaluation failed"
            continue

        # Update entry
        entry["research_tier"] = parsed.get("research_tier", "D")
        entry["research_tier_reason"] = parsed.get(
            "research_tier_reason", ""
        )
        entry["research_stages"] = parsed.get("research_stages", [])
        if "domain_original" not in entry:
            entry["domain_original"] = entry.get("domain", "")
        entry["domain"] = parsed.get("domain", "unknown")
        entry["added_value"] = parsed.get("added_value", "low")
        entry["added_value_reason"] = parsed.get("added_value_reason", "")
        entry["doc_completeness"] = parsed.get("doc_completeness", {})
        entry["skipped"] = False

        tier_dist[entry["research_tier"]] += 1
        recovered += 1
        fixed_skills.add((skill, repo, theme))
        print(f"OK tier={entry['research_tier']} via {strategy}")

        # Rate limiting
        if idx < len(skipped_entries) - 1:
            time.sleep(0.5)

    print(f"\n   Results:")
    print(f"     Recovered:         {recovered}")
    print(f"     LLM failed:        {llm_failed}")
    print(f"     Confirmed missing: {confirmed_missing}")
    print(f"     Tier distribution: {dict(tier_dist)}")
    print(f"     Strategy stats:    {dict(strategy_stats)}")

    # 6. Re-propagate inheritance
    print("\n5. Re-propagating inheritance for fixed canonicals...")
    propagated = repropagate_inheritance(
        multidim_data, dedup_data, fixed_skills
    )
    print(f"   Re-propagated to {propagated} fork_copies")

    # 7. Verification
    print("\n6. Verification...")
    post_skipped = sum(
        1 for e in multidim_data["results"] if e.get("skipped")
    )
    post_no_content = sum(
        1 for e in multidim_data["results"]
        if e.get("skipped") and "No SKILL.md content" in e.get(
            "research_tier_reason", ""
        )
    )
    post_confirmed = sum(
        1 for e in multidim_data["results"]
        if e.get("skipped") and "Confirmed: SKILL.md not on disk" in e.get(
            "research_tier_reason", ""
        )
    )
    post_not_in_clone = sum(
        1 for e in multidim_data["results"]
        if e.get("skipped") and "not in local clone" in e.get(
            "research_tier_reason", ""
        )
    )
    post_not_skill = sum(
        1 for e in multidim_data["results"]
        if e.get("skipped") and "Not a skill" in e.get(
            "research_tier_reason", ""
        )
    )
    post_placeholder = sum(
        1 for e in multidim_data["results"]
        if e.get("skipped") and "Placeholder" in e.get(
            "research_tier_reason", ""
        )
    )
    post_no_match = sum(
        1 for e in multidim_data["results"]
        if e.get("skipped") and "No matching directory" in e.get(
            "research_tier_reason", ""
        )
    )
    post_llm_fail = sum(
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

    print(f"   Total entries:      {post_total} (should be {total})")
    print(f"   Still skipped:      {post_skipped} (was {len(skipped_entries)})")
    print(f"     No-content:       {post_no_content}")
    print(f"     Confirmed missing:{post_confirmed}")
    print(f"     Not in clone:     {post_not_in_clone}")
    print(f"     Not a skill:      {post_not_skill}")
    print(f"     No match dir:     {post_no_match}")
    print(f"     Placeholder:      {post_placeholder}")
    print(f"     LLM failed:       {post_llm_fail}")
    print(f"   Garbage inherited:  {post_garbage}")
    print(f"   Tier distribution:  {dict(sorted(post_tiers.items()))}")

    ok = post_total == total
    if not ok:
        print("   ERROR: Total entry count changed!")

    # 8. Save
    if ok:
        print("\n7. Saving updated multidim_audit.json...")
        save_json(MULTIDIM_FILE, multidim_data)
        print("   Done!")
    else:
        print("\n7. SKIPPING save due to errors.")
        sys.exit(1)

    # 9. Report confirmed missing
    if missing_list:
        print(f"\n{'='*60}")
        print(f"Confirmed missing ({len(missing_list)} entries):")
        for skill, repo in missing_list:
            print(f"  {skill} @ {repo}")

    # Summary
    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Input:               {len(skipped_entries)} no-content entries")
    print(f"  Recovered:           {recovered}")
    print(f"  LLM failed:          {llm_failed}")
    print(f"  Confirmed missing:   {confirmed_missing}")
    print(f"  Re-propagated:       {propagated} fork_copies")
    print(f"  Remaining skipped:   {post_skipped}")
    print(f"  Garbage remaining:   {post_garbage}")
    print("=" * 60)


if __name__ == "__main__":
    main()

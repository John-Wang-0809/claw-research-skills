#!/usr/bin/env python3
"""
[IN]  Dependencies/Inputs:
 - SKILL_CATALOG.md (skill list: name, english description, url, organized by theme/repo)
 - 科研技能目录.md (Chinese translations of skill descriptions, same structure)
 - audit_results.json (audit results: research_relevance, reason, quality)
 - Final_Research_Skills_Thematic_Split/0*.md (7-col tables: Why Research-Related col4)
 - dedup_results.json (optional: Phase 1 dedup labels - canonical/fork_copy/variant/original)
 - multidim_audit.json (optional: Phase 2 multi-dimensional audit - tier/stages/domain/value/doc)
[OUT] Outputs:
 - relevance_review.html (self-contained interactive review page with multi-dimensional audit)
[POS] Position in the system:
 - One-time build script. Reads six data sources, merges by (skill_name, repo),
   and generates a single-file HTML page for interactive relevance judgment.
   Re-run after data source updates to regenerate. Gracefully handles missing
   dedup/multidim files (falls back to original behavior).

 Change warning: once you modify this file's logic, you must update this comment block,
 and check/update the module doc (README/CLAUDE) in the containing folder; update the root
 global map if necessary.
"""

import json
import os
import re
import sys
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
CATALOG_EN = BASE / "SKILL_CATALOG.md"
CATALOG_ZH = BASE / "科研技能目录.md"
AUDIT_FILE = BASE / "audit_results.json"
DEDUP_FILE = BASE / "dedup_results.json"
MULTIDIM_FILE = BASE / "multidim_audit.json"
THEME_DIR = BASE / "Final_Research_Skills_Thematic_Split"
OUTPUT = BASE / "relevance_review.html"

THEME_NAMES = {
    "01": "信息检索与证据收集",
    "02": "文献综述、写作与引用",
    "03": "实验、基准测试与可复现性验证",
    "04": "数据分析与证据解读",
    "05": "科研运营与工作流支持",
    "06": "其他科学技能",
}

# Map theme file stems to theme keys
THEME_FILE_MAP = {
    "01_information_retrieval_evidence_collection": "01",
    "02_literature_review_writing_citation_part1": "02",
    "02_literature_review_writing_citation_part2": "02",
    "03_experiment_benchmark_reproducibility_validation_part1": "03",
    "03_experiment_benchmark_reproducibility_validation_part2": "03",
    "04_data_analysis_and_evidence_interpretation": "04",
    "05_research_operations_and_workflow_support": "05",
    "06_Additional_Scientific_Skills": "06",
}


# ---------------------------------------------------------------------------
# 1) Parse SKILL_CATALOG.md / 科研技能目录.md
# ---------------------------------------------------------------------------

def parse_catalog(filepath):
    """Parse a catalog markdown file (EN or ZH).
    Returns: list of dicts {theme, repo, skill_name, description, url}
    """
    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")

    current_theme = ""
    current_repo = ""
    entries = []

    for line in lines:
        stripped = line.strip()

        # Detect ## theme headers like "## 01 信息检索..."
        m = re.match(r"^## (\d{2})\s", stripped)
        if m:
            current_theme = m.group(1)
            continue

        # Detect ### repo headers
        if stripped.startswith("### ") and not stripped.startswith("### Notes"):
            current_repo = stripped[4:].strip()
            continue

        # Skip table headers and separators
        if (stripped.startswith("| Skill")
            or stripped.startswith("| 技能名称")
            or stripped.startswith("|---")
            or stripped.startswith("| #")):
            continue

        # Parse table data rows
        if stripped.startswith("|") and current_repo:
            cols = stripped.split("|")
            # cols[0] is empty (before first |)
            if len(cols) >= 4:
                skill_name = cols[1].strip()
                description = cols[2].strip()
                url_cell = cols[3].strip() if len(cols) > 3 else ""
                url = extract_url(url_cell)
                if skill_name:
                    entries.append({
                        "theme": current_theme,
                        "repo": current_repo,
                        "skill_name": skill_name,
                        "description": description,
                        "url": url,
                    })

    return entries


def extract_url(cell):
    """Extract URL from markdown link or bare URL in a table cell."""
    m = re.search(r"\[.*?\]\((https?://[^)]+)\)", cell)
    if m:
        return m.group(1)
    m = re.search(r"(https?://\S+)", cell)
    if m:
        return m.group(1)
    return ""


# ---------------------------------------------------------------------------
# 2) Parse audit_results.json
# ---------------------------------------------------------------------------

def load_audit_results():
    """Load audit results and index by (skill_name, repo).
    Returns: dict of (skill_name, repo) -> audit record
    """
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    index = {}
    for r in data["results"]:
        key = (r["skill_name"], r["repo"])
        index[key] = {
            "relevance": r.get("research_relevance", "unknown"),
            "relevance_reason": r.get("research_relevance_reason", ""),
            "quality": r.get("overall_quality", 0),
            "function_accuracy": r.get("function_accuracy", ""),
            "function_accuracy_reason": r.get("function_accuracy_reason", ""),
        }
    return index


# ---------------------------------------------------------------------------
# 2b) Load dedup_results.json (optional)
# ---------------------------------------------------------------------------

def load_dedup_results():
    """Load dedup results and index by (skill_name, repo).
    Returns: dict of (skill_name, repo) -> dedup record, or empty dict if file missing.
    """
    if not DEDUP_FILE.exists():
        return {}
    try:
        with open(DEDUP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        index = {}
        for r in data["results"]:
            key = (r["skill_name"], r["repo"])
            index[key] = {
                "uniqueness": r.get("uniqueness", "unknown"),
                "duplicate_group": r.get("duplicate_group"),
                "duplicate_count": r.get("duplicate_count", 1),
                "canonical_repo": r.get("canonical_repo"),
                "similarity": r.get("similarity"),
            }
        return index
    except Exception as e:
        print(f"  WARNING: Could not load dedup_results.json: {e}")
        return {}


# ---------------------------------------------------------------------------
# 2c) Load multidim_audit.json (optional)
# ---------------------------------------------------------------------------

def load_multidim_results():
    """Load multi-dimensional audit results and index by (skill_name, repo).
    Returns: dict of (skill_name, repo) -> multidim record, or empty dict if file missing.
    """
    if not MULTIDIM_FILE.exists():
        return {}
    try:
        with open(MULTIDIM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        index = {}
        for r in data["results"]:
            key = (r["skill_name"], r["repo"])
            index[key] = {
                "research_tier": r.get("research_tier", ""),
                "research_tier_reason": r.get("research_tier_reason", ""),
                "research_stages": r.get("research_stages", []),
                "domain": r.get("domain", ""),
                "added_value": r.get("added_value", ""),
                "added_value_reason": r.get("added_value_reason", ""),
                "doc_completeness": r.get("doc_completeness", {}),
                "inherited_from": r.get("inherited_from"),
            }
        return index
    except Exception as e:
        print(f"  WARNING: Could not load multidim_audit.json: {e}")
        return {}


# ---------------------------------------------------------------------------
# 3) Parse theme files for "Why Research-Related" (col4)
# ---------------------------------------------------------------------------

def split_row_by_unescaped_pipes(row_line):
    """Split table row respecting escaped pipes."""
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


def load_theme_why_related():
    """Parse all theme files for Why Research-Related field.
    Returns: dict of (theme_key, skill_name_lower) -> why_research_related
    """
    index = {}
    exclude_keywords = ["AUDIT", "CONSISTENCY", "RELEVANCE", "BACKUP", "README"]

    for filepath in sorted(THEME_DIR.glob("0*.md")):
        basename = filepath.name.upper()
        if any(kw in basename for kw in exclude_keywords):
            continue

        stem = filepath.stem
        theme_key = THEME_FILE_MAP.get(stem, stem[:2])

        text = filepath.read_text(encoding="utf-8", errors="replace")
        for line in text.split("\n"):
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue
            if "---" in stripped and re.match(r"^\|[\s\-|]+\|$", stripped):
                continue
            if stripped.startswith("| Skill"):
                continue

            parts = split_row_by_unescaped_pipes(stripped)
            # Remove leading/trailing empty parts from |...|
            if parts and not parts[0].strip():
                parts = parts[1:]
            if parts and not parts[-1].strip():
                parts = parts[:-1]

            if len(parts) >= 4:
                skill_name = parts[0].strip().strip("`").lower()
                why_related = parts[3].strip() if len(parts) > 3 else ""
                if skill_name and why_related:
                    index[(theme_key, skill_name)] = why_related

    return index


# ---------------------------------------------------------------------------
# 4) Merge all data sources
# ---------------------------------------------------------------------------

def build_data():
    """Assemble unified JSON data from all sources."""
    print("Reading SKILL_CATALOG.md...")
    catalog_en = parse_catalog(CATALOG_EN)
    print(f"  {len(catalog_en)} English entries")

    print("Reading 科研技能目录.md...")
    catalog_zh = parse_catalog(CATALOG_ZH)
    print(f"  {len(catalog_zh)} Chinese entries")

    print("Reading audit_results.json...")
    audit_index = load_audit_results()
    print(f"  {len(audit_index)} audit records")

    print("Reading theme files for Why Research-Related...")
    why_index = load_theme_why_related()
    print(f"  {len(why_index)} Why Research-Related entries")

    print("Reading dedup_results.json...")
    dedup_index = load_dedup_results()
    print(f"  {len(dedup_index)} dedup records")

    print("Reading multidim_audit.json...")
    multidim_index = load_multidim_results()
    print(f"  {len(multidim_index)} multidim records")

    # Build Chinese description lookup: (theme, repo, skill_name) -> desc_zh
    zh_lookup = {}
    for entry in catalog_zh:
        key = (entry["theme"], entry["repo"], entry["skill_name"])
        zh_lookup[key] = entry["description"]

    # Build unified skill list from English catalog (primary)
    skills = []
    stats = {"matched_audit": 0, "matched_zh": 0, "matched_why": 0,
             "matched_dedup": 0, "matched_multidim": 0}

    for entry in catalog_en:
        skill_name = entry["skill_name"]
        repo = entry["repo"]
        theme = entry["theme"]

        # Lookup Chinese description
        zh_key = (theme, repo, skill_name)
        desc_zh = zh_lookup.get(zh_key, "")
        if desc_zh:
            stats["matched_zh"] += 1

        # Lookup audit result
        audit_key = (skill_name, repo)
        audit = audit_index.get(audit_key, {})
        if audit:
            stats["matched_audit"] += 1

        # Lookup Why Research-Related
        why_key = (theme, skill_name.lower())
        why_related = why_index.get(why_key, "")
        if why_related:
            stats["matched_why"] += 1

        # Lookup dedup result
        dedup = dedup_index.get(audit_key, {})
        if dedup:
            stats["matched_dedup"] += 1

        # Lookup multidim result
        multidim = multidim_index.get(audit_key, {})
        if multidim:
            stats["matched_multidim"] += 1

        sid = f"{skill_name}__{repo}"
        skill_data = {
            "id": sid,
            "skill_name": skill_name,
            "repo": repo,
            "theme": theme,
            "theme_name": THEME_NAMES.get(theme, f"Theme {theme}"),
            "description_en": entry["description"],
            "description_zh": desc_zh,
            "url": entry["url"],
            "relevance": audit.get("relevance", "unknown"),
            "relevance_reason": audit.get("relevance_reason", ""),
            "quality": audit.get("quality", 0),
            "why_research_related": why_related,
            # Dedup fields
            "uniqueness": dedup.get("uniqueness", ""),
            "duplicate_count": dedup.get("duplicate_count", 1),
            "canonical_repo": dedup.get("canonical_repo", ""),
            "similarity": dedup.get("similarity"),
            # Multidim audit fields
            "research_tier": multidim.get("research_tier", ""),
            "research_tier_reason": multidim.get("research_tier_reason", ""),
            "research_stages": multidim.get("research_stages", []),
            "domain": multidim.get("domain", ""),
            "added_value": multidim.get("added_value", ""),
            "added_value_reason": multidim.get("added_value_reason", ""),
            "doc_completeness": multidim.get("doc_completeness", {}),
        }
        skills.append(skill_data)

    # Compute tier distribution for stats
    from collections import Counter
    tier_dist = Counter(s["research_tier"] for s in skills if s["research_tier"])
    uniq_dist = Counter(s["uniqueness"] for s in skills if s["uniqueness"])

    print(f"\nMerge stats:")
    print(f"  Total skills: {len(skills)}")
    print(f"  Matched audit: {stats['matched_audit']}")
    print(f"  Matched Chinese: {stats['matched_zh']}")
    print(f"  Matched Why-Related: {stats['matched_why']}")
    print(f"  Matched dedup: {stats['matched_dedup']}")
    print(f"  Matched multidim: {stats['matched_multidim']}")
    if tier_dist:
        print(f"  Tier distribution: {dict(sorted(tier_dist.items()))}")
    if uniq_dist:
        print(f"  Uniqueness distribution: {dict(sorted(uniq_dist.items()))}")

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "total": len(skills),
        "tier_dist": dict(sorted(tier_dist.items())) if tier_dist else {},
        "uniq_dist": dict(sorted(uniq_dist.items())) if uniq_dist else {},
        "skills": skills,
    }


# ---------------------------------------------------------------------------
# 5) HTML Template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>科研技能多维度审计 - Multi-dimensional Skill Audit</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --sidebar-w: 300px;
  --bg: #f8fafc; --sidebar-bg: #1e293b; --sidebar-text: #e2e8f0;
  --card-bg: #fff; --border: #e2e8f0;
  --green: #22c55e; --amber: #f59e0b; --red: #ef4444; --blue: #3b82f6; --purple: #8b5cf6;
  --green-bg: #dcfce7; --amber-bg: #fef3c7; --red-bg: #fef2f2; --purple-bg: #ede9fe;
  --tier-a: #059669; --tier-b: #2563eb; --tier-c: #d97706; --tier-d: #6b7280;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans SC', sans-serif;
  background: var(--bg); color: #1e293b;
  display: grid; grid-template-columns: var(--sidebar-w) 1fr;
  height: 100vh; overflow: hidden;
}

/* --- Sidebar --- */
.sidebar { background: var(--sidebar-bg); color: var(--sidebar-text); display: flex; flex-direction: column; overflow: hidden; }
.sidebar-header { padding: 16px 14px 12px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.sidebar-header h1 { font-size: 14px; font-weight: 700; margin-bottom: 8px; }
.progress-bar { background: rgba(255,255,255,0.1); border-radius: 4px; height: 6px; overflow: hidden; }
.progress-fill { height: 100%; background: var(--green); transition: width 0.3s; border-radius: 4px; }
.progress-text { font-size: 11px; color: #94a3b8; margin-top: 6px; line-height: 1.4; }
.stats-bar { font-size: 10px; color: #64748b; margin-top: 6px; line-height: 1.5; }
.stats-bar .tier-badge { display: inline-block; padding: 0 5px; border-radius: 3px; color: #fff; font-weight: 700; margin: 0 1px; font-size: 9px; }
.tier-a-bg { background: var(--tier-a); }
.tier-b-bg { background: var(--tier-b); }
.tier-c-bg { background: var(--tier-c); }
.tier-d-bg { background: var(--tier-d); }
.sidebar-filters { padding: 8px 14px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.sidebar-filters input {
  width: 100%; padding: 6px 10px; border: 1px solid rgba(255,255,255,0.2);
  border-radius: 4px; background: rgba(255,255,255,0.08); color: #e2e8f0;
  font-size: 12px; outline: none;
}
.sidebar-filters input::placeholder { color: #64748b; }
.sidebar-filters input:focus { border-color: var(--blue); }
.filter-chips { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 8px; }
.filter-chip {
  font-size: 10px; padding: 2px 8px; border-radius: 12px; cursor: pointer;
  border: 1px solid rgba(255,255,255,0.2); color: #94a3b8; transition: all 0.15s;
  user-select: none;
}
.filter-chip:hover { border-color: rgba(255,255,255,0.4); color: #e2e8f0; }
.filter-chip.active { background: var(--blue); border-color: var(--blue); color: #fff; }
.filter-chip.tier-a { border-color: var(--tier-a); color: var(--tier-a); }
.filter-chip.tier-a.active { background: var(--tier-a); color: #fff; }
.filter-chip.tier-b { border-color: var(--tier-b); color: var(--tier-b); }
.filter-chip.tier-b.active { background: var(--tier-b); color: #fff; }
.filter-chip.tier-c { border-color: var(--tier-c); color: var(--tier-c); }
.filter-chip.tier-c.active { background: var(--tier-c); color: #fff; }
.filter-chip.tier-d { border-color: var(--tier-d); color: var(--tier-d); }
.filter-chip.tier-d.active { background: var(--tier-d); color: #fff; }
.filter-section-label { font-size: 9px; color: #475569; text-transform: uppercase; margin-top: 6px; margin-bottom: 2px; letter-spacing: 0.05em; }
.sidebar-list { flex: 1; overflow-y: auto; padding: 4px 0; }
.sidebar-group { margin-bottom: 2px; }
.sidebar-group-label {
  font-size: 10px; font-weight: 700; text-transform: uppercase; color: #64748b;
  padding: 8px 14px 3px; letter-spacing: 0.04em; cursor: pointer; user-select: none;
  display: flex; align-items: center; gap: 4px;
}
.sidebar-group-label .chevron { transition: transform 0.2s; font-size: 8px; }
.sidebar-group-label .chevron.collapsed { transform: rotate(-90deg); }
.sidebar-group-items { overflow: hidden; }
.sidebar-group-items.collapsed { display: none; }
.sidebar-item {
  padding: 5px 14px 5px 22px; cursor: pointer; font-size: 12px;
  border-left: 3px solid transparent; transition: all 0.12s;
  display: flex; align-items: center; gap: 6px;
  white-space: nowrap; overflow: hidden;
}
.sidebar-item:hover { background: rgba(255,255,255,0.05); }
.sidebar-item.active { background: rgba(59,130,246,0.15); border-left-color: var(--blue); color: #fff; }
.sidebar-item.fork-copy { opacity: 0.45; }
.sidebar-item .dot {
  width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;
}
.dot-valid { background: var(--green); }
.dot-weak { background: var(--amber); }
.dot-invalid { background: var(--red); }
.dot-unknown { background: #64748b; }
.sidebar-item .sname { overflow: hidden; text-overflow: ellipsis; flex: 1; }
.sidebar-item .tier-mini { font-size: 9px; font-weight: 700; padding: 0 3px; border-radius: 2px; flex-shrink: 0; color: #fff; }
.sidebar-item .dup-mark { font-size: 9px; color: #64748b; flex-shrink: 0; }
.sidebar-item .review-mark { margin-left: auto; font-size: 12px; flex-shrink: 0; }
.sidebar-link { color: #64748b; text-decoration: none; font-size: 11px; flex-shrink: 0; opacity: 0; transition: opacity 0.15s; padding: 0 2px; }
.sidebar-item:hover .sidebar-link { opacity: 1; }
.sidebar-link:hover { color: var(--blue); }
.sidebar-actions { padding: 10px 14px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; gap: 6px; }
.sidebar-actions button {
  flex: 1; padding: 7px; border: none; border-radius: 5px; cursor: pointer;
  font-size: 11px; font-weight: 600; transition: opacity 0.15s;
}
.sidebar-actions button:hover { opacity: 0.85; }
.btn-export { background: var(--blue); color: #fff; }
.btn-clear { background: #334155; color: #94a3b8; }

/* --- Main --- */
.main { display: flex; flex-direction: column; overflow: hidden; }
.main-header {
  padding: 14px 20px; border-bottom: 1px solid var(--border);
  background: var(--card-bg); display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
}
.main-header h2 { font-size: 17px; font-weight: 700; }
.main-header h2 a { color: inherit; text-decoration: none; border-bottom: 1px dashed #94a3b8; }
.main-header h2 a:hover { color: var(--blue); border-bottom-color: var(--blue); }
.tag { font-size: 11px; padding: 2px 8px; border-radius: 4px; background: #f1f5f9; color: #475569; }
.tag-link { text-decoration: none; color: var(--blue); }
.tag-link:hover { text-decoration: underline; }
.relevance-tag { font-weight: 700; color: #fff; }
.relevance-tag.valid { background: var(--green); }
.relevance-tag.weak { background: var(--amber); }
.relevance-tag.invalid { background: var(--red); }
.relevance-tag.unknown { background: #64748b; }
.tier-tag { font-weight: 700; color: #fff; }
.tier-tag.tier-A { background: var(--tier-a); }
.tier-tag.tier-B { background: var(--tier-b); }
.tier-tag.tier-C { background: var(--tier-c); }
.tier-tag.tier-D { background: var(--tier-d); }
.dup-tag { font-weight: 600; }
.dup-tag.fork_copy { background: #fee2e2; color: #991b1b; }
.dup-tag.variant { background: var(--amber-bg); color: #92400e; }
.dup-tag.canonical { background: var(--green-bg); color: #166534; }
.dup-tag.original { background: #f1f5f9; color: #475569; }
.main-content { flex: 1; overflow-y: auto; padding: 16px 20px; display: flex; flex-direction: column; gap: 14px; }

/* --- Panels --- */
.panel { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
.panel-title {
  font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em;
  color: #64748b; padding: 8px 14px; background: #f8fafc; border-bottom: 1px solid var(--border);
}
.panel-body { padding: 12px 14px; font-size: 13px; line-height: 1.65; color: #334155; }
.panel-body.reason { white-space: pre-wrap; word-break: break-word; }

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
.info-grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0; }
.info-field { padding: 10px 14px; border-bottom: 1px solid var(--border); }
.info-field:not(:last-child) { border-right: 1px solid var(--border); }
.info-grid .info-field:nth-child(odd) { border-right: 1px solid var(--border); }
.info-grid .info-field:nth-child(even) { border-right: none; }
.info-field.full { grid-column: 1 / -1; border-right: none; }
.info-label { font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 3px; }
.info-value { font-size: 13px; line-height: 1.5; color: #334155; }
.stage-tag { display: inline-block; font-size: 10px; padding: 1px 6px; margin: 2px 2px; border-radius: 3px; background: #e0f2fe; color: #0369a1; }
.value-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 11px; }
.value-high { background: #dcfce7; color: #166534; }
.value-medium { background: #fef3c7; color: #92400e; }
.value-low { background: #f1f5f9; color: #64748b; }
.value-negligible { background: #fee2e2; color: #991b1b; }
.doc-check { display: inline-block; margin-right: 12px; font-size: 12px; }
.doc-check .yes { color: var(--green); }
.doc-check .no { color: #cbd5e1; }

/* --- Action Bar --- */
.action-bar {
  padding: 12px 14px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
}
.action-bar button {
  padding: 8px 18px; border: 2px solid transparent; border-radius: 6px;
  font-size: 13px; font-weight: 700; cursor: pointer; transition: all 0.15s;
}
.action-bar button:hover { transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.action-bar button.selected { box-shadow: 0 0 0 3px rgba(59,130,246,0.3); transform: translateY(-1px); }
.btn-relevant { background: var(--green-bg); color: #166534; border-color: var(--green); }
.btn-weak-rel { background: var(--amber-bg); color: #92400e; border-color: var(--amber); }
.btn-irrelevant { background: var(--red-bg); color: #991b1b; border-color: var(--red); }
.action-hint { font-size: 11px; color: #94a3b8; margin-left: auto; }
.kbd { display: inline-block; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 3px; padding: 0 5px; font-size: 10px; font-family: monospace; margin: 0 1px; }

/* Empty state */
.empty-state { display: flex; align-items: center; justify-content: center; height: 100%; color: #94a3b8; font-size: 14px; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
.sidebar ::-webkit-scrollbar-thumb { background: #475569; }
</style>
</head>
<body>

<div class="sidebar">
  <div class="sidebar-header">
    <h1>科研技能多维度审计</h1>
    <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
    <div class="progress-text" id="progressText">0 / 0 已判定</div>
    <div class="stats-bar" id="statsBar"></div>
  </div>
  <div class="sidebar-filters">
    <input type="text" id="searchBox" placeholder="搜索技能名称、仓库或领域..." />
    <div class="filter-chips" id="filterChips"></div>
    <div class="filter-section-label">研究层级</div>
    <div class="filter-chips" id="tierChips"></div>
    <div class="filter-section-label">去重状态</div>
    <div class="filter-chips" id="dedupChips"></div>
  </div>
  <div class="sidebar-list" id="sidebarList"></div>
  <div class="sidebar-actions">
    <button class="btn-export" onclick="exportJSON()">导出 JSON</button>
    <button class="btn-clear" onclick="clearAll()">清除判定</button>
  </div>
</div>

<div class="main">
  <div class="main-header" id="mainHeader">
    <h2 id="headerTitle">选择一个技能开始审查</h2>
  </div>
  <div class="main-content" id="mainContent">
    <div class="empty-state">点击左侧技能列表开始审查</div>
  </div>
</div>

<script>
// ==== Embedded Data ====
const DATA = /*__DATA__*/;

// ==== State ====
const STATE = {
  skills: DATA.skills,
  filtered: [],
  currentIndex: -1,
  decisions: {},
  filter: "all",
  tierFilter: "",
  dedupFilter: "",
  search: "",
  collapsedGroups: {},
};

const LS_KEY = "relevance_review_v2";
const FILTERS = [
  { key: "all", label: "全部" },
  { key: "pending", label: "待审查" },
  { key: "weak", label: "弱相关" },
  { key: "unknown", label: "未审计" },
  { key: "decided", label: "已判定" },
  { key: "invalid", label: "不相关" },
];
const TIER_FILTERS = [
  { key: "", label: "全部层级" },
  { key: "A", label: "A 核心", cls: "tier-a" },
  { key: "B", label: "B 基础设施", cls: "tier-b" },
  { key: "C", label: "C 生产力", cls: "tier-c" },
  { key: "D", label: "D 间接", cls: "tier-d" },
];
const DEDUP_FILTERS = [
  { key: "", label: "全部" },
  { key: "original", label: "原创" },
  { key: "canonical", label: "规范版" },
  { key: "variant", label: "变体" },
  { key: "fork_copy", label: "副本" },
];
const TIER_COLORS = { A: "var(--tier-a)", B: "var(--tier-b)", C: "var(--tier-c)", D: "var(--tier-d)" };
const TIER_LABELS = { A: "核心科研", B: "科研基础设施", C: "科研生产力", D: "间接相关" };

// ==== Persistence ====
function loadState() {
  try {
    const saved = localStorage.getItem(LS_KEY);
    if (saved) STATE.decisions = JSON.parse(saved);
  } catch(e) {}
}
function persistState() {
  try { localStorage.setItem(LS_KEY, JSON.stringify(STATE.decisions)); } catch(e) {}
}

// ==== Filtering ====
function applyFilter() {
  const q = STATE.search.toLowerCase();
  STATE.filtered = STATE.skills.filter(s => {
    // Text search (also search domain)
    if (q && !s.skill_name.toLowerCase().includes(q) && !s.repo.toLowerCase().includes(q)
        && !(s.domain || "").toLowerCase().includes(q)) return false;
    // Status filter
    const f = STATE.filter;
    if (f === "pending" && (STATE.decisions[s.id] || s.relevance === "unknown")) return false;
    if (f === "weak" && s.relevance !== "weak") return false;
    if (f === "unknown" && s.relevance !== "unknown") return false;
    if (f === "invalid" && s.relevance !== "invalid") return false;
    if (f === "decided" && !STATE.decisions[s.id]) return false;
    // Tier filter
    if (STATE.tierFilter && s.research_tier !== STATE.tierFilter) return false;
    // Dedup filter
    if (STATE.dedupFilter && s.uniqueness !== STATE.dedupFilter) return false;
    return true;
  });
}

// ==== Render Filter Chips ====
function renderFilters() {
  // Status filters
  const container = document.getElementById("filterChips");
  container.innerHTML = FILTERS.map(f =>
    `<span class="filter-chip${STATE.filter === f.key ? ' active' : ''}" data-filter="${f.key}">${f.label}</span>`
  ).join("");
  container.querySelectorAll(".filter-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      STATE.filter = chip.dataset.filter;
      applyFilter(); renderFilters(); renderSidebar();
    });
  });

  // Tier filters
  const tierContainer = document.getElementById("tierChips");
  tierContainer.innerHTML = TIER_FILTERS.map(f =>
    `<span class="filter-chip ${f.cls || ''}${STATE.tierFilter === f.key ? ' active' : ''}" data-tier="${f.key}">${f.label}</span>`
  ).join("");
  tierContainer.querySelectorAll(".filter-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      STATE.tierFilter = chip.dataset.tier;
      applyFilter(); renderFilters(); renderSidebar();
    });
  });

  // Dedup filters
  const dedupContainer = document.getElementById("dedupChips");
  dedupContainer.innerHTML = DEDUP_FILTERS.map(f =>
    `<span class="filter-chip${STATE.dedupFilter === f.key ? ' active' : ''}" data-dedup="${f.key}">${f.label}</span>`
  ).join("");
  dedupContainer.querySelectorAll(".filter-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      STATE.dedupFilter = chip.dataset.dedup;
      applyFilter(); renderFilters(); renderSidebar();
    });
  });
}

// ==== Render Stats Bar ====
function renderStatsBar() {
  const td = DATA.tier_dist || {};
  const ud = DATA.uniq_dist || {};
  const bar = document.getElementById("statsBar");
  let html = "";
  if (Object.keys(td).length) {
    html += "层级: ";
    for (const [t, n] of Object.entries(td)) {
      html += `<span class="tier-badge tier-${t.toLowerCase()}-bg">${t}:${n}</span> `;
    }
  }
  if (Object.keys(ud).length) {
    const fc = ud.fork_copy || 0;
    const orig = (ud.original || 0) + (ud.canonical || 0) + (ud.variant || 0);
    html += `| 独立:${orig} 副本:${fc}`;
  }
  bar.innerHTML = html;
}

// ==== Render Sidebar ====
function renderSidebar() {
  applyFilter();
  const list = document.getElementById("sidebarList");

  // Group by theme
  const groups = {};
  STATE.filtered.forEach((s, i) => {
    const key = s.theme;
    if (!groups[key]) groups[key] = { label: `${s.theme} ${s.theme_name}`, items: [] };
    groups[key].items.push({ skill: s, filteredIndex: i });
  });

  let html = "";
  for (const [themeKey, group] of Object.entries(groups)) {
    const collapsed = STATE.collapsedGroups[themeKey];
    html += `<div class="sidebar-group">`;
    html += `<div class="sidebar-group-label" data-theme="${themeKey}">
      <span class="chevron${collapsed ? ' collapsed' : ''}">&#9660;</span>
      ${esc(group.label)} (${group.items.length})
    </div>`;
    html += `<div class="sidebar-group-items${collapsed ? ' collapsed' : ''}">`;
    for (const { skill, filteredIndex } of group.items) {
      const decision = STATE.decisions[skill.id];
      let mark = "";
      if (decision) {
        if (decision.judgment === "relevant") mark = '<span style="color:#22c55e">&#10003;</span>';
        else if (decision.judgment === "weak") mark = '<span style="color:#f59e0b">~</span>';
        else mark = '<span style="color:#ef4444">&#10007;</span>';
      }
      const active = filteredIndex === STATE.currentIndex ? " active" : "";
      const dotCls = `dot-${skill.relevance}`;
      const isForkCopy = skill.uniqueness === "fork_copy";
      const forkClass = isForkCopy ? " fork-copy" : "";
      const dupMark = isForkCopy ? '<span class="dup-mark">[副]</span>' : "";
      const tierMini = skill.research_tier ? `<span class="tier-mini" style="background:${TIER_COLORS[skill.research_tier] || '#6b7280'}">${skill.research_tier}</span>` : "";
      const linkIcon = skill.url ? `<a class="sidebar-link" href="${esc(skill.url)}" target="_blank" title="GitHub" onclick="event.stopPropagation()">&#8599;</a>` : "";
      html += `<div class="sidebar-item${active}${forkClass}" data-idx="${filteredIndex}">
        <span class="dot ${dotCls}"></span>
        ${tierMini}
        <span class="sname">${esc(skill.skill_name)}</span>
        ${dupMark}
        ${linkIcon}
        <span class="review-mark">${mark}</span>
      </div>`;
    }
    html += `</div></div>`;
  }
  list.innerHTML = html;

  // Bind events
  list.querySelectorAll(".sidebar-group-label").forEach(label => {
    label.addEventListener("click", () => {
      const theme = label.dataset.theme;
      STATE.collapsedGroups[theme] = !STATE.collapsedGroups[theme];
      renderSidebar();
    });
  });
  list.querySelectorAll(".sidebar-item").forEach(item => {
    item.addEventListener("click", () => {
      selectSkill(parseInt(item.dataset.idx));
    });
  });

  updateProgress();
}

function updateProgress() {
  const total = STATE.skills.length;
  const decided = Object.keys(STATE.decisions).length;
  const relevant = Object.values(STATE.decisions).filter(d => d.judgment === "relevant").length;
  const weak = Object.values(STATE.decisions).filter(d => d.judgment === "weak").length;
  const irrelevant = Object.values(STATE.decisions).filter(d => d.judgment === "irrelevant").length;
  document.getElementById("progressFill").style.width = `${(decided/total)*100}%`;
  document.getElementById("progressText").textContent =
    `已判定 ${decided}/${total}（相关 ${relevant}，弱相关 ${weak}，不相关 ${irrelevant}）`;
}

// ==== Detail View ====
function selectSkill(filteredIndex) {
  STATE.currentIndex = filteredIndex;
  const skill = STATE.filtered[filteredIndex];
  if (!skill) return;
  renderDetail(skill);
  renderSidebar();
  setTimeout(() => {
    const active = document.querySelector(".sidebar-item.active");
    if (active) active.scrollIntoView({ block: "nearest" });
  }, 50);
}

function renderDetail(skill) {
  const header = document.getElementById("mainHeader");
  const relCls = skill.relevance;
  const relLabel = { valid: "相关", weak: "弱相关", invalid: "不相关", unknown: "未审计", partial: "部分" }[skill.relevance] || skill.relevance;
  const dupLabel = { fork_copy: "副本", variant: "变体", canonical: "规范版", original: "原创" }[skill.uniqueness] || "";
  const dupCls = skill.uniqueness || "";

  header.innerHTML = `
    <h2>${skill.url ? `<a href="${esc(skill.url)}" target="_blank">${esc(skill.skill_name)}</a>` : esc(skill.skill_name)}</h2>
    <span class="tag">${esc(skill.repo)}</span>
    <span class="tag">${esc(skill.theme)} ${esc(skill.theme_name)}</span>
    <span class="tag relevance-tag ${relCls}">${relLabel}</span>
    ${skill.research_tier ? `<span class="tag tier-tag tier-${skill.research_tier}">Tier ${skill.research_tier}</span>` : ""}
    ${dupLabel ? `<span class="tag dup-tag ${dupCls}">${dupLabel}</span>` : ""}
    ${skill.quality ? `<span class="tag">质量 ${skill.quality}/5</span>` : ""}
    ${skill.url ? `<a href="${esc(skill.url)}" target="_blank" class="tag tag-link">GitHub &rarr;</a>` : ""}
  `;

  const main = document.getElementById("mainContent");
  const decision = STATE.decisions[skill.id];

  // Build multidim panel if data exists
  let multidimPanel = "";
  if (skill.research_tier) {
    const dc = skill.doc_completeness || {};
    const stages = (skill.research_stages || []).map(s => `<span class="stage-tag">${esc(s)}</span>`).join(" ");
    const valCls = { high: "value-high", medium: "value-medium", low: "value-low", negligible: "value-negligible" }[skill.added_value] || "value-low";
    const valLabel = { high: "高", medium: "中", low: "低", negligible: "极低" }[skill.added_value] || skill.added_value;
    const ck = (v) => v ? '<span class="yes">&#10003;</span>' : '<span class="no">&#10007;</span>';
    const clarity = dc.instruction_clarity || 0;
    const clarityStars = "&#9733;".repeat(clarity) + "&#9734;".repeat(5 - clarity);

    multidimPanel = `
    <div class="panel">
      <div class="panel-title">多维度审计 (Multi-dimensional Audit)</div>
      <div class="info-grid">
        <div class="info-field">
          <div class="info-label">研究层级 (Research Tier)</div>
          <div class="info-value">
            <span class="tag tier-tag tier-${skill.research_tier}" style="font-size:13px">Tier ${skill.research_tier} - ${TIER_LABELS[skill.research_tier] || ""}</span>
          </div>
        </div>
        <div class="info-field">
          <div class="info-label">增量价值 (Added Value)</div>
          <div class="info-value"><span class="value-badge ${valCls}">${valLabel}</span></div>
        </div>
        <div class="info-field">
          <div class="info-label">学科领域 (Domain)</div>
          <div class="info-value">${esc(skill.domain) || '-'}</div>
        </div>
        <div class="info-field">
          <div class="info-label">研究阶段 (Stages)</div>
          <div class="info-value">${stages || '-'}</div>
        </div>
        <div class="info-field full">
          <div class="info-label">层级理由</div>
          <div class="info-value">${esc(skill.research_tier_reason) || '-'}</div>
        </div>
        <div class="info-field full">
          <div class="info-label">增量价值理由</div>
          <div class="info-value">${esc(skill.added_value_reason) || '-'}</div>
        </div>
        <div class="info-field full">
          <div class="info-label">文档完整性</div>
          <div class="info-value">
            <span class="doc-check">${ck(dc.has_when_to_use)} 使用场景</span>
            <span class="doc-check">${ck(dc.has_prerequisites)} 前置条件</span>
            <span class="doc-check">${ck(dc.has_examples)} 示例</span>
            <span class="doc-check">清晰度: ${clarityStars}</span>
          </div>
        </div>
      </div>
    </div>`;
  }

  // Build dedup panel if applicable
  let dedupPanel = "";
  if (skill.uniqueness === "fork_copy" || skill.uniqueness === "variant") {
    dedupPanel = `
    <div class="panel">
      <div class="panel-title">去重信息 (Deduplication)</div>
      <div class="info-grid">
        <div class="info-field">
          <div class="info-label">去重状态</div>
          <div class="info-value"><span class="tag dup-tag ${skill.uniqueness}">${{fork_copy:"副本 (Fork Copy)",variant:"变体 (Variant)"}[skill.uniqueness]}</span></div>
        </div>
        <div class="info-field">
          <div class="info-label">相似度</div>
          <div class="info-value">${skill.similarity != null ? (skill.similarity * 100).toFixed(1) + '%' : '-'}</div>
        </div>
        <div class="info-field full">
          <div class="info-label">规范版本仓库</div>
          <div class="info-value">${esc(skill.canonical_repo) || '-'}</div>
        </div>
      </div>
    </div>`;
  } else if (skill.uniqueness === "canonical" && skill.duplicate_count > 1) {
    dedupPanel = `
    <div class="panel">
      <div class="panel-title">去重信息 (Deduplication)</div>
      <div class="panel-body">此技能是 <strong>${skill.duplicate_count}</strong> 个同名技能中的<span class="tag dup-tag canonical">规范版本</span></div>
    </div>`;
  }

  main.innerHTML = `
    <!-- Description -->
    <div class="panel">
      <div class="panel-title">功能描述</div>
      <div class="info-grid">
        <div class="info-field full">
          <div class="info-label">功能描述（中文）</div>
          <div class="info-value">${esc(skill.description_zh) || '<span style="color:#94a3b8">无中文描述</span>'}</div>
        </div>
        <div class="info-field full">
          <div class="info-label">Function Description (English)</div>
          <div class="info-value">${esc(skill.description_en) || '<span style="color:#94a3b8">No description</span>'}</div>
        </div>
      </div>
    </div>

    ${multidimPanel}

    ${dedupPanel}

    <!-- Audit Judgment Reason -->
    <div class="panel">
      <div class="panel-title">审计判定理由（完整文本）</div>
      <div class="panel-body reason">${esc(skill.relevance_reason) || '<span style="color:#94a3b8">无审计记录</span>'}</div>
    </div>

    <!-- Why Research-Related -->
    ${skill.why_research_related ? `
    <div class="panel">
      <div class="panel-title">为什么与研究相关（Why Research-Related）</div>
      <div class="panel-body">${esc(skill.why_research_related)}</div>
    </div>
    ` : ""}

    <!-- Action Bar -->
    <div class="panel">
      <div class="panel-title">您的判定</div>
      <div class="action-bar">
        <button class="btn-relevant${decision?.judgment === 'relevant' ? ' selected' : ''}" onclick="decide('relevant')">&#10004; 相关</button>
        <button class="btn-weak-rel${decision?.judgment === 'weak' ? ' selected' : ''}" onclick="decide('weak')">&#9888; 弱相关</button>
        <button class="btn-irrelevant${decision?.judgment === 'irrelevant' ? ' selected' : ''}" onclick="decide('irrelevant')">&#10006; 不相关</button>
        <span class="action-hint">
          <span class="kbd">&larr;</span><span class="kbd">&rarr;</span> 导航
          <span class="kbd">1</span> 相关
          <span class="kbd">2</span> 弱相关
          <span class="kbd">3</span> 不相关
          ${decision ? `<br>当前: <strong>${{relevant:'相关',weak:'弱相关',irrelevant:'不相关'}[decision.judgment]}</strong>` : ""}
        </span>
      </div>
    </div>
  `;
}

// ==== Actions ====
function decide(judgment) {
  const skill = STATE.filtered[STATE.currentIndex];
  if (!skill) return;
  STATE.decisions[skill.id] = {
    judgment,
    skill_name: skill.skill_name,
    repo: skill.repo,
    theme: skill.theme,
    original_relevance: skill.relevance,
    research_tier: skill.research_tier || "",
    decided_at: new Date().toISOString(),
  };
  persistState();

  let nextIdx = -1;
  for (let i = STATE.currentIndex + 1; i < STATE.filtered.length; i++) {
    if (!STATE.decisions[STATE.filtered[i].id]) { nextIdx = i; break; }
  }
  if (nextIdx === -1) {
    for (let i = 0; i < STATE.currentIndex; i++) {
      if (!STATE.decisions[STATE.filtered[i].id]) { nextIdx = i; break; }
    }
  }

  if (nextIdx !== -1) {
    selectSkill(nextIdx);
  } else {
    renderSidebar();
    renderDetail(skill);
  }
}

function clearAll() {
  if (!confirm("确定要清除所有判定结果吗？")) return;
  STATE.decisions = {};
  persistState();
  renderSidebar();
  if (STATE.currentIndex >= 0 && STATE.filtered[STATE.currentIndex]) {
    renderDetail(STATE.filtered[STATE.currentIndex]);
  }
}

function exportJSON() {
  const decisions = Object.values(STATE.decisions).map(d => ({
    skill_name: d.skill_name,
    repo: d.repo,
    theme: d.theme,
    judgment: d.judgment,
    original_relevance: d.original_relevance,
    research_tier: d.research_tier || "",
    decided_at: d.decided_at,
  }));
  const data = {
    exported_at: new Date().toISOString(),
    total_skills: STATE.skills.length,
    total_decided: decisions.length,
    summary: {
      relevant: decisions.filter(d => d.judgment === "relevant").length,
      weak: decisions.filter(d => d.judgment === "weak").length,
      irrelevant: decisions.filter(d => d.judgment === "irrelevant").length,
    },
    decisions,
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `relevance_decisions_${new Date().toISOString().slice(0,10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

// ==== Keyboard ====
document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT") return;
  if (e.key === "ArrowLeft" && STATE.currentIndex > 0) selectSkill(STATE.currentIndex - 1);
  if (e.key === "ArrowRight" && STATE.currentIndex < STATE.filtered.length - 1) selectSkill(STATE.currentIndex + 1);
  if (e.key === "1") decide("relevant");
  if (e.key === "2") decide("weak");
  if (e.key === "3") decide("irrelevant");
});

// ==== Search ====
document.getElementById("searchBox").addEventListener("input", (e) => {
  STATE.search = e.target.value;
  STATE.currentIndex = -1;
  renderSidebar();
});

// ==== Utility ====
function esc(s) {
  if (!s) return "";
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

// ==== Init ====
loadState();
renderFilters();
renderStatsBar();
renderSidebar();
if (STATE.filtered.length > 0) selectSkill(0);
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# 6) Generate
# ---------------------------------------------------------------------------

def main():
    print("=== Building Relevance Review Page ===\n")

    # Verify inputs exist
    for f in [CATALOG_EN, CATALOG_ZH, AUDIT_FILE]:
        if not f.exists():
            print(f"ERROR: Required file not found: {f}")
            sys.exit(1)

    # Build data
    data = build_data()

    # Generate HTML
    data_json = json.dumps(data, ensure_ascii=False, indent=None)
    html = HTML_TEMPLATE.replace("/*__DATA__*/", data_json)
    OUTPUT.write_text(html, encoding="utf-8")

    print(f"\nGenerated: {OUTPUT}")
    print(f"Total skills embedded: {data['total']}")
    print(f"Open in browser to review.")


if __name__ == "__main__":
    main()

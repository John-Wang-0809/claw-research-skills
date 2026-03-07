#!/usr/bin/env python3
"""
Build an interactive audit review HTML page for the 22 remaining skills.

Reads from:
  - remaining_issues_for_review.md (22 skills with audit reasons)
  - Final_Research_Skills_Thematic_Split/*.md (7-column table rows)
  - SKILL.md files (ground truth content)

Outputs:
  - audit_review.html (self-contained single-page app)
"""

import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
ISSUES_FILE = BASE / "remaining_issues_for_review.md"
THEME_DIR = BASE / "Final_Research_Skills_Thematic_Split"
OUTPUT = BASE / "audit_review.html"


# ---------------------------------------------------------------------------
# 1) Parse remaining_issues_for_review.md
# ---------------------------------------------------------------------------

def parse_issues():
    text = ISSUES_FILE.read_text(encoding="utf-8", errors="replace")
    entries = []

    # Determine status by position relative to section headers
    section_positions = []
    for m in re.finditer(r"^## (INACCURATE|PARTIAL|CANNOT_VERIFY)", text, re.MULTILINE):
        section_positions.append((m.start(), m.group(1)))

    # Find all skill entry positions
    entry_pattern = re.compile(r"^### \d+\.\s+", re.MULTILINE)
    entry_starts = [(m.start(), m.end()) for m in entry_pattern.finditer(text)]

    for i, (start, content_start) in enumerate(entry_starts):
        end = entry_starts[i + 1][0] if i + 1 < len(entry_starts) else len(text)
        block = text[content_start:end].strip()
        lines = block.split("\n")
        header = lines[0]
        m = re.match(r"`([^`]+)`\s*(?:--|-)\s*(.+)", header)
        if not m:
            continue
        skill_name = m.group(1).strip()
        repo = m.group(2).strip()

        # Determine status from which section this entry falls under
        status = "UNKNOWN"
        for pos, stype in section_positions:
            if start > pos:
                status = stype

        entry = {"skill_name": skill_name, "repo": repo, "status": status}
        full = "\n".join(lines[1:])

        for field, key in [
            ("Theme", "theme"),
            ("Audit Reason", "audit_reason"),
            ("Skill URL", "skill_url"),
            ("SKILL.md", "skill_md_path"),
            ("Reason", "audit_reason"),  # CANNOT_VERIFY uses "Reason"
        ]:
            pattern = rf"^\- \*\*{re.escape(field)}\*\*:\s*(.+)"
            match = re.search(pattern, full, re.MULTILINE)
            if match:
                val = match.group(1).strip()
                if key == "skill_md_path":
                    val = val.strip("`")
                if key not in entry:
                    entry[key] = val


        entries.append(entry)

    print(f"Parsed {len(entries)} skills from issues file")
    return entries


# ---------------------------------------------------------------------------
# 2) Table row parsing (from apply_audit_corrections_to_theme.py)
# ---------------------------------------------------------------------------

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


def parse_row(row_line):
    result = {
        "skill": "", "evidence_file": "", "skill_url_cell": "",
        "why_research_related": "", "function_explanation": "",
        "execution_flow": "", "evidence": "",
    }
    parts = split_row_by_unescaped_pipes(row_line)
    if parts and row_line.lstrip().startswith("|") and not parts[0].strip():
        parts = parts[1:]
    if parts and row_line.rstrip().endswith("|") and not parts[-1].strip():
        parts = parts[:-1]
    if len(parts) < 7:
        return result
    if len(parts) > 7:
        parts = parts[:6] + ["|".join(parts[6:])]
    result["skill"] = parts[0].strip()
    result["evidence_file"] = parts[1].strip()
    result["skill_url_cell"] = parts[2].strip()
    result["why_research_related"] = parts[3].strip()
    result["function_explanation"] = parts[4].strip()
    result["execution_flow"] = parts[5].strip()
    result["evidence"] = parts[6].strip()
    return result


def find_table_row(theme, skill_name):
    theme_file = THEME_DIR / f"{theme}.md"
    if not theme_file.exists():
        print(f"  WARNING: theme file not found: {theme_file}")
        return None
    text = theme_file.read_text(encoding="utf-8", errors="replace")
    for line in text.split("\n"):
        if not line.strip().startswith("|"):
            continue
        if "---" in line and re.match(r"^\|[\s\-|]+\|$", line.strip()):
            continue
        row = parse_row(line)
        row_skill = row["skill"].strip().strip("`").lower()
        if row_skill == skill_name.strip().lower():
            return row
    print(f"  WARNING: row not found for {skill_name} in {theme_file.name}")
    return None


# ---------------------------------------------------------------------------
# 3) Read SKILL.md files
# ---------------------------------------------------------------------------

def read_skill_md(path_str):
    if not path_str:
        return "[No SKILL.md path provided]"
    p = Path(path_str)
    if not p.exists():
        # Try forward-slash variant
        alt = Path(str(path_str).replace("/", "\\"))
        if alt.exists():
            p = alt
        else:
            return f"[SKILL.md not found at: {path_str}]"
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"[Error reading SKILL.md: {e}]"


# ---------------------------------------------------------------------------
# 4) Extract highlight keywords from function explanation
# ---------------------------------------------------------------------------

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "it", "its", "this",
    "that", "these", "those", "as", "if", "when", "than", "then", "so",
    "not", "no", "nor", "each", "every", "all", "both", "few", "more",
    "most", "other", "some", "such", "only", "also", "just", "very",
    "use", "using", "used", "uses", "skill", "provides", "supports",
    "including", "based", "via", "into", "about", "which", "where",
}


def extract_keywords(func_explanation):
    if not func_explanation:
        return []
    # Split into phrases on sentence boundaries, commas, semicolons
    phrases = re.split(r"[.,;:()]+", func_explanation)
    keywords = []
    for phrase in phrases:
        phrase = phrase.strip()
        if len(phrase) < 4:
            continue
        # Extract multi-word technical terms (2-4 word sequences)
        words = phrase.split()
        # Full phrase if short enough
        if 2 <= len(words) <= 5:
            clean = " ".join(w for w in words if w.lower() not in STOP_WORDS)
            if len(clean) > 5:
                keywords.append(clean)
        # Individual significant words
        for w in words:
            w_clean = re.sub(r"[^a-zA-Z0-9\-_]", "", w)
            if len(w_clean) > 4 and w_clean.lower() not in STOP_WORDS:
                keywords.append(w_clean)
    # Deduplicate preserving order
    seen = set()
    result = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower not in seen:
            seen.add(kw_lower)
            result.append(kw)
    return result[:30]  # Cap at 30 keywords


# ---------------------------------------------------------------------------
# 5) Assemble data
# ---------------------------------------------------------------------------

THEME_DISPLAY = {
    "01_information_retrieval_evidence_collection": "01 Information Retrieval & Evidence Collection",
    "02_literature_review_writing_citation_part1": "02 Literature Review & Citation (Part 1)",
    "02_literature_review_writing_citation_part2": "02 Literature Review & Citation (Part 2)",
    "03_experiment_benchmark_reproducibility_validation_part1": "03 Experiment & Validation (Part 1)",
    "03_experiment_benchmark_reproducibility_validation_part2": "03 Experiment & Validation (Part 2)",
    "04_data_analysis_and_evidence_interpretation": "04 Data Analysis & Evidence Interpretation",
    "05_research_operations_and_workflow_support": "05 Research Operations & Workflow",
    "06_Additional_Scientific_Skills": "06 Additional Scientific Skills",
}


def build_data(entries):
    skills = []
    for e in entries:
        skill_name = e["skill_name"]
        theme = e.get("theme", "")
        sid = f"{skill_name}__{theme}"

        # Find table row
        row = find_table_row(theme, skill_name)
        table_row = row if row else {
            "skill": skill_name, "evidence_file": "", "skill_url_cell": "",
            "why_research_related": "", "function_explanation": "",
            "execution_flow": "", "evidence": "",
        }

        # Read SKILL.md
        skill_md = read_skill_md(e.get("skill_md_path", ""))

        # Extract keywords
        keywords = extract_keywords(table_row.get("function_explanation", ""))

        skills.append({
            "id": sid,
            "skill_name": skill_name,
            "repo": e.get("repo", ""),
            "theme": theme,
            "theme_display": THEME_DISPLAY.get(theme, theme),
            "status": e.get("status", "UNKNOWN"),
            "audit_reason": e.get("audit_reason", ""),
            "skill_url": e.get("skill_url", ""),
            "skill_md_content": skill_md,
            "table_row": table_row,
            "highlight_keywords": keywords,
        })

    return {"generated_at": "2026-03-06", "total": len(skills), "skills": skills}


# ---------------------------------------------------------------------------
# 6) HTML Template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Skill Audit Review - 22 Remaining Skills</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/14.0.0/marked.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --sidebar-w: 300px;
  --bg: #f8fafc; --sidebar-bg: #1e293b; --sidebar-text: #e2e8f0;
  --card-bg: #fff; --border: #e2e8f0;
  --red: #ef4444; --amber: #f59e0b; --green: #22c55e; --blue: #3b82f6;
  --hl-supported: rgba(34,197,94,0.13); --hl-mentioned: rgba(234,179,8,0.13);
  --hl-disputed: rgba(249,115,22,0.18);
}
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: #1e293b; display: grid; grid-template-columns: var(--sidebar-w) 1fr; height: 100vh; overflow: hidden; }

/* --- Sidebar --- */
.sidebar { background: var(--sidebar-bg); color: var(--sidebar-text); display: flex; flex-direction: column; overflow: hidden; }
.sidebar-header { padding: 20px 16px 12px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.sidebar-header h1 { font-size: 15px; font-weight: 700; margin-bottom: 8px; }
.progress-bar { background: rgba(255,255,255,0.1); border-radius: 4px; height: 6px; overflow: hidden; }
.progress-fill { height: 100%; background: var(--green); transition: width 0.3s; border-radius: 4px; }
.progress-text { font-size: 12px; color: #94a3b8; margin-top: 6px; }
.sidebar-list { flex: 1; overflow-y: auto; padding: 8px 0; }
.sidebar-group-label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; padding: 12px 16px 4px; letter-spacing: 0.05em; }
.sidebar-item { padding: 8px 16px; cursor: pointer; font-size: 13px; border-left: 3px solid transparent; transition: all 0.15s; display: flex; align-items: center; gap: 8px; }
.sidebar-item:hover { background: rgba(255,255,255,0.05); }
.sidebar-item.active { background: rgba(59,130,246,0.15); border-left-color: var(--blue); color: #fff; }
.sidebar-item .badge { font-size: 10px; padding: 1px 6px; border-radius: 3px; font-weight: 600; flex-shrink: 0; }
.badge-inaccurate { background: var(--red); color: #fff; }
.badge-partial { background: var(--amber); color: #fff; }
.sidebar-item .review-icon { margin-left: auto; font-size: 14px; flex-shrink: 0; }
.sidebar-actions { padding: 12px 16px; border-top: 1px solid rgba(255,255,255,0.1); }
.sidebar-actions button { width: 100%; padding: 8px; background: var(--blue); color: #fff; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; }
.sidebar-actions button:hover { opacity: 0.9; }

/* --- Main --- */
.main { display: flex; flex-direction: column; overflow: hidden; }
.main-header { padding: 16px 24px; border-bottom: 1px solid var(--border); background: var(--card-bg); display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.main-header h2 { font-size: 18px; font-weight: 700; }
.main-header .tag { font-size: 11px; padding: 2px 8px; border-radius: 4px; background: #f1f5f9; color: #475569; }
.main-header .status-tag { font-weight: 700; color: #fff; }
.main-header .status-tag.inaccurate { background: var(--red); }
.main-header .status-tag.partial { background: var(--amber); }
.main-content { flex: 1; overflow-y: auto; padding: 20px 24px; display: flex; flex-direction: column; gap: 16px; }

/* --- Panels --- */
.panel { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
.panel-title { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: #64748b; padding: 10px 16px; background: #f8fafc; border-bottom: 1px solid var(--border); }

/* Description fields */
.desc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
.desc-field { padding: 10px 16px; border-bottom: 1px solid var(--border); }
.desc-field:nth-child(odd) { border-right: 1px solid var(--border); }
.desc-field.full-width { grid-column: 1 / -1; }
.desc-label { font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 4px; }
.desc-value { font-size: 13px; line-height: 1.5; color: #334155; max-height: 120px; overflow-y: auto; }
.desc-field.highlighted .desc-value { background: #fffbeb; padding: 4px 6px; border-radius: 4px; border-left: 3px solid var(--amber); }

/* Two-column middle */
.mid-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.skillmd-panel { max-height: 400px; overflow-y: auto; padding: 16px; font-size: 13px; line-height: 1.6; }
.skillmd-panel h1, .skillmd-panel h2, .skillmd-panel h3 { margin: 12px 0 6px; color: #1e293b; }
.skillmd-panel h1 { font-size: 16px; } .skillmd-panel h2 { font-size: 14px; } .skillmd-panel h3 { font-size: 13px; }
.skillmd-panel p, .skillmd-panel li { margin-bottom: 6px; }
.skillmd-panel pre { background: #f1f5f9; padding: 8px; border-radius: 4px; overflow-x: auto; font-size: 12px; }
.skillmd-panel code { background: #f1f5f9; padding: 1px 4px; border-radius: 3px; font-size: 12px; }
.skillmd-panel pre code { background: none; padding: 0; }
.audit-panel { padding: 16px; font-size: 13px; line-height: 1.7; max-height: 400px; overflow-y: auto; }

/* Highlights */
.hl-supported { background: var(--hl-supported); border-radius: 2px; }
.hl-mentioned { background: var(--hl-mentioned); border-radius: 2px; }
.hl-disputed { background: var(--hl-disputed); border-radius: 2px; }
mark.hl-negative { background: #fecaca; color: #991b1b; padding: 0 3px; border-radius: 2px; }
mark.hl-positive { background: #bbf7d0; color: #166534; padding: 0 3px; border-radius: 2px; }

/* Action area */
.action-area { padding: 16px; }
.action-area textarea { width: 100%; min-height: 80px; padding: 10px; border: 1px solid var(--border); border-radius: 6px; font-family: inherit; font-size: 13px; line-height: 1.5; resize: vertical; }
.action-area textarea:focus { outline: none; border-color: var(--blue); box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }
.action-buttons { display: flex; gap: 10px; margin-top: 12px; }
.action-buttons button { padding: 8px 20px; border: none; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.15s; }
.btn-approve { background: #dcfce7; color: #166534; } .btn-approve:hover { background: #bbf7d0; }
.btn-correct { background: var(--blue); color: #fff; } .btn-correct:hover { opacity: 0.9; }
.btn-skip { background: #f1f5f9; color: #64748b; } .btn-skip:hover { background: #e2e8f0; }
.btn-reset { background: #fef2f2; color: #991b1b; } .btn-reset:hover { background: #fecaca; }
.action-hint { font-size: 11px; color: #94a3b8; margin-top: 8px; }

/* Keyboard hint */
.kbd { display: inline-block; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 3px; padding: 0 5px; font-size: 11px; font-family: monospace; margin: 0 2px; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-track { background: transparent; } ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
.sidebar ::-webkit-scrollbar-thumb { background: #475569; }

/* Empty state */
.empty-state { display: flex; align-items: center; justify-content: center; height: 100%; color: #94a3b8; font-size: 15px; }
</style>
</head>
<body>

<div class="sidebar">
  <div class="sidebar-header">
    <h1>Skill Audit Review</h1>
    <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
    <div class="progress-text" id="progressText">0 / 0 reviewed</div>
  </div>
  <div class="sidebar-list" id="sidebarList"></div>
  <div class="sidebar-actions">
    <button onclick="exportJSON()">Export Decisions (JSON)</button>
  </div>
</div>

<div class="main">
  <div class="main-header" id="mainHeader">
    <h2 id="headerTitle">Select a skill</h2>
  </div>
  <div class="main-content" id="mainContent">
    <div class="empty-state">Click a skill in the sidebar to begin review</div>
  </div>
</div>

<script>
// Embedded data
const SKILL_DATA = /*__SKILL_DATA__*/;

// State
const STATE = {
  skills: SKILL_DATA.skills,
  currentIndex: -1,
  reviews: {},
};

// LocalStorage keys
const LS_KEY = "audit_review_state_v1";

function loadState() {
  try {
    const saved = localStorage.getItem(LS_KEY);
    if (saved) STATE.reviews = JSON.parse(saved);
  } catch(e) {}
}
function persistState() {
  try { localStorage.setItem(LS_KEY, JSON.stringify(STATE.reviews)); } catch(e) {}
}

// --- Sidebar ---
function renderSidebar() {
  const list = document.getElementById("sidebarList");
  const groups = { INACCURATE: [], PARTIAL: [] };
  STATE.skills.forEach((s, i) => {
    (groups[s.status] || (groups.OTHER = groups.OTHER || [])).push({ skill: s, index: i });
  });

  let html = "";
  for (const [status, items] of Object.entries(groups)) {
    if (!items.length) continue;
    html += `<div class="sidebar-group-label">${status} (${items.length})</div>`;
    for (const { skill, index } of items) {
      const review = STATE.reviews[skill.id];
      const icon = review ? (review.action === "approved" ? "&#10003;" : review.action === "corrected" ? "&#9998;" : "&#8212;") : "";
      const iconColor = review ? (review.action === "approved" ? "#22c55e" : review.action === "corrected" ? "#3b82f6" : "#94a3b8") : "";
      const active = index === STATE.currentIndex ? " active" : "";
      const badgeCls = status === "INACCURATE" ? "badge-inaccurate" : "badge-partial";
      html += `<div class="sidebar-item${active}" onclick="selectSkill(${index})">
        <span class="badge ${badgeCls}">${status.slice(0,3)}</span>
        <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${skill.skill_name}</span>
        <span class="review-icon" style="color:${iconColor}">${icon}</span>
      </div>`;
    }
  }
  list.innerHTML = html;
  updateProgress();
}

function updateProgress() {
  const total = STATE.skills.length;
  const reviewed = Object.keys(STATE.reviews).length;
  const approved = Object.values(STATE.reviews).filter(r => r.action === "approved").length;
  const corrected = Object.values(STATE.reviews).filter(r => r.action === "corrected").length;
  const skipped = Object.values(STATE.reviews).filter(r => r.action === "skipped").length;
  document.getElementById("progressFill").style.width = `${(reviewed/total)*100}%`;
  document.getElementById("progressText").textContent =
    `${reviewed}/${total} reviewed (${approved} approved, ${corrected} corrected, ${skipped} skipped)`;
}

// --- Detail View ---
function selectSkill(index) {
  STATE.currentIndex = index;
  const skill = STATE.skills[index];
  renderDetail(skill);
  renderSidebar();
}

function renderDetail(skill) {
  // Header
  const header = document.getElementById("mainHeader");
  const statusCls = skill.status === "INACCURATE" ? "inaccurate" : "partial";
  header.innerHTML = `
    <h2 id="headerTitle">${skill.skill_name}</h2>
    <span class="tag">${skill.repo}</span>
    <span class="tag">${skill.theme_display}</span>
    <span class="tag status-tag ${statusCls}">${skill.status}</span>
    ${skill.skill_url ? `<a href="${skill.skill_url}" target="_blank" class="tag" style="text-decoration:none;color:var(--blue)">GitHub &rarr;</a>` : ""}
  `;

  // Main content
  const main = document.getElementById("mainContent");
  const row = skill.table_row;
  const review = STATE.reviews[skill.id];

  main.innerHTML = `
    <!-- Current Description -->
    <div class="panel">
      <div class="panel-title">Current Theme Doc Description (7 Columns)</div>
      <div class="desc-grid">
        <div class="desc-field">
          <div class="desc-label">Skill Name</div>
          <div class="desc-value">${esc(row.skill)}</div>
        </div>
        <div class="desc-field">
          <div class="desc-label">Evidence File</div>
          <div class="desc-value" style="font-family:monospace;font-size:12px">${esc(row.evidence_file)}</div>
        </div>
        <div class="desc-field full-width">
          <div class="desc-label">Why Research-Related</div>
          <div class="desc-value">${esc(row.why_research_related)}</div>
        </div>
        <div class="desc-field full-width highlighted">
          <div class="desc-label">Function Explanation (audit target)</div>
          <div class="desc-value">${highlightAuditPhrases(esc(row.function_explanation))}</div>
        </div>
        <div class="desc-field full-width">
          <div class="desc-label">Execution Flow</div>
          <div class="desc-value">${esc(row.execution_flow)}</div>
        </div>
        <div class="desc-field full-width">
          <div class="desc-label">Evidence</div>
          <div class="desc-value">${esc(row.evidence)}</div>
        </div>
      </div>
    </div>

    <!-- SKILL.md + Audit Reason -->
    <div class="mid-row">
      <div class="panel">
        <div class="panel-title">SKILL.md (Ground Truth)</div>
        <div class="skillmd-panel" id="skillmdPanel">${renderSkillMd(skill)}</div>
      </div>
      <div class="panel">
        <div class="panel-title">Audit Reason</div>
        <div class="audit-panel">${highlightAuditPhrases(esc(skill.audit_reason))}</div>
      </div>
    </div>

    <!-- Action Area -->
    <div class="panel">
      <div class="panel-title">Your Decision</div>
      <div class="action-area">
        <label class="desc-label" style="margin-bottom:6px;display:block">Corrected Function Explanation</label>
        <textarea id="correctionText">${esc(review?.corrected_text || row.function_explanation)}</textarea>
        <div class="action-buttons">
          <button class="btn-approve" onclick="saveReview('approved')">Approve as-is</button>
          <button class="btn-correct" onclick="saveReview('corrected')">Save Correction</button>
          <button class="btn-skip" onclick="saveReview('skipped')">Skip</button>
          ${review ? '<button class="btn-reset" onclick="resetReview()">Reset</button>' : ''}
        </div>
        <div class="action-hint">
          Keyboard: <span class="kbd">&larr;</span><span class="kbd">&rarr;</span> navigate
          &middot; <span class="kbd">A</span> approve &middot; <span class="kbd">S</span> save correction
          &middot; <span class="kbd">K</span> skip
          ${review ? `<br>Current decision: <strong style="color:${review.action==='approved'?'#166534':review.action==='corrected'?'#1d4ed8':'#64748b'}">${review.action}</strong>` : ''}
        </div>
      </div>
    </div>
  `;

  // Apply SKILL.md highlighting after DOM is ready
  highlightSkillMd(skill);
}

function esc(s) {
  if (!s) return "";
  return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

function renderSkillMd(skill) {
  const content = skill.skill_md_content || "";
  if (typeof marked !== "undefined") {
    try { return marked.parse(content); } catch(e) {}
  }
  return `<pre>${esc(content)}</pre>`;
}

function highlightAuditPhrases(html) {
  const negatives = ["not supported","not mentioned","not reflected","not evidenced","not established",
    "not explicitly","not the same","not present","not clearly","adds unsupported","introduces",
    "omits","mismatch","stronger than","overreach","over-specif","unsupported claim","not aligned",
    "not substantiated","not guaranteed"];
  const positives = ["supported","correct","matches","aligns","accurately","is supported","are supported"];

  for (const phrase of negatives) {
    const re = new RegExp(`(${phrase.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})`, "gi");
    html = html.replace(re, '<mark class="hl-negative">$1</mark>');
  }
  for (const phrase of positives) {
    // Avoid double-marking inside existing marks
    const re = new RegExp(`(?<!hl-negative">)(${phrase.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})(?!</mark>)`, "gi");
    html = html.replace(re, '<mark class="hl-positive">$1</mark>');
  }
  return html;
}

function highlightSkillMd(skill) {
  const panel = document.getElementById("skillmdPanel");
  if (!panel) return;
  const keywords = skill.highlight_keywords || [];
  if (!keywords.length) return;

  // Get all text-containing elements
  const elements = panel.querySelectorAll("p, li, td, blockquote, h1, h2, h3, h4, h5, h6");
  elements.forEach(el => {
    const text = el.textContent.toLowerCase();
    let matchCount = 0;
    for (const kw of keywords) {
      if (text.includes(kw.toLowerCase())) matchCount++;
    }
    if (matchCount >= 2) {
      el.classList.add("hl-supported");
    } else if (matchCount === 1) {
      el.classList.add("hl-mentioned");
    }
  });
}

// --- Actions ---
function saveReview(action) {
  const skill = STATE.skills[STATE.currentIndex];
  if (!skill) return;
  const textarea = document.getElementById("correctionText");
  STATE.reviews[skill.id] = {
    action,
    skill_name: skill.skill_name,
    repo: skill.repo,
    theme: skill.theme,
    original_text: skill.table_row.function_explanation,
    corrected_text: action === "corrected" ? textarea.value : undefined,
    reviewed_at: new Date().toISOString(),
  };
  persistState();
  renderSidebar();
  // Auto-advance to next unreviewed
  if (STATE.currentIndex < STATE.skills.length - 1) {
    selectSkill(STATE.currentIndex + 1);
  } else {
    renderDetail(skill); // Re-render current to show status
  }
}

function resetReview() {
  const skill = STATE.skills[STATE.currentIndex];
  if (!skill) return;
  delete STATE.reviews[skill.id];
  persistState();
  renderSidebar();
  renderDetail(skill);
}

function exportJSON() {
  const reviews = Object.values(STATE.reviews).map(r => ({
    skill_name: r.skill_name,
    repo: r.repo,
    theme: r.theme,
    action: r.action,
    original_function_explanation: r.original_text,
    corrected_function_explanation: r.corrected_text || null,
    reviewed_at: r.reviewed_at,
  }));
  const data = {
    exported_at: new Date().toISOString(),
    total_skills: STATE.skills.length,
    total_reviewed: reviews.length,
    reviews,
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "audit_review_decisions.json"; a.click();
  URL.revokeObjectURL(url);
}

// --- Keyboard Navigation ---
document.addEventListener("keydown", (e) => {
  // Don't intercept when typing in textarea
  if (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT") return;
  if (e.key === "ArrowLeft" && STATE.currentIndex > 0) selectSkill(STATE.currentIndex - 1);
  if (e.key === "ArrowRight" && STATE.currentIndex < STATE.skills.length - 1) selectSkill(STATE.currentIndex + 1);
  if (e.key === "a" || e.key === "A") saveReview("approved");
  if (e.key === "s" && !e.ctrlKey && !e.metaKey) saveReview("corrected");
  if (e.key === "k" || e.key === "K") saveReview("skipped");
});

// --- Init ---
loadState();
renderSidebar();
if (STATE.skills.length > 0) selectSkill(0);
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# 7) Generate
# ---------------------------------------------------------------------------

def main():
    print("=== Building Audit Review Page ===")

    # Parse issues
    entries = parse_issues()
    if not entries:
        print("ERROR: No entries parsed from issues file")
        sys.exit(1)

    # Build data
    data = build_data(entries)
    print(f"Assembled data for {data['total']} skills")

    # Generate HTML
    data_json = json.dumps(data, ensure_ascii=False, indent=None)
    html = HTML_TEMPLATE.replace("/*__SKILL_DATA__*/", data_json)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Generated: {OUTPUT}")
    print(f"Open in browser to review.")


if __name__ == "__main__":
    main()

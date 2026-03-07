"""
generate_confirmed_invalid.py
[IN]  audit_results.json, x_class_row_ids.json
[OUT] confirmed_invalid_skills.json, confirmed_invalid_skills.md
[POS] Extracts Y-class skills (truly not research-related) after X-class correction.
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
AUDIT_PATH = BASE_DIR / "audit_results.json"
X_CLASS_PATH = BASE_DIR / "x_class_row_ids.json"
OUT_JSON = BASE_DIR / "confirmed_invalid_skills.json"
OUT_MD = BASE_DIR / "confirmed_invalid_skills.md"


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    audit = json.load(open(AUDIT_PATH, encoding='utf-8'))
    x_data = json.load(open(X_CLASS_PATH, encoding='utf-8'))
    x_ids = set(x_data['row_ids'])

    invalid_all = [r for r in audit['results'] if r.get('research_relevance') == 'invalid']
    y_class = [r for r in invalid_all if r['row_id'] not in x_ids]
    y_class.sort(key=lambda x: (x['theme'], x['repo'], x['skill_name']))

    unique_skills = sorted(set(r['skill_name'] for r in y_class))

    # --- JSON ---
    output = {
        "metadata": {
            "date": "2026-03-01",
            "source": "audit_results.json (gpt-5.2 full audit)",
            "total_invalid_in_audit": len(invalid_all),
            "x_class_corrected": len(invalid_all) - len(y_class),
            "y_class_confirmed_invalid": len(y_class),
            "unique_skill_names": len(unique_skills),
            "description": "Skills confirmed as NOT research-related after X-class correction. "
                           "These are general software tools (pentesting, web dev, DevOps, etc.) "
                           "with no credible research use case.",
        },
        "row_ids": [r['row_id'] for r in y_class],
        "unique_skill_names": unique_skills,
        "skills": [
            {
                "row_id": r["row_id"],
                "skill_name": r["skill_name"],
                "repo": r["repo"],
                "theme": r["theme"],
                "overall_quality": r.get("overall_quality", 0),
                "function_accuracy": r.get("function_accuracy", ""),
                "reason": r.get("research_relevance_reason", ""),
                "issues": r.get("issues", []),
            }
            for r in y_class
        ],
    }
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"JSON: {OUT_JSON}")

    # --- Markdown ---
    lines = [
        "# Confirmed Invalid (Non-Research) Skills",
        "",
        "- Date: 2026-03-01",
        "- Source: audit_results.json (gpt-5.2 full audit)",
        f"- Total invalid in audit: {len(invalid_all)}",
        f"- X-class corrected (now valid): {len(invalid_all) - len(y_class)}",
        f"- **Y-class confirmed invalid: {len(y_class)}**",
        f"- Unique skill names: {len(unique_skills)}",
        "",
    ]

    # Summary by theme
    themes = {}
    for r in y_class:
        t = r['theme']
        themes[t] = themes.get(t, 0) + 1

    lines += ["## By Theme", "", "| Theme | Count |", "|-------|------:|"]
    for t, c in sorted(themes.items()):
        lines.append(f"| {t} | {c} |")
    lines.append("")

    # Summary by repo (top 20)
    repos = {}
    for r in y_class:
        repos[r['repo']] = repos.get(r['repo'], 0) + 1

    lines += ["## By Repository (Top 20)", "", "| Repository | Count |", "|------------|------:|"]
    for repo, c in sorted(repos.items(), key=lambda x: -x[1])[:20]:
        lines.append(f"| {repo} | {c} |")
    lines.append("")

    # Full list by theme
    lines += ["## Full List", ""]
    current_theme = ""
    idx = 0
    for r in y_class:
        if r['theme'] != current_theme:
            if current_theme:
                lines.append("")
            current_theme = r['theme']
            lines.append(f"### {current_theme} ({themes[current_theme]})")
            lines.append("")
            lines.append("| # | Skill | Repository | Quality | Reason |")
            lines.append("|--:|-------|------------|--------:|--------|")
            idx = 0

        idx += 1
        reason = r.get('research_relevance_reason', '')
        reason = reason.replace('|', '/').replace('\n', ' ')[:150]
        lines.append(
            f"| {idx} "
            f"| {r['skill_name']} "
            f"| {r['repo']} "
            f"| {r.get('overall_quality', '?')} "
            f"| {reason} |"
        )

    lines.append("")

    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Markdown: {OUT_MD} ({len(lines)} lines)")
    print(f"\nDone! {len(y_class)} confirmed invalid skills exported.")


if __name__ == '__main__':
    main()

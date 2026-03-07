"""
generate_invalid_report.py
[IN]  audit_results.json
[OUT] invalid_skills_report.md
[POS] One-shot script: extracts all research_relevance=="invalid" skills into a structured report.
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
AUDIT_PATH = BASE_DIR / "audit_results.json"
OUTPUT_PATH = BASE_DIR / "invalid_skills_report.md"


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    data = json.load(open(AUDIT_PATH, encoding='utf-8'))
    results = data['results']
    invalid = [r for r in results if r.get('research_relevance') == 'invalid']
    invalid.sort(key=lambda x: (x['theme'], x['repo'], x['skill_name']))

    print(f"Total invalid: {len(invalid)}")

    lines = []
    lines.append('# Invalid Research Relevance Skills')
    lines.append('')
    lines.append('- Date: 2026-03-01')
    lines.append('- Source: audit_results.json (model: gpt-5.2)')
    lines.append(f'- Total: {len(invalid)}')
    lines.append('- Criteria: research_relevance == "invalid" (skill has no credible research use case)')
    lines.append('')

    # --- Summary ---
    lines.append('## Summary')
    lines.append('')

    # By theme
    themes = {}
    for r in invalid:
        t = r['theme']
        themes[t] = themes.get(t, 0) + 1

    lines.append('### By Theme')
    lines.append('')
    lines.append('| Theme | Count |')
    lines.append('|-------|------:|')
    for t, c in sorted(themes.items()):
        lines.append(f'| {t} | {c} |')
    lines.append('')

    # By quality
    quals = {}
    for r in invalid:
        q = r.get('overall_quality', 0)
        quals[q] = quals.get(q, 0) + 1

    lines.append('### By Quality Score')
    lines.append('')
    lines.append('| Score | Count | % |')
    lines.append('|------:|------:|--:|')
    for q in sorted(quals.keys()):
        pct = quals[q] / len(invalid) * 100
        lines.append(f'| {q} | {quals[q]} | {pct:.1f}% |')
    lines.append('')

    # By repo
    repos = {}
    for r in invalid:
        repo = r['repo']
        repos[repo] = repos.get(repo, 0) + 1

    lines.append('### By Repository (Top 20)')
    lines.append('')
    lines.append('| Repository | Count |')
    lines.append('|------------|------:|')
    for repo, c in sorted(repos.items(), key=lambda x: -x[1])[:20]:
        lines.append(f'| {repo} | {c} |')
    lines.append('')

    # By function accuracy
    accs = {}
    for r in invalid:
        a = r.get('function_accuracy', 'unknown')
        accs[a] = accs.get(a, 0) + 1

    lines.append('### By Function Accuracy')
    lines.append('')
    lines.append('| Accuracy | Count |')
    lines.append('|----------|------:|')
    for a, c in sorted(accs.items(), key=lambda x: -x[1]):
        lines.append(f'| {a} | {c} |')
    lines.append('')

    # --- Full List ---
    lines.append('## Full List')
    lines.append('')

    current_theme = ''
    idx = 0
    for r in invalid:
        if r['theme'] != current_theme:
            if current_theme:
                lines.append('')
            current_theme = r['theme']
            theme_count = themes[current_theme]
            lines.append(f'### {current_theme} ({theme_count})')
            lines.append('')
            lines.append('| # | Skill | Repository | Quality | Func Accuracy | Reason |')
            lines.append('|--:|-------|------------|--------:|---------------|--------|')
            idx = 0

        idx += 1
        reason = r.get('research_relevance_reason', '')
        issues = r.get('issues', [])
        issues_text = '; '.join(issues)

        # Combine reason and issues, truncate
        if reason and issues_text:
            combined = f'{reason} // {issues_text}'
        elif reason:
            combined = reason
        else:
            combined = issues_text
        combined = combined.replace('|', '/').replace('\n', ' ')[:180]

        lines.append(
            f'| {idx} '
            f'| {r["skill_name"]} '
            f'| {r["repo"]} '
            f'| {r.get("overall_quality", "?")} '
            f'| {r.get("function_accuracy", "?")} '
            f'| {combined} |'
        )

    lines.append('')

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Written: {OUTPUT_PATH} ({len(lines)} lines)")


if __name__ == '__main__':
    main()

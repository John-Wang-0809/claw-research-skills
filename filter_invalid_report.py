"""
[IN]  Dependencies/Inputs:
 - invalid_skills_report.md — 477-row invalid skills report (markdown tables by theme)
 - confirmed_invalid_skills.json — JSON with row_ids, unique_skill_names, skills array
 - confirmed_invalid_skills.md — confirmed invalid skills in markdown format
 - SKILLS_TO_REMOVE (hardcoded) — 227 skill names user identified as research-related
[OUT] Outputs:
 - Overwrites invalid_skills_report.md with filtered content
 - Overwrites confirmed_invalid_skills.json with filtered content
 - Overwrites confirmed_invalid_skills.md with filtered content
[POS] Position in the system:
 - One-time filter script for Phase 5 of invalid skills re-audit
 - Removes user-identified research-related skills from invalid reports

Usage:
  python filter_invalid_report.py [--dry-run]
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter

BASE = Path(__file__).parent

# Round 2: 23 additional skills user identified as research-related (case-insensitive)
SKILLS_TO_REMOVE = {s.lower() for s in [
    # 1. 结构化数据提取与多模态分析
    "instructor", "ai-multimodal",
    # 2. 数据科学与实验可重复性
    "senior-data-scientist", "ml-pipeline-workflow",
    # 3. 互联网测量与学术网络安全
    "Shodan Reconnaissance and Pentesting", "Wireshark Network Traffic Analysis",
    # 4. 实证软件工程研究
    "semgrep", "binary-analysis-patterns", "coverage-analysis",
    # 5. 密码学与侧信道攻击研究
    "constant-time-analysis", "constant-time-testing",
    # 6. AI 安全与大模型对齐
    "PromptInjection", "azure-ai-contentsafety-py",
    "azure-ai-contentsafety-java", "azure-ai-contentsafety-ts",
    # 7. 自动化漏洞挖掘与恶意软件分析
    "cargo-fuzz", "yara-rule-authoring",
    # 8. Web3 与智能合约形式化验证
    "cairo-vulnerability-scanner", "cosmos-vulnerability-scanner",
    "ton-vulnerability-scanner", "substrate-vulnerability-scanner",
    # 9. 认知科学与逻辑学
    "sequential-thinking", "ReasoningBank Intelligence",
]}


def parse_md_table_rows(lines):
    """Parse markdown table rows, returning list of (line_idx, skill_name, full_line)."""
    rows = []
    for i, line in enumerate(lines):
        line_s = line.strip()
        if not line_s.startswith('|') or line_s.startswith('|--') or line_s.startswith('| #'):
            continue
        cols = [c.strip() for c in line_s.split('|')]
        # cols[0] is empty (before first |), cols[1] is #, cols[2] is Skill name
        if len(cols) >= 3 and cols[1].strip().isdigit():
            skill_name = cols[2].strip()
            rows.append((i, skill_name, line))
    return rows


def should_remove(skill_name):
    return skill_name.lower() in SKILLS_TO_REMOVE


def filter_invalid_report_md(dry_run=False):
    """Filter invalid_skills_report.md — remove rows matching SKILLS_TO_REMOVE."""
    path = BASE / "invalid_skills_report.md"
    lines = path.read_text(encoding='utf-8').splitlines(keepends=True)

    # Find all table rows and mark which to remove (only in Full List section)
    rows_to_remove = set()
    removed_by_theme = Counter()
    kept_by_theme = Counter()

    current_theme = None
    in_full_list = False
    for i, line in enumerate(lines):
        line_s = line.strip()

        if line_s == '## Full List':
            in_full_list = True
            continue

        if not in_full_list:
            continue

        # Detect theme headers like "### 01_information_retrieval... (48)"
        m = re.match(r'^### (\S+)\s+\((\d+)\)', line_s)
        if m:
            current_theme = m.group(1)
            continue

        if not line_s.startswith('|') or line_s.startswith('|--') or line_s.startswith('| #'):
            continue
        cols = [c.strip() for c in line_s.split('|')]
        if len(cols) >= 3 and cols[1].strip().isdigit():
            skill_name = cols[2].strip()
            if should_remove(skill_name):
                rows_to_remove.add(i)
                removed_by_theme[current_theme] += 1
            else:
                kept_by_theme[current_theme] += 1

    print(f"[invalid_skills_report.md] Removing {len(rows_to_remove)} rows")

    # Build new lines, skipping removed rows
    new_lines = []
    for i, line in enumerate(lines):
        if i in rows_to_remove:
            continue
        new_lines.append(line)

    # Now renumber rows within each theme section and update theme counts
    result_lines = []
    in_full_list_renum = False
    row_counter = 0

    for line in new_lines:
        line_s = line.strip()

        if line_s == '## Full List':
            in_full_list_renum = True
            result_lines.append(line)
            continue

        if not in_full_list_renum:
            result_lines.append(line)
            continue

        # Update theme header counts
        m = re.match(r'^(### \S+)\s+\(\d+\)', line_s)
        if m:
            theme_name = m.group(1).replace('### ', '')
            new_count = kept_by_theme.get(theme_name, 0)
            result_lines.append(f"### {theme_name} ({new_count})\n")
            row_counter = 0
            continue

        # Renumber table rows
        if line_s.startswith('|') and not line_s.startswith('|--') and not line_s.startswith('| #'):
            cols = line_s.split('|')
            if len(cols) >= 3 and cols[1].strip().isdigit():
                row_counter += 1
                cols[1] = f' {row_counter} '
                result_lines.append('|'.join(cols) + '\n')
                continue

        result_lines.append(line)

    # Update summary statistics
    content = ''.join(result_lines)

    # Update "By Theme" summary table
    for theme, count in kept_by_theme.items():
        if theme is None:
            continue
        content = re.sub(
            rf'\| {re.escape(theme)} \| \d+ \|',
            f'| {theme} | {count} |',
            content
        )

    # Update total
    total_kept = sum(kept_by_theme.values())
    content = re.sub(r'- Total: \d+', f'- Total: {total_kept}', content)

    # Update "By Quality Score" — need to recount from remaining data
    # Update "By Repository" — need to recount
    # Update "By Function Accuracy" — need to recount
    # These are complex; we'll recompute from the remaining rows

    # Count unique skill names remaining — only in "Full List" section
    remaining_skills = set()
    remaining_repos = Counter()
    remaining_quality = Counter()
    remaining_accuracy = Counter()

    in_full_list = False
    for line in content.split('\n'):
        line_s = line.strip()
        if line_s == '## Full List':
            in_full_list = True
            continue
        if not in_full_list:
            continue
        if not line_s.startswith('|') or line_s.startswith('|--') or line_s.startswith('| #'):
            continue
        cols = [c.strip() for c in line_s.split('|')]
        if len(cols) >= 6 and cols[1].strip().isdigit():
            remaining_skills.add(cols[2].strip())
            remaining_repos[cols[3].strip()] += 1
            try:
                remaining_quality[int(cols[4].strip())] += 1
            except ValueError:
                pass
            remaining_accuracy[cols[5].strip()] += 1

    # Rebuild "By Quality Score" table
    quality_section = "### By Quality Score\n\n| Score | Count | % |\n|------:|------:|--:|\n"
    for score in sorted(remaining_quality.keys()):
        cnt = remaining_quality[score]
        pct = cnt / total_kept * 100 if total_kept else 0
        quality_section += f"| {score} | {cnt} | {pct:.1f}% |\n"
    content = re.sub(
        r'### By Quality Score\n\n\| Score \| Count \| % \|\n\|[-:\| ]+\n(?:\| \d+ \| \d+ \| [\d.]+% \|\n)+',
        quality_section,
        content
    )

    # Rebuild "By Repository (Top 20)" table
    top_repos = remaining_repos.most_common(20)
    repo_section = "### By Repository (Top 20)\n\n| Repository | Count |\n|------------|------:|\n"
    for repo, cnt in top_repos:
        repo_section += f"| {repo} | {cnt} |\n"
    content = re.sub(
        r'### By Repository \(Top 20\)\n\n\| Repository \| Count \|\n\|[-:\| ]+\n(?:\| .+ \| \d+ \|\n)+',
        repo_section,
        content
    )

    # Rebuild "By Function Accuracy" table
    accuracy_section = "### By Function Accuracy\n\n| Accuracy | Count |\n|----------|------:|\n"
    for acc in ['accurate', 'partial', 'cannot_verify']:
        if remaining_accuracy.get(acc, 0) > 0:
            accuracy_section += f"| {acc} | {remaining_accuracy[acc]} |\n"
    content = re.sub(
        r'### By Function Accuracy\n\n\| Accuracy \| Count \|\n\|[-:\| ]+\n(?:\| \w+ \| \d+ \|\n)+',
        accuracy_section,
        content
    )

    if dry_run:
        print(f"  Would write {total_kept} rows ({len(remaining_skills)} unique skills)")
        print(f"  Themes: {dict(kept_by_theme)}")
    else:
        path.write_text(content, encoding='utf-8')
        print(f"  Written: {total_kept} rows, {len(remaining_skills)} unique skills")

    return remaining_skills, total_kept


def filter_confirmed_json(dry_run=False):
    """Filter confirmed_invalid_skills.json — remove entries matching SKILLS_TO_REMOVE."""
    path = BASE / "confirmed_invalid_skills.json"
    data = json.loads(path.read_text(encoding='utf-8'))

    original_count = len(data['skills'])

    # Filter skills
    kept_skills = [s for s in data['skills'] if not should_remove(s['skill_name'])]
    kept_row_ids = [s['row_id'] for s in kept_skills]
    kept_unique = sorted(set(s['skill_name'] for s in kept_skills))

    removed_count = original_count - len(kept_skills)
    print(f"[confirmed_invalid_skills.json] Removing {removed_count} entries, keeping {len(kept_skills)}")

    # Update data
    data['row_ids'] = kept_row_ids
    data['skills'] = kept_skills
    data['unique_skill_names'] = kept_unique
    data['metadata']['y_class_confirmed_invalid'] = len(kept_skills)
    data['metadata']['unique_skill_names'] = len(kept_unique)
    data['metadata']['description'] = (
        "Skills confirmed as NOT research-related after X-class correction and user review. "
        "Primarily security/pentesting tools with no credible research use case."
    )

    if dry_run:
        print(f"  Would keep {len(kept_skills)} skills ({len(kept_unique)} unique)")
    else:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f"  Written: {len(kept_skills)} skills, {len(kept_unique)} unique")

    return kept_unique, len(kept_skills)


def filter_confirmed_md(dry_run=False):
    """Filter confirmed_invalid_skills.md — same logic as invalid_skills_report.md."""
    path = BASE / "confirmed_invalid_skills.md"
    lines = path.read_text(encoding='utf-8').splitlines(keepends=True)

    rows_to_remove = set()
    removed_by_theme = Counter()
    kept_by_theme = Counter()
    current_theme = None
    in_full_list = False

    for i, line in enumerate(lines):
        line_s = line.strip()

        if line_s == '## Full List':
            in_full_list = True
            continue

        if not in_full_list:
            continue

        m = re.match(r'^### (\S+)\s+\((\d+)\)', line_s)
        if m:
            current_theme = m.group(1)
            continue

        if not line_s.startswith('|') or line_s.startswith('|--') or line_s.startswith('| #'):
            continue
        cols = [c.strip() for c in line_s.split('|')]
        if len(cols) >= 3 and cols[1].strip().isdigit():
            skill_name = cols[2].strip()
            if should_remove(skill_name):
                rows_to_remove.add(i)
                removed_by_theme[current_theme] += 1
            else:
                kept_by_theme[current_theme] += 1

    print(f"[confirmed_invalid_skills.md] Removing {len(rows_to_remove)} rows")

    # Build new lines
    new_lines = [line for i, line in enumerate(lines) if i not in rows_to_remove]

    # Renumber and update counts
    result_lines = []
    in_full_list_renum = False
    row_counter = 0

    for line in new_lines:
        line_s = line.strip()

        if line_s == '## Full List':
            in_full_list_renum = True
            result_lines.append(line)
            continue

        if not in_full_list_renum:
            result_lines.append(line)
            continue

        m = re.match(r'^(### \S+)\s+\(\d+\)', line_s)
        if m:
            theme_name = m.group(1).replace('### ', '')
            new_count = kept_by_theme.get(theme_name, 0)
            result_lines.append(f"### {theme_name} ({new_count})\n")
            row_counter = 0
            continue

        if line_s.startswith('|') and not line_s.startswith('|--') and not line_s.startswith('| #'):
            cols = line_s.split('|')
            if len(cols) >= 3 and cols[1].strip().isdigit():
                row_counter += 1
                cols[1] = f' {row_counter} '
                result_lines.append('|'.join(cols) + '\n')
                continue

        result_lines.append(line)

    content = ''.join(result_lines)

    # Update theme summary table
    for theme, count in kept_by_theme.items():
        if theme is None:
            continue
        content = re.sub(
            rf'\| {re.escape(theme)} \| \d+ \|',
            f'| {theme} | {count} |',
            content
        )

    # Update total and metadata
    total_kept = sum(kept_by_theme.values())
    content = re.sub(r'\*\*Y-class confirmed invalid: \d+\*\*', f'**Y-class confirmed invalid: {total_kept}**', content)

    # Count unique names — only in "Full List" section
    remaining_skills = set()
    remaining_repos = Counter()
    in_full_list = False
    for line in content.split('\n'):
        line_s = line.strip()
        if line_s == '## Full List':
            in_full_list = True
            continue
        if not in_full_list:
            continue
        if not line_s.startswith('|') or line_s.startswith('|--') or line_s.startswith('| #'):
            continue
        cols = [c.strip() for c in line_s.split('|')]
        if len(cols) >= 3 and cols[1].strip().isdigit():
            remaining_skills.add(cols[2].strip())
            if len(cols) >= 4:
                remaining_repos[cols[3].strip()] += 1

    content = re.sub(r'- Unique skill names: \d+', f'- Unique skill names: {len(remaining_skills)}', content)

    # Rebuild "By Repository (Top 20)" table
    top_repos = remaining_repos.most_common(20)
    repo_section = "## By Repository (Top 20)\n\n| Repository | Count |\n|------------|------:|\n"
    for repo, cnt in top_repos:
        repo_section += f"| {repo} | {cnt} |\n"
    content = re.sub(
        r'## By Repository \(Top 20\)\n\n\| Repository \| Count \|\n\|[-:\| ]+\n(?:\| .+ \| \d+ \|\n)+',
        repo_section,
        content
    )

    if dry_run:
        print(f"  Would write {total_kept} rows ({len(remaining_skills)} unique skills)")
    else:
        path.write_text(content, encoding='utf-8')
        print(f"  Written: {total_kept} rows, {len(remaining_skills)} unique skills")

    return remaining_skills, total_kept


def verify_consistency(md_skills, md_count, json_unique, json_count, confirmed_skills, confirmed_count):
    """Verify all three files are consistent."""
    print("\n=== Verification ===")
    print(f"invalid_skills_report.md:   {md_count} rows, {len(md_skills)} unique skills")
    print(f"confirmed_invalid_skills.json: {json_count} entries, {len(json_unique)} unique skills")
    print(f"confirmed_invalid_skills.md:   {confirmed_count} rows, {len(confirmed_skills)} unique skills")

    # Check no removed skills remain
    for name in SKILLS_TO_REMOVE:
        name_orig = name  # already lowered in the set
        for s in md_skills:
            if s.lower() == name_orig:
                print(f"  ERROR: '{s}' still in invalid_skills_report.md!")
        for s in json_unique:
            if s.lower() == name_orig:
                print(f"  ERROR: '{s}' still in confirmed_invalid_skills.json!")
        for s in confirmed_skills:
            if s.lower() == name_orig:
                print(f"  ERROR: '{s}' still in confirmed_invalid_skills.md!")

    # Cross-check unique skill names
    json_set = set(s.lower() for s in json_unique)
    confirmed_set = set(s.lower() for s in confirmed_skills)

    if json_set != confirmed_set:
        diff1 = json_set - confirmed_set
        diff2 = confirmed_set - json_set
        if diff1:
            print(f"  WARN: In JSON but not confirmed MD: {diff1}")
        if diff2:
            print(f"  WARN: In confirmed MD but not JSON: {diff2}")
    else:
        print("  JSON and confirmed MD unique skills match.")

    print("  Verification complete.")


def main():
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        print("=== DRY RUN MODE ===\n")

    print(f"Skills to remove: {len(SKILLS_TO_REMOVE)} unique names\n")

    md_skills, md_count = filter_invalid_report_md(dry_run)
    json_unique, json_count = filter_confirmed_json(dry_run)
    confirmed_skills, confirmed_count = filter_confirmed_md(dry_run)

    verify_consistency(md_skills, md_count, json_unique, json_count, confirmed_skills, confirmed_count)


if __name__ == '__main__':
    main()

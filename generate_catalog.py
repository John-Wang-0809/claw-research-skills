"""
[IN]  Dependencies/Inputs:
 - Final_Research_Skills_Thematic_Split/0*.md (8 theme documents, cleaned)
 - multidim_audit.json (1408 audited entries: research_tier, domain, added_value)
 - dedup_results.json (1408 entries after dedup: uniqueness, similarity)
[OUT] Outputs:
 - SKILL_CATALOG.md (skills catalog with audit columns: Tier, Domain, Value)
[POS] Position in the system:
 - Catalog generator script. Reads theme documents and produces a unified
   skills directory. Filters entries against multidim_audit.json so only
   audited entries appear. Re-run after data updates to regenerate.

 Change warning: once you modify this file's logic, you must update this
 comment block, and check/update the module doc (README/CLAUDE) in the
 containing folder; update the root global map if necessary.
"""

import glob
import json
import os
import re
from collections import OrderedDict
from datetime import datetime

# Theme display names
THEME_NAMES = {
    '01': '信息检索与证据收集',
    '02': '文献综述、写作与引用',
    '03': '实验、基准测试与可复现性验证',
    '04': '数据分析与证据解读',
    '05': '科研运营与工作流支持',
    '06': '其他科学技能',
}

def extract_first_sentence(text, max_len=100):
    """Extract first sentence from Function Explanation, truncate if needed."""
    text = text.strip()
    if not text:
        return ''
    for pattern in ['. ', '。']:
        idx = text.find(pattern)
        if idx != -1 and idx < max_len:
            return text[:idx + 1].strip()
    if len(text) > max_len:
        truncated = text[:max_len]
        last_space = truncated.rfind(' ')
        if last_space > max_len * 0.6:
            return truncated[:last_space] + '...'
        return truncated + '...'
    return text

def extract_url_from_cell(cell):
    """Extract URL from markdown link in table cell."""
    m = re.search(r'\[.*?\]\((https?://[^)]+)\)', cell)
    if m:
        return m.group(1)
    m = re.search(r'(https?://\S+)', cell)
    if m:
        return m.group(1)
    return ''

def parse_theme_file(filepath):
    """Parse a theme markdown file.
    Returns: OrderedDict of {repo_name: [(skill_name, description, url), ...]}
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    repos = OrderedDict()
    current_repo = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('### ') and not stripped.startswith('### Notes'):
            current_repo = stripped[4:].strip()
            if current_repo not in repos:
                repos[current_repo] = []
            continue
        if stripped.startswith('| Skill') or stripped.startswith('|---'):
            continue
        if stripped.startswith('|') and current_repo is not None:
            cols = [c.strip() for c in stripped.split('|')]
            if len(cols) >= 7:
                skill_name = cols[1].strip()
                url = extract_url_from_cell(cols[3]) if len(cols) > 3 else ''
                func_explanation = cols[5].strip() if len(cols) > 5 else ''
                description = extract_first_sentence(func_explanation)
                if skill_name:
                    repos[current_repo].append((skill_name, description, url))

    return repos

def get_theme_key(filename):
    """Extract theme number from filename like '01_info..._part1.md' -> '01'."""
    basename = os.path.basename(filename)
    m = re.match(r'(\d{2})_', basename)
    return m.group(1) if m else '99'

def is_main_theme_file(filepath):
    """Filter to only main theme data files, excluding audit/consistency reports."""
    basename = os.path.basename(filepath).upper()
    exclude = ['AUDIT', 'CONSISTENCY', 'RELEVANCE', 'BACKUP', 'README']
    return not any(kw in basename for kw in exclude)

def load_audit_index(audit_path):
    """Load multidim_audit.json and build a lookup dict keyed by (skill_name, repo)."""
    with open(audit_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    index = {}
    for entry in data['results']:
        key = (entry['skill_name'], entry['repo'])
        index[key] = entry
    return index, data.get('metadata', {})

def main():
    theme_pattern = 'Final_Research_Skills_Thematic_Split/0*.md'
    audit_path = 'multidim_audit.json'
    output_path = 'SKILL_CATALOG.md'

    # Load audit index for filtering
    print('Loading multidim_audit.json...')
    audit_index, audit_meta = load_audit_index(audit_path)
    print('  Audit entries: %d' % len(audit_index))

    # Group files by theme (only main theme files)
    theme_files = OrderedDict()
    for filepath in sorted(glob.glob(theme_pattern)):
        if not is_main_theme_file(filepath):
            continue
        key = get_theme_key(filepath)
        if key not in theme_files:
            theme_files[key] = []
        theme_files[key].append(filepath)

    # Parse all theme files and filter by audit index
    all_themes = OrderedDict()
    total_skills = 0
    total_repos = set()
    skipped = 0

    for theme_key, files in theme_files.items():
        theme_repos = OrderedDict()
        for filepath in files:
            repos = parse_theme_file(filepath)
            for repo, skills in repos.items():
                filtered_skills = []
                for skill_name, description, url in skills:
                    key = (skill_name, repo)
                    if key in audit_index:
                        audit = audit_index[key]
                        tier = audit.get('research_tier', '?')
                        domain = audit.get('domain', '?')
                        value = audit.get('added_value', '?')
                        filtered_skills.append(
                            (skill_name, description, url, tier, domain, value)
                        )
                    else:
                        skipped += 1
                if filtered_skills:
                    if repo in theme_repos:
                        theme_repos[repo].extend(filtered_skills)
                    else:
                        theme_repos[repo] = list(filtered_skills)
                    total_repos.add(repo)
        all_themes[theme_key] = theme_repos
        theme_skill_count = sum(len(s) for s in theme_repos.values())
        total_skills += theme_skill_count

    print('  Total after filter: %d (skipped %d)' % (total_skills, skipped))

    # Generate catalog
    lines = []
    lines.append('# 科研技能目录 / Research Skills Catalog\n')
    lines.append(
        '\n> %s 个研究相关 Claude Code Skills（经多维审计），'
        '来自 %d 个 GitHub 仓库。\n' % ('{:,}'.format(total_skills), len(total_repos))
    )
    lines.append(
        '\n*自动生成于 %s，'
        '数据源：`Final_Research_Skills_Thematic_Split/0*.md` + '
        '`multidim_audit.json`*\n' % datetime.now().strftime("%Y-%m-%d")
    )

    # Summary table
    lines.append('\n## 统计概览\n')
    lines.append('\n| # | 主题 | 技能数 | 仓库数 |')
    lines.append('\n|---|------|--------|--------|')
    for theme_key, theme_repos in all_themes.items():
        name = THEME_NAMES.get(theme_key, 'Theme %s' % theme_key)
        skill_count = sum(len(s) for s in theme_repos.values())
        repo_count = len(theme_repos)
        lines.append('\n| %s | %s | %d | %d |' % (theme_key, name, skill_count, repo_count))
    lines.append(
        '\n| | **合计** | **%s** | **%d** |' % ('{:,}'.format(total_skills), len(total_repos))
    )
    lines.append('\n')

    # Per-theme sections
    for theme_key, theme_repos in all_themes.items():
        name = THEME_NAMES.get(theme_key, 'Theme %s' % theme_key)
        theme_skill_count = sum(len(s) for s in theme_repos.values())
        lines.append('\n---\n')
        lines.append('\n## %s %s (%d skills)\n' % (theme_key, name, theme_skill_count))

        for repo, skills in theme_repos.items():
            lines.append('\n### %s\n' % repo)
            lines.append('\n| Skill | Description | Tier | Domain | Value | URL |')
            lines.append('\n|-------|-------------|------|--------|-------|-----|')
            for skill_name, description, url, tier, domain, value in skills:
                desc_escaped = description.replace('|', '\\|')
                domain_escaped = domain.replace('|', '\\|')
                if url:
                    url_cell = '[link](%s)' % url
                else:
                    url_cell = ''
                lines.append(
                    '\n| %s | %s | %s | %s | %s | %s |' %
                    (skill_name, desc_escaped, tier, domain_escaped, value, url_cell)
                )
            lines.append('\n')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(lines))

    print('Generated %s' % output_path)
    print('  Total skills: %s' % '{:,}'.format(total_skills))
    print('  Total repos: %d' % len(total_repos))
    print('  Themes: %d' % len(all_themes))

if __name__ == '__main__':
    main()

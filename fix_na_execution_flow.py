"""
fix_na_execution_flow.py
[IN]  Final_Research_Skills_Thematic_Split/06_Additional_Scientific_Skills.md
      Final_Research_Skills_Link_Downloads_By_Theme_LATEST/ (local SKILL.md files)
[OUT] Updated 06_Additional_Scientific_Skills.md with Execution Flow extracted from SKILL.md body
[POS] One-shot fix script: replaces N/A Execution Flow by extracting workflow/pattern names
      from SKILL.md body text (Orchestra-Research, K-Dense-AI, Galaxy-Dawn formats)
"""

import os
import re

BASE_DIR = "e:/LLM/EDU+LLM/1/Good_Tools/research-skills"
DOWNLOAD_DIR = os.path.join(BASE_DIR, "Final_Research_Skills_Link_Downloads_By_Theme_LATEST")
THEME_FILE = os.path.join(BASE_DIR, "Final_Research_Skills_Thematic_Split", "06_Additional_Scientific_Skills.md")


def build_repo_dir_map():
    repo_map = {}
    for theme_dir in os.listdir(DOWNLOAD_DIR):
        theme_path = os.path.join(DOWNLOAD_DIR, theme_dir)
        if not os.path.isdir(theme_path):
            continue
        for repo_dir in os.listdir(theme_path):
            repo_path = os.path.join(theme_path, repo_dir)
            if not os.path.isdir(repo_path):
                continue
            if '__' in repo_dir:
                owner, repo = repo_dir.split('__', 1)
                repo_map[f"{owner}/{repo}"] = repo_path
    return repo_map


def extract_h3_under_section(content, section_pattern, max_items=4):
    """Extract ### headings under a ## section matching section_pattern"""
    items = []
    in_section = False
    for line in content.split('\n'):
        line = line.rstrip('\r')
        if re.match(section_pattern, line):
            in_section = True
            continue
        if in_section and line.startswith('## '):
            break
        if in_section and line.startswith('### '):
            name = line[4:].strip()
            # Remove leading numbers like "1. " or "1: "
            name = re.sub(r'^\d+[.:]\s*', '', name)
            # Remove markdown bold/italic
            name = re.sub(r'\*+', '', name).strip()
            if name:
                items.append(name)
    return items[:max_items]


def extract_workflows(skill_path, repo_name):
    """Extract workflow names from SKILL.md based on repo format"""
    try:
        content = open(skill_path, encoding='utf-8').read()
    except Exception:
        return []

    # Strategy 1: ## Common workflows/Workflows -> ### Workflow N: [name]
    workflows = []
    in_section = False
    for line in content.split('\n'):
        line = line.rstrip('\r')
        if re.match(r'^## Common [Ww]orkflows?$', line):
            in_section = True
            continue
        if in_section and line.startswith('## '):
            break
        if in_section:
            m = re.match(r'^### Workflow \d+:\s*(.+)', line)
            if m:
                workflows.append(m.group(1).strip())
    if workflows:
        return workflows[:4]

    # Strategy 2: ## Common patterns -> ### [Name] (no numbers)
    items = extract_h3_under_section(content, r'^## Common [Pp]atterns?$')
    if items:
        return items

    # Strategy 3: ## Using This Skill -> ### N. [Name] (K-Dense-AI format)
    items = extract_h3_under_section(content, r'^## Using This Skill$')
    if items:
        return items

    # Strategy 4: ## Core operations/concepts -> ### N. [Name]
    items = extract_h3_under_section(content, r'^## Core (operations|concepts|capabilities)$')
    if items:
        return items

    # Strategy 5: ## Quick start/Start -> ### [Name]
    items = extract_h3_under_section(content, r'^## Quick [Ss]tart$')
    if items:
        return items

    # Strategy 6: ## Training Strategies / ## Implementation Workflow -> ### [Name]
    items = extract_h3_under_section(content, r'^## (Training Strategies|Implementation Workflow)$')
    if items:
        return items

    # Strategy 7: ## Workflow N: at h2 level (e.g., ## Workflow 0: Starting from...)
    h2_workflows = re.findall(r'^## Workflow \d+:\s*(.+)', content, re.MULTILINE)
    if h2_workflows:
        return [w.strip() for w in h2_workflows[:4]]

    # Strategy 8: ## Framework N: at h2 level
    h2_frameworks = re.findall(r'^## Framework \d+:\s*(.+)', content, re.MULTILINE)
    if h2_frameworks:
        return [f.strip() for f in h2_frameworks[:4]]

    # Strategy 9: ## Core Ideation Frameworks / ## Core [X] -> ### N. [Name]
    items = extract_h3_under_section(content, r'^## Core .+$')
    if items:
        return items

    # Strategy 10: ## Working with This Skill -> ### [Name]
    items = extract_h3_under_section(content, r'^## Working with This Skill$')
    if items:
        return items

    # Strategy 11: ## Step-by-step procedure -> ### [Name]
    items = extract_h3_under_section(content, r'^## Step-by-step procedure$')
    if items:
        return items

    return []


def format_flow(workflows):
    if not workflows:
        return None
    parts = [f"Workflow{i+1}: {name}" for i, name in enumerate(workflows)]
    return ' -> '.join(parts)


def fix_na_rows(dry_run=False):
    repo_map = build_repo_dir_map()
    print(f"Repo map: {len(repo_map)} repos found")

    content = open(THEME_FILE, encoding='utf-8').read()
    lines = content.split('\n')

    current_repo = None
    updated = 0
    skipped = 0
    new_lines = []

    for line in lines:
        if line.startswith('### '):
            current_repo = line[4:].strip()
            new_lines.append(line)
            continue

        if not (line.startswith('|') and '| N/A |' in line):
            new_lines.append(line)
            continue

        parts = line.split('|')
        if len(parts) < 8:
            new_lines.append(line)
            skipped += 1
            continue

        evidence_path = parts[2].strip().strip('`')

        repo_dir = repo_map.get(current_repo)
        if not repo_dir:
            print(f"  SKIP (no local dir): {current_repo}")
            new_lines.append(line)
            skipped += 1
            continue

        skill_path = os.path.join(repo_dir, evidence_path)
        if not os.path.exists(skill_path):
            new_lines.append(line)
            skipped += 1
            continue

        workflows = extract_workflows(skill_path, current_repo)
        flow_text = format_flow(workflows)

        if not flow_text:
            print(f"  SKIP (no workflows): {evidence_path}")
            new_lines.append(line)
            skipped += 1
            continue

        new_line = line.replace('| N/A |', f'| {flow_text} |', 1)
        new_lines.append(new_line)
        updated += 1
        if dry_run:
            skill_name = parts[1].strip().strip('`')
            print(f"  UPDATED: {skill_name} -> {flow_text[:70]}")

    print(f"\nResults: {updated} updated, {skipped} skipped")

    if not dry_run:
        new_content = '\n'.join(new_lines)
        with open(THEME_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Written to {THEME_FILE}")

    return updated, skipped


if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        print("=== DRY RUN MODE ===")
    fix_na_rows(dry_run=dry_run)

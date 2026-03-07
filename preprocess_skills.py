"""
Pre-process all SKILL.md files in LATEST directory.
Creates a lookup table: {repo_name}/{relative_path} -> {description, use_cases}
This helps Update Agents efficiently find skill descriptions.
"""
import json
import re
from pathlib import Path

BASE_DIR = Path("e:/LLM/EDU+LLM/1/Good_Tools/research-skills")
LATEST_DIR = BASE_DIR / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"

def extract_yaml_description(content):
    """Extract description from YAML frontmatter."""
    # Match YAML frontmatter
    yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        return None
    yaml_content = yaml_match.group(1)
    # Extract description field (may be multi-line with | or >)
    desc_match = re.search(r'^description:\s*\|?\s*\n?(.*?)(?=\n\w|\Z)', yaml_content, re.DOTALL | re.MULTILINE)
    if desc_match:
        desc = desc_match.group(1).strip()
        # Clean up indentation
        lines = [l.strip() for l in desc.split('\n') if l.strip()]
        return ' '.join(lines)
    # Try inline description
    inline_match = re.search(r'^description:\s*(.+)$', yaml_content, re.MULTILINE)
    if inline_match:
        return inline_match.group(1).strip().strip('"\'')
    return None

def extract_when_to_apply(content):
    """Extract 'When to Apply' section."""
    match = re.search(r'##\s+When\s+to\s+(?:Apply|Use|Trigger)\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1).strip()
        # Get first 3 bullet points
        bullets = re.findall(r'[-*]\s+(.+)', text)
        return bullets[:3]
    return []

def process_skill_file(skill_path, repo_dir):
    """Process a single SKILL.md file."""
    try:
        content = skill_path.read_text(encoding='utf-8', errors='ignore')
        rel_path = skill_path.relative_to(repo_dir)
        description = extract_yaml_description(content)
        use_cases = extract_when_to_apply(content)
        # Also try to get name from YAML
        name_match = re.search(r'^name:\s*(.+)$', content[:500], re.MULTILINE)
        name = name_match.group(1).strip() if name_match else skill_path.parent.name
        return {
            'path': str(rel_path).replace('\\', '/'),
            'name': name,
            'description': description or '',
            'use_cases': use_cases,
        }
    except Exception as e:
        return None

def main():
    lookup = {}  # {repo_name: {relative_path: skill_info}}
    total = 0

    for theme_dir in sorted(LATEST_DIR.iterdir()):
        if not theme_dir.is_dir():
            continue
        for repo_dir in sorted(theme_dir.iterdir()):
            if not repo_dir.is_dir():
                continue
            # Convert dir name back to repo name: owner__repo -> owner/repo
            repo_name = repo_dir.name.replace('__', '/', 1)
            if repo_name not in lookup:
                lookup[repo_name] = {}

            for skill_file in repo_dir.rglob('SKILL.md'):
                info = process_skill_file(skill_file, repo_dir)
                if info:
                    lookup[repo_name][info['path']] = info
                    total += 1

    # Save lookup table
    output_path = BASE_DIR / "skill_lookup_20260227.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(lookup, f, indent=2, ensure_ascii=False)

    print(f"[OK] Skill lookup table saved: {output_path}")
    print(f"  Total repos: {len(lookup)}")
    print(f"  Total skills: {total}")

    # Print sample
    for repo, skills in list(lookup.items())[:2]:
        print(f"\n  {repo}: {len(skills)} skills")
        for path, info in list(skills.items())[:2]:
            print(f"    {path}: {info['description'][:80]}...")

if __name__ == "__main__":
    main()

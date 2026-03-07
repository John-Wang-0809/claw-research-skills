#!/usr/bin/env python3
"""
Generate download manifest from existing download directory structure.
"""
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def main():
    base_dir = Path("e:/LLM/EDU+LLM/1/Good_Tools/research-skills")
    old_download_dir = base_dir / "Final_Research_Skills_Link_Downloads_By_Theme"

    repos_by_theme = defaultdict(list)
    all_repos = {}

    # Scan existing download directory
    for theme_dir in old_download_dir.iterdir():
        if not theme_dir.is_dir() or theme_dir.name.startswith('_') or theme_dir.name == '06_Additional_Scientific_Skills':
            continue

        theme_name = theme_dir.name
        print(f"Scanning theme: {theme_name}")

        for repo_dir in theme_dir.iterdir():
            if not repo_dir.is_dir():
                continue

            # Convert directory name back to owner/repo format
            repo_name = repo_dir.name.replace('__', '/')

            # Count SKILL.md files
            skill_files = list(repo_dir.rglob('SKILL.md'))
            skills_count = len(skill_files)

            if repo_name not in all_repos:
                all_repos[repo_name] = {
                    'repo_name': repo_name,
                    'repo_url': f'https://github.com/{repo_name}',
                    'themes': [],
                    'skills_count': 0
                }

            all_repos[repo_name]['themes'].append(theme_name)
            all_repos[repo_name]['skills_count'] += skills_count
            repos_by_theme[theme_name].append(repo_name)

    # Generate download manifest
    manifest = {
        'generated_at': datetime.now().isoformat(),
        'total_repos': len(all_repos),
        'total_skills': sum(r['skills_count'] for r in all_repos.values()),
        'repos': []
    }

    for repo_name, repo_data in sorted(all_repos.items()):
        # Use the first theme for directory organization
        primary_theme = repo_data['themes'][0]
        target_dir = f"Final_Research_Skills_Link_Downloads_By_Theme_LATEST/{primary_theme}/{repo_name.replace('/', '__')}"

        manifest['repos'].append({
            'repo_name': repo_name,
            'repo_url': repo_data['repo_url'],
            'themes': repo_data['themes'],
            'skills_count': repo_data['skills_count'],
            'target_dir': target_dir
        })

    # Save manifest
    manifest_path = base_dir / "download_manifest_20260227.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Download manifest generated: {manifest_path}")
    print(f"  Total repos: {manifest['total_repos']}")
    print(f"  Total skills: {manifest['total_skills']}")
    print("\nRepos by theme:")
    for theme_name, repos in sorted(repos_by_theme.items()):
        print(f"  {theme_name}: {len(repos)} repos")

if __name__ == '__main__':
    main()

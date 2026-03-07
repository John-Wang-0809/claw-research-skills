#!/usr/bin/env python3
"""
Copy failed repos from old download directory to new directory.
"""
import json
import shutil
from pathlib import Path

def main():
    base_dir = Path("e:/LLM/EDU+LLM/1/Good_Tools/research-skills")
    old_dir = base_dir / "Final_Research_Skills_Link_Downloads_By_Theme"
    new_dir = base_dir / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"
    results_file = base_dir / "download_results_20260227.json"

    # Load download results
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # Get failed repos
    failed_repos = [r['repo'] for r in results['results'] if r['status'] == 'failed']

    print(f"Copying {len(failed_repos)} failed repos from old download directory...")
    print()

    copied_count = 0
    not_found_count = 0
    skill_count = 0

    for repo_name in failed_repos:
        repo_dir_name = repo_name.replace('/', '__')

        # Search for repo in old directory (across all themes)
        found = False
        for theme_dir in old_dir.iterdir():
            if not theme_dir.is_dir() or theme_dir.name.startswith('_'):
                continue

            old_repo_path = theme_dir / repo_dir_name
            if old_repo_path.exists():
                # Determine target theme from new directory structure
                # Use the same theme as in old directory
                new_theme_dir = new_dir / theme_dir.name
                new_theme_dir.mkdir(parents=True, exist_ok=True)

                new_repo_path = new_theme_dir / repo_dir_name

                if not new_repo_path.exists():
                    # Copy entire repo directory
                    shutil.copytree(old_repo_path, new_repo_path)

                    # Count SKILL.md files
                    skills = list(new_repo_path.rglob('SKILL.md'))
                    skill_count += len(skills)

                    print(f"[OK] {repo_name} -> {theme_dir.name} ({len(skills)} SKILL.md files)")
                    copied_count += 1
                    found = True
                    break
                else:
                    print(f"[SKIP] {repo_name} - already exists in new directory")
                    found = True
                    break

        if not found:
            print(f"[NOT FOUND] {repo_name} - not in old directory")
            not_found_count += 1

    print()
    print("=" * 80)
    print(f"Copy completed:")
    print(f"  Copied: {copied_count}")
    print(f"  Not found: {not_found_count}")
    print(f"  Total SKILL.md files copied: {skill_count}")
    print(f"  Total SKILL.md files (new + old): {results['total_skills'] + skill_count}")

if __name__ == '__main__':
    main()

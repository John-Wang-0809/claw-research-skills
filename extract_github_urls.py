#!/usr/bin/env python3
"""
Extract GitHub URLs from theme documents and generate download manifest.
"""
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Theme document files
THEME_FILES = [
    "01_information_retrieval_evidence_collection.md",
    "02_literature_review_writing_citation_part1.md",
    "02_literature_review_writing_citation_part2.md",
    "03_experiment_benchmark_reproducibility_validation_part1.md",
    "03_experiment_benchmark_reproducibility_validation_part2.md",
    "04_data_analysis_and_evidence_interpretation.md",
    "05_research_operations_and_workflow_support.md",
]

# Map part files to their theme
THEME_MAP = {
    "01_information_retrieval_evidence_collection.md": "01_information_retrieval_evidence_collection",
    "02_literature_review_writing_citation_part1.md": "02_literature_review_writing_citation",
    "02_literature_review_writing_citation_part2.md": "02_literature_review_writing_citation",
    "03_experiment_benchmark_reproducibility_validation_part1.md": "03_experiment_benchmark_reproducibility_validation",
    "03_experiment_benchmark_reproducibility_validation_part2.md": "03_experiment_benchmark_reproducibility_validation",
    "04_data_analysis_and_evidence_interpretation.md": "04_data_analysis_and_evidence_interpretation",
    "05_research_operations_and_workflow_support.md": "05_research_operations_and_workflow_support",
}

def extract_repo_from_url(url):
    """Extract owner/repo from GitHub URL."""
    match = re.search(r'github\.com/([^/]+/[^/]+)', url)
    if match:
        return match.group(1).rstrip('.git')
    return None

def parse_theme_document(file_path):
    """Parse theme document and extract GitHub URLs."""
    repos = {}
    current_repo = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Match repository header: ### owner/repo
            repo_match = re.match(r'^###\s+([^/]+/[^/\s]+)', line)
            if repo_match:
                current_repo = repo_match.group(1)
                if current_repo not in repos:
                    repos[current_repo] = {
                        'repo_name': current_repo,
                        'repo_url': f'https://github.com/{current_repo}',
                        'skills': []
                    }

            # Match skill rows in table (contains GitHub URL)
            if '| ' in line and 'github.com' in line:
                # Extract skill name (first column)
                parts = line.split('|')
                if len(parts) >= 2:
                    skill_name = parts[1].strip()
                    if skill_name and skill_name != 'Skill' and skill_name != '---':
                        if current_repo and skill_name not in repos[current_repo]['skills']:
                            repos[current_repo]['skills'].append(skill_name)

    return repos

def main():
    base_dir = Path("e:/LLM/EDU+LLM/1/Good_Tools/research-skills")
    theme_dir = base_dir / "Final_Research_Skills_Thematic_Split"

    all_repos = {}
    theme_stats = defaultdict(lambda: {'repos': set(), 'skills': 0})

    print("Extracting GitHub URLs from theme documents...")

    for theme_file in THEME_FILES:
        file_path = theme_dir / theme_file
        if not file_path.exists():
            print(f"Warning: {theme_file} not found")
            continue

        theme_name = THEME_MAP[theme_file]
        print(f"Processing {theme_file} (theme: {theme_name})...")

        repos = parse_theme_document(file_path)

        for repo_name, repo_data in repos.items():
            if repo_name not in all_repos:
                all_repos[repo_name] = {
                    'repo_name': repo_name,
                    'repo_url': repo_data['repo_url'],
                    'themes': [],
                    'skills_count': 0
                }

            all_repos[repo_name]['themes'].append(theme_name)
            all_repos[repo_name]['skills_count'] += len(repo_data['skills'])

            theme_stats[theme_name]['repos'].add(repo_name)
            theme_stats[theme_name]['skills'] += len(repo_data['skills'])

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
    for theme_name, stats in sorted(theme_stats.items()):
        print(f"  {theme_name}: {len(stats['repos'])} repos, {stats['skills']} skills")

if __name__ == '__main__':
    main()

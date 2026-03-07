"""
Create filtered lookup tables for each theme document.
Each filtered table only contains repos that appear in that theme document.
"""
import json
import re
from pathlib import Path

BASE_DIR = Path("e:/LLM/EDU+LLM/1/Good_Tools/research-skills")
THEME_DIR = BASE_DIR / "Final_Research_Skills_Thematic_Split"

THEME_FILES = [
    "01_information_retrieval_evidence_collection.md",
    "02_literature_review_writing_citation_part1.md",
    "02_literature_review_writing_citation_part2.md",
    "03_experiment_benchmark_reproducibility_validation_part1.md",
    "03_experiment_benchmark_reproducibility_validation_part2.md",
    "04_data_analysis_and_evidence_interpretation.md",
    "05_research_operations_and_workflow_support.md",
    "06_Additional_Scientific_Skills.md",
]

def extract_repos_from_theme(file_path):
    """Extract all repo names from a theme document."""
    repos = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^###\s+([^/\s]+/[^/\s]+)', line)
            if match:
                repos.add(match.group(1))
    return repos

def main():
    # Load full lookup table
    with open(BASE_DIR / "skill_lookup_20260227.json", 'r', encoding='utf-8') as f:
        full_lookup = json.load(f)

    for theme_file in THEME_FILES:
        file_path = THEME_DIR / theme_file
        if not file_path.exists():
            print(f"Warning: {theme_file} not found")
            continue

        repos = extract_repos_from_theme(file_path)
        filtered = {repo: full_lookup[repo] for repo in repos if repo in full_lookup}
        missing = repos - set(full_lookup.keys())

        # Save filtered lookup
        output_name = theme_file.replace('.md', '_lookup.json')
        output_path = BASE_DIR / output_name
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(filtered, f, indent=2, ensure_ascii=False)

        print(f"{theme_file}:")
        print(f"  Repos in doc: {len(repos)}, in lookup: {len(filtered)}, missing: {len(missing)}")
        if missing:
            print(f"  Missing repos: {missing}")

if __name__ == "__main__":
    main()

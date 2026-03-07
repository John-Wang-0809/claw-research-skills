"""
Re-download 3 repos that have SKILL.md files but failed due to Windows path length.
Strategy: Clone to short temp path, then copy only SKILL.md files to target.
"""
import subprocess
import shutil
import tempfile
from pathlib import Path

BASE_DIR = Path("e:/LLM/EDU+LLM/1/Good_Tools/research-skills")
LATEST_DIR = BASE_DIR / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"

REPOS = [
    {
        "repo": "Shubhamsaboo/awesome-llm-apps",
        "url": "https://github.com/Shubhamsaboo/awesome-llm-apps",
        "target": LATEST_DIR / "01_information_retrieval_evidence_collection" / "Shubhamsaboo__awesome-llm-apps",
    },
    {
        "repo": "ahmedibrahim085/Claude-Multi-Agent-Research-System-Skill",
        "url": "https://github.com/ahmedibrahim085/Claude-Multi-Agent-Research-System-Skill",
        "target": LATEST_DIR / "01_information_retrieval_evidence_collection" / "ahmedibrahim085__Claude-Multi-Agent-Research-System-Skill",
    },
    {
        "repo": "coffeefuelbump/csv-data-summarizer-claude-skill",
        "url": "https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill",
        "target": LATEST_DIR / "03_experiment_benchmark_reproducibility_validation" / "coffeefuelbump__csv-data-summarizer-claude-skill",
    },
]

def redownload_repo(repo_info):
    repo = repo_info["repo"]
    url = repo_info["url"]
    target = repo_info["target"]

    print(f"\n[START] {repo}")

    # Clone to short temp path
    with tempfile.TemporaryDirectory(prefix="skill_") as tmp_dir:
        tmp_path = Path(tmp_dir) / "repo"
        print(f"  Cloning to temp: {tmp_path}")

        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(tmp_path)],
            capture_output=True, text=True, timeout=300
        )

        if result.returncode != 0:
            print(f"  [FAIL] Clone failed: {result.stderr[:300]}")
            return 0

        # Find all SKILL.md files in temp clone
        skill_files = list(tmp_path.rglob("SKILL.md"))
        print(f"  Found {len(skill_files)} SKILL.md files in temp clone")

        if not skill_files:
            print(f"  [SKIP] No SKILL.md files found")
            return 0

        # Clear target directory (keep it, just remove contents)
        if target.exists():
            subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(target)], capture_output=True)
        target.mkdir(parents=True, exist_ok=True)

        # Copy SKILL.md files preserving relative structure
        copied = 0
        for skill_file in skill_files:
            rel_path = skill_file.relative_to(tmp_path)
            dest = target / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(skill_file, dest)
            print(f"    Copied: {rel_path}")
            copied += 1

        print(f"  [OK] Copied {copied} SKILL.md files to {target}")
        return copied

def main():
    print("Re-downloading 3 failed repos (clone to temp, copy SKILL.md)...")
    total = 0
    for repo_info in REPOS:
        count = redownload_repo(repo_info)
        total += count
    print(f"\n[DONE] Total SKILL.md files recovered: {total}")

if __name__ == "__main__":
    main()

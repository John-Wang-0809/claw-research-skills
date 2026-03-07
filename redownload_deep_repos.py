"""
Try to re-download 3 repos that have 0 SKILL.md in both old and new downloads.
These repos have deeply nested SKILL.md files that may have been missed.
"""
import subprocess
import shutil
import tempfile
from pathlib import Path

BASE_DIR = Path("e:/LLM/EDU+LLM/1/Good_Tools/research-skills")
LATEST_DIR = BASE_DIR / "Final_Research_Skills_Link_Downloads_By_Theme_LATEST"

REPOS = [
    {
        "repo": "danielmiessler/Personal_AI_Infrastructure",
        "url": "https://github.com/danielmiessler/Personal_AI_Infrastructure",
        "targets": [
            LATEST_DIR / "01_information_retrieval_evidence_collection" / "danielmiessler__Personal_AI_Infrastructure",
            LATEST_DIR / "02_literature_review_writing_citation" / "danielmiessler__Personal_AI_Infrastructure",
            LATEST_DIR / "03_experiment_benchmark_reproducibility_validation" / "danielmiessler__Personal_AI_Infrastructure",
        ],
    },
    {
        "repo": "HKUDS/DeepCode",
        "url": "https://github.com/HKUDS/DeepCode",
        "targets": [
            LATEST_DIR / "02_literature_review_writing_citation" / "HKUDS__DeepCode",
        ],
    },
    {
        "repo": "Dr-AneeshJoseph/Claude-Metacognitive-Skills",
        "url": "https://github.com/Dr-AneeshJoseph/Claude-Metacognitive-Skills",
        "targets": [
            LATEST_DIR / "03_experiment_benchmark_reproducibility_validation" / "Dr-AneeshJoseph__Claude-Metacognitive-Skills",
        ],
    },
]

def try_clone_repo(repo_info):
    repo = repo_info["repo"]
    url = repo_info["url"]
    targets = repo_info["targets"]

    print(f"\n[START] {repo}")

    with tempfile.TemporaryDirectory(prefix="skill_deep_") as tmp_dir:
        tmp_path = Path(tmp_dir) / "repo"
        print(f"  Cloning to temp: {tmp_path}")

        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(tmp_path)],
            capture_output=True, text=True, timeout=600
        )

        if result.returncode != 0:
            print(f"  [FAIL] Clone failed: {result.stderr[:300]}")
            return 0

        skill_files = list(tmp_path.rglob("SKILL.md"))
        print(f"  Found {len(skill_files)} SKILL.md files in temp clone")

        if not skill_files:
            print(f"  [CONFIRMED] No SKILL.md files in this repo")
            return 0

        # Copy to all target directories
        for target in targets:
            if target.exists():
                subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(target)], capture_output=True)
            target.mkdir(parents=True, exist_ok=True)

            copied = 0
            for skill_file in skill_files:
                rel_path = skill_file.relative_to(tmp_path)
                dest = target / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(skill_file, dest)
                copied += 1

            print(f"  [OK] Copied {copied} SKILL.md to {target.name}")

        return len(skill_files)

def main():
    print("Attempting to re-download 3 deeply-nested repos...")
    total = 0
    for repo_info in REPOS:
        count = try_clone_repo(repo_info)
        total += count
    print(f"\n[DONE] Total SKILL.md files recovered: {total}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Deduplicate danielmiessler repository.

This script:
1. Identifies the 3 copies of danielmiessler/Personal_AI_Infrastructure
2. Keeps the theme 01 copy (primary)
3. Deletes theme 02 and theme 03 copies
4. Creates symbolic links in theme 02 and theme 03 pointing to theme 01
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Configuration
BASE_DIR = Path("Final_Research_Skills_Link_Downloads_By_Theme_LATEST")
REPO_DIR_NAME = "danielmiessler__Personal_AI_Infrastructure"

THEME_DIRS = {
    "01": BASE_DIR / "01_information_retrieval_evidence_collection",
    "02": BASE_DIR / "02_literature_review_writing_citation",
    "03": BASE_DIR / "03_experiment_benchmark_reproducibility_validation",
}

def check_repo_exists(theme_dir):
    """Check if danielmiessler repo exists in a theme directory."""
    repo_path = theme_dir / REPO_DIR_NAME
    return repo_path.exists()

def delete_directory(dir_path):
    """Delete a directory using Windows rmdir command."""
    try:
        # Use Windows rmdir /s /q for reliable deletion
        result = subprocess.run(
            ["cmd", "/c", "rmdir", "/s", "/q", str(dir_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"[OK] Deleted directory: {dir_path}")
            return True
        else:
            print(f"[FAIL] Failed to delete: {result.stderr}")
            return False
    except Exception as e:
        print(f"[FAIL] Error deleting directory: {e}")
        return False

def create_symbolic_link(source_path, target_path):
    """Create a symbolic link for a repository directory."""
    try:
        # Try symlink first (requires admin or developer mode)
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/D", str(target_path), str(source_path)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"[OK] Created symbolic link: {target_path} -> {source_path}")
            return True
        else:
            # If symlink fails, try junction (doesn't require admin)
            print(f"  Symlink failed, trying junction...")
            result = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(target_path), str(source_path)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"[OK] Created junction: {target_path} -> {source_path}")
                return True
            else:
                print(f"[FAIL] Failed to create link: {result.stderr}")
                return False
    except Exception as e:
        print(f"[FAIL] Error creating link: {e}")
        return False

def main():
    """Main execution function."""
    print("=" * 60)
    print("Deduplicate danielmiessler Repository")
    print("=" * 60)

    # Step 1: Check which copies exist
    print("\n[Step 1] Checking danielmiessler repo copies...")
    copies = {}
    for theme_id, theme_dir in THEME_DIRS.items():
        repo_path = theme_dir / REPO_DIR_NAME
        exists = check_repo_exists(theme_dir)
        copies[theme_id] = {"path": repo_path, "exists": exists}
        status = "[OK] Found" if exists else "[FAIL] Not found"
        print(f"  Theme {theme_id}: {status} at {repo_path}")

    # Verify theme 01 exists (primary copy)
    if not copies["01"]["exists"]:
        print("\n[FAIL] Error: Primary copy (theme 01) not found!")
        return 1

    primary_path = copies["01"]["path"]
    print(f"\n[OK] Primary copy confirmed: {primary_path}")

    # Step 2: Delete theme 02 and 03 copies
    print("\n[Step 2] Deleting duplicate copies...")
    for theme_id in ["02", "03"]:
        if copies[theme_id]["exists"]:
            print(f"\nDeleting theme {theme_id} copy...")
            if not delete_directory(copies[theme_id]["path"]):
                print(f"[FAIL] Failed to delete theme {theme_id} copy")
                return 1
        else:
            print(f"  Theme {theme_id}: Already deleted or not found")

    # Step 3: Create symbolic links
    print("\n[Step 3] Creating symbolic links...")
    success_count = 0
    for theme_id in ["02", "03"]:
        target_path = copies[theme_id]["path"]
        print(f"\nCreating link for theme {theme_id}...")
        if create_symbolic_link(primary_path, target_path):
            success_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Primary copy: {primary_path}")
    print(f"Symbolic links created: {success_count}/2")

    if success_count == 2:
        print("\n[OK] Deduplication completed successfully!")
        return 0
    else:
        print("\n[FAIL] Some symbolic links failed to create")
        return 1

if __name__ == "__main__":
    sys.exit(main())
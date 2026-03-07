#!/usr/bin/env python3
"""
Fix directory structure: Create theme 05 directory and symbolic links.

This script:
1. Reads the theme 05 lookup file to get the list of 10 repos
2. Creates the theme 05 directory
3. Creates symbolic links for the 10 repos (source: theme 01, target: theme 05)
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Configuration
BASE_DIR = Path("Final_Research_Skills_Link_Downloads_By_Theme_LATEST")
THEME_01_DIR = BASE_DIR / "01_information_retrieval_evidence_collection"
THEME_05_DIR = BASE_DIR / "05_research_operations_and_workflow_support"
LOOKUP_FILE = Path("05_research_operations_and_workflow_support_lookup.json")

def load_theme_05_repos():
    """Load the list of repos from theme 05 lookup file."""
    with open(LOOKUP_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return list(data.keys())

def create_theme_05_directory():
    """Create the theme 05 directory if it doesn't exist."""
    if not THEME_05_DIR.exists():
        THEME_05_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Created directory: {THEME_05_DIR}")
    else:
        print(f"[OK] Directory already exists: {THEME_05_DIR}")

def create_symbolic_link(repo_name, source_dir, target_dir):
    """Create a symbolic link for a repository directory."""
    # Convert repo name to directory name (replace / with __)
    dir_name = repo_name.replace('/', '__')

    source_path = source_dir / dir_name
    target_path = target_dir / dir_name

    # Check if source exists
    if not source_path.exists():
        print(f"[FAIL] Source not found: {source_path}")
        return False

    # Check if target already exists
    if target_path.exists():
        if target_path.is_symlink():
            print(f"[OK] Symbolic link already exists: {target_path}")
            return True
        else:
            print(f"[FAIL] Target exists but is not a symlink: {target_path}")
            return False

    # Create symbolic link using mklink /D (directory junction)
    # Use relative path to avoid absolute path issues
    rel_source = os.path.relpath(source_path, target_path.parent)

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
    print("Fix Directory Structure: Create Theme 05 Directory")
    print("=" * 60)

    # Step 1: Load theme 05 repos
    print("\n[Step 1] Loading theme 05 repos from lookup file...")
    repos = load_theme_05_repos()
    print(f"[OK] Found {len(repos)} repos in theme 05")

    # Step 2: Create theme 05 directory
    print("\n[Step 2] Creating theme 05 directory...")
    create_theme_05_directory()

    # Step 3: Create symbolic links
    print("\n[Step 3] Creating symbolic links for theme 05 repos...")
    success_count = 0
    failed_repos = []

    for repo_name in repos:
        print(f"\nProcessing: {repo_name}")
        if create_symbolic_link(repo_name, THEME_01_DIR, THEME_05_DIR):
            success_count += 1
        else:
            failed_repos.append(repo_name)

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total repos: {len(repos)}")
    print(f"Success: {success_count}")
    print(f"Failed: {len(failed_repos)}")

    if failed_repos:
        print("\nFailed repos:")
        for repo in failed_repos:
            print(f"  - {repo}")
        return 1
    else:
        print("\n[OK] All symbolic links created successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(main())

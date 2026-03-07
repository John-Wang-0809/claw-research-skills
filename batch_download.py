#!/usr/bin/env python3
"""
Batch download latest SKILL.md files from GitHub repositories.
Supports parallel downloading and resume from interruption.
"""
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def clone_repo(repo_data, base_dir, log_file):
    """Clone a single repository using git clone --depth 1."""
    repo_name = repo_data['repo_name']
    repo_url = repo_data['repo_url']
    target_dir = base_dir / repo_data['target_dir']

    # Skip if already downloaded
    if target_dir.exists() and list(target_dir.rglob('SKILL.md')):
        msg = f"[SKIP] {repo_name} - already exists"
        print(msg)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} {msg}\n")
        return {'status': 'skipped', 'repo': repo_name, 'reason': 'already_exists'}

    # Create parent directory
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    # Clone repository
    start_time = time.time()
    try:
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', repo_url, str(target_dir)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )

        elapsed = time.time() - start_time

        if result.returncode == 0:
            # Count SKILL.md files
            skill_files = list(target_dir.rglob('SKILL.md'))
            msg = f"[OK] {repo_name} - {len(skill_files)} SKILL.md files ({elapsed:.1f}s)"
            print(msg)
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().isoformat()} {msg}\n")
            return {'status': 'success', 'repo': repo_name, 'skills_count': len(skill_files), 'elapsed': elapsed}
        else:
            error_msg = result.stderr.strip()
            msg = f"[FAIL] {repo_name} - {error_msg[:100]}"
            print(msg)
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().isoformat()} {msg}\n")
                f.write(f"  stderr: {result.stderr}\n")
            return {'status': 'failed', 'repo': repo_name, 'error': error_msg}

    except subprocess.TimeoutExpired:
        msg = f"[TIMEOUT] {repo_name} - exceeded 5 minutes"
        print(msg)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} {msg}\n")
        # Clean up partial download
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
        return {'status': 'timeout', 'repo': repo_name}

    except Exception as e:
        msg = f"[ERROR] {repo_name} - {str(e)}"
        print(msg)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} {msg}\n")
        return {'status': 'error', 'repo': repo_name, 'error': str(e)}

def main():
    base_dir = Path("e:/LLM/EDU+LLM/1/Good_Tools/research-skills")
    manifest_path = base_dir / "download_manifest_20260227.json"
    log_file = base_dir / "download_log_20260227.txt"

    # Load manifest
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    repos = manifest['repos']
    total_repos = len(repos)

    print(f"Starting download of {total_repos} repositories...")
    print(f"Log file: {log_file}")
    print(f"Parallel workers: 5")
    print()

    # Initialize log file
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Download started at: {datetime.now().isoformat()}\n")
        f.write(f"Total repos: {total_repos}\n")
        f.write(f"Parallel workers: 5\n")
        f.write("-" * 80 + "\n")

    # Download repositories in parallel
    results = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(clone_repo, repo, base_dir, log_file): repo for repo in repos}

        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            print(f"Progress: {i}/{total_repos} ({i*100//total_repos}%)")

    elapsed_total = time.time() - start_time

    # Generate summary
    success_count = sum(1 for r in results if r['status'] == 'success')
    skipped_count = sum(1 for r in results if r['status'] == 'skipped')
    failed_count = sum(1 for r in results if r['status'] in ['failed', 'timeout', 'error'])
    total_skills = sum(r.get('skills_count', 0) for r in results if r['status'] == 'success')

    print()
    print("=" * 80)
    print(f"Download completed in {elapsed_total/60:.1f} minutes")
    print(f"  Success: {success_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total SKILL.md files: {total_skills}")
    print(f"  Success rate: {(success_count+skipped_count)*100//total_repos}%")

    # Write summary to log
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("-" * 80 + "\n")
        f.write(f"Download completed at: {datetime.now().isoformat()}\n")
        f.write(f"Total time: {elapsed_total/60:.1f} minutes\n")
        f.write(f"Success: {success_count}, Skipped: {skipped_count}, Failed: {failed_count}\n")
        f.write(f"Total SKILL.md files: {total_skills}\n")

    # Save results
    results_path = base_dir / "download_results_20260227.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump({
            'completed_at': datetime.now().isoformat(),
            'total_repos': total_repos,
            'success': success_count,
            'skipped': skipped_count,
            'failed': failed_count,
            'total_skills': total_skills,
            'elapsed_minutes': elapsed_total / 60,
            'results': results
        }, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to: {results_path}")

if __name__ == '__main__':
    main()

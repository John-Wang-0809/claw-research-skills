"""
URL reachability checker for research-skills audit.
Parses the markdown table, extracts skill URLs, checks reachability,
cross-checks evidence file paths, and writes results to JSON.
"""

import re
import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, unquote

MD_PATH = r"E:\LLM\EDU+LLM\1\Good_Tools\research-skills\Final_Research_Skills_Thematic_Split\01_information_retrieval_evidence_collection.md"
OUTPUT_PATH = r"E:\LLM\EDU+LLM\1\Good_Tools\research-skills\url_check_results.json"

HEADERS = {"User-Agent": "research-skills-audit/1.0"}
TIMEOUT = 10
MAX_WORKERS = 4
MAX_RETRIES = 5

def parse_skills(md_path):
    """Parse all skill rows from the markdown file."""
    skills = []
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match table rows with skill data
    # Pattern: | skill_name | `evidence_file_path` | [link](URL) | ...
    row_pattern = re.compile(
        r'^\|\s*(.+?)\s*\|\s*`(.+?)`\s*\|\s*\[link\]\((https://[^)]+)\)\s*\|',
        re.MULTILINE
    )

    for match in row_pattern.finditer(content):
        skill_name = match.group(1).strip()
        evidence_file = match.group(2).strip()
        url = match.group(3).strip()
        skills.append({
            "skill": skill_name,
            "evidence_file": evidence_file,
            "url": url
        })

    return skills


def check_url(skill_entry):
    """Check a single URL with HEAD/GET and retry transient failures."""
    url = skill_entry["url"]
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.head(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
            if resp.status_code in (403, 405, 429) or 500 <= resp.status_code < 600:
                resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True, stream=True)
            if resp.status_code == 429 or 500 <= resp.status_code < 600:
                wait = 2 ** (attempt + 1)
                time.sleep(wait)
                continue
            return {**skill_entry, "status_code": resp.status_code}
        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
                continue
            return {**skill_entry, "status_code": 0, "error": str(e)}
    return {**skill_entry, "status_code": 429, "error": "Rate limited after retries"}


def cross_check_path(skill_entry):
    """Check if evidence_file matches the URL path after blob/{branch}/."""
    url = skill_entry["url"]
    evidence_file = skill_entry["evidence_file"]

    # Extract path after blob/{branch}/ from GitHub URL
    # e.g., https://github.com/owner/repo/blob/main/path/to/SKILL.md
    blob_match = re.search(r'/blob/[^/]+/(.+)$', url)
    if not blob_match:
        return {
            "skill": skill_entry["skill"],
            "evidence_file": evidence_file,
            "url_path": "(could not extract)",
            "url": url,
            "mismatch": True
        }

    url_path = unquote(blob_match.group(1))

    # Normalize: strip leading ./ or / from evidence_file
    norm_evidence = evidence_file.lstrip("./")
    norm_url = url_path.lstrip("./")

    if norm_evidence != norm_url:
        return {
            "skill": skill_entry["skill"],
            "evidence_file": evidence_file,
            "url_path": url_path,
            "url": url,
            "mismatch": True
        }
    return None


def main():
    print("Parsing skills from markdown...")
    skills = parse_skills(MD_PATH)
    print(f"Found {len(skills)} skill URLs to check.")

    # Cross-check paths
    print("Cross-checking evidence file paths vs URL paths...")
    path_mismatches = []
    for s in skills:
        result = cross_check_path(s)
        if result:
            path_mismatches.append(result)
    print(f"Path mismatches found: {len(path_mismatches)}")

    # Check URLs concurrently
    print(f"Checking URL reachability with {MAX_WORKERS} workers...")
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_url, s): s for s in skills}
        done_count = 0
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            done_count += 1
            if done_count % 20 == 0:
                print(f"  Checked {done_count}/{len(skills)}...")

    print(f"  Checked {len(results)}/{len(skills)} complete.")

    # Classify results
    reachable = [r for r in results if 200 <= r.get("status_code", 0) < 400]
    unreachable = [r for r in results if not (200 <= r.get("status_code", 0) < 400)]

    unreachable_details = [
        {"skill": r["skill"], "url": r["url"], "status_code": r["status_code"]}
        for r in unreachable
    ]

    mismatch_details = [
        {"skill": m["skill"], "evidence_file": m["evidence_file"],
         "url_path": m["url_path"], "url": m["url"]}
        for m in path_mismatches
    ]

    output = {
        "total_urls": len(skills),
        "reachable": len(reachable),
        "unreachable": len(unreachable),
        "path_mismatches": len(path_mismatches),
        "unreachable_urls": unreachable_details,
        "path_mismatch_details": mismatch_details
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nResults written to {OUTPUT_PATH}")
    print(f"  Total URLs:       {output['total_urls']}")
    print(f"  Reachable:        {output['reachable']}")
    print(f"  Unreachable:      {output['unreachable']}")
    print(f"  Path mismatches:  {output['path_mismatches']}")

    if unreachable_details:
        print("\nUnreachable URLs:")
        for u in unreachable_details:
            print(f"  [{u['status_code']}] {u['skill']}: {u['url']}")

    if mismatch_details:
        print(f"\nPath mismatch details ({len(mismatch_details)} total):")
        for m in mismatch_details[:10]:
            print(f"  Skill: {m['skill']}")
            print(f"    Evidence: {m['evidence_file']}")
            print(f"    URL path: {m['url_path']}")
        if len(mismatch_details) > 10:
            print(f"  ... and {len(mismatch_details) - 10} more")


if __name__ == "__main__":
    main()

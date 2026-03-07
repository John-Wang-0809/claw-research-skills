"""
[IN]  Dependencies/Inputs:
 - plans/5a_audit_results.json (5a audit decisions)
 - plans/5b_audit_results.json (5b audit decisions)
 - multidim_audit.json.bak.phase5a (backup with all original entries)
 - dedup_results.json.bak.phase5a (backup dedup data)
 - multidim_audit.json (current data to restore into)
 - dedup_results.json (current dedup data to restore into)
[OUT] Outputs:
 - Updated multidim_audit.json with restored entries
 - Updated dedup_results.json with restored entries
 - Console summary of changes
[POS] Position in the system:
 - One-time restoration script for Phase 5 remediation
 - Reads audit decisions and applies them to current data files
"""

import json
import sys
from datetime import datetime


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {path}")


def main():
    # Load audit results
    try:
        results_5a = load_json('plans/5a_audit_results.json')
    except FileNotFoundError:
        print("ERROR: plans/5a_audit_results.json not found. Run 5a audit first.")
        sys.exit(1)

    try:
        results_5b = load_json('plans/5b_audit_results.json')
    except FileNotFoundError:
        print("ERROR: plans/5b_audit_results.json not found. Run 5b audit first.")
        sys.exit(1)

    # Collect entries to restore
    restore_keys = set()

    for r in results_5a:
        if r['decision'] == 'restore':
            restore_keys.add((r['skill_name'], r['repo']))

    for r in results_5b:
        if r['decision'] == 'restore':
            restore_keys.add((r['skill_name'], r['repo']))

    print(f"\n=== Restoration Summary ===")
    print(f"5a entries to restore: {sum(1 for r in results_5a if r['decision'] == 'restore')}")
    print(f"5b entries to restore: {sum(1 for r in results_5b if r['decision'] == 'restore')}")
    print(f"Total unique keys to restore: {len(restore_keys)}")

    if not restore_keys:
        print("\nNo entries to restore. All deletions confirmed correct.")
        return

    print("\nEntries to restore:")
    for sk, repo in sorted(restore_keys):
        # Find the entry details
        detail = None
        for r in results_5a + results_5b:
            if r['skill_name'] == sk and r['repo'] == repo and r['decision'] == 'restore':
                detail = r
                break
        reason = detail.get('reason', 'N/A') if detail else 'N/A'
        print(f"  - {sk} ({repo}): {reason}")

    # Load backup data
    bak_audit = load_json('multidim_audit.json.bak.phase5a')
    bak_dedup = load_json('dedup_results.json.bak.phase5a')

    # Load current data
    cur_audit = load_json('multidim_audit.json')
    cur_dedup = load_json('dedup_results.json')

    # Find entries to restore from backup
    cur_audit_keys = {(r['skill_name'], r['repo']) for r in cur_audit['results']}

    # Restore to multidim_audit.json
    restored_audit = []
    for r in bak_audit['results']:
        key = (r['skill_name'], r['repo'])
        if key in restore_keys and key not in cur_audit_keys:
            restored_audit.append(r)

    if restored_audit:
        cur_audit['results'].extend(restored_audit)
        # Update metadata
        cur_audit['metadata']['total_entries'] = len(cur_audit['results'])
        cur_audit['metadata']['restored_at'] = datetime.now().isoformat()
        cur_audit['metadata']['restored_count'] = len(restored_audit)
        save_json('multidim_audit.json', cur_audit)
        print(f"\nRestored {len(restored_audit)} entries to multidim_audit.json")
        print(f"New total: {len(cur_audit['results'])} entries")

    # Restore to dedup_results.json
    cur_dedup_keys = {(r['skill_name'], r['repo']) for r in cur_dedup['results']}

    restored_dedup = []
    for r in bak_dedup['results']:
        key = (r['skill_name'], r['repo'])
        if key in restore_keys and key not in cur_dedup_keys:
            restored_dedup.append(r)

    if restored_dedup:
        cur_dedup['results'].extend(restored_dedup)
        cur_dedup['total_skills'] = len(cur_dedup['results'])
        save_json('dedup_results.json', cur_dedup)
        print(f"Restored {len(restored_dedup)} entries to dedup_results.json")
        print(f"New total: {len(cur_dedup['results'])} entries")

    print(f"\n=== Done ===")
    print(f"Next steps:")
    print(f"  1. Run: python normalize_domains.py  (apply domain rules to restored entries)")
    print(f"  2. Run: python generate_catalog.py  (regenerate catalogs)")
    print(f"  3. Run: python build_relevance_page.py  (regenerate review page)")
    print(f"  4. Run: python credibility_audit.py  (verify 0 polluted)")


if __name__ == '__main__':
    main()

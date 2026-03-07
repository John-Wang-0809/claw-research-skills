import json

# Load both audit results
with open('audit_results.json', encoding='utf-8') as f:
    new_audit = {r['row_id']: r for r in json.load(f).get('results', [])}

# Load fix report to get the old audit data
with open('fix_report.json', encoding='utf-8') as f:
    fixes = json.load(f)['fixes']

# Compare ratings for fixed skills
accurate_count = 0
still_bad = []

for fix in fixes[:30]:  # Check first 30
    row_id = fix['row_id']
    if row_id in new_audit:
        new_fa = new_audit[row_id].get('function_accuracy', '')
        skill_name = fix['skill_name'][:35]
        print(f"{skill_name:35} | old: partial/inaccurate -> new: {new_fa}")
        if new_fa == 'accurate':
            accurate_count += 1
        else:
            still_bad.append(fix['skill_name'])

print(f"\nAccurate after fix: {accurate_count}/30")
print(f"Still not accurate: {len(still_bad)}/30")

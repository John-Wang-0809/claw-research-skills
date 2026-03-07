"""
[IN]  Dependencies/Inputs:
 - confirmed_invalid_skills.json (134 confirmed invalid skills)
 - Final_Research_Skills_Thematic_Split/0*.md (8 theme documents)
[OUT] Outputs:
 - Modified theme documents with invalid skill rows removed
 - Console report of removed rows
[POS] Position in the system:
 - One-time cleanup script to remove remaining invalid skills from theme docs.
 - After running, all 134 invalid skills should be absent from theme documents.
"""

import json
import glob
import os
import re

def load_invalid_names(json_path):
    """Load set of invalid skill names (lowercased) from confirmed_invalid_skills.json."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    names = set()
    for s in data['skills']:
        names.add(s['skill_name'].strip().lower())
    return names

def is_table_data_row(line):
    """Check if line is a Markdown table data row (not header or separator)."""
    stripped = line.strip()
    if not stripped.startswith('|'):
        return False
    if stripped.startswith('| Skill') or stripped.startswith('|---'):
        return False
    return True

def extract_skill_name(line):
    """Extract skill name (first column) from a table row."""
    cols = line.split('|')
    if len(cols) >= 2:
        return cols[1].strip().lower()
    return ''

def is_table_header_or_sep(line):
    """Check if line is a table header or separator."""
    stripped = line.strip()
    return stripped.startswith('| Skill') or stripped.startswith('|---')

def clean_theme_doc(filepath, invalid_names):
    """Remove invalid skill rows from a theme document. Returns count of removed rows."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    removed = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if is_table_data_row(line):
            skill_name = extract_skill_name(line)
            if skill_name in invalid_names:
                removed.append(skill_name)
                i += 1
                continue
        new_lines.append(line)
        i += 1

    # Second pass: remove repo headers (### ...) that have no table rows after them
    final_lines = []
    i = 0
    while i < len(new_lines):
        line = new_lines[i]
        # Check if this is a ### repo header
        if line.strip().startswith('### ') and not line.strip().startswith('### Notes'):
            # Look ahead: should find table header + separator + at least 1 data row
            j = i + 1
            # Skip blank lines
            while j < len(new_lines) and new_lines[j].strip() == '':
                j += 1
            # Check for table header
            has_table_data = False
            if j < len(new_lines) and is_table_header_or_sep(new_lines[j]):
                k = j
                # Skip header and separator
                while k < len(new_lines) and is_table_header_or_sep(new_lines[k]):
                    k += 1
                # Check for at least one data row
                if k < len(new_lines) and is_table_data_row(new_lines[k]):
                    has_table_data = True

            if not has_table_data:
                # Skip this repo header and its empty table header/separator
                # Skip the ### line
                i += 1
                # Skip blank lines
                while i < len(new_lines) and new_lines[i].strip() == '':
                    i += 1
                # Skip table header and separator if present
                while i < len(new_lines) and is_table_header_or_sep(new_lines[i]):
                    i += 1
                continue

        final_lines.append(line)
        i += 1

    if removed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)

    return removed

def main():
    json_path = 'confirmed_invalid_skills.json'
    theme_pattern = 'Final_Research_Skills_Thematic_Split/0*.md'

    invalid_names = load_invalid_names(json_path)
    print(f"Loaded {len(invalid_names)} unique invalid skill names")

    total_removed = 0
    for filepath in sorted(glob.glob(theme_pattern)):
        basename = os.path.basename(filepath)
        removed = clean_theme_doc(filepath, invalid_names)
        if removed:
            print(f"\n{basename}: removed {len(removed)} rows")
            for name in removed:
                print(f"  - {name}")
            total_removed += len(removed)

    print(f"\n{'='*50}")
    print(f"Total removed: {total_removed}")

if __name__ == '__main__':
    main()

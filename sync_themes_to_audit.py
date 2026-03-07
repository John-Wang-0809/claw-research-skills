"""
[IN]  Dependencies/Inputs:
 - multidim_audit.json (1408 audited entries: the single source of truth)
 - Final_Research_Skills_Thematic_Split/0*.md (8 theme documents)
[OUT] Outputs:
 - Modified theme documents with only audit-present (skill_name, repo) rows retained
 - Backup of originals in Final_Research_Skills_Thematic_Split/backup_before_audit_sync/
 - Console report of per-file removals
[POS] Position in the system:
 - One-time sync script. After running, theme files contain exactly the rows
   whose (skill_name, repo) pairs exist in multidim_audit.json.
 - Uses the same two-pass cleanup pattern as remove_invalid_from_themes.py:
   Pass 1 removes non-audit data rows; Pass 2 removes orphaned repo sections.

 Change warning: once you modify this file's logic, you must update this
 comment block, and check/update the module doc (README/CLAUDE) in the
 containing folder; update the root global map if necessary.
"""

import json
import glob
import os
import shutil


def load_audit_keys(audit_path):
    """Load set of (skill_name, repo) from multidim_audit.json. Case-sensitive."""
    with open(audit_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    keys = set()
    for entry in data['results']:
        keys.add((entry['skill_name'], entry['repo']))
    return keys


def is_table_data_row(line):
    """Check if line is a Markdown table data row (not header or separator)."""
    stripped = line.strip()
    if not stripped.startswith('|'):
        return False
    if stripped.startswith('| Skill') or stripped.startswith('|---'):
        return False
    return True


def extract_skill_name(line):
    """Extract skill name (first column) from a table row. Case-preserving.
    Note: theme 06 uses backtick-wrapped names (`skill`) which won't match
    audit keys; those entries are correctly excluded (known 46-entry gap)."""
    cols = line.split('|')
    if len(cols) >= 2:
        return cols[1].strip()
    return ''


def is_table_header_or_sep(line):
    """Check if line is a table header or separator."""
    stripped = line.strip()
    return stripped.startswith('| Skill') or stripped.startswith('|---')


def is_main_theme_file(filepath):
    """Filter to only main theme data files, excluding audit/consistency reports."""
    basename = os.path.basename(filepath).upper()
    exclude = ['AUDIT', 'CONSISTENCY', 'RELEVANCE', 'BACKUP', 'README']
    return not any(kw in basename for kw in exclude)


def sync_theme_doc(filepath, audit_keys):
    """Remove rows whose (skill_name, repo) is NOT in audit_keys.
    Returns (kept_count, removed_list)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Pass 1: remove data rows not in audit, tracking current_repo from ### headers
    new_lines = []
    removed = []
    kept = 0
    current_repo = None

    for line in lines:
        stripped = line.strip()
        # Track current repo from ### headers (same logic as generate_catalog.py)
        if stripped.startswith('### ') and not stripped.startswith('### Notes'):
            current_repo = stripped[4:].strip()
            new_lines.append(line)
            continue

        if is_table_data_row(line) and current_repo is not None:
            skill_name = extract_skill_name(line)
            if (skill_name, current_repo) in audit_keys:
                new_lines.append(line)
                kept += 1
            else:
                removed.append((skill_name, current_repo))
        else:
            new_lines.append(line)

    # Pass 2: remove ### repo headers that have no data rows after them
    final_lines = []
    i = 0
    while i < len(new_lines):
        line = new_lines[i]
        stripped = line.strip()
        if stripped.startswith('### ') and not stripped.startswith('### Notes'):
            # Look ahead: should find table header + separator + at least 1 data row
            j = i + 1
            # Skip blank lines
            while j < len(new_lines) and new_lines[j].strip() == '':
                j += 1
            # Check for table content
            has_table_data = False
            if j < len(new_lines) and is_table_header_or_sep(new_lines[j]):
                k = j
                # Skip header and separator lines
                while k < len(new_lines) and is_table_header_or_sep(new_lines[k]):
                    k += 1
                # Check for at least one data row
                if k < len(new_lines) and is_table_data_row(new_lines[k]):
                    has_table_data = True

            if not has_table_data:
                # Skip this repo header and its empty table header/separator
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

    # Write back (always write, even if no removals, to normalize)
    if removed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)

    return kept, removed


def main():
    audit_path = 'multidim_audit.json'
    theme_pattern = 'Final_Research_Skills_Thematic_Split/0*.md'
    backup_dir = 'Final_Research_Skills_Thematic_Split/backup_before_audit_sync'

    # Load audit keys
    audit_keys = load_audit_keys(audit_path)
    print(f"Loaded {len(audit_keys)} audit (skill_name, repo) pairs")

    # Collect theme files
    theme_files = sorted(
        fp for fp in glob.glob(theme_pattern) if is_main_theme_file(fp)
    )
    print(f"Found {len(theme_files)} theme files to sync")

    # Create backup
    os.makedirs(backup_dir, exist_ok=True)
    for fp in theme_files:
        dst = os.path.join(backup_dir, os.path.basename(fp))
        shutil.copy2(fp, dst)
    print(f"Backups saved to {backup_dir}/")

    # Sync each file
    total_kept = 0
    total_removed = 0
    for fp in theme_files:
        basename = os.path.basename(fp)
        kept, removed = sync_theme_doc(fp, audit_keys)
        total_kept += kept
        total_removed += len(removed)
        print(f"\n{basename}: kept {kept}, removed {len(removed)}")
        if removed:
            for skill, repo in removed[:10]:
                print(f"  - {skill} ({repo})")
            if len(removed) > 10:
                print(f"  ... and {len(removed) - 10} more")

    print(f"\n{'=' * 60}")
    print(f"Total kept:    {total_kept}")
    print(f"Total removed: {total_removed}")
    print(f"Audit entries: {len(audit_keys)}")
    if total_kept != len(audit_keys):
        diff = len(audit_keys) - total_kept
        print(f"Gap: {diff} audit entries not found in theme files")
        print("  (these are entries whose theme files couldn't be parsed)")


if __name__ == '__main__':
    main()

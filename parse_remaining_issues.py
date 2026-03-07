#!/usr/bin/env python3
"""
Parse remaining_issues_for_review.md into a JSON manifest grouped by theme.
Each entry contains: skill_name, repo, theme, issue_type, audit_reason,
current_description, skill_url, skill_md_path.
"""

import json
import re
from pathlib import Path

INPUT = Path("remaining_issues_for_review.md")
OUTPUT = Path("plans/fix_manifest.json")


def parse():
    text = INPUT.read_text(encoding="utf-8", errors="replace")
    entries = []

    # Split by ### headers (each skill entry)
    blocks = re.split(r"^### \d+\.\s+", text, flags=re.MULTILINE)

    for block in blocks[1:]:  # skip preamble
        lines = block.strip().split("\n")
        # First line: `skill-name` — repo/name
        header = lines[0]
        m = re.match(r"`([^`]+)`\s*(?:—|--)\s*(.+)", header)
        if not m:
            continue
        skill_name = m.group(1).strip()
        repo = m.group(2).strip()

        entry = {"skill_name": skill_name, "repo": repo}

        full = "\n".join(lines[1:])

        # Extract fields
        for field, key in [
            ("Theme", "theme"),
            ("Issue Type", "issue_type"),
            ("Audit Reason", "audit_reason"),
            ("Current Function Explanation", "current_description"),
            ("Overall Quality", "overall_quality"),
            ("Issues", "issues"),
            ("Skill URL", "skill_url"),
            ("SKILL.md", "skill_md_path"),
        ]:
            pattern = rf"^\- \*\*{re.escape(field)}\*\*:\s*(.+)"
            match = re.search(pattern, full, re.MULTILINE)
            if match:
                val = match.group(1).strip()
                # For SKILL.md path, remove backticks
                if key == "skill_md_path":
                    val = val.strip("`")
                entry[key] = val

        entries.append(entry)

    # Group by theme
    by_theme = {}
    for e in entries:
        theme = e.get("theme", "unknown")
        by_theme.setdefault(theme, []).append(e)

    manifest = {
        "total": len(entries),
        "by_theme": by_theme,
        "theme_counts": {t: len(v) for t, v in by_theme.items()},
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Parsed {len(entries)} entries across {len(by_theme)} themes")
    for t, v in sorted(by_theme.items()):
        print(f"  {t}: {len(v)} skills")


if __name__ == "__main__":
    parse()

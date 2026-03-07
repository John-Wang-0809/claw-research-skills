"""
Cleanup script: merge multi-line table rows and remove template suffixes.
"""
import re

DOC_PATH = r"e:\LLM\EDU+LLM\1\Good_Tools\research-skills\Final_Research_Skills_Thematic_Split\02_literature_review_writing_citation.md"

TEMPLATE_SUFFIX = ". It is used for literature review, citation handling, and academic writing support. In research workflows, it improves traceability of sources and the quality of scholarly outputs."
TEMPLATE_SUFFIX2 = "It is used for literature review, citation handling, and academic writing support. In research workflows, it improves traceability of sources and the quality of scholarly outputs."

with open(DOC_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: Merge multi-line table rows
# A continuation line is one that doesn't start with | or # or empty, and follows a table row
lines = content.split('\n')
merged_lines = []
i = 0
merge_count = 0
while i < len(lines):
    line = lines[i]
    if line.startswith('|') and not line.startswith('|---') and not line.startswith('| Skill'):
        # This is a data row - check if next lines are continuations
        full_line = line
        while i + 1 < len(lines) and lines[i + 1] and not lines[i + 1].startswith('|') and not lines[i + 1].startswith('#') and not lines[i + 1].startswith('\n'):
            i += 1
            # Merge continuation into the current row
            full_line = full_line.rstrip() + ' ' + lines[i].strip()
            merge_count += 1
        merged_lines.append(full_line)
    else:
        merged_lines.append(line)
    i += 1

print(f"Merged {merge_count} continuation lines")

# Step 2: Remove template suffixes from all lines
content = '\n'.join(merged_lines)

# Remove the template suffix patterns
# Pattern: "|. It is used for literature review..." or "| It is used for literature review..."
content = content.replace('|' + TEMPLATE_SUFFIX, '')
content = content.replace('|. ' + TEMPLATE_SUFFIX2, '')
content = content.replace(TEMPLATE_SUFFIX, '')
content = content.replace(TEMPLATE_SUFFIX2, '')

# Also remove the "This skill centers on" template prefix pattern for any remaining entries
# Pattern: 'This skill centers on "X" and primarily provides Y'
content = re.sub(
    r'This skill centers on "[^"]*" and primarily provides ',
    '',
    content
)

with open(DOC_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(DOC_PATH, 'r', encoding='utf-8') as f:
    final = f.read()

remaining_template = final.count("It is used for literature review")
remaining_centers = final.count("This skill centers on")
line_count = final.count('\n') + 1
print(f"Remaining template suffixes: {remaining_template}")
print(f"Remaining 'centers on' templates: {remaining_centers}")
print(f"Final line count: {line_count}")

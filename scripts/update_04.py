#!/usr/bin/env python3
"""Update theme 04 document with local SKILL.md descriptions."""
import re
import os

theme_file = r"e:\LLM\EDU+LLM\1\Good_Tools\research-skills\Final_Research_Skills_Thematic_Split\04_data_analysis_and_evidence_interpretation.md"
base_dir = r"e:\LLM\EDU+LLM\1\Good_Tools\research-skills\Final_Research_Skills_Link_Downloads_By_Theme\04_data_analysis_and_evidence_interpretation"

# Build description map from local SKILL.md files
def extract_description(filepath):
    """Extract description from SKILL.md frontmatter."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return None

    # Try to find description in YAML frontmatter
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return None

    fm = fm_match.group(1)

    # Handle multi-line description (YAML | or >)
    desc_match = re.search(r'^description:\s*[|>]\s*\n((?:\s+.+\n?)+)', fm, re.MULTILINE)
    if desc_match:
        lines = desc_match.group(1).strip().split('\n')
        return ' '.join(l.strip() for l in lines)

    # Handle single-line description (possibly quoted)
    desc_match = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', fm, re.MULTILINE)
    if desc_match:
        return desc_match.group(1).strip()

    # Handle description: > multi-line
    desc_match = re.search(r'^description:\s*>\s*\n((?:\s+.+\n?)+)', fm, re.MULTILINE)
    if desc_match:
        lines = desc_match.group(1).strip().split('\n')
        return ' '.join(l.strip() for l in lines)

    return None


# Map repo names to directory names
repo_to_dir = {
    "acertainKnight/project-thoth": "acertainKnight__project-thoth",
    "affaan-m/everything-claude-code": "affaan-m__everything-claude-code",
    "anthropics/claude-agent-sdk-demos": "anthropics__claude-agent-sdk-demos",
    "ComposioHQ/awesome-claude-skills": "ComposioHQ__awesome-claude-skills",
    "ForaeFactory/antigravity-skills": "ForaeFactory__antigravity-skills",
    "GPTomics/bioSkills": "GPTomics__bioSkills",
    "hangoclong/skills-antigravity-awesome": "hangoclong__skills-antigravity-awesome",
    "huysynf/antigravity-awesome-skills": "huysynf__antigravity-awesome-skills",
    "Jeffallan/claude-skills": "Jeffallan__claude-skills",
    "K-Dense-AI/claude-scientific-skills": "K-Dense-AI__claude-scientific-skills",
    "mrgoonie/claudekit-skills": "mrgoonie__claudekit-skills",
    "muratcankoylan/Agent-Skills-for-Context-Engineering": "muratcankoylan__Agent-Skills-for-Context-Engineering",
    "ruvnet/claude-flow": "ruvnet__claude-flow",
    "sickn33/antigravity-awesome-skills": "sickn33__antigravity-awesome-skills",
    "trailofbits/skills": "trailofbits__skills",
    "treasure-data/td-skills": "treasure-data__td-skills",
    "wshobson/agents": "wshobson__agents",
    "yusufkaraaslan/Skill_Seekers": "yusufkaraaslan__Skill_Seekers",
}

# Map skill names to file name prefixes (handle special chars)
def skill_to_prefix(skill_name):
    """Convert skill name to file prefix pattern."""
    return skill_name.replace(' ', '_').replace('{', '').replace('}', '')


# Build full description map
desc_map = {}
for repo, dirname in repo_to_dir.items():
    repo_dir = os.path.join(base_dir, dirname)
    if not os.path.isdir(repo_dir):
        continue
    for fname in os.listdir(repo_dir):
        if not (fname.endswith('__SKILL.md') or fname.endswith('__BOOTSTRAP_SKILL.md') or fname.endswith('__domain-skill.md') or fname.endswith('__tool-skill.md')):
            continue
        # Extract skill name from filename: name__hash__SKILL.md
        parts = fname.split('__')
        if len(parts) >= 3:
            skill_prefix = parts[0]
        else:
            continue

        filepath = os.path.join(repo_dir, fname)
        desc = extract_description(filepath)
        if desc:
            desc_map[(repo, skill_prefix)] = desc

# NOT_RESEARCH skills
not_research = {
    ("acertainKnight/project-thoth", "MCP Server Management"): "MCP connection management tool, not data analysis",
    ("affaan-m/everything-claude-code", "continuous-learning-v2"): "Session learning system, not data analysis",
    ("affaan-m/everything-claude-code", "security-scan"): "Security scanning tool, not data analysis",
    ("ForaeFactory/antigravity-skills", "graphql"): "GraphQL API development framework",
    ("ForaeFactory/antigravity-skills", "lint-and-validate"): "Code quality linting tool, not data analysis",
    ("ForaeFactory/antigravity-skills", "Linux Production Shell Scripts"): "Linux system administration scripts, not data analysis",
    ("hangoclong/skills-antigravity-awesome", "graphql"): "GraphQL API development framework (fork)",
    ("hangoclong/skills-antigravity-awesome", "lint-and-validate"): "Code quality linting tool (fork), not data analysis",
    ("hangoclong/skills-antigravity-awesome", "Linux Production Shell Scripts"): "Linux system administration scripts (fork), not data analysis",
    ("huysynf/antigravity-awesome-skills", "graphql"): "GraphQL API development framework (fork)",
    ("huysynf/antigravity-awesome-skills", "lint-and-validate"): "Code quality linting tool (fork), not data analysis",
    ("huysynf/antigravity-awesome-skills", "Linux Production Shell Scripts"): "Linux system administration scripts (fork), not data analysis",
    ("Jeffallan/claude-skills", "graphql-architect"): "GraphQL schema architecture design, not data analysis",
    ("Jeffallan/claude-skills", "postgres-pro"): "PostgreSQL database administration, not data analysis",
    ("Jeffallan/claude-skills", "swift-expert"): "Swift/iOS mobile development, not data analysis",
    ("mrgoonie/claudekit-skills", "ai-multimodal"): "Multimodal AI media processing, not data analysis",
    ("mrgoonie/claudekit-skills", "sequential-thinking"): "Sequential reasoning pattern, not data analysis",
    ("muratcankoylan/Agent-Skills-for-Context-Engineering", "bdi-mental-states"): "BDI cognitive architecture for agents, not data analysis",
    ("ruvnet/claude-flow", "agent-production-validator"): "Production deployment validation, not data analysis",
    ("sickn33/antigravity-awesome-skills", "angular-migration"): "Angular framework migration, not data analysis",
    ("sickn33/antigravity-awesome-skills", "azure-ai-contentsafety-java"): "Content safety moderation (Java), not data analysis",
    ("sickn33/antigravity-awesome-skills", "azure-ai-contentsafety-py"): "Content safety moderation (Python), not data analysis",
    ("sickn33/antigravity-awesome-skills", "azure-mgmt-apicenter-py"): "Azure API Center management, not data analysis",
    ("sickn33/antigravity-awesome-skills", "binary-analysis-patterns"): "Binary reverse engineering, not data analysis",
    ("sickn33/antigravity-awesome-skills", "code-documentation-code-explain"): "Code explanation tool, not data analysis",
    ("sickn33/antigravity-awesome-skills", "code-documentation-doc-generate"): "Documentation generation tool, not data analysis",
    ("sickn33/antigravity-awesome-skills", "codebase-cleanup-deps-audit"): "Dependency security audit, not data analysis",
    ("sickn33/antigravity-awesome-skills", "database-migrations-sql-migrations"): "Database schema migration, not data analysis",
    ("sickn33/antigravity-awesome-skills", "dependency-management-deps-audit"): "Dependency management audit, not data analysis",
    ("sickn33/antigravity-awesome-skills", "documentation-generation-doc-generate"): "Documentation generation (duplicate), not data analysis",
    ("sickn33/antigravity-awesome-skills", "error-diagnostics-error-trace"): "Error tracking and observability, not data analysis",
    ("sickn33/antigravity-awesome-skills", "framework-migration-code-migrate"): "Framework migration tool, not data analysis",
    ("sickn33/antigravity-awesome-skills", "frontend-mobile-security-xss-scan"): "XSS vulnerability scanning, not data analysis",
    ("sickn33/antigravity-awesome-skills", "graphql"): "GraphQL API development, not data analysis",
    ("sickn33/antigravity-awesome-skills", "lint-and-validate"): "Code quality linting, not data analysis",
    ("sickn33/antigravity-awesome-skills", "Linux Production Shell Scripts"): "Linux system administration scripts, not data analysis",
    ("sickn33/antigravity-awesome-skills", "n8n-code-python"): "n8n workflow automation Python nodes, not data analysis",
    ("sickn33/antigravity-awesome-skills", "php-pro"): "PHP development, not data analysis",
    ("sickn33/antigravity-awesome-skills", "security-requirement-extraction"): "Security requirements from threat models, not data analysis",
    ("sickn33/antigravity-awesome-skills", "security-scanning-security-dependencies"): "Security dependency scanning, not data analysis",
    ("sickn33/antigravity-awesome-skills", "shellcheck-configuration"): "Shell script linting configuration, not data analysis",
    ("sickn33/antigravity-awesome-skills", "unit-testing-test-generate"): "Unit test generation, not data analysis",
    ("trailofbits/skills", "fuzzing-obstacles"): "Fuzzing technique for security testing, not data analysis",
    ("trailofbits/skills", "sarif-parsing"): "SARIF security scan result parsing, not data analysis",
    ("trailofbits/skills", "{domain-name-lowercase}"): "Template placeholder, not an actual skill",
    ("trailofbits/skills", "{tool-name-lowercase}"): "Template placeholder, not an actual skill",
    ("treasure-data/td-skills", "field-agent-documentation"): "Agent documentation template, not data analysis",
    ("treasure-data/td-skills", "trino-to-hive-migration"): "SQL engine migration tool, not data analysis",
    ("wshobson/agents", "angular-migration"): "Angular framework migration (duplicate), not data analysis",
    ("wshobson/agents", "binary-analysis-patterns"): "Binary reverse engineering (duplicate), not data analysis",
    ("wshobson/agents", "python-type-safety"): "Python type annotation tool, not data analysis",
    ("wshobson/agents", "security-requirement-extraction"): "Security requirements (duplicate), not data analysis",
    ("wshobson/agents", "shellcheck-configuration"): "Shell script linting (duplicate), not data analysis",
}

# Research-related Why descriptions for genuinely relevant non-bio skills
research_why = {
    ("Jeffallan/claude-skills", "pandas-pro"): "Provides core data manipulation and analysis capabilities essential for research data cleaning, transformation, and exploratory analysis.",
    ("K-Dense-AI/claude-scientific-skills", "dask"): "Enables distributed computing for larger-than-RAM scientific datasets, critical for processing large research data beyond single-machine memory limits.",
    ("K-Dense-AI/claude-scientific-skills", "pymc-bayesian-modeling"): "Provides Bayesian statistical modeling and probabilistic inference, fundamental for research hypothesis testing and uncertainty quantification.",
    ("K-Dense-AI/claude-scientific-skills", "seaborn"): "Enables statistical visualization for exploring distributions, relationships, and categorical comparisons in research data.",
    ("K-Dense-AI/claude-scientific-skills", "shap"): "Provides model interpretability and explainability for machine learning, essential for understanding and validating research model predictions.",
    ("sickn33/antigravity-awesome-skills", "azure-ai-textanalytics-py"): "Provides NLP capabilities (sentiment analysis, entity recognition, key phrases) useful for text-based research data analysis.",
    ("sickn33/antigravity-awesome-skills", "azure-ai-vision-imageanalysis-java"): "Provides computer vision capabilities (captioning, OCR, object detection) applicable to image-based research data analysis.",
    ("sickn33/antigravity-awesome-skills", "azure-ai-vision-imageanalysis-py"): "Provides computer vision capabilities (captioning, OCR, object detection) applicable to image-based research data analysis.",
    ("sickn33/antigravity-awesome-skills", "dbt-transformation-patterns"): "Supports analytics engineering with data transformation pipelines, useful for structuring research data workflows.",
    ("sickn33/antigravity-awesome-skills", "sql-optimization-patterns"): "Enables SQL query optimization and indexing strategies, essential for efficient research database queries.",
    ("treasure-data/td-skills", "trino"): "Provides Trino SQL with TD-specific functions for time-based data filtering and query patterns, useful for research data querying.",
}


def find_desc(repo, skill_name):
    """Find description for a skill, trying various key formats."""
    # Direct match with skill name as prefix
    prefix = skill_to_prefix(skill_name)
    key = (repo, prefix)
    if key in desc_map:
        return desc_map[key]

    # Try lowercase
    key = (repo, prefix.lower())
    if key in desc_map:
        return desc_map[key]

    # Try with spaces replaced by hyphens
    prefix2 = skill_name.replace(' ', '-')
    key = (repo, prefix2)
    if key in desc_map:
        return desc_map[key]

    # Try exact skill name
    key = (repo, skill_name)
    if key in desc_map:
        return desc_map[key]

    # Brute force: check all keys for this repo
    for (r, p), d in desc_map.items():
        if r == repo and (p.lower() == skill_name.lower().replace(' ', '_') or
                          p.lower() == skill_name.lower().replace(' ', '-') or
                          p.lower() == skill_name.lower()):
            return d

    return None


def generate_bio_why(skill_name, desc):
    """Generate a specific Why Research-Related for bio skills."""
    # Map skill categories to research relevance
    categories = {
        'alignment': 'sequence alignment analysis',
        'variant': 'genetic variant analysis',
        'expression': 'gene expression analysis',
        'pathway': 'biological pathway analysis',
        'population-genetics': 'population genetics analysis',
        'hi-c': 'chromatin interaction analysis',
        'methylation': 'DNA methylation analysis',
        'proteomics': 'proteomics data analysis',
        'metabolomics': 'metabolomics data analysis',
        'spatial-transcriptomics': 'spatial transcriptomics analysis',
        'single-cell': 'single-cell data analysis',
        'chipseq': 'ChIP-seq data analysis',
        'rna-quantification': 'RNA quantification analysis',
        'data-visualization': 'bioinformatics data visualization',
        'genome': 'genome analysis',
        'workflows': 'end-to-end bioinformatics pipeline',
        'read-qc': 'sequencing read quality control',
        'copy-number': 'copy number variation analysis',
        'flow-cytometry': 'flow cytometry data analysis',
        'ribo-seq': 'ribosome profiling analysis',
        'microbiome': 'microbiome data analysis',
        'crispr': 'CRISPR screen analysis',
        'splicing': 'alternative splicing analysis',
        'systems-biology': 'systems biology modeling',
        'epidemiological': 'epidemiological genomics analysis',
        'imaging-mass-cytometry': 'imaging mass cytometry analysis',
        'gene-regulatory': 'gene regulatory network analysis',
        'clinical-databases': 'clinical genomics database analysis',
        'causal-genomics': 'causal genomics analysis',
        'temporal-genomics': 'temporal genomics analysis',
        'multi-omics': 'multi-omics integration analysis',
        'small-rna': 'small RNA analysis',
    }

    for cat_key, cat_desc in categories.items():
        if cat_key in skill_name.lower():
            return f"Directly supports bioinformatics research through {cat_desc}."

    # Default for bio skills
    return f"Supports bioinformatics data analysis and evidence interpretation in genomics research."


# Read the file
with open(theme_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

current_repo = None
updated_count = 0
not_research_count = 0
missing_count = 0

for i, line in enumerate(lines):
    # Detect repo header
    repo_match = re.match(r'^### (.+)$', line)
    if repo_match:
        current_repo = repo_match.group(1).strip()
        continue

    # Skip non-data rows
    if not line.startswith('| ') or line.startswith('| Skill ') or line.startswith('|---'):
        continue

    # Parse the table row by splitting on ' | '
    parts = line.split(' | ')
    if len(parts) < 7:
        continue

    skill_name = parts[0].lstrip('| ').strip()

    if not current_repo or not skill_name:
        continue

    key = (current_repo, skill_name)

    # Get description from local SKILL.md
    desc = find_desc(current_repo, skill_name)

    # Determine new Why Research-Related
    if key in not_research:
        new_why = "[NOT_RESEARCH: " + not_research[key] + "]"
        not_research_count += 1
    elif key in research_why:
        new_why = research_why[key]
    elif current_repo == "GPTomics/bioSkills":
        new_why = generate_bio_why(skill_name, desc or "")
    else:
        if desc:
            new_why = desc[:150] if len(desc) > 150 else desc
        else:
            new_why = "[LOCAL_FILE_MISSING]"
            missing_count += 1

    # Determine new Function Explanation
    if desc:
        new_func = desc
    else:
        new_func = "[LOCAL_FILE_MISSING]"
        if key not in not_research:
            pass  # already counted

    # Update columns 3 (Why) and 4 (Function Explanation) - 0-indexed from parts
    parts[3] = new_why
    parts[4] = new_func
    # Keep parts[5] (execution flow) as-is

    lines[i] = ' | '.join(parts)
    updated_count += 1

# Write back
with open(theme_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Updated {updated_count} skill rows")
print(f"Marked {not_research_count} as NOT_RESEARCH")
print(f"Missing local files: {missing_count}")
print(f"Description map has {len(desc_map)} entries")

"""
[IN]  Dependencies/Inputs:
 - Final_Research_Skills_Thematic_Split/02_literature_review_writing_citation.md
 - Final_Research_Skills_Link_Downloads_By_Theme/02_literature_review_writing_citation/[owner]__[repo]/[skill]__[hash]__SKILL.md
[OUT] Outputs:
 - Updated 02_literature_review_writing_citation.md with regenerated fields
[POS] Position in the system:
 - One-time batch update script for theme 02 document
"""
import os, re, glob, yaml

BASE = r"e:\LLM\EDU+LLM\1\Good_Tools\research-skills"
DOC_PATH = os.path.join(BASE, "Final_Research_Skills_Thematic_Split", "02_literature_review_writing_citation.md")
SKILLS_DIR = os.path.join(BASE, "Final_Research_Skills_Link_Downloads_By_Theme", "02_literature_review_writing_citation")

# Misclassification keywords for NOT_RESEARCH detection
NOT_RESEARCH_PATTERNS = [
    # Security/pentest (removed 'ids' and 'ips' - too generic, causes false positives with 'arXiv IDs' etc.)
    (r'\b(burp.suite|pentest|penetration.test|red.team|xss|cross.site.scripting|html.injection|'
     r'web.vulnerabilities|security.scanning|wireshark|network.traffic|attack.tree|'
     r'vulnerability|exploit|ctf|malware|phishing|brute.force|sql.injection|'
     r'owasp|threat.model|incident.response|forensic|siem|firewall|'
     r'nmap|metasploit|kali|reverse.engineer|intrusion.detection|intrusion.prevention)\b', 'security/pentest tool'),
    # Pure web/mobile dev frameworks
    (r'\b(angular|react|vue|swift|flutter|ionic|xamarin|cordova|electron|'
     r'app.builder|app.store.optimization|aso|mobile.app|frontend.framework|'
     r'backend.development|feature.development)\b', 'web/mobile development tool'),
    # DevOps/infrastructure
    (r'\b(azure.ai|azure.cognitive|azure.devops|architecture.decision.record|'
     r'terraform|kubernetes|docker.compose|helm|ansible|puppet|chef|'
     r'ci.cd|pipeline|infrastructure.as.code)\b', 'DevOps/infrastructure tool'),
    # Marketing/business
    (r'\b(analytics.tracking|seo.optimization|marketing.automation|'
     r'conversion.rate|a.b.testing|growth.hack|lead.generation)\b', 'marketing/business tool'),
    # Pure debugging
    (r'\b(error.diagnostics.smart.debug|smart.debug)\b', 'debugging tool'),
]

# Research-positive keywords
RESEARCH_KEYWORDS = [
    r'research', r'paper', r'literature', r'citation', r'academic', r'scholarly',
    r'peer.review', r'bibliography', r'abstract', r'manuscript', r'journal',
    r'conference', r'arxiv', r'pubmed', r'doi', r'thesis', r'dissertation',
    r'systematic.review', r'meta.analysis', r'hypothesis', r'methodology',
    r'experiment', r'data.analysis', r'statistical', r'scientific',
    r'bioinformatics', r'genomics', r'proteomics', r'clinical',
    r'knowledge.graph', r'ontology', r'taxonomy', r'corpus',
    r'nlp', r'natural.language', r'text.mining', r'information.extraction',
    r'summariz', r'writing', r'draft', r'proofread', r'grammar',
    r'plagiarism', r'reference', r'footnote', r'endnote',
    r'notion', r'obsidian', r'zotero', r'mendeley',
    r'deep.research', r'rag', r'retrieval', r'embedding',
    r'synthesis', r'triangulat', r'verify', r'fact.check',
    r'mycolog', r'fungi', r'mushroom', r'species.identif',
]


def extract_skill_info(skill_md_path):
    """Extract name, description, and workflow from a SKILL.md file."""
    try:
        with open(skill_md_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception:
        return None

    # Extract YAML frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return None

    try:
        fm = yaml.safe_load(fm_match.group(1))
    except Exception:
        # Try manual extraction
        fm = {}
        for line in fm_match.group(1).split('\n'):
            if line.startswith('name:'):
                fm['name'] = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith('description:'):
                fm['description'] = line.split(':', 1)[1].strip().strip('"\'')

    if not fm or not isinstance(fm, dict):
        return None

    name = fm.get('name', '')
    desc = fm.get('description', '')
    if isinstance(desc, list):
        desc = ' '.join(str(d) for d in desc)
    desc = str(desc).strip()
    # Sanitize: replace newlines with spaces to avoid breaking markdown tables
    desc = re.sub(r'\s*\n\s*', ' ', desc)
    # Remove pipe characters that would break table columns
    desc = desc.replace('|', '/')

    # Extract workflow/steps if present
    workflow = extract_workflow(content)

    return {'name': name, 'description': desc, 'workflow': workflow}


def extract_workflow(content):
    """Extract workflow/execution steps from SKILL.md content."""
    # Look for workflow sections
    workflow_patterns = [
        r'##\s*(?:Execution\s*)?(?:Flow|Workflow|Steps|Process|Pipeline|Phases?)\s*\n(.*?)(?=\n##|\Z)',
        r'##\s*(?:How\s*(?:to|it)\s*(?:Use|Works?))\s*\n(.*?)(?=\n##|\Z)',
        r'##\s*(?:When\s*to\s*Use)\s*\n(.*?)(?=\n##|\Z)',
    ]
    for pat in workflow_patterns:
        m = re.search(pat, content, re.DOTALL | re.IGNORECASE)
        if m:
            section = m.group(1).strip()
            # Extract numbered/bulleted steps
            steps = re.findall(r'(?:^|\n)\s*(?:\d+[\.\)]\s*|[-*]\s*)(.*?)(?=\n|$)', section)
            if steps and len(steps) >= 2:
                return ' → '.join(s.strip() for s in steps[:10] if s.strip())
    return None


def classify_research_relevance(name, description):
    """Determine if a skill is research-related and generate Why Research-Related."""
    combined = f"{name} {description}".lower()

    # First check if description has strong research-positive signals
    strong_research_signals = [
        r'academic', r'scholarly', r'literature.review', r'paper.discovery',
        r'citation', r'arxiv', r'pubmed', r'doi\b', r'peer.review',
        r'research.paper', r'scientific.writing', r'manuscript',
        r'bibliography', r'systematic.review', r'meta.analysis',
    ]
    has_strong_research = any(re.search(s, combined, re.IGNORECASE) for s in strong_research_signals)

    # Check NOT_RESEARCH patterns - but skip if strong research signals present
    if not has_strong_research:
        for pattern, category in NOT_RESEARCH_PATTERNS:
            if re.search(pattern, combined, re.IGNORECASE):
                return f"[NOT_RESEARCH: {category}]"

    # Check for template placeholder patterns
    if '{domain-name' in combined or '{' in name:
        return "[NOT_RESEARCH: template placeholder]"

    # Check research-positive keywords
    matches = []
    for kw in RESEARCH_KEYWORDS:
        if re.search(kw, combined, re.IGNORECASE):
            matches.append(kw.replace('.', ' ').replace(r'\b', ''))

    if matches:
        # Generate personalized Why Research-Related
        return generate_why_research(name, description, matches)

    # If no clear signal, try to infer from description
    if len(description) > 20:
        return generate_why_research_generic(name, description)

    return "[NOT_RESEARCH: no clear research relevance in description]"


def generate_why_research(name, description, matched_keywords):
    """Generate a personalized Why Research-Related statement."""
    desc_lower = description.lower()

    # Specific patterns for common research skill types
    if any(k in desc_lower for k in ['deep research', 'comprehensive analysis', 'multi-source']):
        return f"Enables deep, multi-source research synthesis with citation tracking and verification, directly supporting literature review workflows."
    if any(k in desc_lower for k in ['literature review', 'literature search']):
        return f"Directly supports systematic literature review by automating search, filtering, and synthesis of academic sources."
    if any(k in desc_lower for k in ['citation', 'reference', 'bibliography']):
        return f"Manages citations and references, ensuring proper attribution and traceability in academic writing."
    if any(k in desc_lower for k in ['paper', 'manuscript', 'academic writing', 'scientific writing']):
        return f"Assists in drafting, structuring, or reviewing academic papers and manuscripts."
    if any(k in desc_lower for k in ['arxiv', 'pubmed', 'doi', 'journal']):
        return f"Interfaces with academic databases to discover, retrieve, or manage scholarly publications."
    if any(k in desc_lower for k in ['peer review', 'peer-review']):
        return f"Supports the peer review process by providing structured evaluation of research quality and methodology."
    if any(k in desc_lower for k in ['knowledge graph', 'ontology', 'taxonomy']):
        return f"Builds structured knowledge representations that support research organization and discovery."
    if any(k in desc_lower for k in ['summariz', 'synthesis', 'abstract']):
        return f"Synthesizes or summarizes research content, aiding comprehension and literature review efficiency."
    if any(k in desc_lower for k in ['rag', 'retrieval', 'embedding']):
        return f"Uses retrieval-augmented generation to ground research outputs in verified sources."
    if any(k in desc_lower for k in ['bioinformatics', 'genomics', 'proteomics', 'clinical', 'bio']):
        return f"Supports domain-specific research workflows in life sciences and biomedical fields."
    if any(k in desc_lower for k in ['mycolog', 'fungi', 'mushroom', 'species']):
        return f"Supports mycological research including species identification and taxonomic analysis."
    if any(k in desc_lower for k in ['nlp', 'natural language', 'text mining']):
        return f"Applies NLP techniques to extract, analyze, or organize research-relevant textual data."
    if any(k in desc_lower for k in ['writing', 'draft', 'proofread', 'grammar']):
        return f"Assists with academic writing quality, including drafting, proofreading, and style improvement."
    if any(k in desc_lower for k in ['notion', 'obsidian']):
        return f"Integrates with knowledge management tools commonly used in research workflows."
    if any(k in desc_lower for k in ['data analysis', 'statistical', 'experiment']):
        return f"Supports research data analysis and experimental methodology."
    if 'research' in desc_lower:
        return f"Supports research workflows by providing tools for investigation, analysis, or knowledge management."

    # Fallback with matched keywords
    kw_str = ', '.join(set(matched_keywords[:3]))
    return f"Relevant to research workflows based on its {kw_str} capabilities."


def generate_why_research_generic(name, description):
    """Generate Why Research-Related for skills without clear keyword matches."""
    name_lower = name.lower().replace('-', ' ').replace('_', ' ')
    desc_lower = description.lower()

    # Check for common non-research patterns by name
    non_research_names = [
        'bash', 'shell', 'docker', 'kubernetes', 'aws', 'gcp', 'azure',
        'react', 'angular', 'vue', 'swift', 'kotlin', 'android', 'ios',
        'css', 'html', 'sass', 'less', 'webpack', 'vite', 'rollup',
        'redis', 'mongodb', 'postgres', 'mysql', 'sqlite',
        'nginx', 'apache', 'caddy', 'traefik',
        'git', 'svn', 'mercurial',
        'slack', 'discord', 'telegram',
        'stripe', 'paypal', 'shopify',
        'seo', 'analytics', 'tracking',
        'game', 'unity', 'unreal',
    ]
    for nn in non_research_names:
        if nn in name_lower and 'research' not in desc_lower and 'paper' not in desc_lower:
            return f"[NOT_RESEARCH: {nn}-related tool, no research relevance in description]"

    # Check for code/dev patterns
    code_patterns = [
        r'code.review', r'code.quality', r'linting', r'formatting',
        r'refactor', r'debug', r'deploy', r'build.system',
        r'package.manag', r'dependency', r'version.control',
        r'api.design', r'rest.api', r'graphql', r'grpc',
        r'authentication', r'authorization', r'oauth', r'jwt',
        r'caching', r'load.balanc', r'scaling',
    ]
    for cp in code_patterns:
        if re.search(cp, f"{name_lower} {desc_lower}", re.IGNORECASE):
            return f"[NOT_RESEARCH: software development tool]"

    # If description mentions useful general capabilities
    if any(k in desc_lower for k in ['automat', 'workflow', 'pipeline', 'orchestrat']):
        if 'research' in desc_lower or 'paper' in desc_lower or 'academic' in desc_lower:
            return f"Automates research-related workflows, improving efficiency in academic tasks."
        return f"[NOT_RESEARCH: general automation tool, no specific research relevance]"

    if any(k in desc_lower for k in ['agent', 'skill', 'claude', 'llm', 'ai']):
        if 'research' in desc_lower:
            return f"AI-powered tool that supports research workflows."
        # Generic AI tool - could be research-adjacent
        return f"General-purpose AI skill; research relevance depends on specific use context. Description: {description[:80]}"

    return f"[NOT_RESEARCH: no clear research relevance in description]"


def build_skill_index(skills_dir):
    """Build an index of all local SKILL.md files: {(owner__repo, skill_name): info}"""
    index = {}
    for repo_dir in os.listdir(skills_dir):
        repo_path = os.path.join(skills_dir, repo_dir)
        if not os.path.isdir(repo_path):
            continue
        for fname in os.listdir(repo_path):
            if not fname.endswith('__SKILL.md'):
                continue
            # Parse: skill-name__hash__SKILL.md
            parts = fname.rsplit('__', 2)
            if len(parts) < 3:
                continue
            skill_name = parts[0]
            fpath = os.path.join(repo_path, fname)
            info = extract_skill_info(fpath)
            if info:
                index[(repo_dir, skill_name)] = info
                # Also index by the name field from YAML
                if info['name'] and info['name'] != skill_name:
                    index[(repo_dir, info['name'])] = info
    return index


def owner_repo_to_dir(owner_repo):
    """Convert 'owner/repo' to 'owner__repo' directory name."""
    return owner_repo.replace('/', '__')


def process_document(doc_path, skill_index):
    """Process the theme document and update fields."""
    with open(doc_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_repo = None
    updated_lines = []
    stats = {'total': 0, 'updated': 0, 'not_research': 0, 'missing': 0}

    for i, line in enumerate(lines):
        # Detect repo section headers
        repo_match = re.match(r'^### (.+/.+)\s*$', line)
        if repo_match:
            current_repo = repo_match.group(1).strip()
            updated_lines.append(line)
            continue

        # Detect table rows (skill data rows, not headers or separators)
        if current_repo and line.startswith('|') and not line.startswith('|---') and not line.startswith('| Skill'):
            updated_line = update_skill_row(line, current_repo, skill_index, stats)
            updated_lines.append(updated_line)
            continue

        updated_lines.append(line)

    with open(doc_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    return stats


def update_skill_row(line, current_repo, skill_index, stats):
    """Update a single skill table row."""
    stats['total'] += 1

    # Parse table columns
    cols = line.split('|')
    if len(cols) < 9:  # Need at least: empty + 7 cols + empty
        return line

    # cols[0] is empty (before first |), cols[1]=Skill, cols[2]=Evidence, cols[3]=URL,
    # cols[4]=Why, cols[5]=Function, cols[6]=Flow, cols[7]=Evidence
    skill_name = cols[1].strip()
    repo_dir = owner_repo_to_dir(current_repo)

    # Look up in index
    info = skill_index.get((repo_dir, skill_name))
    if not info:
        # Try fuzzy match: replace spaces with hyphens, underscores
        for variant in [skill_name.replace(' ', '-'), skill_name.replace(' ', '_'),
                        skill_name.lower(), skill_name.lower().replace(' ', '-')]:
            info = skill_index.get((repo_dir, variant))
            if info:
                break

    if not info:
        stats['missing'] += 1
        # Mark as missing but don't change
        if '[LOCAL_FILE_MISSING]' not in cols[4]:
            cols[4] = f" [LOCAL_FILE_MISSING] {cols[4].strip()} "
        return '|'.join(cols)

    # Update Why Research-Related
    why = classify_research_relevance(info['name'], info['description'])
    if why.startswith('[NOT_RESEARCH'):
        stats['not_research'] += 1
    cols[4] = f" {why} "

    # Update Function Explanation - use full description
    desc = info['description']
    # Clean up any truncation artifacts
    desc = desc.strip()
    if desc:
        cols[5] = f" {desc} "
    # else keep original

    # Update Execution Flow if we have workflow from SKILL.md
    if info.get('workflow'):
        cols[6] = f" {info['workflow']} "
    # else keep original flow

    stats['updated'] += 1
    return '|'.join(cols)


if __name__ == '__main__':
    print("Building skill index from local SKILL.md files...")
    skill_index = build_skill_index(SKILLS_DIR)
    print(f"Indexed {len(skill_index)} skill entries")

    print("Processing document...")
    stats = process_document(DOC_PATH, skill_index)

    print(f"\nDone!")
    print(f"Total skills processed: {stats['total']}")
    print(f"Updated: {stats['updated']}")
    print(f"Marked NOT_RESEARCH: {stats['not_research']}")
    print(f"Missing local files: {stats['missing']}")

"""
[IN]  Dependencies/Inputs:
 - multidim_audit.json (1408 audited entries: skill_name, repo, theme, research_tier, domain)
 - dedup_results.json (1408 entries: uniqueness original/canonical/variant)
 - Final_Research_Skills_Link_Downloads_By_Theme_LATEST/**/**/SKILL.md (2062 files on disk)
[OUT] Outputs:
 - openclaw_deploy/<skill-name>/SKILL.md (flat directory for OpenClaw discovery)
 - ironclaw_deploy/<skill-name>/SKILL.md (with activation block for IronClaw smart selection)
 - deploy_report.json (deployment summary, name mappings, and errors)
[POS] Position in the system:
 - Deployment bridge. Reads audited skill data and disk SKILL.md files, produces
   platform-ready directory layouts for OpenClaw and IronClaw. Normalizes names
   to comply with Agent Skills spec (OpenClaw) and IronClaw naming rules.
   Injects metadata (original_name, source_repo) for traceability.
   Does NOT modify source data. Re-run after audit updates to regenerate deployment dirs.
 - OpenClaw format verified against docs.openclaw.ai/tools/skills (2026-03-16).
 - IronClaw format verified against github.com/nearai/ironclaw (2026-03-16).
   IronClaw uses same SKILL.md format as OpenClaw, extended with activation block.

 Change warning: once you modify this file's logic, you must update this comment
 block, and check/update the module doc (README/CLAUDE) in the containing folder;
 update the root global map if necessary.
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime


# ── Constants ──────────────────────────────────────────────────────────────

SKILL_ROOT = 'Final_Research_Skills_Link_Downloads_By_Theme_LATEST'
AUDIT_PATH = 'multidim_audit.json'
DEDUP_PATH = 'dedup_results.json'
OPENCLAW_DIR = 'openclaw_deploy'
IRONCLAW_DIR = 'ironclaw_deploy'
REPORT_PATH = 'deploy_report.json'


# ── Data loading ───────────────────────────────────────────────────────────

def load_json(path):
    """Load a JSON file with UTF-8 encoding."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_dedup_index(dedup_data):
    """Build lookup: (skill_name, repo) → uniqueness."""
    index = {}
    for entry in dedup_data['results']:
        key = (entry['skill_name'], entry['repo'])
        index[key] = entry['uniqueness']
    return index


def theme_to_dir(theme):
    """Convert audit theme field to disk directory name.

    Examples:
        '02_literature_review_writing_citation_part2'
        → '02_literature_review_writing_citation'
    """
    return re.sub(r'_part\d+$', '', theme)


def repo_to_dir(repo):
    """Convert repo 'owner/name' to disk directory 'owner__name'."""
    return repo.replace('/', '__')


# ── Frontmatter extraction ─────────────────────────────────────────────────

def extract_frontmatter_name(filepath):
    """Extract the 'name' field from SKILL.md YAML frontmatter.

    Returns the name string, or None if not found.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line != '---':
                return None
            fm_lines = []
            for line in f:
                if line.strip() == '---':
                    break
                fm_lines.append(line)
            fm_text = ''.join(fm_lines)
    except Exception:
        return None

    # Quick regex extraction (avoids yaml dependency for indexing)
    m = re.match(r'^name:\s*["\']?(.+?)["\']?\s*$', fm_text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


# ── Disk index ─────────────────────────────────────────────────────────────

def build_disk_index(skill_root):
    """Scan all SKILL.md files and build a multi-strategy lookup index.

    Indexes by:
    1. (repo_dir, dir_name) → path   [directory name = skill folder name]
    2. (repo_dir, fm_name)  → path   [frontmatter name field]

    Returns: (by_dir, by_fm_name) dicts
    """
    by_dir = {}       # (repo_dir, skill_dir_name) → path
    by_fm_name = {}   # (repo_dir, frontmatter_name) → path
    total = 0

    for theme_dir in os.listdir(skill_root):
        theme_path = os.path.join(skill_root, theme_dir)
        if not os.path.isdir(theme_path):
            continue
        for repo_dir in os.listdir(theme_path):
            repo_path = os.path.join(theme_path, repo_dir)
            if not os.path.isdir(repo_path):
                continue
            total += _index_repo_skills(repo_path, repo_dir, by_dir, by_fm_name)

    print(f'  SKILL.md files indexed: {total}')
    return by_dir, by_fm_name


def _index_repo_skills(repo_path, repo_dir, by_dir, by_fm_name):
    """Walk a repo directory, indexing each SKILL.md by dir name and frontmatter name."""
    count = 0
    for dirpath, _dirnames, filenames in os.walk(repo_path):
        if 'SKILL.md' not in filenames:
            continue
        skill_dir = os.path.basename(dirpath)
        full_path = os.path.join(dirpath, 'SKILL.md')
        count += 1
        by_dir[(repo_dir, skill_dir)] = full_path
        fm_name = extract_frontmatter_name(full_path)
        if fm_name:
            by_fm_name[(repo_dir, fm_name)] = full_path
    return count


def _to_kebab(s):
    """Convert a name to kebab-case for fuzzy matching."""
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


# ── Name normalization ────────────────────────────────────────────────────

def _truncate_at_boundary(s, max_len):
    """Truncate string at last hyphen before max_len to avoid breaking words."""
    if len(s) <= max_len:
        return s
    truncated = s[:max_len]
    last_hyphen = truncated.rfind('-')
    if last_hyphen > max_len // 2:
        return truncated[:last_hyphen]
    return truncated.rstrip('-')


def normalize_name(raw_name, platform='openclaw'):
    """Normalize a skill name for the target platform.

    OpenClaw (Agent Skills spec): [a-z0-9-], no leading/trailing -, no --, max 64.
    IronClaw: [a-zA-Z0-9._-], max 64, must start with alphanumeric.
    """
    if platform == 'ironclaw':
        s = re.sub(r'\s+', '-', raw_name)
        s = re.sub(r'[^a-zA-Z0-9._-]', '', s)
        if s and not s[0].isalnum():
            s = 'x' + s
        return s[:64] or 'unnamed'
    # openclaw (default) — strict Agent Skills rules
    s = raw_name.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    s = re.sub(r'-{2,}', '-', s)
    if len(s) > 64:
        s = _truncate_at_boundary(s, 64)
        s = s.strip('-')
    return s or 'unnamed'


def _normalization_reason(original, normalized, uniqueness):
    """Generate a human-readable reason for name normalization."""
    reasons = []
    if uniqueness == 'variant':
        reasons.append('variant-prefix')
    if any(c.isupper() for c in original):
        reasons.append('lowercase')
    if ' ' in original:
        reasons.append('space-to-hyphen')
    if '_' in original:
        reasons.append('underscore-to-hyphen')
    if len(normalized) == 64 and len(original) > 64:
        reasons.append('truncated')
    if not reasons and original != normalized:
        reasons.append('special-chars-removed')
    return ' + '.join(reasons) if reasons else None


def resolve_skill_path(entry, by_dir, by_fm_name):
    """Find the disk path for an audit entry.

    Matching strategy (in order):
    1. Exact dir match: (repo_dir, skill_name)
    2. Exact frontmatter match: (repo_dir, skill_name)
    3. Kebab-case dir match: (repo_dir, kebab(skill_name))
    """
    r_dir = repo_to_dir(entry['repo'])
    s_name = entry['skill_name']

    # 1. Exact directory name match
    key = (r_dir, s_name)
    if key in by_dir:
        return by_dir[key]

    # 2. Exact frontmatter name match
    if key in by_fm_name:
        return by_fm_name[key]

    # 3. Kebab-case directory name match
    kebab = _to_kebab(s_name)
    if kebab != s_name:
        key_k = (r_dir, kebab)
        if key_k in by_dir:
            return by_dir[key_k]

    return None


# ── Deploy name ────────────────────────────────────────────────────────────

def deploy_name(entry, uniqueness):
    """Determine the raw (pre-normalization) deploy name for a skill.

    - original / canonical → skill-name
    - variant → {repo-name}-{skill-name} (repo name only, no owner)

    Returns raw composed name (normalize_name is applied separately).
    """
    skill = entry['skill_name']
    if uniqueness == 'variant':
        repo_name = entry['repo'].split('/')[-1]
        return f"{repo_name}-{skill}"
    return skill


# ── IronClaw activation generation ─────────────────────────────────────────

# Domain → IronClaw tags mapping (from audit domain categories)
DOMAIN_TO_TAGS = {
    'Bioinformatics & Computational Biology': ['biology', 'bioinformatics', 'genomics'],
    'Chemistry & Molecular Science': ['chemistry', 'molecular-science'],
    'Data Science & Statistics': ['data-science', 'statistics', 'analytics'],
    'Environmental & Earth Sciences': ['environmental', 'earth-science'],
    'Information Retrieval & Search': ['search', 'information-retrieval'],
    'Literature Review & Synthesis': ['literature-review', 'synthesis'],
    'Machine Learning & AI': ['machine-learning', 'ai', 'deep-learning'],
    'Mathematics & Formal Methods': ['mathematics', 'formal-methods'],
    'Medical & Health Sciences': ['medical', 'health', 'clinical'],
    'Physics & Engineering': ['physics', 'engineering'],
    'Scientific Writing & Communication': ['writing', 'communication', 'publishing'],
    'Research Operations & Workflow': ['workflow', 'operations', 'automation'],
}

# Tokens-per-char estimate for context budget (conservative)
_TOKENS_PER_CHAR = 0.3


def _extract_keywords(description, max_keywords=8):
    """Extract meaningful keywords from a skill description."""
    if not description:
        return []
    # Remove common stopwords and short words
    stopwords = {
        'the', 'and', 'for', 'with', 'that', 'this', 'from', 'are', 'can',
        'use', 'used', 'using', 'when', 'will', 'into', 'such', 'also',
        'not', 'but', 'its', 'has', 'have', 'been', 'more', 'than', 'each',
        'all', 'any', 'how', 'about', 'which', 'their', 'does', 'should',
        'would', 'could', 'your', 'you', 'skill',
    }
    words = re.findall(r'[a-z]{3,}', description.lower())
    seen = set()
    keywords = []
    for w in words:
        if w not in stopwords and w not in seen:
            seen.add(w)
            keywords.append(w)
        if len(keywords) >= max_keywords:
            break
    return keywords


def _domain_to_tags(domain):
    """Map audit domain to IronClaw tags."""
    if not domain:
        return []
    # Try exact match first
    if domain in DOMAIN_TO_TAGS:
        return DOMAIN_TO_TAGS[domain]
    # Fuzzy: find first matching key
    domain_lower = domain.lower()
    for key, tags in DOMAIN_TO_TAGS.items():
        if any(word in domain_lower for word in key.lower().split()):
            return tags
    # Fallback: kebab-case the domain
    return [re.sub(r'[^a-z0-9]+', '-', domain.lower()).strip('-')]


def generate_activation(content, entry):
    """Generate IronClaw activation block from SKILL.md content and audit data.

    Returns a YAML string to inject into frontmatter.
    """
    # Extract description from frontmatter for keywords
    description = ''
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            m = re.search(r'^description:\s*["\']?(.+?)(?:["\']?\s*)$',
                          parts[1], re.MULTILINE)
            if m:
                description = m.group(1)

    keywords = _extract_keywords(description)
    tags = _domain_to_tags(entry.get('domain', ''))
    token_estimate = int(len(content) * _TOKENS_PER_CHAR)
    max_tokens = min(max(token_estimate, 500), 8000)

    lines = ['activation:']
    if keywords:
        kw_str = ', '.join(f'"{k}"' for k in keywords)
        lines.append(f'  keywords: [{kw_str}]')
    if tags:
        tag_str = ', '.join(f'"{t}"' for t in tags)
        lines.append(f'  tags: [{tag_str}]')
    lines.append(f'  max_context_tokens: {max_tokens}')

    return '\n'.join(lines)


def inject_activation(content, activation_yaml):
    """Inject activation block into SKILL.md frontmatter.

    If frontmatter exists and doesn't already have activation, add it.
    """
    if not content.startswith('---'):
        return content  # No frontmatter, return as-is

    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    fm = parts[1]
    # Don't overwrite existing activation block
    if re.search(r'^activation:', fm, re.MULTILINE):
        return content

    # Inject before closing ---
    new_fm = fm.rstrip() + '\n' + activation_yaml + '\n'
    return '---' + new_fm + '---' + parts[2]


def patch_name_field(content, new_name):
    """Patch the frontmatter name field to match the deploy directory name.

    Required by Agent Skills spec: name must match parent directory name.
    """
    if not content.startswith('---'):
        return content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content
    fm = parts[1]
    patched = re.sub(r'^(name:\s*)["\']?.*?["\']?\s*$',
                     f'\\1{new_name}', fm, count=1, flags=re.MULTILINE)
    return '---' + patched + '---' + parts[2]


# ── Metadata injection ────────────────────────────────────────────────────

def inject_metadata(content, metadata_dict):
    """Inject or merge metadata as single-line JSON in YAML frontmatter.

    OpenClaw requires metadata as single-line JSON.
    If existing metadata line found, merge keys (new keys take precedence).
    """
    if not content.startswith('---'):
        return content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    fm = parts[1]
    meta_json = json.dumps(metadata_dict, ensure_ascii=False)

    existing_match = re.search(r'^metadata:\s*(.+)$', fm, re.MULTILINE)
    if existing_match:
        try:
            existing = json.loads(existing_match.group(1))
            existing.update(metadata_dict)
            meta_json = json.dumps(existing, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            pass
        new_fm = re.sub(r'^metadata:\s*.+$', f'metadata: {meta_json}',
                        fm, count=1, flags=re.MULTILINE)
    else:
        new_fm = fm.rstrip() + f'\nmetadata: {meta_json}\n'

    return '---' + new_fm + '---' + parts[2]


# ── Deploy name computation ───────────────────────────────────────────────

def compute_all_deploy_names(audit_entries, dedup_index):
    """Precompute normalized deploy names with collision resolution.

    Two-pass algorithm:
    1. Compute initial names (variants get repo-name prefix)
    2. Resolve collisions (add owner prefix where needed, skip theme duplicates)

    Returns (results, conflicts_resolved) where results is aligned with audit_entries.
    """
    results = []
    name_to_indices = {}

    # Pass 1: compute initial names
    for i, entry in enumerate(audit_entries):
        key = (entry['skill_name'], entry['repo'])
        uniqueness = dedup_index.get(key, 'original')
        raw = deploy_name(entry, uniqueness)
        name = normalize_name(raw, 'openclaw')
        reason = _normalization_reason(entry['skill_name'], name, uniqueness)

        results.append({
            'deploy_name': name,
            'raw': raw,
            'reason': reason,
            'skip': False,
        })
        name_to_indices.setdefault(name, []).append(i)

    # Pass 2: resolve collisions
    conflicts_resolved = 0
    for name, indices in name_to_indices.items():
        if len(indices) <= 1:
            continue

        # Group by repo to separate theme-duplicates from real collisions
        repo_groups = {}
        for idx in indices:
            repo = audit_entries[idx]['repo']
            repo_groups.setdefault(repo, []).append(idx)

        # Mark same-repo later entries as skip (theme duplicates)
        for repo_indices in repo_groups.values():
            for idx in repo_indices[1:]:
                results[idx]['skip'] = True

        # Get one representative per repo
        unique_repo_indices = [idxs[0] for idxs in repo_groups.values()]
        if len(unique_repo_indices) <= 1:
            continue

        # Real collision (different repos) → add owner prefix to ALL colliding
        for idx in unique_repo_indices:
            entry = audit_entries[idx]
            key = (entry['skill_name'], entry['repo'])
            uniqueness = dedup_index.get(key, 'original')
            owner = entry['repo'].split('/')[0]
            repo_nm = entry['repo'].split('/')[-1]

            if uniqueness == 'variant':
                raw_prefixed = f"{owner}-{repo_nm}-{entry['skill_name']}"
            else:
                raw_prefixed = f"{owner}-{entry['skill_name']}"

            new_name = normalize_name(raw_prefixed, 'openclaw')
            results[idx]['deploy_name'] = new_name
            results[idx]['raw'] = raw_prefixed
            results[idx]['reason'] = 'collision: owner prefix added'
            conflicts_resolved += 1

    return results, conflicts_resolved


# ── Deploy logic ───────────────────────────────────────────────────────────

def deploy(args):
    """Main deployment logic."""
    print('Loading audit data...')
    audit_data = load_json(AUDIT_PATH)
    dedup_data = load_json(DEDUP_PATH)
    audit_entries = audit_data['results']
    dedup_index = build_dedup_index(dedup_data)

    # Filter by tier if requested
    if args.tier:
        allowed_tiers = set(t.strip().upper() for t in args.tier.split(','))
        before = len(audit_entries)
        audit_entries = [e for e in audit_entries if e.get('research_tier', '').upper() in allowed_tiers]
        print(f'  Tier filter {args.tier}: {before} → {len(audit_entries)}')

    print(f'  Audit entries to deploy: {len(audit_entries)}')

    print('Building disk index (reading frontmatter from all SKILL.md files)...')
    by_dir, by_fm_name = build_disk_index(SKILL_ROOT)

    do_openclaw = args.target in ('all', 'openclaw')
    do_ironclaw = args.target in ('all', 'ironclaw')

    # Precompute deploy names with normalization and collision resolution
    print('Computing deploy names (normalization + collision resolution)...')
    deploy_names, conflicts_resolved = compute_all_deploy_names(
        audit_entries, dedup_index)
    skipped = sum(1 for dn in deploy_names if dn['skip'])
    normalized = sum(1 for dn in deploy_names if dn['reason'] and not dn['skip'])
    print(f'  Names normalized: {normalized}, collisions resolved: {conflicts_resolved}, '
          f'theme duplicates skipped: {skipped}')

    # Prepare output directories
    if not args.dry_run:
        if do_openclaw and os.path.exists(OPENCLAW_DIR):
            shutil.rmtree(OPENCLAW_DIR)
        if do_ironclaw and os.path.exists(IRONCLAW_DIR):
            shutil.rmtree(IRONCLAW_DIR)
        if do_openclaw:
            os.makedirs(OPENCLAW_DIR, exist_ok=True)
        if do_ironclaw:
            os.makedirs(IRONCLAW_DIR, exist_ok=True)

    # Report accumulators
    report = {
        'generated_at': datetime.now().isoformat(),
        'target': args.target,
        'tier_filter': args.tier,
        'dry_run': args.dry_run,
        'openclaw': {'deployed': 0, 'skipped': 0, 'conflicts_resolved': conflicts_resolved},
        'ironclaw': {'deployed': 0, 'activation_injected': 0},
        'name_mappings': [],
        'errors': [],
    }

    deployed_count = 0

    for i, entry in enumerate(audit_entries):
        skill = entry['skill_name']
        repo = entry['repo']

        # Skip theme duplicates (same repo+skill in different themes)
        dn = deploy_names[i]
        if dn['skip']:
            continue

        out_name = dn['deploy_name']

        # Record name mapping if normalization occurred
        if dn['reason']:
            report['name_mappings'].append({
                'original_name': skill,
                'deploy_name': out_name,
                'repo': repo,
                'reason': dn['reason'],
            })

        # Resolve disk path
        disk_path = resolve_skill_path(entry, by_dir, by_fm_name)
        if disk_path is None:
            report['errors'].append({
                'skill': skill, 'repo': repo,
                'error': 'SKILL.md not found on disk',
            })
            if do_openclaw:
                report['openclaw']['skipped'] += 1
            continue

        # Read SKILL.md content
        try:
            with open(disk_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            report['errors'].append({
                'skill': skill, 'repo': repo,
                'error': f'Failed to read: {e}',
            })
            if do_openclaw:
                report['openclaw']['skipped'] += 1
            continue

        # Build metadata (source_repo always; original_name only if changed)
        metadata = {
            'source_repo': repo,
            'source_url': f'https://github.com/{repo}',
        }
        if out_name != skill:
            metadata['original_name'] = skill

        # Ensure frontmatter exists (rare: ~1 file lacks it)
        if not content.startswith('---'):
            content = f'---\nname: {out_name}\n---\n' + content

        # ── OpenClaw deploy ──
        if do_openclaw:
            oc_dir = os.path.join(OPENCLAW_DIR, out_name)
            oc_file = os.path.join(oc_dir, 'SKILL.md')
            oc_content = patch_name_field(content, out_name)
            oc_content = inject_metadata(oc_content, metadata)
            if not args.dry_run:
                os.makedirs(oc_dir, exist_ok=True)
                with open(oc_file, 'w', encoding='utf-8') as f:
                    f.write(oc_content)
            report['openclaw']['deployed'] += 1

        # ── IronClaw deploy (SKILL.md with activation block) ──
        if do_ironclaw:
            ic_dir = os.path.join(IRONCLAW_DIR, out_name)
            ic_file = os.path.join(ic_dir, 'SKILL.md')
            ic_content = patch_name_field(content, out_name)
            ic_content = inject_metadata(ic_content, metadata)
            activation_yaml = generate_activation(content, entry)
            ic_content = inject_activation(ic_content, activation_yaml)
            if not args.dry_run:
                os.makedirs(ic_dir, exist_ok=True)
                with open(ic_file, 'w', encoding='utf-8') as f:
                    f.write(ic_content)
            report['ironclaw']['deployed'] += 1
            if 'activation:' in activation_yaml:
                report['ironclaw']['activation_injected'] += 1

        deployed_count += 1

    # Write report
    if not args.dry_run:
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f'\n{"[DRY RUN] " if args.dry_run else ""}Deployment complete.')
    print(f'  Total entries processed: {len(audit_entries)}')
    print(f'  Names normalized: {len(report["name_mappings"])}')
    if do_openclaw:
        oc = report['openclaw']
        print(f'  OpenClaw: {oc["deployed"]} deployed, {oc["skipped"]} skipped, {oc["conflicts_resolved"]} conflicts resolved')
    if do_ironclaw:
        ic = report['ironclaw']
        print(f'  IronClaw: {ic["deployed"]} deployed, {ic["activation_injected"]} with activation blocks')
    if report['errors']:
        print(f'  Errors: {len(report["errors"])}')
        for err in report['errors'][:10]:
            print(f'    - {err["skill"]} ({err["repo"]}): {err["error"]}')
        if len(report['errors']) > 10:
            print(f'    ... and {len(report["errors"]) - 10} more (see {REPORT_PATH})')

    return report


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Deploy audited SKILL.md files to OpenClaw/IronClaw format'
    )
    parser.add_argument(
        '--target', choices=['all', 'openclaw', 'ironclaw'], default='all',
        help='Deployment target (default: all)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Preview deployment without writing files'
    )
    parser.add_argument(
        '--tier', type=str, default=None,
        help='Comma-separated tiers to deploy (e.g. A,B). Default: all tiers'
    )
    args = parser.parse_args()

    # Validate inputs exist
    for path in (AUDIT_PATH, DEDUP_PATH, SKILL_ROOT):
        if not os.path.exists(path):
            print(f'Error: {path} not found. Run from the project root.', file=sys.stderr)
            sys.exit(1)

    report = deploy(args)

    if report['errors']:
        sys.exit(0)  # Errors are expected (some skills have no SKILL.md on disk)


if __name__ == '__main__':
    main()

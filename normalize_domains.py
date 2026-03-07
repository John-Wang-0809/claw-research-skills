#!/usr/bin/env python3
"""
[IN]  Dependencies/Inputs:
 - multidim_audit.json (1414+ records with domain field)
[OUT] Outputs:
 - multidim_audit.json (updated: domain normalized, domain_original added)
 - domain_mapping.json (mapping from original -> normalized for human review)
 - Backup: multidim_audit.json.bak.phase1b
[POS] Position in the system:
 - Domain normalization script. Reduces domain fragmentation using:
   1. Auto-normalization (case + order)
   2. Keyword-based regex mapping (DOMAIN_RULES)
   3. Skill-name-based fallback (SKILL_NAME_RULES) for "unknown" domains
   Preserves original values in domain_original field.
   Phase 5c extended with additional regex rules and skill_name fallback.

 Change warning: once you modify this file's logic, you must update this
 comment block, and check/update the module doc (README/CLAUDE) in the
 containing folder; update the root global map if necessary.
"""

import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

# ─────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────
BASE = Path(__file__).parent
MULTIDIM_FILE = BASE / "multidim_audit.json"
OUTPUT_MAPPING = BASE / "domain_mapping.json"
BACKUP_SUFFIX = ".bak.phase1b"

# Keyword-based domain mapping rules.
# Order matters: first match wins. More specific patterns go first.
# Each tuple: (compiled_regex_on_lowercase, canonical_category)
DOMAIN_RULES = [
    # ── Life Sciences (specific first) ──
    (r"single.cell|scrna|scatac", "Single-Cell Biology"),
    (r"spatial.transcript", "Spatial Transcriptomics"),
    (r"transcript", "Transcriptomics"),
    (r"proteom|mass.spectrom", "Proteomics"),
    (r"metabolom", "Metabolomics"),
    (r"epigenom|chromatin|histone|methylat", "Epigenomics"),
    (r"metagenom|microbiom", "Metagenomics & Microbiome"),
    (r"immunoinformat|immunolog|flow.cytom|immun", "Immunology & Immunoinformatics"),
    (r"population.genet|phylogenet|evolut.*bio", "Population & Evolutionary Genetics"),
    (r"genom|bioinformat|computational.bio|systems.bio|"
     r"sequenc.*analy|variant.call|vcf",
     "Bioinformatics & Genomics"),
    (r"structur.+bio|protein.struct|molecular.model|alphafold|cryo.?em",
     "Structural Biology"),
    (r"cheminformat|chemoinformat|computational.chem|drug.discov|"
     r"molecular.dock|biochem|enzyme",
     "Computational Chemistry & Drug Discovery"),
    (r"neurosci|brain.imag|eeg|fmri", "Neuroscience"),
    (r"lab.informat|lims|lab.autom|laboratory.autom", "Laboratory Informatics"),
    (r"computational.microscop|high.content.screen|imaging.mass.cytom",
     "Single-Cell Biology"),
    (r"computational.material|material.sci", "Computational Chemistry & Drug Discovery"),
    (r"mycolog", "Environmental & Earth Sciences"),
    (r"molecular.epidemiolog|genetic.epidemiolog", "Population & Evolutionary Genetics"),
    (r"rna.seq.align|nanopore.sequenc|computational.cytom",
     "Bioinformatics & Genomics"),
    (r"clinical|medic|health|pharma|biomedic|patholog",
     "Clinical & Medical Research"),
    (r"ecolog|environment|climate|geosci|earth.sci|remote.sens",
     "Environmental & Earth Sciences"),
    (r"molecular.bio", "Molecular Biology"),

    # ── Computing & Engineering ──
    (r"quantum.comput", "Quantum Computing"),
    (r"reinforcement.learn", "Reinforcement Learning"),
    (r"computer.vision|image.process|multimodal.*ai|vision.*ai",
     "Computer Vision & Multimodal AI"),
    (r"nlp|natural.language.process|text.mining|language.model",
     "Natural Language Processing"),
    (r"interpret|explainab|mechanistic", "AI Interpretability"),
    (r"llm|large.language|agent.*(system|orchestrat|evaluat)|ai.*(engineer|system)|"
     r"autonomous.*(system|agent)|ai.agent|"
     r"ai.*(safe|quality|tool|evaluat|benchmark)|content.modera|"
     r"general.purpose.*ai|multimedia.*ai|azure.*ai",
     "LLM & AI Systems"),
    (r"machine.learn|deep.learn|neural|ml.?ops|model.optim|"
     r"ai.*(research|workflow)|data.science|"
     r"multi.objective.optim|distribut.*comput.*optim",
     "Machine Learning & Data Science"),
    (r"high.perform|hpc|parallel.comput|gpu.comput|"
     r"numerical.comput|scientific.comput|computational.sci|computational.method",
     "High-Performance Computing"),
    (r"audio.process|speech.recogni", "Computer Vision & Multimodal AI"),
    (r"network.sci|graph.analy|graph.neural", "Network Science & Graph Analysis"),
    (r"statistic|bayesian|time.series|causal.infer",
     "Statistics & Mathematical Methods"),

    # ── Software & DevOps ──
    (r"cybersec|security|penetrat|vulnerab|binary.analy|reverse.engin",
     "Cybersecurity"),
    (r"devops|ci.?cd|container|docker|kubernetes|cloud.infra|"
     r"systems?.admin|infrastructure|distribut.*system|consensus.*protocol|"
     r"incident.resp|data.platform.oper",
     "DevOps & Cloud Infrastructure"),
    (r"web.develop|frontend|react|vue|angular|backend|api.develop|"
     r"full.?stack|node\.?js|django|flask|fastapi|"
     r"web.app.*develop|e.commerce.*develop|web.autom",
     "Web Development"),
    (r"mobile.develop|ios|android|react.native|flutter", "Mobile Development"),
    (r"database|sql|nosql|data.engineer|etl|data.pipeline|"
     r"data.analyt.*engineer|data.manag.*spreadsheet|data.platform|"
     r"spreadsheet",
     "Data Engineering & Databases"),
    (r"software.*(eng|develop|quality)|code.quality|test|debug|refactor|"
     r"research.software|software.architect|systems.programm|"
     r"performance.optim|systems.optim|product.engineer|"
     r"version.control|python.*(program|package)|cli.develop|"
     r"engineer.*(lead|manag)",
     "Software Engineering"),

    # ── Research Process ──
    (r"data.visual|scientif.*visual|plot|chart|present",
     "Data Visualization & Communication"),
    (r"scientif.*(writ|communic|publish)|academ.*(writ|communic|present|publish|"
     r"disseminat|document|paper.*(prep|public))|scholarly|manuscript|"
     r"research.disseminat|citation|research.communic|"
     r"scientif.*(report|document)|science.commun|"
     r"corporate.communic|business.communic",
     "Scientific Writing & Communication"),
    (r"literature.review|systematic.review|evidence.synth|meta.analy|"
     r"literature.analy|research.synth|"
     r"literature.*discover|bibliograph|academ.*literature|"
     r"literature.*retriev|literature.*search",
     "Literature Review & Evidence Synthesis"),
    (r"grant|fund|proposal", "Research Grant & Funding"),
    (r"research.method|research.design|experiment.design|survey.method|"
     r"qualitative|quantitative.research|cross.disciplin|interdisciplin|"
     r"multi.?disciplin|scientif.*method|hypothesis.*develop|"
     r"research.strateg|scientif.*protocol",
     "Research Methodology"),
    (r"research.*(integrity|ethic|reproduc|verif)|peer.review|"
     r"scientif.*reproduc|data.*reproduc",
     "Research Integrity & Verification"),
    (r"research.*(oper|infra|comput|tool|workflow)|"
     r"information.retriev|data.collect|document.process|"
     r"document.engineer|office.automat|data.access|data.retriev|"
     r"research.automat|research.document|data.analy(?!tic)|"
     r"research.*(data|inform|plan|organiz|coordinat|conversation|knowledge|support)|"
     r"knowledge.manag|documentation.manag|technical.doc.*manag|"
     r"research.*(content|literatur.*discover)|"
     r"web.*research.*inform|technology.*research.*doc",
     "Research Operations & Infrastructure"),
    (r"project.manage|workflow.organ|task.manage|agile|scrum|"
     r"workflow.*(orchestrat|autom)",
     "Project Management"),
    (r"teach|educat|pedagog|tutori|learn.*platform",
     "Education & Training"),

    # ── Domain-Specific ──
    (r"financ|trading|quant|portfolio|econom|market",
     "Finance & Economics"),
    (r"geograph|gis|spatial.*analy|cartograph|geospat",
     "Geospatial Analysis"),
    (r"physics|astro|cosmol|particle", "Physics & Astronomy"),
    (r"math|algebra|topology|number.theory", "Mathematics"),
    (r"social.sci|sociolog|psycholog|political|anthropol",
     "Social Sciences"),
    (r"legal|law|regulat|complian|patent|intellectual.prop",
     "Legal & Compliance"),
    (r"marketing|seo|content.creat|copywriting",
     "Marketing & Content"),
    (r"design|ux|ui|user.experience|figma|accessibility",
     "Design & User Experience"),

    # ── Catch-all for Claude/tool-specific ──
    (r"claude|mcp|anthropic|skill", "Claude Code & Tools"),
]

# Compile regex patterns once
COMPILED_RULES = [(re.compile(pat, re.IGNORECASE), cat) for pat, cat in DOMAIN_RULES]


def auto_normalize(domain):
    """Normalize by lowercasing, splitting on separators, sorting, rejoining.

    This merges "A/B" with "B/A", "a / b" with "A/B", etc.
    """
    if not domain or domain == "unknown":
        return domain.lower() if domain else ""
    # Split on /, &, and |
    parts = re.split(r"\s*/\s*|\s*&\s*|\s*\|\s*", domain)
    parts = [p.strip().lower() for p in parts if p.strip()]
    if not parts:
        return domain.lower()
    parts.sort()
    return " / ".join(parts)


def keyword_map(normalized_domain):
    """Map a normalized domain string to a canonical category via regex rules."""
    if not normalized_domain or normalized_domain == "unknown":
        return "Unknown"
    for pattern, category in COMPILED_RULES:
        if pattern.search(normalized_domain):
            return category
    return None  # No match


# Skill-name-based domain inference for entries with "unknown" domain_original.
# Order matters: first match wins. More specific patterns first.
SKILL_NAME_RULES = [
    # Life Sciences
    (r"bio-metagenom", "Metagenomics & Microbiome"),
    (r"bio-methylat|bio-epitranscript", "Epigenomics"),
    (r"bio-rna|bio-ribo", "Transcriptomics"),
    (r"bio-pdb|bio-.*struct", "Structural Biology"),
    (r"bio-pathway", "Bioinformatics & Genomics"),
    (r"bio-", "Bioinformatics & Genomics"),
    (r"scvi.tool|opentarget|pyopenms", "Bioinformatics & Genomics"),
    # Security
    (r"vulnerab|exploit|xss|injection|pentest|burp|scanner|"
     r"cross.site|fuzzing|security|wireshark|red.team|stride.analy|libafl|"
     r"cosmos.vulnerab",
     "Cybersecurity"),
    # AI/ML
    (r"fine.tuning|evaluating.*(llm|code.model|model)|"
     r"rlhf|train.*model|lora|qlora|gemini.api|"
     r"agent.?db|deep.research|creative.thinking.for.research|"
     r"llama.cpp|sparse.autoencod|training.llm|optimizing.attention|"
     r"hugging.face|torch.geometric|llm.evaluat|phoenix.observab",
     "Machine Learning & Data Science"),
    (r"llm.app.pattern|rag.engineer|prompt.cach|prompt.engineer|"
     r"v3.deep.integrat",
     "LLM & AI Systems"),
    # Computer Vision
    (r"senior.computer.vision", "Computer Vision & Multimodal AI"),
    # DevOps
    (r"github.*(workflow|code.review|action)|distribut.*trac|"
     r"azure.map|cloud|linux.prod.*shell",
     "DevOps & Cloud Infrastructure"),
    # Web
    (r"frontend.dev|web.scraping",
     "Web Development"),
    # Data Viz / Office docs
    (r"paper.visual|pptx|xlsx", "Data Visualization & Communication"),
    # Comms/Writing
    (r"content.research.writer|content.writing|post.accept",
     "Scientific Writing & Communication"),
    # Research Integrity
    (r"peer.review", "Research Integrity & Verification"),
    # Research Ops
    (r"exa.search|context7.auto.research|research.planning|"
     r"wiki.research|notion.autom|surveymonkey|"
     r"box.autom|dropbox.autom|gmail.autom|google.*(sheet|drive)",
     "Research Operations & Infrastructure"),
    # Research Methodology
    (r"research.before.coding|first.?princip",
     "Research Methodology"),
    # Claude Code
    (r"mcp.server.manag|update.skill|writing.hookify|"
     r"spec.workflow.orchestrat",
     "Claude Code & Tools"),
    # Project Management
    (r"pi.planning", "Project Management"),
    # Software
    (r"codebase.cleanup|code.review|error.diagnos|"
     r"fp.ts|typescript|data.engineer|java.architect|"
     r"property.based.test",
     "Software Engineering"),
    # Data Engineering
    (r"pytd", "Data Engineering & Databases"),
    # Azure AI
    (r"azure.ai|textanalyt",
     "LLM & AI Systems"),
    # NLP
    (r"text.analy|sentiment",
     "Natural Language Processing"),
    # Context/LLM
    (r"context.engineer",
     "LLM & AI Systems"),
]

COMPILED_SKILL_NAME_RULES = [
    (re.compile(pat, re.IGNORECASE), cat)
    for pat, cat in SKILL_NAME_RULES
]


def skill_name_map(skill_name):
    """Infer domain from skill_name for entries with unknown domain_original."""
    if not skill_name:
        return None
    for pattern, category in COMPILED_SKILL_NAME_RULES:
        if pattern.search(skill_name):
            return category
    return None


def normalize_all_domains(multidim_data):
    """Normalize all domain values in multidim_data.

    Returns (mapping_dict, stats).
    """
    mapping = {}  # original_domain -> canonical_category
    unmapped = Counter()
    category_counts = Counter()

    for entry in multidim_data["results"]:
        # Always normalize from original value (supports re-runs)
        if "domain_original" in entry:
            original = entry["domain_original"]
        else:
            original = entry.get("domain", "")
            entry["domain_original"] = original

        # Auto-normalize
        auto_norm = auto_normalize(original)

        # Keyword map
        canonical = keyword_map(auto_norm)

        if canonical is None:
            # No rule matched — try the original (un-normalized) too
            canonical = keyword_map(original.lower())

        # For "Unknown" results, try skill-name-based inference as fallback
        if canonical is None or canonical == "Unknown":
            skill_name = entry.get("skill_name", "")
            inferred = skill_name_map(skill_name)
            if inferred is not None:
                canonical = inferred

        if canonical is None:
            unmapped[auto_norm] += 1
            canonical = "Other"

        entry["domain"] = canonical
        mapping[original] = canonical
        category_counts[canonical] += 1

    return mapping, {
        "total_entries": len(multidim_data["results"]),
        "unique_original": len(set(
            e.get("domain_original", "") for e in multidim_data["results"]
        )),
        "unique_normalized": len(category_counts),
        "category_counts": dict(sorted(
            category_counts.items(), key=lambda x: -x[1]
        )),
        "unmapped_count": len(unmapped),
        "unmapped_top": dict(unmapped.most_common(20)),
    }


def main():
    """Main entry point for normalize_domains."""
    print("=" * 60)
    print("Phase 1b: Normalize Domain Values")
    print("=" * 60)

    # Load data
    print("\n1. Loading multidim_audit.json...")
    multidim_data = load_json(MULTIDIM_FILE)
    total = len(multidim_data["results"])

    # Pre-normalization stats
    pre_domains = Counter(
        e.get("domain", "") for e in multidim_data["results"]
    )
    print(f"   {total} entries, {len(pre_domains)} unique domains")

    # Backup
    print("\n2. Creating backup...")
    backup_path = str(MULTIDIM_FILE) + BACKUP_SUFFIX
    shutil.copy2(MULTIDIM_FILE, backup_path)
    print(f"   Backed up to {backup_path}")

    # Normalize
    print("\n3. Normalizing domains...")
    mapping, stats = normalize_all_domains(multidim_data)
    print(f"   Original unique domains: {stats['unique_original']}")
    print(f"   Normalized categories: {stats['unique_normalized']}")
    print(f"   Unmapped entries (-> 'Other'): {stats['unmapped_count']}")

    # Show category distribution
    print("\n4. Category distribution:")
    for cat, cnt in sorted(
        stats["category_counts"].items(), key=lambda x: -x[1]
    ):
        print(f"   {cnt:5d}  {cat}")

    # Show unmapped samples
    if stats["unmapped_top"]:
        print("\n5. Top unmapped domains (assigned to 'Other'):")
        for dom, cnt in stats["unmapped_top"].items():
            print(f"   {cnt:4d}  {dom}")

    # Verification
    print("\n6. Verification...")
    post_total = len(multidim_data["results"])
    has_original = sum(
        1 for e in multidim_data["results"] if "domain_original" in e
    )
    unique_final = len(set(
        e.get("domain", "") for e in multidim_data["results"]
    ))

    print(f"   Total entries: {post_total} (should be {total})")
    print(f"   Entries with domain_original: {has_original} (should be {total})")
    print(f"   Final unique domains: {unique_final}")

    ok = True
    if post_total != total:
        print("   ERROR: Total entry count changed!")
        ok = False
    if has_original != total:
        print("   ERROR: Not all entries have domain_original!")
        ok = False
    if unique_final > 60:
        print(f"   WARNING: {unique_final} categories is more than target 30-50")

    # Save
    if ok:
        print("\n7. Saving updated multidim_audit.json...")
        save_json(MULTIDIM_FILE, multidim_data)
        print("   Done!")

        print("\n8. Saving domain_mapping.json...")
        mapping_output = {
            "metadata": {
                "original_unique": stats["unique_original"],
                "normalized_unique": stats["unique_normalized"],
                "unmapped_count": stats["unmapped_count"],
            },
            "category_counts": stats["category_counts"],
            "mapping": {k: v for k, v in sorted(mapping.items())},
            "unmapped_samples": stats["unmapped_top"],
        }
        save_json(OUTPUT_MAPPING, mapping_output)
        print("   Done!")
    else:
        print("\n7. SKIPPING save due to errors above.")
        sys.exit(1)

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Domains: {len(pre_domains)} -> {unique_final} categories")
    print(f"  Unmapped (Other): {stats['unmapped_count']}")
    print(f"  Outputs: multidim_audit.json, domain_mapping.json")
    print("=" * 60)


def load_json(filepath):
    """Load JSON file with UTF-8 encoding."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    """Save JSON file with UTF-8 encoding, indented for readability."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

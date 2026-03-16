# Research Skills Catalog

> **1,367 audited research skills** from 56 GitHub repositories — curated, classified, and ready to deploy to Claude Code, OpenClaw, or IronClaw.

## What Is This?

A curated catalog of [Agent Skills](https://github.com/anthropics/skills) (SKILL.md files) for scientific research, covering everything from genome assembly to literature review to statistical analysis. Each skill has been through multi-dimensional LLM audit (accuracy, relevance, credibility) and classified by research tier, domain, and added value.

**Key numbers:**

| Metric | Value |
|--------|-------|
| Audited skills | 1,408 |
| In catalog | 1,367 (41 filtered) |
| Source repositories | 56 |
| Research themes | 6 |
| Description accuracy | 99.3% (after 9 audit rounds) |
| Platform-ready | OpenClaw + IronClaw deployment included |

## Quick Start

### Browse the Catalog

- **[SKILL_CATALOG.md](SKILL_CATALOG.md)** — Full English catalog (Skill / Description / Tier / Domain / Value / URL)
- **[科研技能目录.md](科研技能目录.md)** — Chinese translation

### Deploy to OpenClaw / IronClaw

```bash
# Generate deployment directories
python deploy_skills.py                    # Both platforms
python deploy_skills.py --target openclaw  # OpenClaw only
python deploy_skills.py --target ironclaw  # IronClaw only
python deploy_skills.py --dry-run          # Preview without writing
python deploy_skills.py --tier A,B         # Deploy only top-tier skills

# Install to OpenClaw
cp -r openclaw_deploy/* ~/.openclaw/skills/

# IronClaw output includes activation blocks for smart skill selection
```

All 1,391 deployed names comply with the [Agent Skills specification](https://agentskills.io/specification) (`[a-z0-9-]`, max 64 chars).

### Use a Single Skill

Copy any `SKILL.md` from `Final_Research_Skills_Link_Downloads_By_Theme_LATEST/` to your Claude Code skills directory:

```bash
# Example: use the genome assembly skill
cp Final_Research_Skills_Link_Downloads_By_Theme_LATEST/03_.../sanger-pathogens__skills/bio-genome-assembly-short-read-assembly/SKILL.md \
   ~/.claude/skills/bio-genome-assembly/SKILL.md
```

## Research Themes

| # | Theme | Skills |
|---|-------|--------|
| 01 | Information Retrieval & Evidence Collection | 140 |
| 02 | Literature Review, Writing & Citation | 505 |
| 03 | Experiment, Benchmarking & Reproducibility | 502 |
| 04 | Data Analysis & Evidence Interpretation | 164 |
| 05 | Research Operations & Workflow | 50 |
| 06 | Additional Scientific Skills | 17 |

Theme documents are in [`Final_Research_Skills_Thematic_Split/`](Final_Research_Skills_Thematic_Split/).

## Repository Structure

```
research-skills/
├── SKILL_CATALOG.md                        # English catalog (1,367 skills)
├── 科研技能目录.md                          # Chinese catalog
├── deploy_skills.py                        # Platform deployment script
├── multidim_audit.json                     # Audit database (1,408 entries)
├── Final_Research_Skills_Thematic_Split/   # Theme documents (source data)
└── Final_Research_Skills_Link_Downloads_By_Theme_LATEST/
    └── <theme>/<owner__repo>/<skill>/SKILL.md  # 2,062 skill files
```

## Audit Quality

Each skill was evaluated across 4 dimensions:

- **research_tier** (A/B/C/D) — How central to research workflows
- **domain** — Normalized to 50 categories (from 979 original labels)
- **added_value** — Whether the skill provides unique value (high/medium/low)
- **doc_completeness** — Quality of documentation

## Cross-Platform Compatibility

Skills follow the [Anthropic Agent Skills open standard](https://github.com/anthropics/skills) (YAML frontmatter + Markdown body). ~90% work directly on any compatible platform without modification.

| Platform | Status |
|----------|--------|
| Claude Code | Native (original target) |
| OpenClaw | Compatible — use `deploy_skills.py` for directory conversion |
| IronClaw | Compatible — deployment includes `activation` blocks |
| OpenAI Codex CLI | Compatible (same standard) |

## License

This project is [MIT licensed](LICENSE). Individual SKILL.md files retain the license specified in their source repositories — check the `license` field in each file's YAML frontmatter before redistribution.

## Attribution

All skills in this catalog originate from open-source GitHub repositories. Each skill entry in [SKILL_CATALOG.md](SKILL_CATALOG.md) includes a direct URL to the original SKILL.md file on GitHub. Deployed skills also include `metadata.source_repo` in their frontmatter for traceability.

<details>
<summary><strong>Source Repositories (60)</strong></summary>

| Repository | Link |
|------------|------|
| 199-biotechnologies/claude-deep-research-skill | [GitHub](https://github.com/199-biotechnologies/claude-deep-research-skill) |
| CUN-bjy/research-skills | [GitHub](https://github.com/CUN-bjy/research-skills) |
| Chenghao-Wu/skill_lammps | [GitHub](https://github.com/Chenghao-Wu/skill_lammps) |
| ComposioHQ/awesome-claude-skills | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills) |
| DasBluEyedDevil/Daem0n-MCP | [GitHub](https://github.com/DasBluEyedDevil/Daem0n-MCP) |
| EveryInc/every-marketplace | [GitHub](https://github.com/EveryInc/every-marketplace) |
| ForaeFactory/antigravity-skills | [GitHub](https://github.com/ForaeFactory/antigravity-skills) |
| GPTomics/bioSkills | [GitHub](https://github.com/GPTomics/bioSkills) |
| Galaxy-Dawn/claude-scholar | [GitHub](https://github.com/Galaxy-Dawn/claude-scholar) |
| GitZH-Chen/AI-Research-Skills | [GitHub](https://github.com/GitZH-Chen/AI-Research-Skills) |
| HKUDS/DeepCode | [GitHub](https://github.com/HKUDS/DeepCode) |
| Jeffallan/claude-skills | [GitHub](https://github.com/Jeffallan/claude-skills) |
| K-Dense-AI/claude-scientific-skills | [GitHub](https://github.com/K-Dense-AI/claude-scientific-skills) |
| K-Dense-AI/claude-scientific-writer | [GitHub](https://github.com/K-Dense-AI/claude-scientific-writer) |
| Orchestra-Research/AI-Research-SKILLs | [GitHub](https://github.com/Orchestra-Research/AI-Research-SKILLs) |
| OthmanAdi/planning-with-files | [GitHub](https://github.com/OthmanAdi/planning-with-files) |
| Prat011/awesome-llm-skills | [GitHub](https://github.com/Prat011/awesome-llm-skills) |
| Przemocny/generic-skills | [GitHub](https://github.com/Przemocny/generic-skills) |
| Ronitnair/research-skills | [GitHub](https://github.com/Ronitnair/research-skills) |
| Shubhamsaboo/awesome-llm-apps | [GitHub](https://github.com/Shubhamsaboo/awesome-llm-apps) |
| Weizhena/Deep-Research-skills | [GitHub](https://github.com/Weizhena/Deep-Research-skills) |
| WilsonWukz/paper-visualizer-skill | [GitHub](https://github.com/WilsonWukz/paper-visualizer-skill) |
| acertainKnight/project-thoth | [GitHub](https://github.com/acertainKnight/project-thoth) |
| affaan-m/everything-claude-code | [GitHub](https://github.com/affaan-m/everything-claude-code) |
| ahmedibrahim085/Claude-Multi-Agent-Research-System-Skill | [GitHub](https://github.com/ahmedibrahim085/Claude-Multi-Agent-Research-System-Skill) |
| alaliqing/claude-paper | [GitHub](https://github.com/alaliqing/claude-paper) |
| alirezarezvani/claude-skills | [GitHub](https://github.com/alirezarezvani/claude-skills) |
| anombyte93/claude-research-skill | [GitHub](https://github.com/anombyte93/claude-research-skill) |
| anthropics/claude-agent-sdk-demos | [GitHub](https://github.com/anthropics/claude-agent-sdk-demos) |
| anthropics/claude-code | [GitHub](https://github.com/anthropics/claude-code) |
| anthropics/life-sciences | [GitHub](https://github.com/anthropics/life-sciences) |
| anthropics/skills | [GitHub](https://github.com/anthropics/skills) |
| biocontext-ai/skill-to-mcp | [GitHub](https://github.com/biocontext-ai/skill-to-mcp) |
| coffeefuelbump/csv-data-summarizer-claude-skill | [GitHub](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) |
| danielmiessler/Personal_AI_Infrastructure | [GitHub](https://github.com/danielmiessler/Personal_AI_Infrastructure) |
| hangoclong/skills-antigravity-awesome | [GitHub](https://github.com/hangoclong/skills-antigravity-awesome) |
| huysynf/antigravity-awesome-skills | [GitHub](https://github.com/huysynf/antigravity-awesome-skills) |
| issol14/paper2code-skill | [GitHub](https://github.com/issol14/paper2code-skill) |
| langchain-ai/deepagents | [GitHub](https://github.com/langchain-ai/deepagents) |
| liangdabiao/simple_claude_deep_research_agent | [GitHub](https://github.com/liangdabiao/simple_claude_deep_research_agent) |
| luwill/research-skills | [GitHub](https://github.com/luwill/research-skills) |
| makenotion/notion-cookbook | [GitHub](https://github.com/makenotion/notion-cookbook) |
| masinu/wemush-skills | [GitHub](https://github.com/masinu/wemush-skills) |
| mrgoonie/claudekit-skills | [GitHub](https://github.com/mrgoonie/claudekit-skills) |
| muratcankoylan/Agent-Skills-for-Context-Engineering | [GitHub](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |
| oinani0721/zero-hallucination-research | [GitHub](https://github.com/oinani0721/zero-hallucination-research) |
| proyecto26/research-skills | [GitHub](https://github.com/proyecto26/research-skills) |
| proyecto26/sherlock-ai-plugin | [GitHub](https://github.com/proyecto26/sherlock-ai-plugin) |
| rand/cc-polymath | [GitHub](https://github.com/rand/cc-polymath) |
| ruvnet/claude-flow | [GitHub](https://github.com/ruvnet/claude-flow) |
| sickn33/antigravity-awesome-skills | [GitHub](https://github.com/sickn33/antigravity-awesome-skills) |
| sstklen/infinite-gratitude | [GitHub](https://github.com/sstklen/infinite-gratitude) |
| tommy-ca/notion-skills | [GitHub](https://github.com/tommy-ca/notion-skills) |
| trailofbits/skills | [GitHub](https://github.com/trailofbits/skills) |
| treasure-data/td-skills | [GitHub](https://github.com/treasure-data/td-skills) |
| u9401066/pubmed-search-mcp | [GitHub](https://github.com/u9401066/pubmed-search-mcp) |
| wshobson/agents | [GitHub](https://github.com/wshobson/agents) |
| xpepper/perplexity-agent-skill | [GitHub](https://github.com/xpepper/perplexity-agent-skill) |
| ychampion/claude-self-learning | [GitHub](https://github.com/ychampion/claude-self-learning) |
| zsyggg/paper-craft-skills | [GitHub](https://github.com/zsyggg/paper-craft-skills) |

</details>

## Known Limitations

- `scientific-writing`: Path not found under Claude Scholar repo; GitHub URL needs manual confirmation
- `spatial-econometrics`: Source labeled only "chan"; cannot uniquely locate GitHub repo

# Research Skills Catalog

> **1,367 quality-checked research skills** from 56 GitHub repositories — ready to use in Claude Code, OpenClaw, or IronClaw.

A curated collection of [Agent Skills](https://github.com/anthropics/skills) (SKILL.md files) for scientific research, covering genome assembly, literature review, statistical analysis, and more. Each skill is classified by research tier, domain, and added value.

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/John-Wang-0809/claw-research-skills.git
cd claw-research-skills
```

No external dependencies — only Python 3.7+ standard library is required.

### 2. Browse the Catalog

- **[SKILL_CATALOG.md](SKILL_CATALOG.md)** — Full English catalog (Skill / Description / Tier / Domain / Value / URL)
- **[SKILL_CATALOG_CN.md](SKILL_CATALOG_CN.md)** — Chinese translation

### 3. Use a Single Skill in Claude Code

Copy any `SKILL.md` into your Claude Code skills directory:

```bash
# List available skills under a theme
ls Final_Research_Skills_Link_Downloads_By_Theme_LATEST/03_experiment_benchmark_reproducibility_validation/

# Copy a skill to Claude Code
cp Final_Research_Skills_Link_Downloads_By_Theme_LATEST/03_experiment_benchmark_reproducibility_validation/anthropics__life-sciences/scvi-tools/SKILL.md \
   ~/.claude/skills/scvi-tools/SKILL.md
```

Claude Code will automatically discover skills under `~/.claude/skills/`.

### 4. Batch Deploy to OpenClaw / IronClaw

```bash
# Preview what will be deployed (no files written)
python deploy_skills.py --dry-run

# Generate deployment directories
python deploy_skills.py                    # Both platforms
python deploy_skills.py --target openclaw  # OpenClaw only
python deploy_skills.py --target ironclaw  # IronClaw only
python deploy_skills.py --tier A,B         # Deploy only top-tier skills

# Install to OpenClaw
cp -r openclaw_deploy/* ~/.openclaw/skills/

# Install to IronClaw
cp -r ironclaw_deploy/* ~/.ironclaw/skills/
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

## Platform Compatibility

| Platform | Status |
|----------|--------|
| Claude Code | Native support |
| OpenClaw | Compatible — use `deploy_skills.py` |
| IronClaw | Compatible — deployment includes `activation` blocks |
| OpenAI Codex CLI | Compatible |

## License

[MIT licensed](LICENSE). Individual SKILL.md files retain the license from their source repositories — check the `license` field in each file's YAML frontmatter before redistribution.

## Source Repositories

All skills originate from open-source GitHub repositories. Each entry in [SKILL_CATALOG.md](SKILL_CATALOG.md) links to the original file.

<details>
<summary><strong>56 Source Repositories</strong></summary>

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

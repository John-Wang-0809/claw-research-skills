# Audit Report: 03 Experiment, Benchmark, Reproducibility & Validation

- Audit Date: 2026-02-26
- Theme Document: `Final_Research_Skills_Thematic_Split/03_experiment_benchmark_reproducibility_validation.md`
- Theme Doc Claimed Skill Count: 648
- Actual Skill Rows in Theme Doc: 601
- Local SKILL.md Files Downloaded: 736
- Unique GitHub Repos in Theme Doc: 34
- Local Repo Directories: 42
- URL Valid: 34 | URL Updated: 0 | URL Broken: 0
- Content Corrections: See below

## Executive Summary

All 34 GitHub repository URLs are valid and accessible. No broken or migrated URLs found.

However, three systemic issues were identified:

1. **Templated "Why Research-Related" field**: All 601 skill entries use the identical generic text
   "Supports experiment design, benchmarking, reproducibility, and quantitative validation."
   This provides zero differentiation and does not explain WHY each specific skill belongs in this theme.

2. **Templated "Function Explanation" field**: All 601 entries follow the same template:
   "This skill centers on [name] and primarily provides [truncated description]. It supports
   experiment setup, benchmark evaluation, and reproducibility-oriented validation. In research
   workflows, it helps produce measurable comparisons, logs, and defensible conclusions."
   The actual skill description is truncated mid-sentence and padded with generic filler.

3. **Skill count discrepancy**: Theme doc header claims 648 skills, but only 601 actual skill
   rows exist. Additionally, 8 local repo directories (with 135 SKILL.md files) have no
   corresponding section in the theme document.

## Systemic Issue: Questionable Theme Classification

Many skills in this theme have no clear connection to "experiment design, benchmarking,
reproducibility, or validation." Examples of misclassified skills:

- `django-patterns` (affaan-m) - Django web framework patterns, not experiment-related
- `springboot-patterns` (affaan-m) - Spring Boot backend patterns
- `continuous-learning` (affaan-m) - Claude Code session pattern extraction
- `BrightData` (danielmiessler) - Web scraping tool
- `Browser` (danielmiessler) - Browser automation
- `PromptInjection` (danielmiessler) - LLM security testing
- `nextjs-best-practices` (ForaeFactory) - Next.js web framework
- `nodejs-best-practices` (ForaeFactory) - Node.js development
- `Cloud Penetration Testing` (ForaeFactory) - Security testing
- `Broken Authentication Testing` (ForaeFactory) - Security testing
- `conversation-memory` (ForaeFactory) - LLM memory systems
- `prompt-caching` (ForaeFactory) - LLM prompt caching
- `software-architecture` (ForaeFactory) - General software architecture
- `andrew-kane-gem-writer` (EveryInc) - Ruby gem writing patterns
- `skill-developer` (diet103, ForaeFactory) - Claude Code skill creation
- `Apify Automation` (ComposioHQ) - Web scraping automation
- `Mistral AI Automation` (ComposioHQ) - Mistral AI operations

These skills appear to have been bulk-assigned to this theme via keyword matching rather
than genuine relevance assessment.

## URL Verification Results (All 34 Repos)

| # | Repository | URL Status | Description (from GitHub) |
|---|-----------|-----------|--------------------------|
| 1 | affaan-m/everything-claude-code | ✓ | Complete Claude Code configuration collection |
| 2 | ahmedibrahim085/Claude-Multi-Agent-Research-System-Skill | ✓ | Multi-Agent Research System using Claude Code Skills |
| 3 | alirezarezvani/claude-skills | ✓ | Collection of Skills for Claude Code and Claude AI |
| 4 | anthropics/claude-code | ✓ | Agentic coding tool in terminal |
| 5 | anthropics/life-sciences | ✓ | Claude Code Marketplace for Life Sciences |
| 6 | coffeefuelbump/csv-data-summarizer-claude-skill | ✓ | CSV file analysis with summary statistics |
| 7 | ComposioHQ/awesome-claude-skills | ✓ | Curated list of Claude Skills and resources |
| 8 | CUN-bjy/research-skills | ✓ | AI research skills for Claude Code |
| 9 | danielmiessler/Personal_AI_Infrastructure | ✓ | Agentic AI Infrastructure for human capabilities |
| 10 | diet103/claude-code-infrastructure-showcase | ✓ | Claude Code infrastructure examples |
| 11 | dion-jy/research-skills | ✓ | AI research skills for Claude Code |
| 12 | Dr-AneeshJoseph/Claude-Metacognitive-Skills | ✓ | LLM Metacognition research skills |
| 13 | EveryInc/every-marketplace | ✓ | Claude Code compound engineering plugin |
| 14 | ForaeFactory/antigravity-skills | ✓ | 200+ Agentic Skills for Claude Code |
| 15 | GPTomics/bioSkills | ✓ | Bioinformatics skills for AI agents |
| 16 | hangoclong/skills-antigravity-awesome | ✓ | 200+ Agentic Skills (fork) |
| 17 | huysynf/antigravity-awesome-skills | ✓ | 200+ Agentic Skills (fork) |
| 18 | Jeffallan/claude-skills | ✓ | 66 Specialized Skills for Full-Stack Developers |
| 19 | K-Dense-AI/claude-scientific-skills | ✓ | 147+ scientific and research skills |
| 20 | mrgoonie/claudekit-skills | ✓ | ClaudeKit skills marketplace |
| 21 | muratcankoylan/Agent-Skills-for-Context-Engineering | ✓ | Agent Skills for context engineering |
| 22 | obra/superpowers | ✓ | Agentic skills framework & dev methodology |
| 23 | Orchestra-Research/AI-Research-SKILLs | ✓ | AI research and engineering skills library |
| 24 | proyecto26/research-skills | ✓ | Sherlock AI research skills |
| 25 | proyecto26/sherlock-ai-plugin | ✓ | Sherlock AI plugin for research |
| 26 | rand/cc-polymath | ✓ | Claude Code skills for context-efficiency |
| 27 | ruvnet/claude-flow | ✓ | Enterprise AI orchestration platform |
| 28 | Shubhamsaboo/awesome-llm-apps | ✓ | Collection of awesome LLM apps |
| 29 | sickn33/antigravity-awesome-skills | ✓ | 946+ Agentic Skills (original) |
| 30 | trailofbits/skills | ✓ | Security research skills for Claude Code |
| 31 | treasure-data/td-skills | ✓ | Treasure Data Skills for Claude Code |
| 32 | Weizhena/Deep-Research-skills | ✓ | Deep research skill with human-in-the-loop |
| 33 | wshobson/agents | ✓ | Multi-agent orchestration for Claude Code |
| 34 | zubayer0077/Claude-Multi-Agent-Research-System-Skill | ✓ | Multi-agent research system |

## Missing from Theme Doc (Local Dirs with No Theme Section)

8 local repo directories exist in the downloads folder but have no corresponding `### repo`
section in the theme document:

| # | Local Directory | Local SKILL.md Count | Notes |
|---|----------------|---------------------|-------|
| 1 | K-Dense-AI__claude-scientific-writer | 1 | Has local files, missing from theme doc |
| 2 | Prat011__awesome-llm-skills | 2 | Has local files, missing from theme doc |
| 3 | aaron-he-zhu__seo-geo-claude-skills | 1 | Has local files, missing from theme doc |
| 4 | anthropics__skills | 1 | Has local files, missing from theme doc |
| 5 | forgeclaw-dev__puter-ai-skill | 1 | Has local files, missing from theme doc |
| 6 | langchain-ai__deepagents | 2 | Has local files, missing from theme doc |
| 7 | le-dat__claude-skill-engineer | 1 | Has local files, missing from theme doc |
| 8 | lignertys__reddit-research-skills | 1 | Has local files, missing from theme doc |

Total missing skills: ~10 SKILL.md files downloaded but not in theme doc.

## Content Accuracy Sampling (Local SKILL.md vs Theme Doc)

Sampled 6 local SKILL.md files against theme doc entries:

| Skill | Repo | Local Description Match | Workflow Match | Notes |
|-------|------|------------------------|---------------|-------|
| bio-alignment-validation | GPTomics/bioSkills | Partial | Partial | Theme doc truncates description; workflow is generic |
| adaptyv | K-Dense-AI/claude-scientific-skills | Partial | Partial | Theme doc truncates "Cloud laboratory platform..." |
| django-patterns | affaan-m/everything-claude-code | ✓ | ✓ | Description matches but skill is not research-related |
| golang-testing | affaan-m/everything-claude-code | ✓ | ✓ | Description matches; workflow from SKILL.md "When to Activate" |
| springboot-patterns | affaan-m/everything-claude-code | ✓ | ✓ | Description matches but skill is not research-related |
| continuous-learning | affaan-m/everything-claude-code | ✓ | ✓ | Description matches but skill is not research-related |

Key finding: The "Function Explanation" column in the theme doc consistently truncates the
actual SKILL.md description at ~100 characters and appends generic filler text. The "Execution
Flow" column extracts bullet points or list items from the SKILL.md but does not represent a
coherent workflow.

## Skill Count by Repository (Theme Doc)

| Repository | Skills in Theme Doc | Local SKILL.md Files |
|-----------|--------------------|--------------------|
| GPTomics/bioSkills | ~178 | 178 |
| sickn33/antigravity-awesome-skills | ~112 | 161 |
| K-Dense-AI/claude-scientific-skills | ~63 | 63 |
| ruvnet/claude-flow | ~54 | 54 |
| Orchestra-Research/AI-Research-SKILLs | ~32 | 32 |
| hangoclong/skills-antigravity-awesome | ~28 | 31 |
| huysynf/antigravity-awesome-skills | ~28 | 34 |
| wshobson/agents | ~24 | 28 |
| ForaeFactory/antigravity-skills | ~22 | 28 |
| Jeffallan/claude-skills | ~17 | 14 |
| trailofbits/skills | ~10 | 12 |
| danielmiessler/Personal_AI_Infrastructure | ~8 | 9 |
| ComposioHQ/awesome-claude-skills | ~6 | 30 |
| Other repos (21) | ~19 | various |

Note: Theme doc counts are approximate due to table parsing limitations. Local file counts
include all downloaded SKILL.md files for this theme.

## Duplicate/Fork Repos

Three repos are forks of the same original (sickn33/antigravity-awesome-skills):
- sickn33/antigravity-awesome-skills (original, 946+ skills)
- hangoclong/skills-antigravity-awesome (fork)
- huysynf/antigravity-awesome-skills (fork)
- ForaeFactory/antigravity-skills (fork)

Many skills from these forks are duplicates. The theme doc lists them separately, inflating
the total skill count.

## Recommendations

1. **Re-evaluate theme classification**: The bulk assignment of "Supports experiment design,
   benchmarking, reproducibility, and quantitative validation" to all 601 skills is not
   meaningful. A manual or improved automated review should classify skills based on actual
   SKILL.md content.

2. **Fix "Function Explanation" truncation**: The current template truncates descriptions and
   pads with generic text. Use the full SKILL.md description field instead.

3. **Deduplicate fork repos**: Skills from fork repos (hangoclong, huysynf, ForaeFactory)
   that are identical to sickn33 originals should be deduplicated or cross-referenced.

4. **Reconcile skill count**: The header claims 648 but only 601 rows exist. The 8 missing
   local repo directories should either be added to the theme doc or explained.

5. **Remove clearly non-research skills**: Skills like `django-patterns`, `springboot-patterns`,
   `nextjs-best-practices`, `Cloud Penetration Testing`, `Broken Authentication Testing`,
   `BrightData`, `Browser`, etc. should be moved to more appropriate themes.

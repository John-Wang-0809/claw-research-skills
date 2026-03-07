# 科研技能研究相关性判定报告

> 基于 LLM 审计数据（gpt-5.2, 2026-03-04）对 1918 个技能的研究相关性评估。

## 统计概览

| 判定 | 数量 | 占比 | 说明 |
|------|------|------|------|
| 相关 (valid) | 1528 | 79% | 与科研直接相关 |
| 弱相关 (weak) | 122 | 6% | 可间接支持科研，但关联较弱 |
| 不相关 (invalid) | 4 | 0% | 与科研无关 |
| 未审计 (unknown) | 264 | 13% | 未被审计覆盖 |

---

## 弱相关技能（122 个）

以下技能被审计判定为与科研弱相关——它们可能间接支持研究工作，但核心功能并非面向科研场景。

### 01 信息检索与证据收集 (158 skills) (10 个)

| 技能名称 | 仓库 | 质量分 | 判定理由 |
|----------|------|--------|----------|
| claude-scientific-skills | sickn33/antigravity-awesome-skills | 2 | Rationale is generic and does not specify actual capabilities beyond stating it is research-related; SKILL.md content is... |
| project-guidelines-example | affaan-m/everything-claude-code | 3 | It is mainly a software project documentation/template skill; the research tie (reproducibility/maintainability) is plau... |
| make-automation | ComposioHQ/awesome-claude-skills | 3 | It is mainly automation ops monitoring and enum lookup; it can support research operations but is not inherently researc... |
| skill-share | ComposioHQ/awesome-claude-skills | 3 | Collaboration/sharing is useful, but the skill is about distribution/notification rather than research or evidence colle... |
| BeCreative | danielmiessler/Personal_AI_Infrastructure | 3 | It supports ideation for research directions, but it is not an evidence collection or retrieval tool and is only indirec... |
| action-creator | anthropics/claude-agent-sdk-demos | 4 | Primarily email/workflow automation; it can support coordination around research but is administrative rather than resea... |
| help | biocontext-ai/skill-to-mcp | 4 | It enables discovering/loading skills which may help research, but the skill content is operational documentation rather... |
| skill-creator | ComposioHQ/awesome-claude-skills | 4 | Like Skill Development, it indirectly supports standardizing workflows but is not itself a research retrieval/analysis s... |
| CORE | danielmiessler/Personal_AI_Infrastructure | 4 | A structured problem-solving method can aid research rigor, but the connection to information retrieval/evidence collect... |
| django-pro | sickn33/antigravity-awesome-skills | 4 | It’s plausible for building research-supporting web apps/APIs, but the rationale is indirect and not strongly tied to ev... |

### 02 文献综述、写作与引用 (673 skills) (74 个)

| 技能名称 | 仓库 | 质量分 | 判定理由 |
|----------|------|--------|----------|
| skill-creation-workshop | acertainKnight/project-thoth | 3 | It is primarily a meta-skill for building workflows; its research connection is indirect (useful for research tooling bu... |
| api-design | affaan-m/everything-claude-code | 3 | Helpful for research software engineering, but not specifically tied to conducting or managing research (literature revi... |
| spec-workflow-orchestrator | ahmedibrahim085/Claude-Multi-Agent-Research-System-Skill | 3 | It is useful for specifying software, but the research link is indirect (general planning/requirements) and not inherent... |
| app-builder | hangoclong/skills-antigravity-awesome | 3 | Can support research engineering, but the provided rationale is broad and not tied to research-specific needs (e.g., rep... |
| blockrun | hangoclong/skills-antigravity-awesome | 3 | May help research when real-time data or external model outputs are needed, but the rationale is capability-based and no... |
| codex-review | huysynf/antigravity-awesome-skills | 3 | Code review/changelog supports reproducible research software practices, but the link is research-adjacent rather than r... |
| context7-auto-research | huysynf/antigravity-awesome-skills | 3 | Useful for implementing computational methods correctly, but it is primarily developer documentation retrieval rather th... |
| notion-meeting-intelligence | makenotion/notion-cookbook | 3 | Primarily meeting preparation and coordination; research connection is indirect (useful for research teams but not a res... |
| skill-template | muratcankoylan/Agent-Skills-for-Context-Engineering | 3 | Connection to research is indirect; it supports organization/reuse of workflows but is primarily documentation scaffoldi... |
| agent-app-store | ruvnet/claude-flow | 3 | Marketplace management is generally software-ecosystem related; the research connection (reusable research apps/template... |
| agent-challenges | ruvnet/claude-flow | 3 | Primarily gamified learning/competitive programming; research connection is indirect and not tied to conducting or commu... |
| ddd-architect | u9401066/pubmed-search-mcp | 3 | Helps long-term maintainability, but the link to research outcomes is indirect and broadly applicable to any software pr... |
| roadmap-updater | u9401066/pubmed-search-mcp | 3 | Roadmap maintenance is project management; it can support research software planning, but the connection to research out... |
| configure-ecc | affaan-m/everything-claude-code | 4 | It can help reproducibility via standardized setup, but the connection to research is indirect and the provided evidence... |
| capa-officer | alirezarezvani/claude-skills | 4 | Relevance is plausible mainly for regulated R&D/clinical/medical-device research contexts; for general research it is ni... |
| cto-advisor | alirezarezvani/claude-skills | 4 | The stated connection to research is indirect (organizational/strategy guidance rather than research methods), though AD... |
| quality-manager-qmr | alirezarezvani/claude-skills | 4 | Connection to research is indirect (quality governance/management review); it can support regulated development environm... |
| senior-architect | alirezarezvani/claude-skills | 4 | Research relevance is indirect: it can support building/assessing research software platforms, but the skill is primaril... |
| senior-backend | alirezarezvani/claude-skills | 4 | Helpful for engineering data-collection/processing systems used in research, but the link to research is infrastructural... |
| senior-frontend | alirezarezvani/claude-skills | 4 | Research connection is indirect via building dashboards/interfaces for data visualization or participant interaction; ra... |
| Agent Development | anthropics/claude-code | 4 | Connection to research is indirect (automation potential) and not tied to a concrete research workflow or research-speci... |
| Command Development | anthropics/claude-code | 4 | The rationale is generic (automation/standardization) without a specific research-linked command use case; still tangent... |
| skill-creator | anthropics/skills | 4 | Can indirectly help research via building custom automation, but the connection is generic and not inherently research-f... |
| developer-growth-analysis | ComposioHQ/awesome-claude-skills | 4 | Primarily a developer self-improvement/workflow tool; research connection is indirect (helps research software engineeri... |
| frontend-dev-guidelines | diet103/claude-code-infrastructure-showcase | 4 | Connection to research is indirect (building UIs to present info) and not tied to research methods; rationale is plausib... |
| coding-tutor | EveryInc/every-marketplace | 4 | Rationale is indirect (learning programming to implement tools). It’s supportive of research engineering but not a resea... |
| create-agent-skills | EveryInc/every-marketplace | 4 | The rationale correctly notes it’s not a direct research workflow; any research link is incidental (tooling enablement). |
| every-marketplace | EveryInc/every-marketplace | 4 | Research link is indirect (QA for tools used in research workflows). The rationale states this appropriately but it rema... |
| every-style-editor | EveryInc/every-marketplace | 4 | Editing for house style is adjacent to research writing but not research-specific; rationale admits it’s not inherently ... |
| heal-skill | EveryInc/every-marketplace | 4 | It’s a maintenance utility; any research relevance is indirect (keeping tooling docs correct). The provided rationale re... |
| github-workflow-automation | ForaeFactory/antigravity-skills | 4 | Useful for research software maintenance, but the rationale is indirect and broadly applies to any software project rath... |
| nestjs-expert | ForaeFactory/antigravity-skills | 4 | Mostly generic backend engineering; relevance to research depends on building research software, which is plausible but ... |
| parallel-agents | ForaeFactory/antigravity-skills | 4 | Multi-perspective analysis can help research work, but the justification is generic and primarily oriented to software/c... |
| ui-ux-pro-max | ForaeFactory/antigravity-skills | 4 | The connection to research is mostly indirect (design guidance and accessibility criteria), and the rationale is more ab... |
| frontend-dev-guidelines | hangoclong/skills-antigravity-awesome | 4 | Research connection is plausible (dashboards/UIs) but remains generic and not tied to a research-specific workflow beyon... |
| nestjs-expert | hangoclong/skills-antigravity-awesome | 4 | Backend engineering may appear in research projects, but the rationale is broad and not distinctly research-specific. |
| skill-creator | HKUDS/DeepCode | 4 | The connection is indirect: it helps build agent skills that could support research workflows, but it is meta-infrastruc... |
| app-builder | huysynf/antigravity-awesome-skills | 4 | Building apps can support research tooling, but the rationale is general-purpose software engineering and not specifical... |
| blockrun | huysynf/antigravity-awesome-skills | 4 | Real-time social data and image generation can be research-relevant in some cases, but the stated rationale is situation... |
| frontend-dev-guidelines | huysynf/antigravity-awesome-skills | 4 | Helpful for building research-adjacent UIs, but largely generic frontend engineering guidance rather than research-focus... |
| nestjs-expert | huysynf/antigravity-awesome-skills | 4 | Useful for research-adjacent infrastructure, but the rationale is fairly general and not tightly tied to research method... |
| parallel-agents | huysynf/antigravity-awesome-skills | 4 | Multi-agent coordination can help complex analysis, but the rationale is broad and not explicitly research-specific beyo... |
| receiving-code-review | huysynf/antigravity-awesome-skills | 4 | Applies to research software engineering quality, but the linkage is indirect and not unique to research vs general soft... |
| csharp-developer | Jeffallan/claude-skills | 4 | Plausible for building research-adjacent apps/services, but the rationale is fairly generic and not tied to concrete res... |
| treatment-plans | K-Dense-AI/claude-scientific-skills | 4 | The skill is primarily clinical documentation; while it can support clinical research/QI protocol standardization and au... |
| treatment-plans | K-Dense-AI/claude-scientific-writer | 4 | Rationale leans toward clinical protocol standardization; while it can support clinical research documentation, the skil... |
| frontend-dev-guidelines | mrgoonie/claudekit-skills | 4 | Connection depends on the research project requiring a web UI; rationale is plausible but more engineering-support than ... |
| digital-brain | muratcankoylan/Agent-Skills-for-Context-Engineering | 4 | There is a knowledge/research-organization module, but the skill is primarily positioned around personal brand/network/o... |
| create-pr | n8n-io/n8n | 4 | It can help collaborative research software hygiene, but the rationale is indirect and not specific to research beyond g... |
| agentmd-creator | Przemocny/generic-skills | 4 | It can be used to configure a research assistant, but the skill itself is generic agent-config scaffolding rather than r... |
| general-skill-refiner | Przemocny/generic-skills | 4 | Primarily software/skill QA; research relevance is indirect (maintaining tooling used in research workflows) rather than... |
| general-skill-upgrader | Przemocny/generic-skills | 4 | Indirectly relevant by improving research-related automation skills, but not a research workflow skill itself. |
| elegant-design | rand/cc-polymath | 4 | Applies to research-adjacent software UX, but the rationale is indirect (interface design helps tools used in research r... |
| agent-automation-smart-agent | ruvnet/claude-flow | 4 | Coordination/automation can help research workflows, but the rationale is generic and not tied to specific research task... |
| agent-coordination | ruvnet/claude-flow | 4 | Orchestration can help research tasks, but the provided rationale remains high-level and focuses on parallelization mech... |
| agent-migration-plan | ruvnet/claude-flow | 4 | Migration planning is generally software-process related; the research connection (reproducibility/continuity of researc... |
| agent-project-board-sync | ruvnet/claude-flow | 4 | Project-board synchronization can help manage research engineering, but the rationale leans toward general project manag... |
| agent-queen-coordinator | ruvnet/claude-flow | 4 | High-level swarm governance is generally applicable coordination; the research linkage is generic and not specific to re... |
| backend-development-feature-development | sickn33/antigravity-awesome-skills | 4 | Connection to research is plausible but somewhat generic (software engineering workflow). It doesn't clearly target rese... |
| design-md | sickn33/antigravity-awesome-skills | 4 | The rationale is plausible for UI/documentation analysis, but the connection to research workflows is niche and less dir... |
| frontend-dev-guidelines | sickn33/antigravity-awesome-skills | 4 | Can support research software UI quality, but the rationale is more general software engineering; connection to research... |
| on-call-handoff-patterns | sickn33/antigravity-awesome-skills | 4 | Connection to research is indirect: useful for operations practice and could support software engineering research, but ... |
| prompt-library | sickn33/antigravity-awesome-skills | 4 | Helpful for standardizing prompting in research writing/analysis, but the provided rationale is general and not tied to ... |
| server-management | sickn33/antigravity-awesome-skills | 4 | Relevant mainly for research ops/infrastructure; rationale is plausible but indirect and not specific to research method... |
| stitch-ui-design | sickn33/antigravity-awesome-skills | 4 | HCI/user-testing relevance is plausible, but rationale is somewhat speculative and not clearly tied to typical literatur... |
| git-cleanup | trailofbits/skills | 4 | Connection to research is plausible (managing experimental branches), but is more about general developer hygiene than r... |
| parent-segment-analysis | treasure-data/td-skills | 4 | Connection to research is plausible (behavioral/marketing analysis), but it is framed more as business analytics; the ra... |
| changelog-updater | u9401066/pubmed-search-mcp | 4 | Changelog maintenance supports research software engineering practices, but the rationale is indirect (process documenta... |
| code-refactor | u9401066/pubmed-search-mcp | 4 | Refactoring is useful for maintainable research codebases, but the justification is general software engineering rather ... |
| git-doc-updater | u9401066/pubmed-search-mcp | 4 | Documentation syncing supports collaboration and reproducibility, but the rationale is still largely process-focused and... |
| git-precommit | u9401066/pubmed-search-mcp | 4 | Pre-commit orchestration improves engineering hygiene; research connection is indirect unless tied to reproducibility or... |
| readme-i18n | u9401066/pubmed-search-mcp | 4 | Bilingual documentation can aid collaboration and accessibility, but the rationale is more about software documentation ... |
| baoyu-gemini-web | zsyggg/paper-craft-skills | 4 | It can support research content generation/vision-conditioned tasks, but the rationale is somewhat generic and not tight... |
| slo-implementation | sickn33/antigravity-awesome-skills | 5 | Applicable when research depends on operational services, but the rationale is more DevOps/SRE than research-specific an... |

### 03 实验、基准测试与可复现性验证 (589 skills) (31 个)

| 技能名称 | 仓库 | 质量分 | 判定理由 |
|----------|------|--------|----------|
| PAI | danielmiessler/Personal_AI_Infrastructure | 3 | While a structured problem-solving/verification system can aid research workflows, the rationale is broad and not tied t... |
| route-tester | diet103/claude-code-infrastructure-showcase | 3 | Useful for engineering validation, but the connection to research is indirect unless the research specifically involves ... |
| Claude-Metacognitive-Skills | Dr-AneeshJoseph/Claude-Metacognitive-Skills | 3 | It can be relevant for qualitative inquiry into AI phenomenology, but claims about evaluating authenticity/substrate in ... |
| nextjs-best-practices | hangoclong/skills-antigravity-awesome | 3 | Rationale is generic (web app guidance) and doesn’t clearly connect to research experimentation, benchmarking, or valida... |
| nodejs-best-practices | hangoclong/skills-antigravity-awesome | 3 | Primarily general backend engineering guidance; research link is plausible (building research tooling/services) but not ... |
| production-code-audit | hangoclong/skills-antigravity-awesome | 3 | Mostly about enterprise hardening; research tie-in is indirect unless framed as improving reliability of research softwa... |
| nextjs-best-practices | huysynf/antigravity-awesome-skills | 3 | Connection to research is plausible (building research web apps), but the rationale is fairly generic and not tied to re... |
| software-architecture | huysynf/antigravity-awesome-skills | 3 | Helpful for maintainable research software, but the rationale is general software engineering rather than research-speci... |
| nextjs-developer | Jeffallan/claude-skills | 3 | Web app development can support dissemination/surveys, but the connection is indirect and not specific to research metho... |
| rust-engineer | Jeffallan/claude-skills | 3 | High-performance tooling can help research, but the rationale is broad and not tightly linked to specific research workf... |
| V3 Swarm Coordination | ruvnet/claude-flow | 3 | Primarily an implementation/project coordination plan; research value exists for studying coordination, but the skill is... |
| elixir-pro | sickn33/antigravity-awesome-skills | 3 | Connection to research is indirect (general backend/service engineering); rationale is plausible but not strongly tied t... |
| fp-ts-react | sickn33/antigravity-awesome-skills | 3 | Connection to research is plausible (UIs for research workflows) but relatively indirect and not strongly tied to reprod... |
| java-pro | sickn33/antigravity-awesome-skills | 3 | The rationale is plausible (high-performance pipelines), but it is broad and not strongly tied to the provided skill’s m... |
| django-patterns | affaan-m/everything-claude-code | 4 | Connection to research is plausible (building research data platforms), but the rationale is somewhat general and not ti... |
| springboot-patterns | affaan-m/everything-claude-code | 4 | Useful for building research infrastructure, but the stated research tie is indirect and broadly applicable to general b... |
| Hook Development | anthropics/claude-code | 4 | Automation/policy enforcement can support reproducibility/validation in tool-driven workflows, but the rationale is more... |
| nodejs-best-practices | huysynf/antigravity-awesome-skills | 4 | It can support research software engineering quality, but the rationale is largely general software best-practice value ... |
| production-code-audit | huysynf/antigravity-awesome-skills | 4 | Improves robustness of research software, but the connection to research methodology is indirect; it is primarily an ent... |
| skill-developer | huysynf/antigravity-awesome-skills | 4 | Custom skills can standardize team practices (including research workflows), but the provided rationale is speculative a... |
| web-frameworks | mrgoonie/claudekit-skills | 4 | Mostly general web engineering; research relevance is plausible for tooling/UI around research but not inherently tied t... |
| error-debugging-error-analysis | sickn33/antigravity-awesome-skills | 4 | Rationale is operationally plausible but indirect; it’s mainly SRE/production reliability rather than research methodolo... |
| error-detective | sickn33/antigravity-awesome-skills | 4 | Useful for operational troubleshooting of research-related services, but the research linkage is indirect and not tied t... |
| network-engineer | sickn33/antigravity-awesome-skills | 4 | Rationale ties to research infrastructure reliability and measurability, but it is more general IT/ops support and not t... |
| nextjs-best-practices | sickn33/antigravity-awesome-skills | 4 | Building web tools can support research workflows, but the connection is generic and not specific to research evaluation... |
| nodejs-best-practices | sickn33/antigravity-awesome-skills | 4 | Applies to building services that might be used in research, but the rationale is largely general software engineering r... |
| bazel-build-optimization | wshobson/agents | 4 | Useful for engineering productivity and reproducible builds, but the provided rationale is indirectly research-related r... |
| e2e-testing-patterns | wshobson/agents | 4 | E2E testing can support reliability of research systems, but the connection is secondary unless the research context exp... |
| event-store-design | wshobson/agents | 4 | Immutable event logs can support audit trails for experiments, but the skill is primarily general system design and not ... |
| modern-javascript-patterns | wshobson/agents | 4 | Can help build research tooling, but the rationale is largely general software engineering and not a research method or ... |
| python-design-patterns | wshobson/agents | 4 | Better architecture can aid maintainability of research code, but the connection is indirect and broadly applicable to a... |

### 04 数据分析与证据解读 (178 skills) (4 个)

| 技能名称 | 仓库 | 质量分 | 判定理由 |
|----------|------|--------|----------|
| angular-migration | sickn33/antigravity-awesome-skills | 3 | Modernizing research infrastructure can matter, but the connection is indirect and focused on web framework migration ra... |
| graphql | ForaeFactory/antigravity-skills | 4 | It can support research indirectly when research depends on GraphQL data services, but the rationale is more infrastruct... |
| Linux Production Shell Scripts | ForaeFactory/antigravity-skills | 4 | Useful for maintaining research compute environments, but the connection is somewhat indirect and could apply to many no... |
| angular-migration | wshobson/agents | 4 | Relevance is indirect (maintaining dashboards/tools); rationale is plausible but not inherently research-specific. |

### 05 科研运营与工作流支持 (56 skills) (3 个)

| 技能名称 | 仓库 | 质量分 | 判定理由 |
|----------|------|--------|----------|
| agent-base-template-generator | ruvnet/claude-flow | 3 | Rationale is plausible (accelerates research software prototyping/quality), but it is generic and not tied to research-s... |
| agent-refinement | ruvnet/claude-flow | 4 | Improving code quality benefits research software, but the rationale remains general software-engineering value rather t... |
| agent-tdd-london-swarm | ruvnet/claude-flow | 4 | Can support reliable research software, but the connection is generic; SKILL.md is focused on testing methodology rather... |

---

## 不相关技能（4 个）

| 技能名称 | 仓库 | 质量分 | 判定理由 |
|----------|------|--------|----------|
| dhh-rails-style | EveryInc/every-marketplace | 4 | Rationale explicitly says it’s engineering style guidance without research workflows; no substantive research connection... |
| app-builder | ForaeFactory/antigravity-skills | 4 | Rationale correctly notes the skill is general application-building with no research-specific workflows; the described u... |
| docker-expert | ForaeFactory/antigravity-skills | 4 | Rationale states it lacks research-specific workflows; the connection to research is not established beyond general engi... |
| frontend-dev-guidelines | ForaeFactory/antigravity-skills | 4 | Rationale correctly notes it is general frontend guidance without a research workflow tie-in. |

---

## 未审计技能（264 个）

以下技能未被 audit_results.json 覆盖，无法自动判定研究相关性，需人工审查。

| 技能名称 | 仓库 | 主题 | 功能描述 |
|----------|------|------|----------|
| 01 |  |  | 信息检索与证据收集 |
| 02 |  |  | 文献综述、写作与引用 |
| 03 |  |  | 实验、基准测试与可复现性验证 |
| 04 |  |  | 数据分析与证据解读 |
| 05 |  |  | 科研运营与工作流支持 |
| 06 |  |  | 其他科学技能 |
| `deep-research` | liangdabiao/simple_claude_deep_research_agent | 06 其他科学技能 (258 skill | "Conduct deep research on any topic using parallel subagents and web tools (web_search, web_fetch,..... |
| `research-subagent` | liangdabiao/simple_claude_deep_research_agent | 06 其他科学技能 (258 skill | "Internal skill - Research subagent that executes focused research tasks using web tools. |
| `citations` | liangdabiao/simple_claude_deep_research_agent | 06 其他科学技能 (258 skill | "Add citations to research reports. |
| `daily-paper-generator` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | Automates the workflow of discovering, reviewing, and summarizing recent arXiv papers related to... |
| `research-ideation` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | Supports the full research project initiation workflow, from generating and refining ideas through..... |
| `citation-verification` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | This skill provides reference guidance for citation verification in academic writing. |
| `doc-coauthoring` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | Guides users through a structured workflow for collaboratively co-authoring documentation such as... |
| `latex-conference-template-organizer` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | Organize messy conference LaTeX template .zip files into clean Overleaf-ready structure. |
| `ml-paper-writing` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | This skill provides expert guidance for writing publication-ready ML and AI papers targeting venues.... |
| `paper-self-review` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | This skill should be used when the user asks to "review paper quality", "check paper completeness",.... |
| `review-response` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | Systematic review response workflow from comment analysis to professional rebuttal writing. |
| `writing-anti-ai` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | Rewrites English and Chinese text to remove common AI-generated writing patterns and sound more... |
| `kaggle-learner` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | This skill should be used when the user asks to "learn from Kaggle", "study Kaggle solutions",... |
| `verification-loop` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | This skill should be used when the user asks to "verify code", "run verification", "check quality",.... |
| `results-analysis` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | This skill should be used when the user asks to "analyze experimental results", "generate results... |
| `architecture-design` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | Use ONLY when creating NEW registrable components in ML projects that require Factory/Registry... |
| `bug-detective` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | This skill should be used when the user asks to "debug this", "fix this error", "investigate this... |
| `code-review-excellence` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | Master effective code review practices to provide constructive feedback, catch bugs early, and... |
| `git-workflow` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | This skill should be used when the user asks to "create git commit", "manage branches", "follow git.... |
| `post-acceptance` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | This skill should be used when the user asks to "prepare conference presentation", "create... |
| `uv-package-manager` | Galaxy-Dawn/claude-scholar | 06 其他科学技能 (258 skill | Master the uv package manager for fast Python dependency management, virtual environments, and... |
| `distributed-llm-pretraining-torchtitan` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Provides PyTorch-native distributed LLM pretraining using torchtitan with 4D parallelism (FSDP2,... |
| `langchain` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Framework for building LLM-powered applications with agents, chains, and RAG. |
| `llamaindex` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Data framework for building LLM applications with RAG. |
| `chroma` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Open-source embedding database for AI applications. |
| `faiss` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Facebook's library for efficient similarity search and clustering of dense vectors. |
| `pinecone` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Managed vector database for production AI applications. |
| `qdrant-vector-search` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | High-performance vector similarity search engine for RAG and semantic search. |
| `sentence-transformers` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Framework for state-of-the-art sentence, text, and image embeddings. |
| `ml-paper-writing` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM. |
| `implementing-llms-litgpt` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Implements and trains LLMs using Lightning AI's LitGPT with 20+ pretrained architectures (Llama,... |
| `mamba-architecture` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | State-space model architecture for sequence modeling with O(n) complexity (vs Transformers’ O(n²)),.... |
| `nanogpt` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Educational GPT implementation in ~300 lines. |
| `rwkv-architecture` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | RNN+Transformer hybrid architecture with O(n) inference, linear-time processing, constant memory,... |
| `huggingface-tokenizers` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Fast Rust-core tokenizers with Python/Node bindings that support BPE, WordPiece, and Unigram, with..... |
| `sentencepiece` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Language-independent tokenizer that treats text as raw Unicode and supports BPE and Unigram. |
| `axolotl` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA,... |
| `llama-factory` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Generic documentation-based assistance for working with LLaMA-Factory. |
| `peft-fine-tuning` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. |
| `unsloth` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory,... |
| `nemo-curator` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | GPU-accelerated data curation for LLM training. |
| `ray-data` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Scalable data processing for ML workloads. |
| `grpo-rl-training` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training |
| `miles-rl-training` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Provides guidance for enterprise-grade RL training using miles, a production-ready fork of slime. |
| `openrlhf-training` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | OpenRLHF is a high-performance RLHF training framework that uses Ray for distributed orchestration..... |
| `simpo-training` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Simple Preference Optimization for LLM alignment. |
| `slime-rl-training` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Provides guidance for LLM post-training with RL using slime, a Megatron+SGLang framework. |
| `torchforge-rl-training` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Provides guidance for PyTorch-native agentic RL using torchforge, Meta's library separating infra... |
| `fine-tuning-with-trl` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for... |
| `verl-rl-training` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Provides guidance for training LLMs with reinforcement learning using verl (Volcano Engine RL). |
| `constitutional-ai` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Anthropic's method for training harmless AI through self-improvement. |
| `llamaguard` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Meta's 7-8B specialized moderation model for LLM input/output filtering. |
| `nemo-guardrails` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | NVIDIA runtime safety framework for LLM applications that provides jailbreak detection,... |
| `prompt-guard` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Meta 86M-parameter classifier for detecting prompt injection and jailbreak attempts to filter user..... |
| `huggingface-accelerate` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Provides a minimal-change API for adding distributed training support to PyTorch scripts, with an... |
| `deepspeed` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Documentation-based assistance for DeepSpeed. |
| `training-llms-megatron` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Train large language models (2B–462B parameters) using NVIDIA Megatron-Core with advanced... |
| `pytorch-fsdp2` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Adds PyTorch FSDP2 (fully_shard) to training scripts with correct init, sharding, mixed... |
| `pytorch-lightning` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | High-level PyTorch framework with Trainer class, automatic distributed training... |
| `ray-train` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Orchestrates distributed machine learning training across clusters for PyTorch, TensorFlow, and... |
| `awq-quantization` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | AWQ is an activation-aware weight quantization method that compresses LLMs to 4-bit weights while... |
| `quantizing-models-bitsandbytes` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Quantizes LLMs to 8-bit or 4-bit for 50-75% memory reduction with minimal accuracy loss. |
| `optimizing-attention-flash` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | This skill focuses on optimizing transformer attention using Flash Attention to achieve roughly... |
| `gptq` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | GPTQ is a post-training quantization method that compresses large language models to 4-bit weights..... |
| `hqq-quantization` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Half-Quadratic Quantization for LLMs without calibration data. |
| `evaluating-code-models` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Evaluates code generation models across more than 15 benchmarks, including HumanEval, MBPP, and... |
| `evaluating-llms-harness` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Evaluates LLMs across 60+ academic benchmarks (including MMLU, HumanEval, GSM8K, TruthfulQA, and... |
| `nemo-evaluator-sdk` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | NeMo Evaluator SDK is an enterprise-grade platform for evaluating large language models across over.... |
| `sglang` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Fast structured generation and serving for LLMs with RadixAttention prefix caching. |
| `serving-llms-vllm` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. |
| `mlflow` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Track ML experiments, manage model registry with versioning, deploy models to production, and... |
| `weights-and-biases` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Track ML experiments with automatic logging, visualize training in real-time, optimize... |
| `dspy` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Build complex AI systems with declarative programming, optimize prompts automatically, create... |
| `guidance` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce... |
| `langsmith-observability` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | LLM observability platform for tracing, evaluation, and monitoring. |
| `phoenix-observability` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Open-source AI observability platform for LLM tracing, evaluation, and monitoring. |
| `audiocraft-audio-generation` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | PyTorch library for audio generation including text-to-music (MusicGen) and text-to-sound... |
| `blip-2-vision-language` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Vision-language pre-training framework bridging frozen image encoders and LLMs. |
| `clip` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | CLIP is OpenAI’s vision-language model that connects images and text to enable zero-shot image... |
| `llava` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | LLaVA (Large Language and Vision Assistant) is a vision-language model for visual instruction... |
| `segment-anything-model` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Foundation model for image segmentation with zero-shot transfer. |
| `stable-diffusion-image-generation` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. |
| `knowledge-distillation` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Compress large language models using knowledge distillation from teacher to student models. |
| `long-context` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Extend transformer context windows using RoPE, YaRN, ALiBi, and position interpolation techniques. |
| `model-merging` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Merge multiple fine-tuned models using mergekit to combine capabilities without retraining. |
| `model-pruning` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Reduce LLM size and accelerate inference using pruning techniques such as Wanda and SparseGPT. |
| `moe-training` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | This skill covers training Mixture of Experts (MoE) models using DeepSpeed or HuggingFace tooling. |
| `speculative-decoding` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | This skill accelerates LLM inference using speculative decoding techniques, including draft-model... |
| `nnsight-remote-interpretability` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Provides guidance for interpreting and manipulating neural network internals using nnsight with... |
| `pyvene-interventions` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Provides guidance for performing causal interventions on PyTorch models using pyvene's declarative..... |
| `sparse-autoencoder-training` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Provides guidance for training and analyzing Sparse Autoencoders (SAEs) using SAELens to decompose..... |
| `transformer-lens-interpretability` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Provides guidance for mechanistic interpretability research using TransformerLens to inspect and... |
| `tensorboard` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Visualize training metrics, debug models with histograms, compare experiments, visualize model... |
| `whisper` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | OpenAI's general-purpose speech recognition model. |
| `lambda-labs-gpu-cloud` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Reserved and on-demand GPU cloud instances for ML training and inference. |
| `modal-serverless-gpu` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Serverless GPU cloud platform for running ML workloads. |
| `skypilot-multi-cloud-orchestration` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Multi-cloud orchestration for ML workloads with automatic cost optimization. |
| `gguf-quantization` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | GGUF format and llama.cpp quantization for efficient CPU/GPU inference. |
| `llama-cpp` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Runs LLM inference on CPU, Apple Silicon, and consumer GPUs without NVIDIA hardware. |
| `tensorrt-llm` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Optimizes LLM inference with NVIDIA TensorRT for maximum throughput and lowest latency. |
| `autogpt-agents` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Autonomous AI agent platform for building and deploying continuous agents. |
| `crewai-multi-agent` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Multi-agent orchestration framework for autonomous AI collaboration. |
| `instructor` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Extract structured data from LLM responses with Pydantic validation, retry failed extractions... |
| `outlines` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe... |
| `brainstorming-research-ideas` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Guides researchers through structured ideation frameworks to discover high-impact research... |
| `creative-thinking-for-research` | Orchestra-Research/AI-Research-SKILLs | 06 其他科学技能 (258 skill | Applies cognitive science frameworks for creative thinking to CS and AI research ideation. |
| `alphafold-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Access AlphaFold 200M+ AI-predicted protein structures. |
| `biopython` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive molecular biology toolkit. |
| `biorxiv-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Efficient database search tool for bioRxiv preprint server. |
| `bioservices` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | BioServices is a Python package that provides programmatic access to over 40 bioinformatics web... |
| `brenda-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Access BRENDA enzyme database via SOAP API. |
| `cellxgene-census` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Enables programmatic querying of the CELLxGENE Census, including expression data across tissues,... |
| `chembl-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Query ChEMBL bioactive molecules and drug discovery data. |
| `clinicaltrials-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Query ClinicalTrials.gov via API v2. |
| `clinpgx-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Access ClinPGx pharmacogenomics data (successor to PharmGKB). |
| `clinvar-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Query NCBI ClinVar for variant clinical significance. |
| `cosmic-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Access COSMIC cancer mutation database. |
| `datacommons-client` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Provides access to the Data Commons Python API v2 for querying public statistical observations,... |
| `drugbank-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Enables programmatic access to DrugBank data for comprehensive drug and drug-target information,... |
| `ena-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | API and FTP client for the European Nucleotide Archive enabling retrieval of DNA/RNA sequences, raw.... |
| `ensembl-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | REST API client for Ensembl supporting gene lookups, sequence retrieval, variant analysis,... |
| `fda-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | openFDA API client for querying drug information, medical device records, adverse event reports,... |
| `fred-economic-data` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | API client for the Federal Reserve Economic Data (FRED) database providing access to 800,000+... |
| `gene-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | E-utilities and Datasets API client for NCBI Gene supporting symbol/ID-based searches and batch... |
| `geo-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Provides workflows for searching and downloading gene expression and genomics datasets from NCBI... |
| `gget` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Provides fast command-line and Python-based queries to over 20 bioinformatics databases through a... |
| `gwas-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | API client for the NHGRI-EBI GWAS Catalog enabling searches for GWAS results by rs ID,... |
| `hmdb-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Access to the Human Metabolome Database (HMDB) covering 220,000+ metabolites with retrieval of... |
| `imaging-data-commons` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | This skill uses the idc-index Python package to query and download public cancer imaging data from..... |
| `kegg-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Direct HTTP/REST client for KEGG supporting pathway analysis, gene-pathway mapping, metabolic... |
| `markitdown` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | File format converter transforming office documents, PDFs, HTML, and spreadsheets into Markdown... |
| `metabolomics-workbench-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | REST API client for the NIH Metabolomics Workbench (4,200+ studies) supporting metabolite queries,..... |
| `openalex-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | API client for the OpenAlex scholarly literature database (240M+ works) supporting paper searches... |
| `opentargets-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | API client for the Open Targets Platform providing target-disease association scores, drug target... |
| `pdb-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Search and download client for the RCSB Protein Data Bank supporting text, sequence, and... |
| `pdf` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | PDF manipulation toolkit for programmatic document processing and analysis. |
| `perplexity-search` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Perplexity Search performs AI-powered web searches using Perplexity models through LiteLLM and... |
| `pubchem-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Queries PubChem using the PUG-REST API and PubChemPy to access chemical structure and bioactivity... |
| `pubmed-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Direct HTTP/REST and E-utilities API client for PubMed supporting advanced Boolean/MeSH queries and.... |
| `reactome-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | REST API client for the Reactome pathway database supporting pathway analysis,... |
| `research-lookup` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Automated search tool using Perplexity's Sonar Pro Search or Sonar Reasoning Pro via OpenRouter to..... |
| `string-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | API client for the STRING database covering 59M proteins and 20B interactions across 5,000+ species.... |
| `uniprot-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Direct REST API and ID mapping client for UniProt enabling protein searches, FASTA sequence... |
| `uspto-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Multi-API client for USPTO data including PatentSearch for patent discovery, PEDS for prosecution... |
| `zinc-database` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Access to the ZINC database of 230M+ commercially available compounds supporting searches by ZINC... |
| `citation-management` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive citation management for academic research. |
| `clinical-reports` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Write comprehensive clinical reports including case reports (CARE guidelines), diagnostic reports... |
| `latex-posters` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Creates professional research posters in LaTeX using beamerposter, tikzposter, or baposter. |
| `literature-review` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Conduct comprehensive, systematic literature reviews using multiple academic databases (PubMed,... |
| `markdown-mermaid-writing` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive markdown and Mermaid diagram writing framework covering 24 diagram type references... |
| `paper-2-web` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Tool for converting academic papers from LaTeX or PDF sources into promotional and presentation... |
| `peer-review` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Provides a structured, checklist-based workflow for writing formal peer reviews of manuscripts or... |
| `pptx-posters` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Web-based research poster design tool using HTML/CSS that exports to PDF or PPTX format with modern.... |
| `scholar-evaluation` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Structured scholarly work assessment using the ScholarEval framework with quantitative scoring... |
| `scientific-writing` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Core scientific writing framework using a two-stage process (section outlines with research-lookup,.... |
| `venue-templates` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive collection of LaTeX templates, formatting requirements, and submission guidelines for.... |
| `adaptyv` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Adaptyv is a cloud laboratory platform for automated protein testing and validation, where users... |
| `aeon` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | This skill should be used for time series machine learning tasks including classification,... |
| `cirq` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Google quantum computing framework. |
| `cobrapy` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Constraint-based metabolic modeling (COBRA). |
| `deepchem` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Molecular ML library with diverse featurizers (fingerprints, graph representations, descriptors)... |
| `diffdock` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Diffusion-based molecular docking. |
| `esm` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | ESM is a comprehensive toolkit for protein language models that features ESM3 for generative... |
| `fluidsim` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Python-based CFD simulation framework for Navier-Stokes equations (2D/3D), shallow water equations,.... |
| `geniml` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Python package for machine learning on genomic interval data (BED files). |
| `hypogenic` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Automated system for LLM-driven hypothesis generation and testing on tabular empirical datasets,... |
| `hypothesis-generation` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Structured hypothesis formulation framework converting experimental observations into testable... |
| `opentrons-integration` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Official Opentrons Protocol API v2 client for writing production protocols for OT-2 and Flex... |
| `pathml` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | PathML is a comprehensive Python toolkit designed for computational pathology workflows and the... |
| `pennylane` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | PennyLane is a hardware-agnostic quantum ML framework that provides automatic differentiation for... |
| `pufferlib` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | High-performance reinforcement learning framework for fast parallel training and vectorized... |
| `pyhealth` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive healthcare AI toolkit for developing, testing, and deploying ML models on clinical... |
| `pylabrobot` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Vendor-agnostic lab automation framework for unified programming across Hamilton, Tecan, Opentrons,.... |
| `pymc-bayesian-modeling` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Probabilistic programming library for building Bayesian hierarchical models with MCMC inference... |
| `pymoo` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Multi-objective optimization framework implementing NSGA-II, NSGA-III, MOEA/D, and other... |
| `pytdc` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Therapeutics Data Commons library providing standardized AI-ready drug discovery datasets (ADME,... |
| `pytorch-lightning` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Deep learning training framework organizing PyTorch code into LightningModules with Trainers for... |
| `qiskit` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | IBM's quantum computing framework for IBM Quantum hardware with Qiskit Runtime for production... |
| `qutip` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Quantum physics simulation library for open quantum systems studying master equations, Lindblad... |
| `rowan` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Cloud-based quantum chemistry platform with Python API for pKa prediction, geometry optimization,... |
| `scikit-learn` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive Python ML library covering supervised/unsupervised learning, model evaluation,... |
| `scikit-survival` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive survival analysis toolkit for fitting Cox models, Random Survival Forests, Gradient... |
| `scvi-tools` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Deep generative model framework for single-cell omics supporting probabilistic batch correction... |
| `simpy` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Process-based discrete-event simulation framework for modeling systems with processes, queues,... |
| `stable-baselines3` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Stable Baselines3 provides production-ready PyTorch implementations of standard reinforcement... |
| `torch-geometric` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | PyTorch-based geometric deep learning library implementing GCN, GAT, GraphSAGE, and other GNN... |
| `torchdrug` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | TorchDrug is a PyTorch-native machine learning toolbox tailored for applying graph neural networks..... |
| `transformers` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | The Transformers library provides access to thousands of pre-trained models for natural language... |
| `anndata` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Data structure for annotated matrices in single-cell analysis. |
| `arboreto` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Infer gene regulatory networks (GRNs) from gene expression data using scalable algorithms... |
| `astropy` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive Python library for astronomy and astrophysics. |
| `clinical-decision-support` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | This skill generates professional clinical decision support documents for pharmaceutical and... |
| `dask` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Distributed computing for larger-than-RAM pandas/NumPy workflows. |
| `datamol` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Pythonic wrapper around RDKit with simplified interface and sensible defaults. |
| `deeptools` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | NGS analysis toolkit. |
| `xlsx` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | The xlsx skill is a spreadsheet toolkit for creating, editing, and analyzing data in Excel and CSV..... |
| `etetoolkit` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Phylogenetic tree toolkit (ETE) for tree manipulation in Newick/NHX formats, evolutionary event... |
| `exploratory-data-analysis` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Automated EDA tool for scientific data files across 200+ formats (chemistry, bioinformatics,... |
| `flowio` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | FCS file reading and writing library for flow cytometry data (versions 2.0-3.1). |
| `geopandas` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | GeoPandas extends pandas for working with geospatial vector data such as shapefiles, GeoJSON, and... |
| `gtars` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | High-performance Rust-based toolkit with Python bindings for genomic interval analysis covering BED.... |
| `histolab` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Lightweight whole-slide image (WSI) tile extraction and preprocessing tool with tissue detection,... |
| `matchms` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Spectral similarity and compound identification library for metabolomics using cosine and modified..... |
| `matlab` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | This skill covers MATLAB and GNU Octave numerical computing for matrix operations, data analysis,... |
| `matplotlib` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Matplotlib is a low-level Python plotting library used when you need fine-grained control over plot.... |
| `medchem` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Medicinal chemistry filtering library applying drug-likeness rules (Lipinski, Veber), PAINS... |
| `molfeat` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Molecular featurization library with 100+ featurizers including ECFP, MACCS keys, molecular... |
| `networkx` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive toolkit for creating, analyzing, and visualizing complex networks and graphs covering.... |
| `neurokit2` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive biosignal processing toolkit for ECG, EEG, EDA, RSP, PPG, EMG, and EOG signals... |
| `neuropixels-analysis` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Complete Neuropixels analysis pipeline loading SpikeGLX/OpenEphys data, preprocessing with motion... |
| `plotly` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Interactive visualization library providing hover information, zoom/pan, and web-embeddable charts..... |
| `polars` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Fast in-memory DataFrame library using lazy evaluation, parallel execution, and an Apache Arrow... |
| `pydeseq2` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Python DESeq2 implementation for identifying differentially expressed genes from bulk RNA-seq count.... |
| `pydicom` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Python library for reading, writing, and modifying DICOM medical imaging files with pixel data... |
| `pymatgen` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Materials science analysis toolkit supporting crystal structure manipulation (CIF, POSCAR), phase... |
| `pyopenms` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Complete mass spectrometry analysis platform for proteomics workflows including feature detection,..... |
| `pysam` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Genomic file toolkit for reading/writing SAM/BAM/CRAM alignments, VCF/BCF variant files, and... |
| `rdkit` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Core cheminformatics toolkit for SMILES/SDF parsing, molecular descriptor calculation (MW, LogP,... |
| `scanpy` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Standard single-cell RNA-seq analysis pipeline for QC, normalization, dimensionality reduction... |
| `scikit-bio` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Biological data toolkit for sequence analysis, alignments, phylogenetic trees, diversity metrics... |
| `scientific-critical-thinking` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Framework for evaluating scientific claims and evidence quality covering experimental design... |
| `scientific-visualization` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Meta-skill orchestrating matplotlib/seaborn/plotly for publication-ready figures requiring... |
| `seaborn` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Statistical visualization library with pandas integration providing attractive defaults for box... |
| `shap` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | SHAP provides model interpretability using SHapley Additive exPlanations to explain predictions and.... |
| `statistical-analysis` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Guided statistical analysis framework for test selection based on data characteristics, assumption..... |
| `statsmodels` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Statistical models library providing OLS, GLM, mixed models, and ARIMA with detailed diagnostics,... |
| `sympy` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Symbolic mathematics library for Python supporting algebraic equation solving,... |
| `umap-learn` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | UMAP (Uniform Manifold Approximation and Projection) for fast nonlinear dimensionality reduction... |
| `vaex` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Out-of-core DataFrame library for processing and analyzing large tabular datasets (including... |
| `benchling-integration` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Benchling R&D platform integration. |
| `denario` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Denario is a multiagent AI system designed to automate scientific research workflows from initial... |
| `dnanexus-integration` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | DNAnexus cloud genomics platform. |
| `docx` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Document toolkit (.docx). |
| `pptx` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Presentation toolkit for creating, editing, and processing .pptx files with slides, layouts,... |
| `generate-image` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Generates or edits images using AI models via OpenRouter, supporting Gemini 3.1 Flash Image Preview.... |
| `get-available-resources` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | System resource detection tool creating a JSON report of CPU cores, GPUs, memory, and disk space... |
| `infographics` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Professional infographic creation using Nano Banana Pro AI with iterative quality refinement via... |
| `iso-13485-certification` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive toolkit for ISO 13485 medical device Quality Management System certification covering.... |
| `labarchive-integration` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Electronic lab notebook API integration for accessing notebooks, managing entries and attachments,..... |
| `lamindb` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Open-source data framework for biology making datasets queryable, traceable, reproducible, and FAIR.... |
| `latchbio-integration` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Latch platform integration for building bioinformatics workflows using Latch SDK with... |
| `market-research-reports` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Comprehensive market research report generator producing 50+ page documents in McKinsey/BCG/Gartner.... |
| `modal` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Serverless Python cloud platform with containers, GPUs, and autoscaling for deploying ML models,... |
| `omero-integration` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Microscopy data management platform integration for accessing images via Python, retrieving... |
| `protocolsio-integration` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | API integration for protocols.io supporting protocol search, creation, updating, publishing,... |
| `research-grants` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Competitive research proposal writing framework for NSF, NIH, DOE, DARPA, and Taiwan NSTC with... |
| `scientific-brainstorming` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Creative research ideation framework for open-ended brainstorming, exploring interdisciplinary... |
| `scientific-schematics` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Publication-quality scientific diagram creation using Nano Banana Pro AI with iterative quality... |
| `scientific-slides` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Slide deck creation framework for research talks whose primary workflow uses Nano Banana Pro AI to..... |
| `treatment-plans` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | This skill provides LaTeX templates and validation tools for generating concise, focused medical... |
| `zarr-python` | K-Dense-AI/claude-scientific-skills | 06 其他科学技能 (258 skill | Chunked N-dimensional array storage format supporting compressed arrays, parallel I/O, S3/GCS cloud.... |
| `doc-coauthoring` | anthropics/skills | 06 其他科学技能 (258 skill | Guides users through a structured workflow for collaboratively co-authoring documentation such as... |
| `mcp-builder` | anthropics/skills | 06 其他科学技能 (258 skill | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact... |
| `pdf` | anthropics/skills | 06 其他科学技能 (258 skill | Use this skill whenever the user wants to do anything with PDF files. |
| `xlsx` | anthropics/skills | 06 其他科学技能 (258 skill | This skill is used for tasks where a spreadsheet file is the primary input or output, such as... |
| `study` | alaliqing/claude-paper | 06 其他科学技能 (258 skill | Use this skill when the user wants to read, study, analyze, or deeply understand a research paper... |
| `lammps` | Chenghao-Wu/skill_lammps | 06 其他科学技能 (258 skill | Create and validate LAMMPS input scripts with physics-aware validation and educational feedback |
| `systematic-debugging` | obra/superpowers | 06 其他科学技能 (258 skill | Systematic Debugging is a structured methodology to be applied whenever encountering bugs, test... |

---

## 确认相关技能（1528 个）

以下技能被审计确认与科研直接相关，按主题统计：

| 主题 | 数量 |
|------|------|
| 01 信息检索与证据收集 (158 skills) | 148 |
| 02 文献综述、写作与引用 (673 skills) | 595 |
| 03 实验、基准测试与可复现性验证 (589 skills) | 558 |
| 04 数据分析与证据解读 (178 skills) | 174 |
| 05 科研运营与工作流支持 (56 skills) | 53 |

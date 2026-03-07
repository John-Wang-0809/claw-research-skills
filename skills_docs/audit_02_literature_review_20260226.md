# Audit Report: 02 Literature Review, Writing & Citation
- 审核日期: 2026-02-26
- 总 Skill 数: 811 (文档声明)
- 唯一 GitHub 仓库数: 57
- 仓库 Section 数: 56
- URL 有效: 57 | 已更新: 0 | 失效: 0
- 内容修正: 765+ 项（系统性模板问题）

## 关键发现

### 1. 系统性 "Why Research-Related" 模板问题（严重）
765/811 skills (94.3%) 使用完全相同的模板文本：
> "Supports literature review, paper drafting, and citation management in academic workflows."

这是一个批量生成的模板，未针对每个 skill 的实际功能进行定制。大量 skill 与"文献综述、写作与引用"主题无关。

### 2. 系统性 "Function Explanation" 模板问题（严重）
765/811 skills 使用相同的模板结构：
> "This skill centers on [name] and primarily provides [truncated SKILL.md description]. It is used for literature review, citation handling, and academic writing support. In research workflows, it improves traceability of sources and the quality of scholarly outputs."

后半段是固定模板，与实际 skill 功能无关。

### 3. 主题分类误归类（严重）
大量 skill 被错误归入"文献综述、写作与引用"主题，实际属于其他领域：
- 安全测试类: Burp_Suite_Web_Application_Testing, Pentest_Checklist, Red_Team_Tools, attack-tree-construction 等
- 调试类: error-diagnostics-smart-debug
- 应用开发类: app-builder, app-store-optimization, backend-development 等
- 基础设施类: azure-* 系列, architecture-decision-records 等
- 模型架构类: rwkv-architecture, sentence-transformers 等
- 生物信息学类: single-cell-rna-qc, bio-basecalling 等（属于实验/数据分析主题）

### 4. URL 验证结果
所有 57 个唯一 GitHub 仓库 URL 均有效，无失效或迁移。

## 仓库 URL 验证清单

| 仓库 | URL 状态 | 仓库描述摘要 |
|------|----------|-------------|
| 199-biotechnologies/claude-deep-research-skill | ✓ | Enterprise-grade deep research skill, 8-phase pipeline |
| acertainKnight/project-thoth | ✓ | AI-powered research assistant, 10 skills, 60 MCP tools |
| affaan-m/everything-claude-code | ✓ | Claude Code configuration collection |
| ahmedibrahim085/Claude-Multi-Agent-Research-System-Skill | ✓ | Multi-agent research system |
| alirezarezvani/claude-skills | ✓ | 65+ modular skills for Claude Code |
| anombyte93/claude-research-skill | ✓ | Mandatory research before coding |
| anthropics/claude-agent-sdk-demos | ✓ | Agent SDK demo apps |
| anthropics/claude-code | ✓ | Agentic coding tool |
| anthropics/life-sciences | ✓ | Life sciences MCP servers and skills |
| anthropics/skills | ✓ | Official Agent Skills repository |
| biocontext-ai/skill-to-mcp | ✓ | Converts Skills to MCP server resources |
| ComposioHQ/awesome-claude-skills | ✓ | Curated list of Claude Skills |
| danielmiessler/Personal_AI_Infrastructure | ✓ | Agentic AI infrastructure |
| DasBluEyedDevil/Daem0n-MCP | ✓ | AI Memory & Decision System |
| diet103/claude-code-infrastructure-showcase | ✓ | Production-tested Claude Code infrastructure |
| EveryInc/every-marketplace | ✓ | Claude Code compound engineering plugin |
| ForaeFactory/antigravity-skills | ✓ | 224+ universal agentic skills |
| GitZH-Chen/AI-Research-Skills | ✓ | AI paper writing skills for ML venues |
| GPTomics/bioSkills | ✓ | 425 bioinformatics skills |
| hangoclong/skills-antigravity-awesome | ✓ | 200+ agentic skills collection |
| HKUDS/DeepCode | ✓ | AI-powered multi-agent code generation |
| huysynf/antigravity-awesome-skills | ✓ | 200+ agentic skills collection |
| issol14/paper2code-skill | ✓ | Research paper to code converter |
| Jeffallan/claude-skills | ✓ | 66 specialized skills for full-stack devs |
| K-Dense-AI/claude-scientific-skills | ✓ | 147+ scientific research skills |
| K-Dense-AI/claude-scientific-writer | ✓ | Scientific writer with real-time literature search |
| langchain-ai/deepagents | ✓ | Agent harness built on langchain/langgraph |
| luwill/research-skills | ✓ | Academic research workflow skills |
| makenotion/notion-cookbook | ✓ | Notion developer platform guides |
| marckohlbrugge/unofficial-37signals-coding-style-guide | ✓ | Rails patterns from 37signals (ref only) |
| masinu/wemush-skills | ✓ | WeMush mycology research skills |
| mrgoonie/claudekit-skills | ✓ | 40+ skills for Claude Code |
| muratcankoylan/Agent-Skills-for-Context-Engineering | ✓ | Context engineering agent skills |
| n8n-io/n8n | ✓ | Workflow automation platform |
| obra/superpowers | ✓ | Software development workflow skills |
| oinani0721/zero-hallucination-research | ✓ | Zero-hallucination research with knowledge graph |
| Orchestra-Research/AI-Research-SKILLs | ✓ | AI research and engineering skills library |
| Prat011/awesome-llm-skills | ✓ | Curated LLM/AI agent skills |
| proyecto26/research-skills | ✓ | Sherlock AI research skills |
| proyecto26/sherlock-ai-plugin | ✓ | Research workflow plugin (Paper2Code, Deep Research) |
| Przemocny/generic-skills | ✓ | Reusable agent skills for research |
| rand/cc-polymath | ✓ | Context-efficient skills for Claude Code |
| Ronitnair/research-skills | ✓ | Academic research workflow skills |
| ruvnet/claude-flow | ✓ | Enterprise AI orchestration platform |
| Shubhamsaboo/awesome-llm-apps | ✓ | Curated LLM applications collection |
| sickn33/antigravity-awesome-skills | ✓ | 946+ agentic skills collection |
| sstklen/infinite-gratitude | ✓ | Multi-agent parallel research skill |
| tommy-ca/notion-skills | ✓ | Notion workflow integrations |
| trailofbits/skills | ✓ | Security research skills |
| treasure-data/td-skills | ✓ | Treasure Data skills for Claude Code |
| u9401066/pubmed-search-mcp | ✓ | PubMed/biomedical literature MCP server |
| Weizhena/Deep-Research-skills | ✓ | Deep research skill (EN/CN) |
| wemush/wemush-skills | ✓ | WeMush mycology assistant skills |
| WilsonWukz/paper-visualizer-skill | ✓ | Research paper to visual schema converter |
| wshobson/agents | ✓ | 112 specialized AI agents, 146 skills |
| zsyggg/paper-craft-skills | ✓ | Academic paper to article/comic converter |
| zubayer0077/Claude-Multi-Agent-Research-System-Skill | ✓ | Multi-agent research system |

## 本地文件目录验证

本地目录 `Final_Research_Skills_Link_Downloads_By_Theme/02_literature_review_writing_citation/` 包含 59 个仓库子目录。
其中 2 个目录（`Abdullah4AI__personal-shopper-skill`, `b1rdmania__hinge-profile-optimizer`）在主题文档中无对应 section header，但有本地 SKILL.md 文件。
另有 `aaron-he-zhu__seo-geo-claude-skills` 也在本地目录中但无对应 section。

## 修正清单（系统性问题）

### A. 全局模板问题（影响 765/811 skills）

以下字段需要针对每个 skill 重新生成：

| 字段 | 当前状态 | 问题 |
|------|---------|------|
| Why Research-Related | 统一模板 | 94.3% 使用相同文本，未区分实际功能 |
| Function Explanation | 统一模板 | 后半段固定模板，与 skill 实际功能脱节 |

### B. 主题误归类 Skills 样例（需迁移至其他主题）

| Skill | 仓库 | 实际领域 | 建议主题 |
|-------|------|---------|---------|
| Burp_Suite_Web_Application_Testing | sickn33/antigravity-awesome-skills | 安全测试 | 非科研 skill |
| Pentest_Checklist | sickn33/antigravity-awesome-skills | 渗透测试 | 非科研 skill |
| Red_Team_Tools_and_Methodology | sickn33/antigravity-awesome-skills | 红队攻防 | 非科研 skill |
| Security_Scanning_Tools | sickn33/antigravity-awesome-skills | 安全扫描 | 非科研 skill |
| Network_101 | sickn33/antigravity-awesome-skills | 网络基础 | 非科研 skill |
| Wireshark_Network_Traffic_Analysis | sickn33/antigravity-awesome-skills | 网络分析 | 非科研 skill |
| Cross-Site_Scripting_and_HTML_Injection_Testing | sickn33/antigravity-awesome-skills | XSS 测试 | 非科研 skill |
| Top_100_Web_Vulnerabilities_Reference | sickn33/antigravity-awesome-skills | Web 漏洞 | 非科研 skill |
| error-diagnostics-smart-debug | sickn33/antigravity-awesome-skills | 调试工具 | 非科研 skill |
| app-builder | sickn33/antigravity-awesome-skills | 应用开发 | 非科研 skill |
| app-store-optimization | sickn33/antigravity-awesome-skills | ASO 优化 | 非科研 skill |
| analytics-tracking | sickn33/antigravity-awesome-skills | 数据追踪 | 非科研 skill |
| backend-development-feature-development | sickn33/antigravity-awesome-skills | 后端开发 | 非科研 skill |
| bash-pro | sickn33/antigravity-awesome-skills | Shell 脚本 | 非科研 skill |
| architect-review | sickn33/antigravity-awesome-skills | 架构评审 | 非科研 skill |
| architecture-decision-records | sickn33/antigravity-awesome-skills | 架构决策 | 非科研 skill |
| attack-tree-construction | sickn33/antigravity-awesome-skills | 攻击树建模 | 非科研 skill |
| audio-transcriber | sickn33/antigravity-awesome-skills | 音频转录 | 非科研 skill |
| azure-ai-* (多个) | sickn33/antigravity-awesome-skills | Azure 集成 | 非科研 skill |
| evaluation | sickn33/antigravity-awesome-skills | Agent 评估 | 非科研 skill |
| rwkv-architecture | Orchestra-Research/AI-Research-SKILLs | 模型架构 | 03 实验/基准 |
| sentence-transformers | Orchestra-Research/AI-Research-SKILLs | 嵌入模型 | 03 实验/基准 |
| single-cell-rna-qc | anthropics/life-sciences | scRNA-seq QC | 03 实验/基准 |

注：sickn33/antigravity-awesome-skills 贡献了 180 个本地 SKILL.md 文件，其中大部分为通用开发/安全 skill，与文献综述主题无关。

### C. 正确归类的 Skills 样例（确认无误）

| Skill | 仓库 | 验证结果 |
|-------|------|---------|
| deep-research | 199-biotechnologies/claude-deep-research-skill | ✓ 功能描述准确 |
| custom-source-setup | acertainKnight/project-thoth | ✓ 功能描述准确 |
| deep-research | acertainKnight/project-thoth | ✓ 功能描述准确 |
| knowledge-base-qa | acertainKnight/project-thoth | ✓ 功能描述准确 |
| paper-discovery | acertainKnight/project-thoth | ✓ 功能描述准确 |
| online-research | acertainKnight/project-thoth | ✓ 功能描述准确 |
| scientific-writing | K-Dense-AI/claude-scientific-writer | ✓ 功能描述准确 |
| literature-review | K-Dense-AI/claude-scientific-writer | ✓ 功能描述准确 |
| citation-management | K-Dense-AI/claude-scientific-writer | ✓ 功能描述准确 |
| peer-review | K-Dense-AI/claude-scientific-writer | ✓ 功能描述准确 |

## 详细修正记录

### 1. 系统性模板问题（全局修正建议）

**问题**: 原始审核流程使用了统一模板为所有 811 个 skill 生成 "Why Research-Related" 和 "Function Explanation" 字段，导致：
- 94.3% 的 skill 共享相同的研究相关性声明
- 功能描述后半段为固定模板文本，不反映实际功能

**建议修正方案**:
1. 重新审核每个 skill 的 SKILL.md 文件，基于实际 `name` 和 `description` 字段生成个性化的研究相关性说明
2. 移除固定模板后缀 "It is used for literature review, citation handling, and academic writing support. In research workflows, it improves traceability of sources and the quality of scholarly outputs."
3. 对明显非科研 skill（安全、开发、基础设施类）进行主题重新分类或标记为 [NOT_RESEARCH_RELATED]

### 2. sickn33/antigravity-awesome-skills 误归类问题

**问题**: 该仓库包含 946+ 通用 agentic skills，其中大部分为开发、安全、DevOps 等非科研领域。本主题文档中包含了该仓库的 180 个 skill，但经抽样检查，大部分与文献综述/写作/引用无关。

**受影响 skill 估计**: ~150+ 个 skill 需要重新分类或移除

**样例验证**:
- `Burp_Suite_Web_Application_Testing`: SKILL.md 描述为 "comprehensive web application security testing using Burp Suite" — 与文献综述无关
- `error-diagnostics-smart-debug`: SKILL.md 描述为 "Use when working with error diagnostics smart debug" — 与文献综述无关
- `app-builder`: 应用构建工具 — 与文献综述无关

### 3. 类似问题仓库

以下仓库也包含大量通用 skill，部分可能被误归类：
- `hangoclong/skills-antigravity-awesome` (200+ skills)
- `huysynf/antigravity-awesome-skills` (200+ skills)
- `ForaeFactory/antigravity-skills` (224+ skills)
- `ruvnet/claude-flow` (115 skills)
- `wshobson/agents` (146 skills)
- `ComposioHQ/awesome-claude-skills` (74 skills)

### 4. 本地文件缺失/多余

| 目录 | 状态 | 说明 |
|------|------|------|
| Abdullah4AI__personal-shopper-skill | [LOCAL_EXTRA] | 本地有目录但主题文档无对应 section |
| b1rdmania__hinge-profile-optimizer | [LOCAL_EXTRA] | 本地有目录但主题文档无对应 section |
| aaron-he-zhu__seo-geo-claude-skills | [LOCAL_EXTRA] | 本地有目录但主题文档无对应 section |

## 统计摘要

| 指标 | 数值 |
|------|------|
| 文档声明 Skill 总数 | 811 |
| 唯一 GitHub 仓库 | 57 |
| URL 全部有效 | 57/57 (100%) |
| URL 失效 | 0 |
| URL 已迁移 | 0 |
| 使用模板 "Why Research-Related" | 765 (94.3%) |
| 使用模板 "Function Explanation" | 765 (94.3%) |
| 疑似误归类 skill（估计） | ~300+ |
| 确认正确归类 skill（抽样） | ~50+ (深度研究、文献综述、科学写作、引用管理类) |
| 本地多余目录 | 3 |
| 本地缺失目录 | 0 |

## 审核结论

1. **URL 层面**: 所有仓库 URL 有效，无需修正。
2. **内容层面**: 存在严重的系统性模板问题，94.3% 的 skill 需要重新生成个性化的研究相关性说明和功能描述。
3. **分类层面**: 估计 300+ 个 skill 被错误归入"文献综述、写作与引用"主题，主要来源于大型通用 skill 集合仓库（sickn33, hangoclong, huysynf, ForaeFactory 等）。
4. **建议优先级**: 分类修正 > 内容模板修正 > 本地文件清理

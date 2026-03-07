# Audit Report: 04 Data Analysis & Evidence Interpretation
- 审核日期: 2026-02-26
- 总 Skill 数: 191
- 唯一仓库数: 18
- URL 有效: 18 | 已更新: 0 | 失效: 0
- 内容修正: 53 项（科研相关性不符）

## 关键发现

### 1. 模板化问题（严重）
所有 191 个 skills 的 "Why Research-Related" 字段使用完全相同的模板文本：
> "Supports data-centric investigation, statistical analysis, and evidence interpretation."

所有 192 个 Function Explanation 也包含相同的模板句式：
> "It emphasizes data-centric analysis, interpretation, and evidence structuring. In research workflows, it supports turning raw observations into testable conclusions."

这意味着科研相关性判断和功能描述均为自动生成，未经逐个核实。

### 2. 科研相关性统计
- genuinely relevant（确实与数据分析相关）: 138 (72.3%)
  - GPTomics/bioSkills: 127 个生物信息学技能（全部相关）
  - K-Dense-AI: 4 个（dask, pymc-bayesian-modeling, seaborn, shap）
  - 其他: 7 个（pandas-pro, azure-ai-textanalytics-py, azure-ai-vision-imageanalysis-java/py, dbt-transformation-patterns, sql-optimization-patterns, trino）
- NOT relevant（与数据分析无关）: 53 (27.7%)

### 3. 空表格仓库
以下仓库在主题文档中有 header 但无 skill 行：
- anthropics/claude-agent-sdk-demos（本地有 1 个文件：listener-creator）
- ComposioHQ/awesome-claude-skills（本地有 2 个文件：Coinbase_Automation, Lever_Automation）

### 4. 本地文件多于主题文档
sickn33 仓库本地有 39 个文件，但主题文档仅列出 28 个 skill。11 个额外本地文件未在主题文档中出现。

### 5. 模板占位符 Skills
trailofbits/skills 包含 2 个模板占位符：`{domain-name-lowercase}` 和 `{tool-name-lowercase}`，这些不是实际 skill。

## 仓库 URL 验证结果

| 仓库 | URL | 状态 | 描述 |
|------|-----|------|------|
| acertainKnight/project-thoth | https://github.com/acertainKnight/project-thoth | ✓ | AI research assistant |
| affaan-m/everything-claude-code | https://github.com/affaan-m/everything-claude-code | ✓ | Claude Code configs |
| anthropics/claude-agent-sdk-demos | https://github.com/anthropics/claude-agent-sdk-demos | ✓ | Claude SDK demos |
| ComposioHQ/awesome-claude-skills | https://github.com/ComposioHQ/awesome-claude-skills | ✓ | Curated skills list |
| ForaeFactory/antigravity-skills | https://github.com/ForaeFactory/antigravity-skills | ✓ | Fork of sickn33 |
| GPTomics/bioSkills | https://github.com/GPTomics/bioSkills | ✓ | Bioinformatics skills |
| hangoclong/skills-antigravity-awesome | https://github.com/hangoclong/skills-antigravity-awesome | ✓ | Fork of sickn33 |
| huysynf/antigravity-awesome-skills | https://github.com/huysynf/antigravity-awesome-skills | ✓ | Fork of sickn33 |
| Jeffallan/claude-skills | https://github.com/Jeffallan/claude-skills | ✓ | Full-stack dev skills |
| K-Dense-AI/claude-scientific-skills | https://github.com/K-Dense-AI/claude-scientific-skills | ✓ | Scientific skills |
| mrgoonie/claudekit-skills | https://github.com/mrgoonie/claudekit-skills | ✓ | ClaudeKit skills |
| muratcankoylan/Agent-Skills-for-Context-Engineering | https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering | ✓ | Context engineering |
| ruvnet/claude-flow | https://github.com/ruvnet/claude-flow | ✓ | Agent orchestration |
| sickn33/antigravity-awesome-skills | https://github.com/sickn33/antigravity-awesome-skills | ✓ | 900+ agentic skills |
| trailofbits/skills | https://github.com/trailofbits/skills | ✓ | Security research |
| treasure-data/td-skills | https://github.com/treasure-data/td-skills | ✓ | Treasure Data skills |
| wshobson/agents | https://github.com/wshobson/agents | ✓ | Multi-agent system |
| yusufkaraaslan/Skill_Seekers | https://github.com/yusufkaraaslan/Skill_Seekers | ✓ | Skill generation tool |

## 修正清单

以下 53 个 Skills 与 "Data Analysis and Evidence Interpretation" 主题不符，科研相关性需修正：

| # | Skill | 仓库 | URL状态 | 科研相关性 | 功能描述 | Workflow | 修正摘要 |
|---|-------|------|---------|-----------|---------|---------|---------|
| 1 | MCP Server Management | acertainKnight/project-thoth | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | MCP连接管理，非数据分析 |
| 2 | continuous-learning-v2 | affaan-m/everything-claude-code | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 会话学习系统，非数据分析 |
| 3 | security-scan | affaan-m/everything-claude-code | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 安全扫描，非数据分析 |
| 4 | graphql | ForaeFactory/antigravity-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | GraphQL API开发 |
| 5 | lint-and-validate | ForaeFactory/antigravity-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 代码质量检查 |
| 6 | Linux Production Shell Scripts | ForaeFactory/antigravity-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Linux运维脚本 |
| 7 | graphql | hangoclong/skills-antigravity-awesome | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | GraphQL（fork重复） |
| 8 | lint-and-validate | hangoclong/skills-antigravity-awesome | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 代码检查（fork重复） |
| 9 | Linux Production Shell Scripts | hangoclong/skills-antigravity-awesome | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Linux脚本（fork重复） |
| 10 | graphql | huysynf/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | GraphQL（fork重复） |
| 11 | lint-and-validate | huysynf/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 代码检查（fork重复） |
| 12 | Linux Production Shell Scripts | huysynf/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Linux脚本（fork重复） |
| 13 | graphql-architect | Jeffallan/claude-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | GraphQL架构设计 |
| 14 | postgres-pro | Jeffallan/claude-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | PostgreSQL数据库管理 |
| 15 | swift-expert | Jeffallan/claude-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Swift/iOS开发 |
| 16 | ai-multimodal | mrgoonie/claudekit-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 多模态AI |
| 17 | sequential-thinking | mrgoonie/claudekit-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 顺序思维模式 |
| 18 | bdi-mental-states | muratcankoylan/Agent-Skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | BDI认知架构 |
| 19 | agent-production-validator | ruvnet/claude-flow | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 生产环境验证 |
| 20 | angular-migration | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Angular框架迁移 |
| 21 | azure-ai-contentsafety-java | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 内容安全审核 |
| 22 | azure-ai-contentsafety-py | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 内容安全审核 |
| 23 | azure-mgmt-apicenter-py | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | API中心管理 |
| 24 | binary-analysis-patterns | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 二进制逆向分析 |
| 25 | code-documentation-code-explain | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 代码解释 |
| 26 | code-documentation-doc-generate | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 文档生成 |
| 27 | codebase-cleanup-deps-audit | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 依赖审计 |
| 28 | database-migrations-sql-migrations | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 数据库迁移 |
| 29 | dependency-management-deps-audit | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 依赖管理审计 |
| 30 | documentation-generation-doc-generate | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 文档生成（重复） |
| 31 | error-diagnostics-error-trace | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 错误追踪 |
| 32 | framework-migration-code-migrate | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 框架迁移 |
| 33 | frontend-mobile-security-xss-scan | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | XSS漏洞扫描 |
| 34 | graphql | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | GraphQL开发 |
| 35 | lint-and-validate | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 代码检查 |
| 36 | Linux Production Shell Scripts | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Linux运维脚本 |
| 37 | n8n-code-python | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | n8n工作流Python |
| 38 | php-pro | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | PHP开发 |
| 39 | security-requirement-extraction | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 安全需求提取 |
| 40 | security-scanning-security-dependencies | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 安全依赖扫描 |
| 41 | shellcheck-configuration | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Shell脚本检查 |
| 42 | unit-testing-test-generate | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 单元测试生成 |
| 43 | fuzzing-obstacles | trailofbits/skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 模糊测试技术 |
| 44 | sarif-parsing | trailofbits/skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | SARIF文件解析 |
| 45 | {domain-name-lowercase} | trailofbits/skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 模板占位符，非实际skill |
| 46 | {tool-name-lowercase} | trailofbits/skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 模板占位符，非实际skill |
| 47 | field-agent-documentation | treasure-data/td-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Agent文档模板 |
| 48 | trino-to-hive-migration | treasure-data/td-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | SQL引擎迁移 |
| 49 | angular-migration | wshobson/agents | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Angular迁移（重复） |
| 50 | binary-analysis-patterns | wshobson/agents | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 二进制分析（重复） |
| 51 | python-type-safety | wshobson/agents | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Python类型安全 |
| 52 | security-requirement-extraction | wshobson/agents | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 安全需求（重复） |
| 53 | shellcheck-configuration | wshobson/agents | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | Shell检查（重复） |

## 确认相关的 Skills（138个，无需修正）

### GPTomics/bioSkills（127个）
全部 127 个生物信息学 skills 确实与数据分析相关，涵盖：序列比对过滤、变异检测、基因表达分析、通路富集、群体遗传学、空间转录组学、代谢组学、蛋白质组学、Hi-C分析、单细胞分析等。

### K-Dense-AI/claude-scientific-skills（4个）
- dask: 分布式数据计算 ✓
- pymc-bayesian-modeling: 贝叶斯统计建模 ✓
- seaborn: 统计可视化 ✓
- shap: ML模型可解释性 ✓

### Jeffallan/claude-skills（1个）
- pandas-pro: Pandas数据操作与分析 ✓

### sickn33/antigravity-awesome-skills（5个）
- azure-ai-textanalytics-py: NLP文本分析 ✓
- azure-ai-vision-imageanalysis-java: 图像分析 ✓
- azure-ai-vision-imageanalysis-py: 图像分析 ✓
- dbt-transformation-patterns: 数据转换管道 ✓
- sql-optimization-patterns: SQL查询优化 ✓

### treasure-data/td-skills（1个）
- trino: Trino SQL数据查询 ✓

## 详细修正记录

### 系统性问题：模板化科研相关性
- 原文（所有191个skill相同）: "Supports data-centric investigation, statistical analysis, and evidence interpretation."
- 问题: 该描述为自动生成模板，未针对每个skill的实际功能进行判断
- 建议: 对53个不相关skill重新分类到更合适的主题（如 05_research_operations 或移除）

### 系统性问题：模板化功能描述
- 所有192个Function Explanation包含相同的模板句: "It emphasizes data-centric analysis, interpretation, and evidence structuring. In research workflows, it supports turning raw observations into testable conclusions."
- 建议: 基于本地SKILL.md的实际description字段重写功能描述

### 模板占位符 Skills
- trailofbits/skills 的 `{domain-name-lowercase}` 和 `{tool-name-lowercase}` 是skill生成器的模板文件，不是实际可用的skill
- 建议: 从审核清单中移除

### Fork 重复 Skills
以下仓库是 sickn33/antigravity-awesome-skills 的 fork，包含完全相同的 skills：
- ForaeFactory/antigravity-skills（3个重复）
- hangoclong/skills-antigravity-awesome（3个重复）
- huysynf/antigravity-awesome-skills（3个重复）
- wshobson/agents 也包含部分重复（angular-migration, binary-analysis-patterns, security-requirement-extraction, shellcheck-configuration）
- 建议: 标记为重复来源，避免重复计数

### 本地文件与主题文档不一致
sickn33 仓库本地有 11 个额外文件未在主题文档中列出：
azure-ai-document-intelligence-dotnet, azure-ai-document-intelligence-ts, azure-ai-formrecognizer-java, blockchain-developer, claude-ally-health, conductor-status, nanobanana-ppt-skills, obsidian-clipper-template-creator, security-compliance-compliance-check, seo-meta-optimizer, team-collaboration-issue

### 空表格仓库
anthropics/claude-agent-sdk-demos 和 ComposioHQ/awesome-claude-skills 在主题文档中有 header 和表头但无 skill 行，本地却有下载文件。建议补充或移除空 header。

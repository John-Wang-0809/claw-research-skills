# Audit Report: 05 Research Operations & Workflow Support
- 审核日期: 2026-02-26
- 总 Skill 数: 60 (文档声称 107，实际提取 60)
- URL 有效: 10 | 已更新: 0 | 失效: 0
- 内容修正: 18 项
- 本地文件匹配: 60/60 (另有 10 个额外本地文件未在主题文档中列出)

## 全局问题

### 1. Skill 计数不一致
主题文档头部声称 "Skill count in this file: **107**"，但实际仅包含 60 个 skill 条目。需修正文档头部计数。

### 2. wshobson/agents 空表
`wshobson/agents` 有章节标题和表头，但无任何 skill 行。本地目录下有 `stripe-integration` 文件但未列入。

### 3. 科研相关性模板化问题
所有 60 个 skill 的 "Why Research-Related" 字段使用完全相同的模板文本：
> "Related to research operations (evidence gathering, analysis, validation, or reporting)."

这对于 GPTomics/bioSkills 的生物信息学技能是合理的，但对于以下技能明显不准确：
- `django-tdd` (Django 测试框架)
- `File Path Traversal Testing` (安全渗透测试)
- `personal-tool-builder` (个人工具开发)
- `agent-base-template-generator` (代码模板生成)
- `agent-refinement` (代码优化重构)
- `agent-tdd-london-swarm` (TDD 测试方法论)

### 4. 功能描述截断
多数 Function Explanation 被截断（以 "." 结尾的不完整句子），这是原始生成时的字段长度限制导致。

## URL 验证结果

| 仓库 | 状态 | 描述 |
|------|------|------|
| affaan-m/everything-claude-code | ✓ | Complete Claude Code configuration collection; 53.1k stars |
| ForaeFactory/antigravity-skills | ✓ | Fork of sickn33/antigravity-awesome-skills; 224+ skills |
| GPTomics/bioSkills | ✓ | Bioinformatics skills for AI coding agents; 287 stars, 425 skills |
| hangoclong/skills-antigravity-awesome | ✓ | Fork of sickn33/antigravity-awesome-skills; 253+ skills |
| huysynf/antigravity-awesome-skills | ✓ | Fork of sickn33/antigravity-awesome-skills; 253+ skills |
| mrgoonie/claudekit-skills | ✓ | ClaudeKit skills collection; 1.8k stars |
| obra/superpowers | ✓ | Agentic skills framework; 62.9k stars |
| ruvnet/claude-flow | ✓ | Agent orchestration platform (Ruflo v3); 14.8k stars |
| sickn33/antigravity-awesome-skills | ✓ | Original antigravity skills; 15.9k stars, 946+ skills |
| wshobson/agents | ✓ | Multi-agent orchestration for Claude Code; 29.4k stars |

## 修正清单

| # | Skill | 仓库 | URL 状态 | 科研相关性 | 功能描述 | Workflow | 修正摘要 |
|---|-------|------|----------|-----------|---------|---------|---------|
| 1 | django-tdd | affaan-m/everything-claude-code | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 非科研技能；Django TDD 与研究运营无关 |
| 2 | File Path Traversal Testing | ForaeFactory/antigravity-skills | ✓ | [RELEVANCE_UPDATED] | ✓ | ✓ | 安全渗透测试技能，非科研运营 |
| 3 | personal-tool-builder | ForaeFactory/antigravity-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 个人工具开发，非科研运营 |
| 4 | verification-before-completion | ForaeFactory/antigravity-skills | ✓ | ✓ | [FUNC_UPDATED] | ✓ | 功能描述截断 |
| 5 | File Path Traversal Testing | hangoclong/skills-antigravity-awesome | ✓ | [RELEVANCE_UPDATED] | ✓ | ✓ | 同 #2，fork 重复 |
| 6 | personal-tool-builder | hangoclong/skills-antigravity-awesome | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 同 #3，fork 重复 |
| 7 | verification-before-completion | hangoclong/skills-antigravity-awesome | ✓ | ✓ | [FUNC_UPDATED] | ✓ | 同 #4，fork 重复 |
| 8 | File Path Traversal Testing | huysynf/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | ✓ | ✓ | 同 #2，fork 重复 |
| 9 | personal-tool-builder | huysynf/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 同 #3，fork 重复 |
| 10 | verification-before-completion | huysynf/antigravity-awesome-skills | ✓ | ✓ | [FUNC_UPDATED] | ✓ | 同 #4，fork 重复 |
| 11 | agent-base-template-generator | ruvnet/claude-flow | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 代码模板生成器，非科研运营 |
| 12 | agent-refinement | ruvnet/claude-flow | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | SPARC 代码优化，非科研运营 |
| 13 | agent-tdd-london-swarm | ruvnet/claude-flow | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | London School TDD，非科研运营 |
| 14 | File Path Traversal Testing | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | ✓ | ✓ | 同 #2，原始仓库 |
| 15 | personal-tool-builder | sickn33/antigravity-awesome-skills | ✓ | [RELEVANCE_UPDATED] | [FUNC_UPDATED] | ✓ | 同 #3，原始仓库 |
| 16 | verification-before-completion | sickn33/antigravity-awesome-skills | ✓ | ✓ | [FUNC_UPDATED] | ✓ | 同 #4，原始仓库 |
| 17 | (全部 42 个 bio-* skills) | GPTomics/bioSkills | ✓ | ✓ | [FUNC_UPDATED] | ✓ | 功能描述均被截断；科研相关性准确 |
| 18 | Verification Before Completion | mrgoonie/claudekit-skills | ✓ | ✓ | ✓ | ✓ | 无修正 |

## 详细修正记录

### django-tdd (affaan-m/everything-claude-code)
- URL 状态: ✓ 有效
- 科研相关性修正: [RELEVANCE_UPDATED] 该 skill 是 Django 框架的 TDD 测试方法论（pytest-django, factory_boy, mocking），属于通用软件工程实践，与科研运营无直接关联。建议重新分类或移除。
- 功能描述修正: [FUNC_UPDATED] 原文截断于 "...testing Django REST Framework APIs."。本地 SKILL.md 完整描述为: "Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs."

### File Path Traversal Testing (4 个仓库: ForaeFactory, hangoclong, huysynf, sickn33)
- URL 状态: ✓ 全部有效
- 科研相关性修正: [RELEVANCE_UPDATED] 该 skill 是 Web 安全渗透测试技能（目录遍历漏洞检测），使用 Burp Suite/OWASP ZAP 等工具。与科研运营完全无关，属于网络安全领域。建议移除出本主题。
- 功能描述: ✓ 与本地文件一致
- 备注: 4 个仓库中的版本内容相同（fork 关系），存在重复计数

### personal-tool-builder (4 个仓库: ForaeFactory, hangoclong, huysynf, sickn33)
- URL 状态: ✓ 全部有效
- 科研相关性修正: [RELEVANCE_UPDATED] 该 skill 关于构建个人工具（scratch-your-own-itch 方法论、CLI 工具开发、本地优先应用）。属于通用软件开发实践，非科研运营。建议移除。
- 功能描述修正: [FUNC_UPDATED] 原文截断于 "...scratch your own itch,"。完整描述为: "Expert in building custom tools that solve your own problems first. The best products often start as personal tools - scratch your own itch, build for yourself, then discover others have the same itch."
- 备注: 4 个仓库中的版本内容相同（fork 关系）

### verification-before-completion (5 个仓库: ForaeFactory, hangoclong, huysynf, sickn33, obra)
- URL 状态: ✓ 全部有效
- 科研相关性: ✓ 验证完成前的证据收集流程可合理映射到科研验证环节
- 功能描述修正: [FUNC_UPDATED] 原文截断于 "...running verification commands and ."。完整描述为: "Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always"
- 备注: 5 个仓库中的版本内容相同（fork 关系 + obra/superpowers 独立实现）

### agent-base-template-generator (ruvnet/claude-flow)
- URL 状态: ✓ 有效
- 科研相关性修正: [RELEVANCE_UPDATED] 该 skill 是代码模板/脚手架生成器（React 组件、API 端点、数据库模型等），属于通用软件工程工具，与科研运营无关。建议移除。
- 功能描述修正: [FUNC_UPDATED] 原文仅为 "Agent skill for base-template-generator - invoke with $agent-base-template-generator"，过于简略。本地文件描述为: 专注于创建干净、结构良好的基础模板和样板代码的架构师角色。

### agent-refinement (ruvnet/claude-flow)
- URL 状态: ✓ 有效
- 科研相关性修正: [RELEVANCE_UPDATED] 该 skill 是 SPARC 方法论的代码优化阶段（code_optimization, test_development, refactoring, performance_tuning），属于软件工程实践，非科研运营。建议移除。
- 功能描述修正: [FUNC_UPDATED] 原文仅为 "Agent skill for refinement - invoke with $agent-refinement"，过于简略。本地文件描述为: SPARC Refinement phase specialist for iterative improvement。

### agent-tdd-london-swarm (ruvnet/claude-flow)
- URL 状态: ✓ 有效
- 科研相关性修正: [RELEVANCE_UPDATED] 该 skill 是 London School TDD 方法论（mock-driven development, outside-in TDD, behavior verification），属于软件测试方法论，非科研运营。建议移除。
- 功能描述修正: [FUNC_UPDATED] 原文仅为 "Agent skill for tdd-london-swarm - invoke with $agent-tdd-london-swarm"，过于简略。本地文件描述为: TDD London School specialist for mock-driven development within swarm coordination。

### GPTomics/bioSkills (42 个 bio-* skills 批量审核)
- URL 状态: ✓ 全部有效
- 科研相关性: ✓ 全部 42 个生物信息学技能与科研运营高度相关（ChIP-seq 可视化、单细胞聚类、宏基因组分析、变异检测、工作流管理等）
- 功能描述修正: [FUNC_UPDATED] 所有 42 个 skill 的 Function Explanation 均使用模板化格式且被截断。模板为: "This skill centers on \"[name]\" and primarily provides [truncated description]. It can be integrated into research execution to standardize recurring operations."。本地 SKILL.md 文件包含完整、准确的技术描述。
- Workflow: ✓ Execution Flow 与本地文件的依赖关系/工作流步骤基本一致
- 涉及的 42 个 skills: bio-chipseq-visualization, bio-clinical-databases-hla-typing, bio-clinical-databases-pharmacogenomics, bio-clinical-databases-somatic-signatures, bio-clip-seq-binding-site-annotation, bio-clip-seq-clip-alignment, bio-compressed-files, bio-ctdna-mutation-detection, bio-data-visualization-multipanel-figures, bio-data-visualization-network-visualization, bio-epitranscriptomics-m6a-peak-calling, bio-epitranscriptomics-modification-visualization, bio-format-conversion, bio-genome-assembly-assembly-polishing, bio-genome-assembly-hifi-assembly, bio-immunoinformatics-immunogenicity-scoring, bio-longread-medaka, bio-longread-structural-variants, bio-metagenomics-abundance, bio-metagenomics-amr-detection, bio-phylo-tree-manipulation, bio-phylo-tree-visualization, bio-primer-design-primer-validation, bio-primer-design-qpcr-primers, bio-reaction-enumeration, bio-read-alignment-bwa-alignment, bio-read-qc-adapter-trimming, bio-read-sequences, bio-reporting-figure-export, bio-sashimi-plots, bio-sequence-slicing, bio-single-cell-clustering, bio-single-cell-markers-annotation, bio-spatial-transcriptomics-spatial-data-io, bio-vcf-basics, bio-workflow-management-cwl-workflows, bio-workflow-management-nextflow-pipelines, bio-workflow-management-wdl-workflows, bio-workflows-fastq-to-variants, bio-workflows-metagenomics-pipeline, bio-workflows-outbreak-pipeline, bio-write-sequences

### Verification Before Completion (mrgoonie/claudekit-skills)
- URL 状态: ✓ 有效
- 科研相关性: ✓ 准确
- 功能描述: ✓ 与本地文件一致
- Workflow: ✓ 与本地文件一致
- 无需修正

### verification-before-completion (obra/superpowers)
- URL 状态: ✓ 有效
- 科研相关性: ✓ 准确
- 功能描述修正: [FUNC_UPDATED] 同上述 verification-before-completion 截断问题
- Workflow: ✓ 与本地文件一致

## 额外本地文件（未在主题文档中列出）

以下 10 个本地 SKILL.md 文件存在于下载目录中，但未出现在主题文档的 skill 表格中：

| 仓库 | Skill | 本地文件 |
|------|-------|---------|
| ForaeFactory/antigravity-skills | interactive-portfolio | interactive-portfolio__2c2d7e2007__SKILL.md |
| ForaeFactory/antigravity-skills | pc-games | pc-games__23f08f1287__SKILL.md |
| hangoclong/skills-antigravity-awesome | interactive-portfolio | interactive-portfolio__db611cdf48__SKILL.md |
| hangoclong/skills-antigravity-awesome | pc-games | pc-games__3b2d73934c__SKILL.md |
| huysynf/antigravity-awesome-skills | interactive-portfolio | interactive-portfolio__a4621ad15d__SKILL.md |
| huysynf/antigravity-awesome-skills | pc-games | pc-games__8cf48c48f0__SKILL.md |
| sickn33/antigravity-awesome-skills | interactive-portfolio | interactive-portfolio__d784fe9da4__SKILL.md |
| sickn33/antigravity-awesome-skills | pc-games | pc-games__a4a2abf2c3__SKILL.md |
| sickn33/antigravity-awesome-skills | stripe-integration | stripe-integration__dfc08473a1__SKILL.md |
| wshobson/agents | stripe-integration | stripe-integration__2f11b16ab3__SKILL.md |

这些文件可能是下载时包含但未通过科研相关性筛选的 skills（interactive-portfolio、pc-games、stripe-integration 确实与科研无关）。

## Fork 重复统计

以下 4 个仓库是 sickn33/antigravity-awesome-skills 的 fork，包含完全相同的 skill 内容：
- ForaeFactory/antigravity-skills (3 skills)
- hangoclong/skills-antigravity-awesome (3 skills)
- huysynf/antigravity-awesome-skills (3 skills)
- sickn33/antigravity-awesome-skills (3 skills, 原始仓库)

去重后，这 12 个条目实际代表 3 个唯一 skill（File Path Traversal Testing, personal-tool-builder, verification-before-completion）。

## 审核总结

| 指标 | 数值 |
|------|------|
| 主题文档声称 skill 数 | 107 |
| 实际 skill 条目数 | 60 |
| 去重后唯一 skill 数 | ~48 (去除 fork 重复后) |
| URL 全部有效 | 10/10 仓库 |
| 科研相关性需修正 | 10 个 skill (去重后 5 个唯一 skill) |
| 功能描述需修正 | 全部 60 个 (模板化截断) |
| 建议移除（非科研） | 8 个条目 (去重后 4 个唯一 skill) |
| 建议保留 | 52 个条目 (去重后 ~44 个唯一 skill) |

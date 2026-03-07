# Research Skills Audit Prompt

> 用途：将此提示词发给 Claude Code Agent，让它对新的 GitHub 仓库列表执行科研技能审计，
> 产出与 `Final_Research_Skills_Thematic_Split/01_*.md` 系列文件完全相同格式的报告。

---

## System / 角色设定

你是一名科研软件工具审计员。你的任务是：系统性地遍历指定的 GitHub 仓库，
从中提取与"广义科学研究"相关的 Skills（技能），并以规定的 Markdown 格式输出审计报告。

---

## Task / 任务描述

请对以下 GitHub 仓库列表执行科研技能审计：

```
<!-- 替换为你的仓库列表，每行一个，格式：owner/repo -->
owner1/repo1
owner2/repo2
owner3/repo3
```

**执行步骤：**

### Step 1 — 仓库可访问性检查

对列表中的每个仓库执行以下操作：

1. 访问 `https://api.github.com/repos/{owner}/{repo}` 确认仓库存在（HTTP 200 = 可访问，404 = 不可访问）。
2. 获取仓库默认分支（`default_branch` 字段）。
3. 记录不可访问的仓库，跳过后续步骤。

### Step 2 — 文件树遍历，定位所有 SKILL.md

对每个可访问的仓库：

1. 访问 `https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1` 获取完整文件树。
2. 在返回的 `tree` 数组中，筛选出 `path` 以 `SKILL.md`（大小写不敏感）结尾的所有文件条目。
3. 构造每个文件的 raw 内容 URL：
   `https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}`
4. 下载并读取每个 `SKILL.md` 的内容。

### Step 3 — 科研相关性过滤

对每个读取到的 `SKILL.md`，按以下 **4步逻辑** 判断是否纳入报告：

**Step 3.1 — 提取动作**：这个技能实际执行什么操作？（阅读文件的 `description`、功能说明、trigger 条件）

**Step 3.2 — 识别领域**：它属于哪个应用领域？

**Step 3.3 — 判定动机**：核心驱动力是下列哪一类？

| 类别 | 判定 |
|---|---|
| 信息检索、证据收集、文献搜索、数据库查询 | ✅ 纳入 |
| 文献综述、学术写作、论文引用、研究笔记 | ✅ 纳入 |
| 实验设计、基准测试、可复现性、结果验证 | ✅ 纳入 |
| 数据分析、统计推断、可视化、证据解读 | ✅ 纳入 |
| 科研工作流、研究自动化、工具集成（服务于研究） | ✅ 纳入 |
| 网络安全攻防、渗透测试（有明确研究/教学背景） | ✅ 纳入 |
| 通用软件工程（代码生成、调试、重构、架构） | ✅ 纳入（CS 工程研究） |
| 商业 SEO / 营销文案 / 广告获客 | ❌ 剔除 |
| 企业战略 / 高管咨询 / 销售流程 | ❌ 剔除 |
| 个人购物 / 约会社交 / 娱乐消费 | ❌ 剔除 |
| 纯商业自动化（发票处理、会计对账、ERP） | ❌ 剔除 |
| 纯视觉艺术 / 游戏美术（无工程研究属性） | ❌ 剔除 |

**Step 3.4 — 得出结论**：如果动机属于 ✅ 类，纳入；否则跳过。

### Step 4 — 填写 7 列审计表

对每个通过过滤的技能，填写以下 7 列，**所有内容必须从源文件中提取，禁止编造**：

| 列名 | 填写规则 |
|---|---|
| **Skill** | 技能目录名称（`SKILL.md` 所在目录的最后一级名称，通常与 frontmatter `name:` 字段一致） |
| **Evidence File** | `SKILL.md` 在仓库中的相对路径（如 `.claude/skills/foo/SKILL.md`）；必须来自 GitHub API 文件树，不得使用本地缓存文件名 |
| **Skill URL** | `[link](https://github.com/{owner}/{repo}/blob/{branch}/{path})` |
| **Why Research-Related** | 1 句话；直接从源文件的 `description:`、`When to use`、触发条件段落摘取或改写；说明为何与科研相关 |
| **Function Explanation (2-3 sentences)** | 2-3 句完整的功能说明；优先使用源文件 `description:` 字段或开头段落的原文 |
| **Execution Flow** | 步骤用 ` -> ` 连接（例：`Step A -> Step B -> Step C`）；只写源文件明确列出的步骤，不推断 |
| **Evidence** | 从源文件摘取的原文引用；两种可接受格式均可：① `description: 内容原文`（带前缀） ② 直接复制 frontmatter description 内容（不带前缀）；两种格式在同一份文档中可以混用 |

### Step 5 — 组织输出格式

输出一份完整的 Markdown 报告，**严格遵守以下结构**：

```markdown
# Research Skills Audit Report

- Generated at: {YYYY-MM-DD HH:MM:SS}
- Source repos: {仓库数量} repositories
- Mentioned GitHub projects (deduped): {数量}
- Accessible and traversed projects: {数量}
- Inaccessible projects (latest check): {数量}
- Extracted research-related skills (deduped): {数量}

## Scope and Method

1. Traverse all GitHub repositories listed in the current research audit scope.
2. For each accessible repository, scan the full repository tree and inspect each `SKILL.md`.
3. Extract research-related skills using keyword + repository-context filtering.
4. For each extracted skill, add a 2-3 sentence function explanation and a full flow in `Step1 → Step2 → Step3 ...` format.

## Inaccessible Projects (Latest Check)

- `owner/repo` - **Repository not found (404).**

## Audit Summary

| Metric | Value |
|---|---:|
| Mentioned projects | {N} |
| Traversed projects | {N} |
| Inaccessible projects | {N} |
| Research-related skills | {N} |
| Projects containing research skills | {N} |

## Top Repositories by Research Skill Count

| Repository | Skills | Tree Files | SKILL.md Files |
|---|---:|---:|---:|
| `owner/repo` | {N} | {N} | {N} |

## Theme

- Current theme: **{主题名称}**
- Split basis: original `Why Research-Related` values + fallback keyword matching.
- Skill count in this file: **{N}**

## Extracted Research Skills (Thematic Subset)

### owner/repo

| Skill | Evidence File | Skill URL | Why Research-Related | Function Explanation (2-3 sentences) | Execution Flow| Evidence |
|---|---|---|---|---|---|---|
| {skill-name} | `{path/to/SKILL.md}` | [link]({github URL}) | {1 sentence} | {2-3 sentences} | {Step A -> Step B -> Step C} | {exact quote} |
```

**格式规则：**
- 每个仓库对应一个 `### owner/repo` 三级标题
- 每个仓库下只有一张 7 列表格（表头 + 分隔行 + 数据行）
- 如果一个仓库没有通过过滤的技能，则整个仓库部分省略（不输出空表）
- `Top Repositories` 表按技能数量降序排列
- 如果不需要主题分割（输出全量），`## Theme` 部分可省略

---

## Quality Rules / 质量规则

1. **提取优先**：所有描述内容必须从 `SKILL.md` 源文件中提取，严禁根据技能名称推断或编造功能描述。
2. **禁止通用措辞**：除非源文件中明确出现，否则不得使用 "cross-verification"、"structured insights"、"evidence collection" 等泛化短语。
3. **Execution Flow 格式**：步骤之间统一使用 ` -> `（空格箭头空格），不使用 `→` 或 `\n` 换行。
4. **Evidence 字段**：优先使用 `description: "..."` 格式的原文引用；若无 description 字段，摘取最能证明功能的完整句子（不超过 2 句）。
5. **去重**：如果同一个技能名称在多个仓库中出现相同路径，保留每个仓库各自的条目，不合并。
6. **表格管道符转义**：如果 Evidence 或其他字段中包含 `|`，必须转义为 `\|`。

---

## Theme Mapping / 主题映射（可选）

如果需要将技能按主题分文件输出，请按以下规则分类：

| 主题编号 | 主题名称 | 关键词信号（参考，非硬性规则） |
|---|---|---|
| 01 | Information Retrieval and Evidence Collection | search, retrieval, fetch, crawl, query, pubmed, arxiv, web search, OSINT, reconnaissance, **GPU cloud, compute infrastructure, distributed training, model serving**（注：ML 实验基础设施也归此类，因其支撑了研究证据的采集过程） |
| 02 | Literature Review, Writing, and Citation | paper, citation, reference, bibliography, latex, abstract, academic writing, summarize |
| 03 | Experiment Design, Benchmarking, Reproducibility, and Validation | benchmark, experiment, reproduce, validate, test, evaluation, metric, ablation, fine-tuning, model training |
| 04 | Data Analysis and Evidence Interpretation | data analysis, statistics, visualization, pandas, SQL, notebook, interpret, insight |
| 05 | Research Operations and Workflow Support | workflow, automation, pipeline, task management, research assistant, orchestration |

**分类优先级（重要）：**
1. 首先读取技能的 `Why Research-Related` 原文，理解其研究用途语义
2. 若描述中有明确研究阶段词汇，直接按上表分类
3. **若技能是 ML 基础设施工具（GPU 平台、分布式训练框架、模型部署、云计算）但没有明确关键词**，归入 01（因这类工具是研究人员"获取实验证据"的计算手段）
4. 关键词匹配仅作回退参考，不得覆盖语义判断

一个技能只归属于一个主题。

---

## Example Output Row / 输出示例行

```markdown
| semantic-search | `.claude/skills/semantic-search/SKILL.md` | [link](https://github.com/ahmedibrahim085/Claude-Multi-Agent-Research-System-Skill/blob/main/.claude/skills/semantic-search/SKILL.md) | Use for understanding unfamiliar codebases, finding similar implementations, or locating functionality by description rather than exact keywords. | Semantic search for finding code by meaning using natural language queries. This skill orchestrates two specialized agents: semantic-search-reader and semantic-search-indexer. Unlike traditional text-based search, it understands the meaning of content, finding functionally similar text even when using different wording. | Spawn appropriate agent via Task tool -> semantic-search-reader handles READ operations -> semantic-search-indexer handles WRITE operations -> Wait for agent completion | Semantic search for finding code by meaning using natural language queries. Orchestrates semantic-search-reader (search/find-similar/list-projects) and semantic-search-indexer (index/reindex/status) agents. |
```

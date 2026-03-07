# 跨平台兼容性分析：Skills 在 OpenClaw / IronClaw 等平台的可用性

> 本仓库包含 **2,062 个 SKILL.md 文件**（磁盘）、**1,408 个已审计条目**（multidim_audit.json）、**1,367 个已入目录**（SKILL_CATALOG.md）。它们能否用于 OpenClaw、IronClaw、OpenAI Codex CLI 等采用同一开放标准的平台？

## 结论

**格式兼容，约 90% 的 skills 可直接使用。但目录结构不兼容，需要部署脚本转换。**

Claude Code、OpenClaw 和 OpenAI Codex CLI 均采用 Anthropic 于 2025 年 12 月发布的 **Agent Skills 开放标准**——以 YAML frontmatter + Markdown 正文构成的 `SKILL.md` 文件。本仓库的 skills 天然符合该标准。但本仓库使用深度嵌套的主题/仓库目录结构，而 OpenClaw 期望扁平的 `~/.openclaw/skills/<skill-name>/SKILL.md` 布局。

**现已提供 `deploy_skills.py` 脚本**，可一键生成两套部署目录（OpenClaw + IronClaw）。

## 格式兼容性

两者共享同一核心格式：

```yaml
---
name: skill-name        # 通用必填字段
description: ...        # 通用必填字段
---
# Markdown 指令正文（agent 读取后执行）
```

本仓库 2,062 个 SKILL.md 文件的 frontmatter 字段分布：

| 字段 | 数量 | 占比 | 兼容性 |
|------|-----:|-----:|--------|
| `name` | 2,055 | 99.7% | 通用标准字段 |
| `description` | 2,060 | 99.9% | 通用标准字段 |
| `license` | 551 | 26.7% | 通用标准字段 |
| `metadata` | 409 | 19.8% | 通用容器 |
| `tool_type` | 425 | 20.6% | 通用扩展字段 |
| `allowed-tools` | 134 | 6.5% | Claude Code 专属（OpenClaw 会忽略） |
| `user-invocable` | 10 | 0.5% | Claude Code 专属（OpenClaw 会忽略） |
| `metadata.openclaw` | 1 | ~0% | OpenClaw 专属 |

**约 93% 的 skills 在 frontmatter 层面无任何平台特定字段。**

## 内容可用性：三个梯度

### 直接可用（约 90%，~1,250 skills）

大部分 skills 的正文是**通用的领域知识和操作指南**——Python 代码、bash 命令、工具使用说明——不依赖任何特定平台的工具系统。例如：

- `bio-genome-assembly-short-read-assembly`：SPAdes 基因组组装指令
- `aeon`：时间序列机器学习 (scikit-learn 兼容)
- `pdf`：pypdf / pdfplumber / reportlab 操作指南
- `perplexity-search`：通过 LiteLLM 调用 Perplexity API

这些 skill 本质上是**可执行的知识卡片**，任何 LLM agent 读到后都能理解并执行。

### 需要小幅适配（约 7%，~134 skills）

使用了 `allowed-tools: Bash, Read, Glob, Grep` 等 Claude Code 专属 frontmatter 字段。OpenClaw 会忽略这些未知字段（不报错），skill 仍可加载使用，只是缺少工具级安全门控。

### 需要重写（约 2%，~28 skills）

正文中深度耦合了 Claude Code 的子代理架构，引用了 `Task(subagent_type=...)` 等 Claude Code 专属 API。这类 skill 需要重写为 OpenClaw 的工具调用方式才能使用。

## 目录结构不兼容（核心问题）

| 维度 | 本仓库 | OpenClaw 期望 |
|------|--------|--------------|
| 路径深度 | `Final_.../01_theme/.../owner__repo/.../skill-name/SKILL.md` | `~/.openclaw/skills/<skill-name>/SKILL.md` |
| 目录布局 | 深度嵌套（按主题/仓库分层） | 扁平（按技能名一级） |
| 技能名重复 | 92 组同名技能（来自不同仓库） | 目录名必须唯一 |

### 名称冲突处理策略

1,408 个已审计条目中的唯一性分布：

| 唯一性 | 数量 | 部署目录名策略 |
|--------|------|----------------|
| **original** | 915 | 使用 `skill-name` |
| **canonical** | 353 | 使用 `skill-name`（同名组中选定的代表版本） |
| **variant** | 140 | 使用 `{repo-name}-{skill-name}`（仅用仓库名，不含 owner） |

### 名称规范化（Name Normalization）

Agent Skills 规范要求 `name` 字段仅含 `[a-z0-9-]`，不能以 hyphen 开头/结尾，不能含连续 hyphen，最长 64 字符。`deploy_skills.py` 自动执行规范化：

| 问题 | 数量 | 处理方式 |
|------|------|---------|
| 已合规的 kebab 名 | ~1,191 (86%) | 不变 |
| 大写/空格→kebab | ~75 (5%) | 小写化 + 空格→hyphen + `metadata.original_name` 保留原名 |
| variant 前缀 | ~140 (10%) | `{repo-name}-{skill-name}` 全 kebab + `metadata.original_name` |
| 碰撞（同名 repo 的不同 fork） | 12 | 回退为 `{owner}-{repo-name}-{skill-name}` |
| 超 64 字符 | ≤1 | 在 hyphen 处截断 + 完整名存入 `metadata.original_name` |

所有部署的 SKILL.md 在 frontmatter 中包含 `metadata` 单行 JSON，至少包含 `source_repo`，被规范化的还包含 `original_name`：

```yaml
metadata: {"source_repo": "anthropics/claude-code", "original_name": "Agent Development"}
```

## 部署脚本 `deploy_skills.py`

一键生成 OpenClaw 和 IronClaw 部署目录：

```bash
# 默认：生成两套输出
python deploy_skills.py

# 仅 OpenClaw
python deploy_skills.py --target openclaw

# 仅 IronClaw
python deploy_skills.py --target ironclaw

# 预览不写入
python deploy_skills.py --dry-run

# 仅部署指定 tier
python deploy_skills.py --tier A,B
```

### OpenClaw 输出 (`openclaw_deploy/`)

- 扁平目录结构：`openclaw_deploy/<skill-name>/SKILL.md`
- 直接复制到 `~/.openclaw/skills/` 即可使用
- variant 技能自动添加仓库前缀避免冲突

### IronClaw 输出 (`ironclaw_deploy/`)

- 扁平目录结构：`ironclaw_deploy/<skill-name>/SKILL.md`
- IronClaw 使用与 OpenClaw 相同的 SKILL.md 格式，但扩展了 `activation` 块用于智能技能选择
- `deploy_skills.py` 自动为每个 skill 生成 `activation` 字段：

```yaml
---
name: pdf
description: Comprehensive PDF manipulation toolkit...
activation:
  keywords: ["pdf", "extract", "merge", "split"]
  tags: ["data-science"]
  max_context_tokens: 2410
---
```

- `keywords`: 从描述中自动提取的关键词，IronClaw 用于上下文匹配
- `tags`: 从审计数据的 domain 字段映射而来
- `max_context_tokens`: 基于文件大小估算的上下文预算

**注意**：IronClaw 的 `.capabilities.json` 是用于 WASM 工具/频道的权限声明系统（HTTP 白名单、凭证注入等），与 SKILL.md 完全独立。Skills 不需要也不使用 capability manifest。

### 部署报告 (`deploy_report.json`)

每次运行后自动生成，包含部署统计、冲突解决和错误列表。

## IronClaw 兼容性

IronClaw（NEAR AI，Rust 实现）采用与 OpenClaw 相同的 SKILL.md 格式，但在 frontmatter 中扩展了 `activation` 块用于智能技能选择。

| 差异点 | OpenClaw / Claude Code | IronClaw |
|--------|----------------------|----------|
| 运行时 | Node.js / Python | Rust（安全沙箱） |
| SKILL.md 格式 | 标准 frontmatter | 标准 frontmatter + `activation` 扩展 |
| 技能选择 | 用户显式调用 | `activation` 关键词/标签自动匹配 |
| 信任模型 | 隐式信任 | Trusted / Installed 分级 |

`deploy_skills.py` 为 IronClaw 输出自动生成 `activation` 块（keywords、tags、max_context_tokens），无需手动编写。

## 其他兼容平台

由于 Agent Skills 开放标准已被广泛采纳，本仓库的 skills 同样适用于：

| 平台 | 状态 |
|------|------|
| **Claude Code** | 原生支持（本仓库的原始目标平台） |
| **OpenClaw** | 格式兼容，需 `deploy_skills.py` 做目录结构转换 |
| **IronClaw** | 格式兼容，`deploy_skills.py` 自动生成 `activation` 扩展块 |
| **OpenAI Codex CLI** | 已采纳同一标准，格式兼容 |
| **LobeHub Skills Marketplace** | 可发布 |
| **Playbooks.com** | 可索引 |

## 参考资料

- [OpenClaw 官网](https://openclaw.ai/)
- [OpenClaw Skills 文档](https://docs.openclaw.ai/tools/skills)
- [ClawHub Skill 格式规范](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)
- [awesome-openclaw-skills（5,400+ 精选）](https://github.com/VoltAgent/awesome-openclaw-skills)
- [跨平台 skills 仓库（Claude Code + Codex + OpenClaw）](https://github.com/alirezarezvani/claude-skills)
- [Anthropic Skills 开放标准](https://github.com/anthropics/skills)

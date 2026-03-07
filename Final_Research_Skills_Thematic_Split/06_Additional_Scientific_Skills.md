<!--
 * [IN]  本地克隆仓库（.tmp_skill_repos/）+ PROMPT_research_skills_audit.md（本地模式 v2.0）
 * [OUT] 全量科研 Skills 审计报告，按 5 主题分节
 * [POS] 只读参考文档；由审计 Agent 生成，不得手动编辑数据行
 *
 * 变更警告: 本文件由自动化审计流程生成；如需更正请重新运行审计，不得手动编辑数据行。
-->

# Research Skills Audit Report — Full

- Generated at: 2026-02-24
- Repos covered: 8 (complete)
- Total SKILL.md files scanned: 32 + 37 + 15 + 14 + 18 + 38 + 146 = 300
- Total research-related skills extracted: 18 + 10 + 15 + 14 + 18 + 38 + 145 = 258

> **Status**: Galaxy-Dawn/claude-scholar ✅ + anthropics/skills+community ✅ + Orchestra O-1 ✅ + Orchestra O-2 ✅ + Orchestra O-3 ✅ + Orchestra O-4 ✅ + K-Dense ✅ | ALL REPOS COMPLETE

## Scope and Method

1. Read local clones in `.tmp_skill_repos/` using Glob + Read tools (no network requests).
2. For each SKILL.md, apply 4-step research relevance filter (see `PROMPT_research_skills_audit.md` v2.0).
3. Fill 7-column audit table from source text only (no inference).
4. Organize by theme (01–05) per Theme Mapping in PROMPT.

## Skipped / Inaccessible Repos

（待全量运行完成后更新）

## Audit Summary

| Metric | Value |
|---|---:|
| Repos covered (pilot) | 1 |
| SKILL.md files scanned (pilot) | 32 |
| Research-related skills (pilot) | 18 |
| Skills excluded / non-research (pilot) | 14 |
| Repos with ≥1 research skill (pilot) | 1 |

## Top Repositories by Research Skill Count

| Repository | Skills | SKILL.md Files |
|---|---:|---:|
| `Galaxy-Dawn/claude-scholar` | 18 | 32 |

## Excluded Skills（被剔除的技能 — Galaxy-Dawn/claude-scholar）

| Skill | 剔除原因 |
|---|---|
| `agent-identifier` | 专注于 Claude Code 插件 Agent 开发规范，属于纯插件开发工具，无科研内容 |
| `command-development` | 专注于 Claude Code 斜杠命令开发（YAML frontmatter、动态参数），属于纯插件开发工具 |
| `command-name` | 专注于 Claude Code 插件目录结构与 manifest 配置，属于纯插件架构文档 |
| `daily-coding` | 通用编码质量检查清单（type safety、security check、cleanup），无科研特异性 |
| `frontend-design` | 专注于生产级前端界面视觉设计（50+ 美学风格），属于纯 UI/商业设计领域 |
| `hook-development` | 专注于 Claude Code 插件事件驱动 Hook 开发（PreToolUse/PostToolUse/Stop），属于纯插件开发工具 |
| `mcp-integration` | 专注于 Model Context Protocol 服务器配置（stdio/SSE/HTTP/WebSocket），属于纯插件集成工具 |
| `planning-with-files` | 通用任务规划与进度跟踪（Manus 风格 Markdown 文件），不具备科研特异性 |
| `skill-development` | 专注于 Claude Code 插件 SKILL.md 文件创作指南，属于纯插件开发元工具 |
| `skill-improver` | 执行 skill-quality-reviewer 改进计划，属于纯技能 QA 工具 |
| `skill-quality-reviewer` | 评估 Claude Skills 质量（描述、组织、写作风格、结构），属于纯技能 QA 元工具 |
| `ui-ux-pro-max` | 提供 50+ 风格、97 调色板的 UI/UX 设计系统，属于纯 Web 设计工具 |
| `web-design-reviewer` | 使用浏览器自动化对网站进行可视化检查，属于纯 Web 设计 QA 工具 |
| `webapp-testing` | 基于 Playwright 的本地 Web 应用测试工具包，属于纯 Web 测试工具 |

---

## 01 — Information Retrieval and Evidence Collection





---

## 02 — Literature Review, Writing, and Citation







---

## 03 — Experiment Design, Benchmarking, Reproducibility, and Validation






---

## 04 — Data Analysis and Evidence Interpretation





---

## 05 — Research Operations and Workflow Support





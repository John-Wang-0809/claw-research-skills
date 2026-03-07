# Prompt: 修复 remaining_issues_for_review.md 中的 141 个剩余问题

## 你的任务

你需要修复 `remaining_issues_for_review.md` 中记录的 141 个技能描述问题。这些技能的 Function Explanation 在 LLM 审计中被判定为 partial/inaccurate/cannot_verify，需要逐个修正后写回主题文档。

## 问题分布

| 问题类型 | 数量 | 说明 |
|----------|------|------|
| HALLUCINATION | 76 | 描述中包含 SKILL.md 未支持的断言 |
| OTHER | 35 | 审计原因不明确或边缘情况 |
| MISSING | 22 | 描述遗漏了 SKILL.md 中的关键功能 |
| HALLUCINATION + MISSING | 8 | 既有虚构内容又遗漏了关键功能 |
| **小计 (partial + inaccurate)** | **135** | 需要修正描述 |
| CANNOT_VERIFY | 6 | 本地缺少 SKILL.md，无法验证 |

## 关键文件（必读）

### 输入文件
1. **`remaining_issues_for_review.md`** — 141 个待修复技能的完整清单，每个包含：
   - 技能名称、所属仓库、主题
   - Issue Type（HALLUCINATION / MISSING / OTHER / HALLUCINATION + MISSING）
   - Audit Reason（审计器给出的具体问题描述）
   - Current Function Explanation（当前需修正的文本）
   - SKILL.md 本地路径（证据文件位置）

2. **本地 SKILL.md 文件** — 位于 `Final_Research_Skills_Link_Downloads_By_Theme_LATEST/` 下，按主题/仓库组织。每个技能条目的 `SKILL.md` 字段给出了完整路径。这是**修正的唯一依据**。

3. **8 个主题文档**（修正的目标文件） — 位于 `Final_Research_Skills_Thematic_Split/`：
   - `01_information_retrieval_evidence_collection.md`
   - `02_literature_review_writing_citation_part1.md`
   - `02_literature_review_writing_citation_part2.md`
   - `03_experiment_benchmark_reproducibility_validation_part1.md`
   - `03_experiment_benchmark_reproducibility_validation_part2.md`
   - `04_data_analysis_and_evidence_interpretation.md`
   - `05_research_operations_and_workflow_support.md`
   - `06_Additional_Scientific_Skills.md`

### 参考文件（理解上下文）
4. **`fix_prompt_problems_analysis.md`** — 之前修复轮次的根因分析，记录了 5 个已知问题（截断、信息输入不足、审计标准模糊等）。**务必阅读**，避免重蹈覆辙。
5. **`analysis.md`** — Fix vs Audit 的差异分析，解释了为什么之前 69% 的修复仍被判为 partial。
6. **`audit_results.json`** — 完整审计结果（2,074 行），包含每个技能的 `function_accuracy`、`function_accuracy_reason`、`research_relevance`、`issues` 等字段。
7. **`fix_report.json`** — 之前修复轮次的记录（哪些技能被修过、修成了什么）。

### 相关脚本（可参考或复用）
8. **`fix_descriptions.py`** — 已有的 LLM 批量修复脚本。关键设计：
   - 按问题分类：A 类（仅 func 有问题）、B 类（仅 relevance 有问题）、C 类（两者都有）
   - 自动检测修复策略：`REMOVE_HALLUCINATION` / `ADD_MISSING` / `REMOVE_AND_ADD` / `GENERAL_FIX`
   - System Prompt 强调 **最小编辑**（不重写，只改审计标记的部分）
   - 支持断点续传（`fix_checkpoint.json`）和并发（`--concurrency`）
   - 配置：API `https://yunwu.ai/v1`，模型 `gpt-5.2`，SKILL.md 截断限制 8000 字符

9. **`audit_all_skills.py`** — LLM 审计脚本。关键设计：
   - System Prompt 中的审计标准（`audit_all_skills.py` 第 65-93 行）：
     - `accurate`：正确捕获主要目的和关键能力
     - `partial`：遗漏主要能力，或引入 SKILL.md 未支持的断言
     - `inaccurate`：从根本上曲解了技能功能
   - 明确定义 "key details" = PRIMARY PURPOSE + MAJOR CAPABILITIES（前 1-3 项），次要特性不算
   - 提供了 accurate / partial 的具体示例

10. **`apply_audit_corrections_to_theme.py`** — 将修正文本写回主题文档的脚本（处理 markdown 表格行内替换、escaped-pipe 等边缘情况）。

## 修复策略

### 对于 135 个 partial/inaccurate 技能

按 Issue Type 采用不同策略：

**HALLUCINATION（76 个）—— 删除虚构内容**
1. 读取对应 SKILL.md（路径在 `remaining_issues_for_review.md` 中给出）
2. 对照 Audit Reason，找到 Function Explanation 中**不被 SKILL.md 支持的具体断言**
3. 删除或弱化这些断言（如将 "automatically does X" 改为 "supports X"，或直接删除）
4. **不要添加新内容**，不要重写其余正确部分

**MISSING（22 个）—— 补充遗漏的关键功能**
1. 读取 SKILL.md，找到 Audit Reason 提到的**被遗漏的主要功能**
2. 在现有 Function Explanation 末尾**追加 1 句话**描述该功能
3. 不修改现有正确内容

**HALLUCINATION + MISSING（8 个）—— 先删后补**
1. 先执行 HALLUCINATION 策略删除虚构内容
2. 再执行 MISSING 策略补充遗漏功能

**OTHER（35 个）—— 根据 Audit Reason 判断**
1. 仔细阅读 Audit Reason 和 Issues 字段
2. 大部分是措辞过于绝对（"comprehensive"、"automatic"）或细节粒度问题
3. 做最小修改使描述与 SKILL.md 一致

### 对于 6 个 cannot_verify 技能

这 6 个全部来自 `ComposioHQ/awesome-claude-skills` 仓库，本地缺少 SKILL.md。处理方式：
1. 尝试从 GitHub 下载对应 SKILL.md（URL 在条目中给出）
2. 如果 URL 有效：下载后按正常流程修正
3. 如果 URL 404：在技能条目旁标注 `[cannot_verify: SKILL.md not found]`，不做修改

## 修正原则（从历史教训中总结）

1. **最小编辑**：只改审计标记的部分，不重写整段。改得越少越好。
2. **每个断言必须可追溯到 SKILL.md**：如果 SKILL.md 含糊，你的描述也应含糊。绝不用猜测填充空白。
3. **不追求面面俱到**：Function Explanation 是高层次摘要（2-5 句话），只需覆盖主要目的 + 关键功能（前 1-3 项）。次要特性、版本号、代码示例、实现细节可以省略。
4. **确保句子完整**：描述必须以完整句子结束，不能截断。
5. **不使用 pipe 字符 `|`**：因为主题文档是 markdown 表格，`|` 会破坏表格结构。
6. **不使用营销语言**：避免 "comprehensive"、"powerful"、"advanced" 等空洞修饰语，除非 SKILL.md 原文确实如此表述。

## 执行方式

### 方式 A：使用现有脚本（推荐大批量）

可以修改 `fix_descriptions.py` 使其只处理 `remaining_issues_for_review.md` 中的 141 个技能：
1. 从 `remaining_issues_for_review.md` 解析出 141 个技能的 skill_name + repo + theme
2. 从 `audit_results.json` 提取这些技能的完整审计数据
3. 复用 `fix_descriptions.py` 的 API 调用逻辑和修复策略检测
4. 修复后运行 `audit_all_skills.py`（可以 `--filter` 只审计这 141 个）验证效果

### 方式 B：手动逐个修复（推荐高质量）

对于每个技能：
1. 读取 SKILL.md 原文
2. 对照 Audit Reason 理解具体问题
3. 手动编辑 Function Explanation
4. 直接在主题文档（`Final_Research_Skills_Thematic_Split/0*.md`）中找到对应表格行，替换 Function Explanation 列

### 方式 C：混合方式（推荐）

1. 先用脚本批量处理 HALLUCINATION 类（76 个）——规则明确，适合自动化
2. 再手动处理 OTHER 和 MISSING 类（57 个）——需要人工判断
3. 最后单独处理 cannot_verify 类（6 个）——需要网络访问

## 验证

修复完成后，必须运行审计验证：

```bash
# 只审计修复过的技能（从 fix_report.json 获取 row_id 列表）
python audit_all_skills.py --concurrency 5
```

目标：
- 141 个技能中 ≥ 120 个达到 `function_accuracy = accurate`（≥ 85% 修复率）
- 0 个新增 `inaccurate`
- cannot_verify 数量 ≤ 6（不增加）

验证后更新 `remaining_issues_for_review.md`，移除已修复的条目，保留仍有问题的。

## 产出物清单

1. 修改后的 8 个主题文档（`Final_Research_Skills_Thematic_Split/0*.md`）
2. 更新后的 `remaining_issues_for_review.md`（仅保留未解决项）
3. 新的 `audit_results.json`（重新审计后）
4. 新的 `audit_summary.md`（更新统计数据）
5. 修复报告 `fix_report.json`（记录本轮修复内容）

# AI Research Skills 使用指南

> 如何安装、配置和使用 AI Research Skills

---

## 📑 目录

1. [什么是 Skills](#什么是-skills)
2. [Skills 的工作原理](#skills-的工作原理)
3. [使用方式概览](#使用方式概览)
4. [详细使用方法](#详细使用方法)
5. [实战示例](#实战示例)
6. [常见问题](#常见问题)
7. [最佳实践](#最佳实践)

---

## 什么是 Skills？

### 📚 定义

**Skills** 是一种特殊的指令文件（通常命名为 `SKILL.md`），它告诉 AI 助手（如 Claude）如何执行特定的专业任务。

### 🎯 核心概念

```
Skill = 专业知识 + 工作流程 + 最佳实践

┌─────────────────────────────────────┐
│         SKILL.md 文件                │
├─────────────────────────────────────┤
│ 1. 元数据（名称、描述、触发条件）    │
│ 2. 使用场景（何时使用这个技能）      │
│ 3. 详细指令（如何执行任务）          │
│ 4. 示例代码和模板                   │
│ 5. 参考资源和文档                   │
└─────────────────────────────────────┘
         ↓
    AI 助手读取
         ↓
    自动应用专业知识
```

### 💡 类比理解

```
Skills ≈ AI 的"专业培训课程"

传统方式：
  你: "帮我做文献综述"
  AI: "好的" (可能不知道学术标准)

使用 Skill：
  你: "帮我做文献综述"
  AI: 自动加载 literature-review 技能
      → 知道学术搜索策略
      → 了解引用管理标准
      → 遵循文献综述结构
      → 使用正确的引用格式
```

---

## Skills 的工作原理

### 🔄 工作流程

```
1. 用户请求
   "帮我分析这个数据集"
         ↓
2. 触发条件匹配
   检测到关键词: "分析", "数据集"
         ↓
3. 加载相关 Skill
   exploratory-data-analysis/SKILL.md
         ↓
4. AI 读取技能指令
   - 数据清洗步骤
   - 统计分析方法
   - 可视化最佳实践
         ↓
5. 执行专业化任务
   生成符合标准的分析报告
```

### 📂 Skill 文件结构

```yaml
# 标准 SKILL.md 结构

---
name: literature-review          # 技能名称
description: 执行系统化文献综述    # 简短描述
triggers:                        # 触发条件
  - "literature review"
  - "systematic review"
  - "文献综述"
---

## When to Use This Skill
当用户需要进行学术文献综述时使用...

## Quick Start
1. 确定研究问题
2. 制定搜索策略
3. 筛选文献
...

## Detailed Instructions
### 步骤1: 制定搜索策略
- 确定关键词
- 选择数据库 (PubMed, Google Scholar, etc.)
...

## Examples
[示例代码和输出]

## References
- [相关文档链接]
```

---

## 使用方式概览

### 🎨 五种主要使用方式

| 方式 | 适用场景 | 难度 | 推荐度 |
|------|---------|------|--------|
| **1. Claude Code CLI** | 终端/命令行用户 | ⭐ 简单 | ⭐⭐⭐⭐⭐ |
| **2. NPM 包安装** | JavaScript/Node.js 项目 | ⭐⭐ 中等 | ⭐⭐⭐⭐ |
| **3. 手动下载** | 单个技能试用 | ⭐ 简单 | ⭐⭐⭐ |
| **4. MCP 服务器** | 需要动态加载 | ⭐⭐⭐ 复杂 | ⭐⭐⭐⭐ |
| **5. IDE 集成** | VSCode/Cursor 用户 | ⭐⭐ 中等 | ⭐⭐⭐⭐⭐ |

---

## 详细使用方法

## 方法1: 使用 Claude Code CLI（推荐）

### 📦 安装 Claude Code

```bash
# 如果还没安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 或使用 yarn
yarn global add @anthropic-ai/claude-code
```

### 🚀 基本使用

#### 1.1 安装单个技能

```bash
# 从 GitHub 仓库安装
claude code skills add GPTomics/bioSkills

# 从特定路径安装
claude code skills add K-Dense-AI/claude-scientific-skills/scientific-skills/pubmed-database

# 安装整个技能库
claude code skills add Orchestra-Research/AI-Research-SKILLs
```

#### 1.2 列出已安装的技能

```bash
# 查看所有技能
claude code skills list

# 搜索特定技能
claude code skills search "literature"
```

#### 1.3 使用技能

```bash
# 启动 Claude Code
claude code

# 在对话中，技能会自动激活
# 例如，当你说：
> "帮我做一个文献综述"

# Claude 会自动：
# 1. 检测到 "文献综述" 关键词
# 2. 加载 literature-review 技能
# 3. 按照专业流程执行
```

#### 1.4 管理技能

```bash
# 更新技能
claude code skills update

# 删除技能
claude code skills remove literature-review

# 查看技能详情
claude code skills info literature-review
```

---

## 方法2: 使用 NPM 包安装

### 📦 适用于 JavaScript/Node.js 项目

#### 2.1 Orchestra Research AI Skills

```bash
# 安装完整的 AI 研究技能库
npm install @orchestra-research/ai-research-skills

# 或者使用 npx（无需安装）
npx @orchestra-research/ai-research-skills
```

#### 2.2 按类别安装

```bash
# 安装特定类别的技能
npx @orchestra-research/ai-research-skills install model-architecture
npx @orchestra-research/ai-research-skills install fine-tuning
npx @orchestra-research/ai-research-skills install data-processing

# 安装多个类别
npx @orchestra-research/ai-research-skills install model-architecture,fine-tuning,evaluation
```

#### 2.3 在项目中使用

```javascript
// package.json
{
  "dependencies": {
    "@orchestra-research/ai-research-skills": "^1.0.0"
  },
  "scripts": {
    "install-skills": "npx @orchestra-research/ai-research-skills"
  }
}

// 运行安装
npm run install-skills
```

---

## 方法3: 手动下载和配置

### 📥 适合单个技能试用

#### 3.1 找到技能文件

```bash
# 1. 访问 GitHub 仓库
https://github.com/K-Dense-AI/claude-scientific-skills

# 2. 导航到技能文件夹
scientific-skills/literature-review/

# 3. 下载 SKILL.md 文件
```

#### 3.2 放置到 Claude 配置目录

```bash
# 创建技能目录
mkdir -p ~/.claude/skills/literature-review

# 复制 SKILL.md 文件
cp SKILL.md ~/.claude/skills/literature-review/

# 或者对于项目特定的技能
mkdir -p .claude/skills/literature-review
cp SKILL.md .claude/skills/literature-review/
```

#### 3.3 目录结构

```
~/.claude/                          # 全局 Claude 配置
├── skills/                         # 技能目录
│   ├── literature-review/
│   │   └── SKILL.md
│   ├── data-analysis/
│   │   └── SKILL.md
│   └── experimental-design/
│       └── SKILL.md
└── config.json                     # Claude 配置文件

项目目录/
├── .claude/                        # 项目特定配置
│   └── skills/
│       └── custom-skill/
│           └── SKILL.md
└── your-project-files/
```

---

## 方法4: 使用 MCP 服务器

### 🔌 适合需要动态加载的场景

#### 4.1 安装 MCP 服务器

```bash
# 安装 K-Dense AI Skills MCP
npm install -g @k-dense-ai/claude-skills-mcp

# 或者使用 Python 版本
pip install claude-skills-mcp
```

#### 4.2 配置 MCP 服务器

```json
// ~/.claude/mcp_config.json
{
  "mcpServers": {
    "skills": {
      "command": "claude-skills-mcp",
      "args": ["--skills-dir", "~/.claude/skills"],
      "env": {
        "SKILLS_AUTO_LOAD": "true"
      }
    }
  }
}
```

#### 4.3 使用向量搜索查找技能

```python
# Python 示例
from claude_skills_mcp import SkillsClient

client = SkillsClient()

# 搜索相关技能
results = client.search_skills("literature review")

# 加载技能
skill = client.load_skill("literature-review")

# 使用技能
response = client.execute_with_skill(
    skill_name="literature-review",
    user_input="帮我做系统化文献综述"
)
```

---

## 方法5: IDE 集成（VSCode/Cursor）

### 💻 适合使用 IDE 的开发者

#### 5.1 VSCode 集成

```bash
# 1. 安装 Claude Code 扩展
# 在 VSCode 中搜索 "Claude Code"

# 2. 配置 skills 目录
# 在项目根目录创建 .claude/skills/

# 3. 添加技能文件
.claude/
└── skills/
    ├── python-research/
    │   └── SKILL.md
    └── data-analysis/
        └── SKILL.md
```

#### 5.2 Cursor 集成

```bash
# Cursor 使用 .cursor 目录
.cursor/
└── skills/
    └── your-skill/
        └── SKILL.md

# 在 Cursor 设置中启用 Claude Skills
# Settings > Claude > Enable Skills: ✓
```

#### 5.3 在 IDE 中使用

```
1. 打开项目
2. 技能自动加载
3. 在 AI 助手面板中输入请求
4. Claude 自动选择合适的技能执行

示例：
> "帮我分析这个 Python 代码的性能"
  → 自动加载 python-performance-optimization 技能
  → 执行性能分析
  → 提供优化建议
```

---

## 实战示例

### 🧪 示例1: 使用文献综述技能

#### 场景：你需要做一个 AI 伦理的文献综述

```bash
# 1. 安装技能
claude code skills add K-Dense-AI/claude-scientific-skills/literature-review

# 2. 启动 Claude Code
claude code

# 3. 在对话中使用
```

**对话示例：**

```
你: 我需要做一个关于 AI 伦理的系统化文献综述，重点关注2020-2024年的研究。

Claude（自动加载 literature-review 技能）:
好的，我将帮你进行系统化文献综述。让我们按照标准流程进行：

## 第1步：定义研究问题
- 主题：AI 伦理
- 时间范围：2020-2024
- 研究重点：（请明确具体方向，例如：隐私、公平性、透明度？）

## 第2步：制定搜索策略
推荐数据库：
1. Google Scholar
2. IEEE Xplore
3. PubMed（如涉及医疗AI）
4. arXiv（预印本）

搜索关键词组合：
- "AI ethics" OR "artificial intelligence ethics"
- "algorithmic fairness" OR "AI bias"
- "AI transparency" OR "explainable AI"
- 时间过滤：2020-2024

## 第3步：文献筛选标准
纳入标准：
- 同行评审的期刊文章或会议论文
- 直接讨论AI伦理问题
- 英文文献

排除标准：
- 新闻报道和博客
- 无同行评审的灰色文献
- 非AI领域的伦理研究

要开始搜索吗？
```

---

### 🧪 示例2: 使用数据分析技能

#### 场景：分析一个 CSV 数据文件

```bash
# 1. 安装技能
claude code skills add K-Dense-AI/claude-scientific-skills/exploratory-data-analysis

# 2. 准备数据文件
# 假设你有 data.csv

# 3. 在 Claude Code 中使用
```

**对话示例：**

```
你: 帮我分析这个销售数据 data.csv

Claude（自动加载 exploratory-data-analysis 技能）:
好的，我将对 data.csv 进行探索性数据分析（EDA）。

## 第1步：数据加载和概览
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
df = pd.read_csv('data.csv')

# 基本信息
print("数据形状:", df.shape)
print("\n数据类型:")
print(df.dtypes)
print("\n前5行:")
print(df.head())
```

## 第2步：数据质量检查
```python
# 缺失值分析
print("缺失值统计:")
print(df.isnull().sum())

# 重复值检查
print("\n重复行数:", df.duplicated().sum())

# 描述性统计
print("\n描述性统计:")
print(df.describe())
```

## 第3步：可视化分析
我将创建以下图表：
1. 数值变量的分布图
2. 相关性热图
3. 时间序列趋势（如有时间列）

需要我执行这些代码吗？
```

---

### 🧪 示例3: 使用多个技能组合

#### 场景：从论文到代码实现

```bash
# 1. 安装多个技能
claude code skills add K-Dense-AI/claude-scientific-skills/paper-discovery
claude code skills add issol14/paper2code-skill
claude code skills add K-Dense-AI/claude-scientific-skills/pytorch-lightning

# 2. 工作流程
```

**对话示例：**

```
你: 我想实现论文 "Attention Is All You Need" 中的 Transformer 模型

Claude:
我将帮你完成从论文到代码的全过程：

## 阶段1: 论文理解（使用 paper-discovery 技能）
让我先帮你找到这篇论文并理解核心内容...

[找到论文并提取关键信息]

## 阶段2: 代码实现（使用 paper2code-skill）
基于论文描述，我将实现以下组件：

1. Multi-Head Attention
2. Position-wise Feed-Forward Networks
3. Positional Encoding
4. Encoder & Decoder 层

## 阶段3: 优化实现（使用 pytorch-lightning 技能）
我将使用 PyTorch Lightning 框架来组织代码，提供：
- 清晰的模块结构
- 训练/验证循环
- 日志和检查点

要开始实现吗？
```

---

### 🧪 示例4: 科学计算工作流

#### 场景：蛋白质结构分析

```bash
# 安装生物信息学技能
claude code skills add GPTomics/bioSkills/biopython
claude code skills add K-Dense-AI/claude-scientific-skills/pdb-database
claude code skills add K-Dense-AI/claude-scientific-skills/scientific-visualization

# 使用示例
```

**对话示例：**

```
你: 帮我分析蛋白质 1ABC 的结构特征

Claude（加载多个技能）:
我将进行完整的蛋白质结构分析：

## 第1步：获取结构数据（pdb-database 技能）
```python
from Bio.PDB import PDBList, PDBParser

# 下载 PDB 文件
pdbl = PDBList()
pdbl.retrieve_pdb_file('1ABC', pdir='.', file_format='pdb')

# 解析结构
parser = PDBParser()
structure = parser.get_structure('1ABC', '1abc.pdb')
```

## 第2步：结构分析（biopython 技能）
```python
# 分析二级结构
from Bio.PDB.DSSP import DSSP

# 计算可达表面积
from Bio.PDB.SASA import ShrakeRupley

# 提取原子坐标
for model in structure:
    for chain in model:
        for residue in chain:
            # 分析每个残基
            pass
```

## 第3步：可视化（scientific-visualization 技能）
我将创建：
1. 3D 蛋白质结构图
2. Ramachandran 图
3. 疏水性分布图

需要执行完整分析吗？
```

---

## 常见问题

### ❓ Q1: Skills 会自动激活吗？

**A:** 是的，根据以下机制：

```
1. 关键词匹配
   你说："literature review"
   → 自动加载 literature-review 技能

2. 上下文感知
   你说："帮我分析蛋白质结构"
   → 检测到生物学上下文
   → 加载 biopython 相关技能

3. 文件类型
   你上传 .pdb 文件
   → 自动加载蛋白质结构分析技能

4. 手动指定
   你说："使用 deep-research 技能帮我调查..."
   → 明确加载指定技能
```

---

### ❓ Q2: 如何知道哪个技能被激活了？

**A:** Claude 通常会告诉你：

```
Claude: "我将使用 literature-review 技能来帮你完成系统化文献综述..."

# 或者在详细模式下
Claude: [已加载技能: literature-review, citation-management]
       让我按照学术标准为你执行文献综述...
```

---

### ❓ Q3: 可以同时使用多个技能吗？

**A:** 可以！Skills 可以组合使用：

```
场景：写一篇带数据分析的科学论文

自动加载的技能组合：
1. literature-review（文献综述）
2. exploratory-data-analysis（数据分析）
3. scientific-visualization（科学可视化）
4. citation-management（引用管理）
5. latex-writing（LaTeX 写作）

Claude 会协调这些技能，按需调用。
```

---

### ❓ Q4: Skills 存储在哪里？

**A:** 三个位置：

```
1. 全局配置（所有项目共享）
   ~/.claude/skills/

2. 项目配置（仅当前项目）
   项目目录/.claude/skills/

3. IDE 配置（编辑器特定）
   .cursor/skills/
   .vscode/skills/

优先级：项目 > IDE > 全局
```

---

### ❓ Q5: 如何创建自定义技能？

**A:** 创建 SKILL.md 文件：

```markdown
---
name: my-custom-skill
description: 我的自定义技能描述
triggers:
  - "custom task"
  - "特定关键词"
---

## When to Use
当用户需要 XXX 时使用此技能

## Instructions
1. 步骤1...
2. 步骤2...

## Examples
示例代码和输出
```

然后放到 `~/.claude/skills/my-custom-skill/SKILL.md`

---

### ❓ Q6: Skills 需要付费吗？

**A:** 大部分是免费的：

```
✅ 免费开源
- Orchestra-Research/AI-Research-SKILLs
- K-Dense-AI/claude-scientific-skills
- GPTomics/bioSkills
- 大部分社区技能

💰 部分商业
- 某些企业特定技能
- 高级 MCP 服务器功能

💳 Claude 使用本身
- Claude Pro 订阅（如使用 Claude Code）
- API 使用费（如使用 Claude API）
```

---

### ❓ Q7: Skills 支持哪些语言？

**A:** 主要是英文，但许多支持中文：

```
英文为主：
- 大部分技能的文档是英文
- 但使用时可以用中文对话

中文支持：
- Claude 理解中文触发词
- 可以用中文描述需求
- 输出可以是中文

示例：
你: "帮我做文献综述"（中文）
→ 触发 literature-review 技能（英文文档）
→ 执行任务并输出中文结果
```

---

### ❓ Q8: 如何更新技能？

**A:** 三种方式：

```bash
# 方式1: CLI 更新
claude code skills update

# 方式2: 重新安装
claude code skills remove old-skill
claude code skills add new-skill

# 方式3: Git 更新
cd ~/.claude/skills/repo-name
git pull origin main

# 方式4: NPM 更新
npm update @orchestra-research/ai-research-skills
```

---

## 最佳实践

### ✅ 推荐做法

#### 1. **项目级别组织**

```
推荐结构：
项目/
├── .claude/
│   ├── skills/              # 项目特定技能
│   │   ├── domain-specific/
│   │   └── custom-workflow/
│   ├── hooks/               # 自动化钩子
│   └── config.json          # 项目配置
├── CLAUDE.md                # 项目说明（Claude 会读取）
└── src/
```

#### 2. **技能分类管理**

```bash
~/.claude/skills/
├── research/                # 研究相关
│   ├── literature-review/
│   ├── data-analysis/
│   └── experimental-design/
├── development/             # 开发相关
│   ├── code-review/
│   ├── testing/
│   └── debugging/
└── writing/                 # 写作相关
    ├── technical-writing/
    └── documentation/
```

#### 3. **渐进式使用**

```
阶段1: 新手（1-2周）
- 安装 3-5 个常用技能
- 熟悉基本使用方式
- 观察技能如何被触发

阶段2: 进阶（1-2月）
- 安装专业领域技能包
- 学习技能组合使用
- 自定义简单技能

阶段3: 专家（3月+）
- 创建自定义技能库
- 配置复杂工作流
- 贡献社区技能
```

#### 4. **文档化你的技能使用**

```markdown
# PROJECT_SKILLS.md

## 已安装技能

### 数据分析
- exploratory-data-analysis: 用于初步数据探索
- statistical-modeling: 用于统计建模

### 机器学习
- pytorch-lightning: 用于深度学习训练
- mlflow-tracking: 用于实验追踪

## 常用工作流

### 数据分析工作流
1. 使用 EDA 技能探索数据
2. 使用可视化技能创建图表
3. 使用统计技能进行假设检验
```

---

### ⚠️ 注意事项

#### 1. **避免技能冲突**

```
问题：
两个技能对同一触发词有不同处理

解决：
- 使用更具体的技能名称
- 在技能中明确使用场景
- 必要时手动指定技能
```

#### 2. **控制技能数量**

```
❌ 不推荐：
安装 100+ 个技能

✅ 推荐：
- 全局：10-20 个通用技能
- 项目：5-10 个特定技能
- 按需安装和卸载
```

#### 3. **保持技能更新**

```bash
# 定期更新
# 每月一次
claude code skills update

# 检查过时技能
claude code skills check-updates
```

#### 4. **测试新技能**

```bash
# 在测试项目中先试用
mkdir test-skills && cd test-skills
claude code skills add new-skill

# 测试满意后再添加到主项目
```

---

### 💡 高级技巧

#### 1. **创建技能组合**

```json
// .claude/skill-sets.json
{
  "research-workflow": [
    "literature-review",
    "data-analysis",
    "scientific-visualization",
    "citation-management"
  ],
  "ml-development": [
    "pytorch-lightning",
    "mlflow-tracking",
    "hyperparameter-tuning",
    "model-evaluation"
  ]
}

// 一键加载技能组
claude code skills load-set research-workflow
```

#### 2. **使用技能模板**

```bash
# 创建技能模板
claude code skills template create my-template

# 基于模板创建新技能
claude code skills create --template my-template new-skill
```

#### 3. **技能性能优化**

```yaml
# .claude/config.json
{
  "skills": {
    "caching": true,           # 缓存技能内容
    "lazy_load": true,         # 延迟加载
    "preload": [               # 预加载常用技能
      "literature-review",
      "data-analysis"
    ]
  }
}
```

#### 4. **集成到 CI/CD**

```yaml
# .github/workflows/skills.yml
name: Update Claude Skills

on:
  schedule:
    - cron: '0 0 * * 0'  # 每周更新

jobs:
  update-skills:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Update skills
        run: |
          claude code skills update
          git commit -am "Update Claude skills"
          git push
```

---

## 🎓 学习路径

### 初学者路线（第1周）

```
Day 1-2: 理解 Skills 概念
- 阅读文档
- 了解工作原理

Day 3-4: 安装和配置
- 安装 Claude Code
- 配置第一个技能

Day 5-7: 实践使用
- 尝试 3-5 个基础技能
- 完成简单任务
```

### 进阶路线（第2-4周）

```
Week 2: 专业技能
- 安装领域特定技能
- 学习技能组合

Week 3: 自定义技能
- 创建简单自定义技能
- 修改现有技能

Week 4: 工作流优化
- 配置自动化工作流
- 集成到开发流程
```

### 专家路线（第2-3月）

```
Month 2: 深度定制
- 创建复杂技能库
- 开发 MCP 服务器
- 贡献社区

Month 3: 生态贡献
- 发布自己的技能
- 参与技能开发
- 分享最佳实践
```

---

## 📚 推荐资源

### 官方文档
- [Claude Skills 官方文档](https://docs.anthropic.com/claude/docs/agent-skills)
- [Claude Code 文档](https://docs.anthropic.com/claude/docs/claude-code)

### 技能仓库
- [Orchestra Research AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) - 83个AI研究技能
- [K-Dense AI claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) - 145个科学技能
- [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) - 159个生物信息学技能

### 社区资源
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
- [Claude Skills 讨论区](https://github.com/anthropics/claude-code/discussions)

---

## 🎯 快速参考

### 常用命令速查

```bash
# 安装
claude code skills add <repo>
npm install @orchestra-research/ai-research-skills

# 管理
claude code skills list
claude code skills search <keyword>
claude code skills update
claude code skills remove <skill>

# 使用
claude code                    # 启动，技能自动加载
claude code --skill <name>     # 指定技能启动

# 配置
~/.claude/skills/              # 全局技能目录
.claude/skills/                # 项目技能目录
```

### 触发示例

| 你说的话 | 触发的技能 | 结果 |
|---------|-----------|------|
| "帮我做文献综述" | literature-review | 系统化文献综述流程 |
| "分析这个数据集" | exploratory-data-analysis | 完整的EDA报告 |
| "解释这个算法" | algorithm-explanation | 详细的算法讲解 |
| "写一个单元测试" | testing-best-practices | 测试代码和策略 |
| "优化这段代码" | code-optimization | 性能优化建议 |

---

## 📞 获取帮助

### 遇到问题？

1. **查看文档** - 大部分问题在文档中有答案
2. **搜索 Issues** - GitHub 仓库的 Issues 区
3. **社区讨论** - Discord/Slack 社区
4. **提交 Issue** - 报告 bug 或建议

### 贡献指南

想要贡献自己的技能？
1. Fork 技能仓库
2. 创建新的 SKILL.md
3. 测试技能
4. 提交 Pull Request

---

**最后更新**: 2026-02-13
**版本**: 1.0
**作者**: Claude Code Guide

希望这份指南能帮助你充分利用 AI Research Skills！🚀

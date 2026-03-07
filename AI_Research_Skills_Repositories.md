# AI Research Skills 完整仓库汇总

> 这是一个全面的 AI 研究相关技能仓库列表，涵盖从基础研究到生产部署的完整流程。
>
> **统计数据：**
> - 📦 **100+ 个专门仓库**
> - 🎯 **2,000+ 个可用技能**
> - 📂 **22 个主要类别**
> - 🔄 **最后更新：** 2026-02-13

---

## 📑 目录

1. [综合 AI 研究技能库](#1-综合-ai-研究技能库)
2. [科学研究专用技能](#2-科学研究专用技能)
3. [数据科学与分析](#3-数据科学与分析)
4. [机器学习框架与工具](#4-机器学习框架与工具)
5. [Agent 框架与工具](#5-agent-框架与工具)
6. [学术写作与研究自动化](#6-学术写作与研究自动化)
7. [Web 开发技能](#7-web-开发技能)
8. [DevOps 与云计算](#8-devops-与云计算)
9. [数据库与后端](#9-数据库与后端)
10. [测试与 QA](#10-测试与-qa)
11. [官方技能仓库](#11-官方技能仓库)
12. [编程语言特定技能](#12-编程语言特定技能)
13. [网络安全](#13-网络安全)
14. [移动开发](#14-移动开发)
15. [区块链与 Web3](#15-区块链与-web3)
16. [游戏开发](#16-游戏开发)
17. [MCP 服务器](#17-mcp-服务器)
18. [自动化与工作流](#18-自动化与工作流)
19. [社区技能集合](#19-社区技能集合)
20. [基准测试与评估](#20-基准测试与评估)
21. [AI 编码助手](#21-ai-编码助手)
22. [其他专业领域](#22-其他专业领域)

---

## 1. 综合 AI 研究技能库

### 🌟 主要综合技能库

#### [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)
- **技能数量：** 83+
- **描述：** 最全面的开源 AI 研究和工程技能库，适用于任何 AI 模型
- **覆盖范围：** 完整的 AI 研究生命周期，从模型架构到部署
- **分类：** 20 个类别
  - 模型架构
  - 分词 (Tokenization)
  - 微调 (Fine-tuning)
  - 机械可解释性 (Mechanistic Interpretability)
  - 数据处理
  - 后训练 (Post-training)
  - 分布式训练
  - 优化
  - 评估
  - 推理
  - 基础设施
  - 代理 (Agents)
  - RAG
  - 多模态
  - 提示工程
  - MLOps
  - 可观测性
  - 新兴技术
  - ML 论文写作
- **安装：** `npm` 包 `@orchestra-research/ai-research-skills` 一键安装
- **特点：** 每个技能提供 200-500 行的重点指导，遵循 Anthropic 官方最佳实践

#### [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)
- **技能数量：** 140+
- **描述：** 即用型科学技能集合，将 Claude 转变为 AI 研究助手
- **主题：** ai-research, claude-skills, scientific-computing
- **覆盖领域：**
  - **生物信息学与基因组学：** 序列分析、单细胞 RNA-seq、基因调控网络、变异注释、系统发育分析
  - **化学信息学与药物发现：** 分子性质预测、虚拟筛选、ADMET 分析、分子对接、先导化合物优化
  - **蛋白质组学与质谱：** LC-MS/MS 处理、肽段鉴定、光谱匹配、蛋白质定量
  - **机器学习与 AI：** 深度学习、强化学习、时间序列分析、模型可解释性、贝叶斯方法
  - **统计分析：** 假设检验、发表级可视化（matplotlib 和 seaborn）
  - **引用管理：** 搜索 Google Scholar 和 PubMed、提取 CrossRef/PubMed/arXiv 元数据、生成格式化的 BibTeX 条目
- **技术栈：** Biopython, Scanpy, RDKit, scikit-learn, PyTorch Lightning 等 50+ 开源项目
- **安装方式：**
  - Claude Code CLI 安装
  - MCP 服务器安装

#### [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
- **技能数量：** 300+
- **描述：** 来自官方开发团队和社区的代理技能集合
- **兼容性：** Claude Code, Codex, Antigravity, Gemini CLI, Cursor, GitHub Copilot, OpenCode, Windsurf 等
- **官方技能来源：**
  - Anthropic
  - Google Labs
  - Vercel
  - Stripe
  - Cloudflare
  - Trail of Bits
  - Sentry
  - Expo
  - Hugging Face
- **特色功能：**
  - Microsoft Azure AI 服务（NLP：情感、实体、关键短语）
  - Azure AI Vision（图像标题、标签、OCR、对象检测）
  - 计算机视觉、图像/视频 AI、实时视觉推理

#### [skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills)
- **描述：** Agent Skills 的权威资源 - 革命性的 AI 代理架构模块化能力
- **定义：** Agent Skills 是模块化的、标准化的 SKILL.md 包，通过渐进式披露提供按需能力
  - 轻量级元数据可提前加载
  - 完整指令仅在相关时加载
  - 支持资源按需访问
- **包含内容：**
  - 当前支持技能的平台
  - 即用型技能目录

#### [Prat011/awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills)
- **描述：** 精选的 LLM 和 AI Agent Skills、资源和工具列表
- **用途：** 定制 AI Agent 工作流
- **兼容性：** Claude Code, Codex, Gemini CLI 和自定义 AI Agents

#### [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)
- **描述：** 精选的技能、工具、教程和能力列表
- **适用对象：** AI 编码代理（Claude, Codex, Copilot, VS Code）

#### [libukai/awesome-agent-skills](https://github.com/libukai/awesome-agent-skills)
- **描述：** Agent Skills 终极指南
- **内容：** 快速入门、推荐技能、最新资讯与实战案例
- **语言：** 中英双语

---

## 2. 科学研究专用技能

### 📚 综合科学研究工具

#### [K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer)
- **描述：** 通用科学写作工具
- **功能：**
  - 结合 AI 驱动的深度研究与格式良好的书面输出
  - 生成发表级科学论文、报告、海报、基金提案、文献综述等学术文档
  - 所有内容都有实时文献搜索和经过验证的引用支持

#### [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills)
- **描述：** Claude Code 的结构化深度研究技能
- **特点：** 人机交互控制
- **工作流程：** 支持两阶段研究
  1. 大纲生成
  2. 深度调查
- **设计理念：** 人机协同设计，确保每个阶段的精确控制

#### [acertainKnight/project-thoth](https://github.com/acertainKnight/project-thoth)
- **描述：** 高级 AI 驱动的研究助手系统
- **设计理念：** 为灵活性、可扩展性和用户控制而构建
- **特点：** Thoth 将智能自动化与全面的定制相结合
  - 每个提示、模式和来源都可以根据你的工作流程进行定制
- **内置技能：** 10 个
  - paper-discovery（论文发现）
  - deep-research（深度研究）
  - knowledge-base-qa（知识库问答）
  - online-research（在线研究）
  - 等
- **来源插件：** 7 个，用于学术论文搜索

---

### 🧬 生物信息学与生命科学

#### [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills)
- **描述：** 一套用于使用代理（如 Claude Code）进行生物信息学的 SKILLS.md
- **特点：** 引导 AI 编码代理完成常见的生物信息学任务
- **功能：** 为生物信息学工作流程提供 AI 代理专家知识

#### [anthropics/life-sciences](https://github.com/anthropics/life-sciences)
- **描述：** Claude Code Marketplace 的官方仓库，用于 Claude for Life Sciences 启动
- **用途：** 提供生命科学工具的 MCP 服务器和技能
- **功能：** 允许用户安装插件，直接在 Claude Code 中访问专业的研究和分析工具
- **维护：** 长期托管 marketplace.json，但不托管实际的 MCP 服务器

#### [biocontext-ai/skill-to-mcp](https://github.com/biocontext-ai/skill-to-mcp)
- **描述：** 将 AI Skills（Claude Skills 格式）转换为 MCP 服务器资源
- **所属：** BioContextAI 的一部分
- **功能：** 通过模型上下文协议将 Claude Skills 作为资源暴露给 LLM 应用程序

---

### 📖 文献管理与学术搜索

#### [luwill/research-skills](https://github.com/luwill/research-skills)
- **描述：** 医学影像 AI 文献综述技能
- **功能：** Claude Code 技能，用于编写医学影像 AI 研究的全面文献综述
- **工作流程：** 提供系统化的工作流程
  - 编写调查论文
  - 系统综述
  - CT、MRI、X 射线成像中的分割、检测和分类主题的文献分析

#### [jannisborn/paperscraper](https://github.com/PhosphorylatedRabbits/paperscraper)
- **描述：** 从 PubMed 或预印本服务器抓取出版物及其元数据的工具
- **支持平台：**
  - PubMed
  - arXiv
  - medRxiv
  - bioRxiv
  - chemRxiv
- **功能：**
  - 检索引用计数（来自 Google Scholar）
  - 检索影响因子（来自期刊）

#### [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp)
- **描述：** 用于从多个来源搜索和下载学术论文的 MCP
- **支持平台：**
  - arXiv
  - PubMed
  - bioRxiv
  - 等
- **适用人群：** 研究人员和 AI 驱动的工作流程

#### [u9401066/pubmed-search-mcp](https://github.com/u9401066/pubmed-search-mcp)
- **描述：** 专业的生物医学文献研究 MCP 服务器
- **工具数量：** 40 个
- **功能：**
  - 多源搜索（PubMed、Europe PMC、CORE、OpenAlex）
  - 全文访问
  - 引用网络
  - PICO 分析
  - 更多

#### [JabRef/jabref](https://github.com/JabRef/jabref)
- **描述：** 用于管理 BibTeX 和 BibLaTeX (.bib) 数据库的图形化 Java 应用程序
- **功能：** 跨多个在线科学目录搜索
  - CiteSeer
  - CrossRef
  - Google Scholar
  - IEEEXplore
  - INSPIRE-HEP
  - Medline PubMed
  - MathSciNet
  - Springer
  - arXiv
  - zbMATH

#### [vict0rsch/PaperMemory](https://github.com/vict0rsch/PaperMemory)
- **描述：** 浏览器的参考文献管理器
- **功能：**
  - 自动论文检测（Arxiv、OpenReview 等）
  - 出版场所匹配
  - 代码仓库发现
- **增强 ArXiv 功能：**
  - BibTex 引用
  - Markdown 链接
  - 直接下载
  - 更多

#### [allenai/citeomatic](https://github.com/allenai/citeomatic)
- **描述：** 引用推荐系统
- **功能：** 允许用户为他们的论文草稿找到相关引用
- **支持：** 由 Semantic Scholar 的 OpenCorpus 数据集支持

#### [AMENEHZAREBIDOKI/Amys_SearchEngine](https://github.com/AMENEHZAREBIDOKI/Amys_SearchEngine)
- **名称：** Amy's Search Engine
- **描述：** 简单的学术搜索工具，聚合来自多个来源的结果
- **支持平台：**
  - Wikipedia
  - Google Scholar
  - arXiv
  - PubMed
- **功能：** 帮助用户在一个地方快速找到相关的研究论文和文章，更容易浏览不同的学术研究来源

#### [allenai/s2orc](https://github.com/allenai/s2orc)
- **名称：** S2ORC: The Semantic Scholar Open Research Corpus
- **描述：** Semantic Scholar 开放研究语料库
- **链接：** https://www.aclweb.org/anthology/2020.acl-main.447/

#### [dvklopfenstein/pmidcite](https://github.com/dvklopfenstein/pmidcite)
- **描述：** 从命令行获取 PubMed 论文的引用计数

---

### 📝 论文写作与学术写作

#### [drshahizan/obsidian](https://github.com/drshahizan/obsidian)
- **描述：** Obsidian.md 专为学术写作定制的卓越笔记应用
- **用途：** 使用 AI 进行系统文献综述研讨会的一部分
- **特点：** 专门为学术写作量身定制

#### [jwwthu/how-to-research](https://github.com/jwwthu/how-to-research)
- **描述：** 研究方法指南
- **内容：** 撰写文献综述需要一系列技能
  - 收集、分类、评估同行评审的已发表数据
  - 将数据总结为相关且信息丰富的无偏见叙述

#### [khufkens/paper_writing_checklist](https://github.com/khufkens/paper_writing_checklist)
- **描述：** 学术论文写作（或同行评审）的清单和建议
- **覆盖内容：**
  - 文本流
  - 风格
  - 图表和表格格式

#### [jtleek/reviews](https://github.com/jtleek/reviews)
- **描述：** 撰写学术论文评审的指南
- **内容：** 描述评审文档的格式、语气和内容
- **目标：** 避免成为那个刻薄的审稿人，同时履行对学术界的职责

#### [LitLLM/LitLLM](https://github.com/LitLLM/LitLLM)
- **描述：** AI 驱动的文献综述助手
- **功能：** 帮助研究人员在大型语言模型（LLMs）的辅助下撰写文献综述

---

## 3. 数据科学与分析

### 📊 数据分析技能

#### [liangdabiao/claude-data-analysis](https://github.com/liangdabiao/claude-data-analysis)
- **描述：** 使用 Claude Code 创建数据分析 AI 代理
- **口号：** 让数据分析变得像聊天一样简单！
- **说明：** Claude Code 也是 agent 框架，类似 langgraph、crewAI、autogen 等框架
- **功能：**
  - 支持多种图表类型
    - 时间序列
    - 直方图
    - 箱线图
    - 密度图
    - 热图
    - 散点图
    - 相关矩阵
  - 使用 Python 库：Pandas、NumPy、Scikit-learn、Matplotlib

#### [coffeefuelbump/csv-data-summarizer-claude-skill](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill)
- **描述：** 自动分析上传的 CSV 文件的 Claude Skill
- **功能：**
  - 生成汇总统计
  - 检测缺失数据
  - 使用 Python 和 pandas 创建快速可视化
- **特点：** 上传任何 CSV 并获得即时、智能的分析，无需被问你想要什么

#### [antvis/mcp-server-chart](https://github.com/antvis/mcp-server-chart)
- **描述：** 包含 25+ 可视化图表的 MCP 服务器和技能
- **使用：** @antvis
- **用途：** 图表生成和数据分析

#### [ruvnet/claude-flow](https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-Data-Science)
- **描述：** CLAUDE MD 数据科学
- **内容：** 数据科学相关的 Claude.md 配置和模板

---

## 4. 机器学习框架与工具

### 🔧 跨框架兼容性工具

#### [arogozhnikov/einops](https://github.com/arogozhnikov/einops)
- **描述：** 灵活而强大的张量操作，提供可读且可靠的代码
- **支持框架：** PyTorch, JAX, TensorFlow 和其他

#### [jonasrauber/eagerpy](https://github.com/jonasrauber/eagerpy)
- **描述：** PyTorch、TensorFlow、JAX 和 NumPy — 使用相同的代码原生运行
- **特点：** 编写的代码自动在所有框架中原生工作

#### [lebrice/torch_jax_interop](https://github.com/lebrice/torch_jax_interop)
- **描述：** 混合和匹配 PyTorch 和 Jax 的简单工具
- **口号：** 两全其美！
- **功能：**
  - torch_to_jax
  - jax_to_torch
  - WrappedJaxFunction
  - torch_module_to_jax

#### [tum-pbs/PhiML](https://github.com/tum-pbs/PhiML)
- **描述：** 使用维度类型进行直观科学计算
- **支持：** Jax, PyTorch, TensorFlow & NumPy
- **优势：** 编写与 PyTorch、Jax 和 TensorFlow 兼容的代码，使共享代码和协作更容易，发布的研究代码将覆盖更广泛的受众

---

### 🔄 PyTorch-JAX 互操作性

#### [torch2jax (samuela/torch2jax)](https://github.com/samuela/torch2jax)
- **描述：** 在 JAX 中运行 PyTorch
- **特点：**
  - 无缝混合匹配 PyTorch 和 JAX 代码
  - 端到端自动微分
  - 在 PyTorch 代码上使用 JAX 经典功能（jit、grad、vmap）
  - 在 TPU 上运行 PyTorch 模型

#### [jax2torch (lucidrains/jax2torch)](https://github.com/lucidrains/jax2torch)
- **描述：** 在 PyTorch 中使用 Jax 函数

#### [functorch (pytorch/functorch)](https://github.com/pytorch/functorch)
- **描述：** PyTorch 的 JAX 风格可组合函数变换

---

### 🤖 专用 ML 框架与工具

#### [Unity-Technologies/ml-agents](https://github.com/Unity-Technologies/ml-agents)
- **名称：** Unity Machine Learning Agents Toolkit (ML-Agents)
- **描述：** 开源项目，使游戏和模拟能够作为环境来训练智能代理
- **技术：**
  - 深度强化学习
  - 模仿学习

#### [MASWorks/ML-Agent](https://github.com/MASWorks/ML-Agent)
- **描述：** "ML-Agent: Reinforcing LLM Agents for Autonomous Machine Learning Engineering" 的官方实现
- **特点：**
  - 能够执行端到端机器学习工程的自主代理
  - 基于 7B 大小的 Qwen-2.5 LLM 构建
  - 使用新颖的代理式 ML 训练框架进行训练
  - 首个通过在线强化学习（RL）从 ML 环境中的交互式实验中学习的 LLM 代理

#### [n2cholas/awesome-jax](https://github.com/n2cholas/awesome-jax)
- **名称：** JAX
- **描述：** 精选资源列表
- **链接：** https://github.com/google/jax

#### [mikeroyal/Machine-Learning-Guide](https://github.com/mikeroyal/Machine-Learning-Guide)
- **描述：** 机器学习指南
- **内容：** 了解所有关于机器学习工具、库、框架、大型语言模型（LLMs）和训练模型的知识

---

## 5. Agent 框架与工具

### 🚀 主要 Agent 框架

#### [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)
- **描述：** 编排角色扮演、自主 AI 代理的框架
- **特点：**
  - 精益、快速的 Python 框架
  - 完全从头开始构建
  - 完全独立于 LangChain 或其他代理框架
  - 通过促进协作智能，CrewAI 使代理能够无缝协作，处理复杂任务

#### [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- **描述：** 将弹性语言代理构建为图
- **特点：**
  - 不抽象提示或架构
  - 提供持久执行：构建能够持续失败的代理，可以运行较长时间，自动从失败的地方恢复
  - 中央优势：持久执行

#### [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents)
- **描述：** Deep Agents 是基于 langchain 和 langgraph 构建的代理工具
- **配备：**
  - 规划工具
  - 文件系统后端
  - 生成子代理的能力
- **特点：** 能够很好地处理复杂的代理任务

#### [AgentOps-AI/agentops](https://github.com/AgentOps-AI/agentops)
- **描述：** Python SDK，用于 AI 代理监控、LLM 成本追踪、基准测试等
- **集成：** 与大多数 LLMs 和代理框架集成
  - CrewAI
  - Agno
  - OpenAI Agents SDK
  - Langchain
  - Autogen
  - AG2
  - CamelAI
- **功能：** 原生集成，用于监控和追踪 LLM 成本

---

### 📚 Agent 学习资源

#### [MDalamin5/End-to-End-Agentic-Ai-Automation-Lab](https://github.com/MDalamin5/End-to-End-Agentic-Ai-Automation-Lab)
- **描述：** 包含实践项目、代码示例和部署工作流程
- **探索内容：**
  - 多代理系统
  - LangChain
  - LangGraph
  - AutoGen
  - CrewAI
  - RAG
  - MCP
  - n8n 自动化
  - 使用 Docker、AWS 和 BentoML 的可扩展代理部署

#### [DharminJoshi/Awesome-Agentic-AI-Learning-Resource-By-DevKay](https://github.com/DharminJoshi/Awesome-Agentic-AI-Learning-Resource-By-DevKay)
- **描述：** Awesome Agentic AI Learning Resource by DevKay
- **内容：** 掌握 Agentic AI 的精选路线图
  - 从 ML 基础到生产就绪的代理
  - 0-12+ 个月路径
  - 实践项目
  - 顶级资源
  - 代理架构
  - 工具：LangChain 和 AutoGen

#### [sinanuozdemir/oreilly-ai-agents](https://github.com/sinanuozdemir/oreilly-ai-agents)
- **描述：** AI Agents 世界介绍
- **内容：** O'Reilly 课程
- **覆盖：**
  - 参与者将从基础概念开始，逐步深入更高级的主题
  - 各种框架：CrewAI、LangChain 和 AutoGen
  - 使用强大的提示工程技术从头开始构建代理

#### [jim-schwoebel/awesome_ai_agents](https://github.com/jim-schwoebel/awesome_ai_agents)
- **描述：** 与 AI 代理相关的 1,500+ 资源和工具的综合列表

#### [tmgthb/Autonomous-Agents](https://github.com/tmgthb/Autonomous-Agents)
- **描述：** 自主代理（LLMs）研究论文
- **更新：** 每日更新

#### [junhua/awesome-llm-agents](https://github.com/junhua/awesome-llm-agents)
- **描述：** 高质量研究论文和开源项目的集合
- **关于：** LLM-agents
- **特点：** 包含精心挑选和仔细分类的阅读列表，每篇论文和项目都有评论

#### [hyp1231/awesome-llm-powered-agent](https://github.com/hyp1231/awesome-llm-powered-agent)
- **描述：** 关于 LLM 驱动代理的精彩内容
- **包含：** Papers / Repos / Blogs / ...

#### [kyrolabs/awesome-agents](https://github.com/kyrolabs/awesome-agents)
- **描述：** 精选的开源工具和产品列表，用于构建 AI 代理

#### [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)
- **描述：** Agent Skills 的综合集合
- **用途：**
  - 上下文工程
  - 多代理架构
  - 生产代理系统
- **使用场景：** 构建、优化或调试需要有效上下文管理的代理系统时使用

---

### 🔗 多框架组合项目

#### [Ionio-io/langgraph-with-crewai](https://github.com/Ionio-io/langgraph-with-crewai)
- **描述：** 包含对 Langgraph 的详细介绍（新的 Langchain 库）
- **学习内容：** 了解 langgraph 并使用 crewai 和 langgraph 创建一个迷你项目

#### [pavanbelagatti/Agentic-RAG-LangChain-CrewAI](https://github.com/pavanbelagatti/Agentic-RAG-LangChain-CrewAI)
- **描述：** Agentic RAG 示例
- **展示：** 结合 CrewAI 和 LangChain 进行检索增强生成

---

## 6. 学术写作与研究自动化

### 🔬 AI 研究助手系统

#### [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher)
- **会议：** [NeurIPS2025]
- **标题：** "AI-Researcher: Autonomous Scientific Innovation"
- **生产版本：** https://novix.science/chat
- **描述：** 自动科学发现的革命性系统
- **特点：**
  - 完全自主
  - 完整的端到端研究自动化
  - 由尖端 AI 代理驱动
  - 提供无缝的研究自动化体验
  - 支持多个 LLM 提供商
  - 完全自动化的系统，消除整个研究生命周期的人工干预

#### [starpig1129/DATAGEN (AI-Data-Analysis-MultiAgent)](https://github.com/starpig1129/AI-Data-Analysis-MultiAgent)
- **描述：** AI 驱动的多代理研究助手
- **自动化功能：**
  - 假设生成
  - 数据分析
  - 报告撰写
- **技术：** 使用 LangGraph 创建管理整个研究过程的状态图

#### [LitLLM/LitLLM](https://github.com/LitLLM/LitLLM)
- **描述：** AI 驱动的文献综述助手
- **用户：** 研究人员
- **功能：** 在大型语言模型（LLMs）的辅助下撰写文献综述

---

## 7. Web 开发技能

### 🎨 前端开发

#### [anthropics/claude-code](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)
- **描述：** Anthropic 官方前端设计技能
- **实现：** 在 HTML/CSS/JS、React、Vue 等中实现工作代码

#### [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills)
- **描述：** 66 个全栈开发人员的专业技能
- **口号：** 将 Claude Code 转变为你的专家结对程序员
- **覆盖：** 12 个类别
  - 语言
  - 后端/前端框架
  - 基础设施
  - APIs
  - 测试
  - DevOps
  - 安全
  - 数据/ML
  - 平台专家

#### [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- **描述：** 100+ 专业 Claude Code 子代理集合
- **覆盖范围：** 广泛的开发用例
- **前端开发者子代理：**
  - 专攻现代 Web 应用程序
  - 深厚的专业知识：React 18+, Vue 3+, Angular 15+
  - 主要关注：构建高性能、可访问、可维护的用户界面

#### [ruvnet/claude-flow](https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-Web-Development)
- **名称：** CLAUDE MD Web Development
- **技术栈：**
  - 前端：React/Vue/Angular + TypeScript
  - 后端：Node.js/Express + RESTful API

#### [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
- **描述：** Claude Skills、资源和工具的精选列表
- **定制：** Claude AI 工作流程，特别是 Claude Code
- **前端设计技能：**
  - 指示 Claude 避免 "AI 陈词滥调" 或通用美学
  - 做出大胆的设计决策
  - 非常适合 React 和 Tailwind

#### [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills)
- **描述：** Claude Skills 的精选列表
- **特色：** web-artifacts-builder 套件
- **功能：** 使用现代前端 web 技术创建精细的多组件 claude.ai HTML artifacts
  - React
  - Tailwind CSS
  - shadcn/ui

#### [le-dat/claude-skill-engineer](https://github.com/le-dat/claude-skill-engineer/blob/master/skills/frontend-design/SKILL.md)
- **描述：** Claude 技能工程师项目
- **包含：** 前端设计技能

#### [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- **描述：** Claude Skills、资源和工具的精选列表
- **用途：** 定制 Claude AI 工作流程

---

## 8. DevOps 与云计算

### ☁️ DevOps 技能与工具

#### [mrgoonie/claudekit-skills](https://github.com/mrgoonie/claudekit-skills)
- **描述：** ClaudeKit.cc 的所有强大技能！
- **后端开发：**
  - DevOps 实践
  - 涵盖 Docker、Kubernetes 和 CI/CD
- **云基础设施部署：**
  - Cloudflare
  - Docker 容器
  - Google Cloud Platform
  - CI/CD 管道设置

#### [rand/cc-polymath](https://github.com/rand/cc-polymath)
- **描述：** Claude Code 技能和工作流程
- **优化：** 上下文效率和技能质量
- **技能范围：** 从云基础设施到设计到高级数学
- **云技能：**
  - AWS
  - GCP
  - Modal.com
  - Cloudflare Workers
  - Vercel
- **容器技能：**
  - Docker
  - Kubernetes
  - 安全
- **发现网关：**
  - 在提及 "PostgreSQL"、"MongoDB"、"Redis" 时触发
  - 在提及 "REST API with PostgreSQL" 时自动激活
- **数据库技能：** 11 个，带决策树
  - Postgres
  - MongoDB
  - Redis
  - 流式传输

#### [Tarique-B-DevOps/AWS-CloudOps-Agent](https://github.com/Tarique-B-DevOps/AWS-CloudOps-Agent)
- **描述：** AWS CloudOps 的 Agentic AI
- **驱动：**
  - Strands Agent
  - Bedrock FMs
  - AgentCore Runtime & Memory
- **CI/CD：** 完整的 CI/CD
  - Docker
  - Terraform
  - Jenkins
- **设计：** 智能 AI 代理，通过自然语言简化 AWS 操作
- **功能：**
  - 管理 EC2 实例
  - IAM 操作
  - 代码生成
  - 成本分析
  - 安全管理
  - 完整的 CI/CD 自动化和容器化部署

#### [in28minutes/devops-master-class](https://github.com/in28minutes/devops-master-class)
- **描述：** 初学者的 Devops 教程
- **学习内容：**
  - Docker
  - Kubernetes
  - Terraform
  - Ansible
  - Jenkins
  - Azure Devops
- **实现：**
  - 持续集成
  - 持续交付
  - 基础设施即代码

#### [bregman-arie/devops-exercises](https://github.com/bregman-arie/devops-exercises)
- **内容：** DevOps 面试题
- **主题：**
  - Linux, Jenkins, AWS, SRE, Prometheus, Docker, Python, Ansible
  - Git, Kubernetes, Terraform, OpenStack, SQL, NoSQL
  - Azure, GCP, DNS, Elastic, Network, Virtualization

#### [aws-samples/sample-devops-agent-eks-workshop](https://github.com/aws-samples/sample-devops-agent-eks-workshop)
- **描述：** AWS DevOps Agent EKS 研讨会示例
- **展示：** AWS DevOps Agent 如何使用自然语言调查跨 EKS 的基础设施问题，以排查复杂的分布式系统

---

## 9. 数据库与后端

### 🗄️ 数据库技能

#### [wshobson/agents](https://github.com/wshobson/agents/blob/main/plugins/database-design/skills/postgresql/SKILL.md)
- **描述：** PostgreSQL 特定的架构设计指南
- **覆盖：**
  - 最佳实践
  - 数据类型
  - 索引
  - 约束
  - 性能模式
  - 高级功能

#### [PostgREST/postgrest](https://github.com/PostgREST/postgrest)
- **描述：** 任何 Postgres 数据库的 REST API
- **功能：** PostgREST 从任何现有的 PostgreSQL 数据库提供完全 RESTful API
- **便利：** 直接从数据库架构创建后端 API

#### [dbgate/dbgate](https://github.com/dbgate/dbgate)
- **描述：** 数据库管理器
- **支持：**
  - MySQL
  - PostgreSQL
  - SQL Server
  - MongoDB
  - SQLite
  - 其他
- **运行环境：** Windows, Linux, Mac 或 Web 应用程序
- **功能：**
  - 查询设计
  - 数据编辑
  - ER 图

#### [documentdb/documentdb](https://github.com/documentdb/documentdb)
- **描述：** MongoDB 兼容的数据库引擎
- **用于：** 云原生和开源工作负载
- **构建目标：**
  - 可扩展性
  - 性能
  - 开发者生产力

---

## 10. 测试与 QA

### 🧪 测试自动化技能

#### [seleniumforchitta/Python-Playground-For-QA](https://github.com/seleniumforchitta/Python-Playground-For-QA)
- **描述：** QA 专业人员和 Python 爱好者的动态练习场
- **内容：** 深入实践 Python 练习
- **探索：** 使用 Selenium 和 PyTest 进行 QA 自动化
- **提供：** 提升技能、实验自动化脚本的空间

#### [setupfromscratch/QA_Testing_Portfolio](https://github.com/setupfromscratch/QA_Testing_Portfolio)
- **描述：** 有志 QA 测试人员和 Python 自动化爱好者的学习指南
- **包含：**
  - 实践任务
  - 代码示例
  - 教育材料
- **帮助：** 提高手动和自动化测试技能
- **使用：** Python, Selenium 等

#### [isFrost/toolshop_test_automation](https://github.com/isFrost/toolshop_test_automation)
- **描述：** 实践项目，旨在提高测试自动化技能
- **使用：**
  - Selenium WebDriver
  - PyTest
  - Allure

#### [vamotest/qa_automation](https://github.com/vamotest/qa_automation)
- **技术栈：**
  - Pytest
  - Selenium
  - Logging
  - Allure
  - CI/CD
  - Robot Framework

#### [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
- **描述：** Python APIs for web automation, testing, and bypassing bot-detection with ease
- **特点：** 授权软件团队更快创新，轻松应对现代 web 挑战的浏览器自动化框架

#### [letsconfuse/DemoQA](https://github.com/letsconfuse/DemoQA)
- **描述：** DemoQA 网站的综合 Selenium & Pytest 测试自动化套件
- **覆盖：** 关键 UI 元素
  - 复选框
  - 表单
  - 滑块
  - 工具提示
  - 更多
- **特点：** 模块化测试用例和 HTML 报告
- **设计：** 展示真实世界的 web 自动化实践，特别适合 QA 作品集或面试

#### [LambdaTest/pytest-selenium-sample](https://github.com/LambdaTest/pytest-selenium-sample)
- **描述：** 使用 pytest 和 LambdaTest 在云上运行测试自动化
- **用途：** 帮助你在 LambdaTest 自动化测试云中并行执行基于 pytest 框架的测试脚本的示例仓库

#### [karimelkomy/Python-Test-Automation-Framework](https://github.com/karimelkomy/Python-Test-Automation-Framework)
- **描述：** 使用 selenium 和 Python 的测试自动化框架
- **特点：**
  - 页面对象模型
  - 使用 Allure 报告进行报告

---

## 11. 官方技能仓库

### 🏢 官方维护的技能库

#### [anthropics/skills](https://github.com/anthropics/skills)
- **维护者：** Anthropic 官方
- **描述：** Agent Skills 公共仓库
- **定义：** Skills 是指令、脚本和资源的文件夹，Claude 动态加载以提高在专门任务上的性能
- **覆盖领域：**
  - 文档操作（DOCX, PDF, PPTX, XLSX）
  - 品牌指南
  - 内部沟通

#### [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)
- **维护者：** Vercel 官方
- **描述：** Vercel 的官方代理技能集合
- **内容：** React 和 Next.js 性能优化指南
- **来源：** 来自 Vercel Engineering
- **规则：** 40+ 条规则，跨 8 个类别

#### [vercel-labs/skills](https://github.com/vercel-labs/skills)
- **维护者：** Vercel 官方
- **描述：** 开放的代理技能工具
- **使用：** `npx skills`
- **功能：** 通过 `npx skills add` 命令添加技能

#### [vercel/ai](https://github.com/vercel/ai)
- **名称：** The AI Toolkit for TypeScript
- **创建者：** Next.js 的创建者
- **描述：** AI SDK 是一个免费的开源库
- **用途：** 构建 AI 驱动的应用程序和代理
- **API：** 统一的 API 与模型提供商交互
  - OpenAI
  - Anthropic
  - Google
  - 更多
- **支持：** Claude Code 或 Cursor 的技能支持

---

### 🌐 官方技能聚合

#### [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)
- **技能数量：** 700+
- **描述：** Claude Code/Antigravity/Cursor 的终极代理技能集合
- **特点：**
  - 经过实战测试
  - 高性能技能
  - 包含 Anthropic 和 Vercel 的官方技能
- **官方技能来源：**
  - Anthropic
  - Google Labs
  - Vercel
  - Stripe
  - Cloudflare
  - Trail of Bits
  - Sentry
  - Expo
  - Hugging Face
  - 更多

#### [ForaeFactory/antigravity-skills](https://github.com/ForaeFactory/antigravity-skills)
- **技能数量：** 200+
- **描述：** Claude Code/Antigravity/Cursor 的终极代理技能集合
- **特点：**
  - 经过实战测试
  - 高性能技能
  - 包含 Anthropic 和 Vercel 的官方技能

#### [hangoclong/skills-antigravity-awesome](https://github.com/hangoclong/skills-antigravity-awesome)
- **技能数量：** 200+
- **描述：** Claude Code/Antigravity/Cursor 的终极代理技能集合
- **特点：**
  - 经过实战测试
  - 高性能技能
  - 包含 Anthropic 和 Vercel 的官方技能

#### [huysynf/antigravity-awesome-skills](https://github.com/huysynf/antigravity-awesome-skills)
- **技能数量：** 200+
- **描述：** Claude Code/Antigravity/Cursor 的终极代理技能集合
- **特点：**
  - 经过实战测试
  - 高性能技能
  - 包含 Anthropic 和 Vercel 的官方技能

---

## 12. 编程语言特定技能

### 💻 多语言编程技能

#### [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)
- **描述：** 完整的 Claude Code 配置集合
- **内容：**
  - agents（12 个）
  - skills（16 个）
  - hooks（多个）
  - commands（24 个）
  - rules（多个）
  - MCPs
- **来源：** Anthropic 黑客马拉松获胜者的实战配置
- **多语言规则架构：**
  - TypeScript 目录
  - Python 目录
  - Go 目录

#### [metacall/core](https://github.com/metacall/core)
- **名称：** MetaCall: The ultimate polyglot programming experience
- **描述：** 可扩展、可嵌入的多语言运行时
- **支持语言：**
  - NodeJS
  - JavaScript
  - TypeScript
  - Python
  - Ruby
  - C#
  - Java
  - WASM
  - Go
  - C++
  - Rust
  - 更多

#### [hlop3z/astroladb](https://github.com/hlop3z/astroladb)
- **描述：** 在 JavaScript 中定义一次，导出强类型模型
- **支持：**
  - Rust
  - Go
  - Python
  - TypeScript
  - 更多
- **功能：** 定义架构一次，然后生成
  - SQL 迁移
  - Rust 结构体
  - Go 模型
  - Python 类
  - TypeScript 类型

#### [horsleyb/opencode-agentai](https://github.com/horsleyb/opencode-agentai)
- **描述：** 容器化的 AI 编码助手
- **技术：**
  - SST OpenCode
  - MCP 服务器
  - 本地 LLM 路由
- **多语言支持：**
  - Python
  - TypeScript/JavaScript
  - Go
  - Rust
  - Java
- **LSP 集成：** 完整的 LSP 集成

#### [DasBluEyedDevil/Daem0n-MCP](https://github.com/DasBluEyedDevil/Daem0n-MCP)
- **描述：** 代码理解层
- **技术：** 使用 tree-sitter 解析代码
- **支持语言：**
  - Python
  - TypeScript
  - JavaScript
  - Go
  - Rust
  - Java
  - C
  - C++
  - C#
  - Ruby
  - PHP

---

### 📚 语言学习资源

#### [rochacbruno/py2rs](https://github.com/rochacbruno/py2rs)
- **描述：** Python 程序员转 Rust 程序员的快速参考指南

#### [ThePrimeagen/rust-for-typescript-devs](https://github.com/ThePrimeagen/rust-for-typescript-devs)
- **描述：** TypeScript 开发者学习 Rust
- **作者：** ThePrimeagen

#### [rust-unofficial/awesome-rust](https://github.com/rust-unofficial/awesome-rust)
- **描述：** Rust 代码和资源的精选列表

---

## 13. 网络安全

### 🔐 网络安全与道德黑客

#### [icdfa/Phase-1-Cybersecurity-Ethical-Hacking-Internship-Labs](https://github.com/icdfa/Phase-1-Cybersecurity-Ethical-Hacking-Internship-Labs)
- **描述：** 网络安全道德黑客实习实验室第一阶段
- **提供：** 基本技能的实践培训
- **探索技术：**
  - 渗透测试
  - 社会工程
  - 漏洞评估
- **包含：**
  - 实验练习
  - 资源
  - 文档
- **指导：** 在实际网络安全应用中指导学习者
- **CTF 挑战：** 模拟真实世界的渗透测试

#### [Hamed233/Cybersecurity-Mastery-Roadmap](https://github.com/Hamed233/Cybersecurity-Mastery-Roadmap)
- **描述：** 全面的逐步指南
- **目标：** 从初学者到专家级别掌握网络安全
- **包含：**
  - 精选资源
  - 工具
  - 职业指导
- **认证：**
  - Certified Ethical Hacker (CEH)
  - 关注道德黑客方法论、工具、技术和对策
- **渗透测试者职责：**
  - 通过模拟攻击测试系统漏洞

#### [sundowndev/hacker-roadmap](https://github.com/sundowndev/hacker-roadmap)
- **描述：** 学习渗透测试的概述仓库
- **集合：** 黑客工具、资源和参考，用于实践道德黑客
- **平台参考：** HackTheBox
  - 用于测试和提升渗透测试和网络安全技能

#### [darpanne/Ethical-Hacking-Lab](https://github.com/darpanne/Ethical-Hacking-Lab)
- **描述：** 道德黑客实验室
- **提供：** 渗透测试和网络安全技术的实践经验
- **关注：**
  - 理解攻击方法
  - 利用漏洞
  - 增强道德黑客的实际技能

#### [n3thawk/Cybersecurity-Perfect-Roadmap](https://github.com/n3thawk/Cybersecurity-Perfect-Roadmap)
- **描述：** 全面的逐步指南
- **目标：** 从初学者到专家级别掌握网络安全
- **包含：**
  - 精选资源
  - 工具
  - 职业指导

#### [enaqx/awesome-pentest](https://github.com/enaqx/awesome-pentest)
- **描述：** 精彩的渗透测试资源、工具和其他精彩内容的集合
- **特色：**
  - Cybrary 的道德黑客和高级渗透测试免费课程
  - 培训材料
  - 漏洞利用教程
  - 安全会议信息

#### [roya0045/Pentest-practice](https://github.com/roya0045/Pentest-practice)
- **描述：** 可以合法安全地训练网络技能的黑客环境精选列表
- **特色：** Hacking-Lab
  - 在线道德黑客、计算机网络和安全挑战平台
  - 致力于寻找和教育网络安全人才

#### [YSCHGroup/art-of-hacking](https://github.com/YSCHGroup/art-of-hacking)
- **描述：** 包含 Pearson 视频课程 "The Art of Hacking and Exploitation" 中涵盖的补充信息
- **服务对象：** 网络和安全专业人员开始道德黑客和渗透测试职业的综合指南
- **帮助：** 个人准备 OSCP 和 CEH 认证

---

## 14. 移动开发

### 📱 移动应用开发技能

#### [contains-studio/agents](https://github.com/contains-studio/agents/blob/main/engineering/mobile-app-builder.md)
- **描述：** 移动应用构建器 Agent
- **角色：** 专家移动应用程序开发人员
- **掌握：**
  - iOS
  - Android
  - 跨平台开发
- **专业知识：**
  - 使用 Swift/Kotlin 的原生开发
  - 使用 React Native 和 Flutter 的跨平台解决方案

#### [hayanisaid/React-Native-developer-roadmap](https://github.com/hayanisaid/React-Native-developer-roadmap)
- **描述：** React Native 是使用 React 和 JavaScript 构建移动应用的跨平台库
- **目的：** 在你的 React Native 之旅中帮助你
- **内容：** 包含与 React Native 艺术一起工作所需的大量资源（文章、教程）

#### [PacktPublishing/Learn-Flutter-and-Dart-to-Build-iOS-and-Android-Apps](https://github.com/PacktPublishing/Learn-Flutter-and-Dart-to-Build-iOS-and-Android-Apps)
- **描述：** 学习 Flutter 和 Dart 以构建 iOS 和 Android 应用
- **出版商：** Packt

#### [GetStream/awesome-stream](https://github.com/GetStream/awesome-stream)
- **描述：** 使用 Stream 构建的资源、工具和项目的官方精彩列表
- **SDK：** 全面的 SDK
  - React
  - iOS
  - Android
  - React Native
  - Flutter
  - 更多

---

### 🔄 框架对比

**React Native vs Flutter 讨论：**
- **React Native：**
  - 更快的开发时间，尤其是对于简单的应用
  - 使用 JavaScript/TypeScript（许多开发者已经知道）
  - 依赖原生组件，因此应用感觉更接近原生 UI
- **Flutter：**
  - 在 UI 设计方面表现出色
  - 为 iOS 和 Android 提供单一代码库
  - 出色的性能，因为它编译为原生代码，导致更快的应用启动时间和流畅的动画
  - 跨平台提供一致的 UI（iOS 和 Android），因为它使用自己的 widget 集
  - 使用 Dart（如果你知道 Java/C++/JavaScript，容易学习）
  - 提供具有漂亮 widget 的单一 UI 框架

---

## 15. 区块链与 Web3

### ⛓️ 区块链开发技能

#### [smartcontractkit/full-blockchain-solidity-course-js](https://github.com/smartcontractkit/full-blockchain-solidity-course-js)
- **描述：** 学习区块链、Solidity 和使用 Javascript 的全栈 Web3 开发
- **版本：** JavaScript 和 TypeScript 版本都可用

#### [smartcontractkit/full-blockchain-solidity-course-py](https://github.com/smartcontractkit/full-blockchain-solidity-course-py)
- **描述：** 终极 Solidity、区块链和智能合约 - 初学者到专家全套课程
- **版本：** Python 版

#### [Cyfrin/foundry-full-course-cu](https://github.com/Cyfrin/foundry-full-course-cu)
- **描述：** 区块链开发者、智能合约和 Solidity 职业路径
- **驱动：** AI 驱动
- **级别：** 从初学者到专家
- **使用：** Foundry
- **课程时长：** 50+ 小时的智能合约开发课程

#### [frankiefab100/Blockchain-Development-Resources](https://github.com/frankiefab100/Blockchain-Development-Resources)
- **描述：** 这个仓库的内容将帮助你启动区块链开发职业
- **学习内容：**
  - 如何在以太坊上部署智能合约
  - 构建 DApps、DeFi、DAO、NFT 和 Token 协议
- **包含：**
  - 区块链技术、Web3、智能合约部署的综合链接
  - 以太坊和其他网络
  - NFTs、DApps、DeFi、DAOs
  - 工具：RemixIDE、Metamask、Hardhat
  - 编程语言：Solidity、Vyper、Rust、Golang

#### [cybergeekgyan/Web3.0-Blockchain-and-CryptoCurrency](https://github.com/cybergeekgyan/Web3.0-Blockchain-and-CryptoCurrency)
- **描述：** 精选资源列表
- **内容：**
  - 基础 Web3.0、区块链和加密货币概念
  - Solidity 和 Ethereum 的开发能力技能
  - 区块链编程

#### [zubairahm3d/Beginner-Level-Solidity-Projects](https://github.com/zubairahm3d/Beginner-Level-Solidity-Projects)
- **项目数：** 100 个初学者友好的以太坊项目
- **帮助：** 新开发者学习 Solidity、智能合约和核心区块链概念
- **方式：** 通过实践练习
- **适合：** 任何开始 Web3 之旅的人！

#### [Shubham0850/awesome-web3-projects](https://github.com/Shubham0850/awesome-web3-projects)
- **描述：** 精心挑选的鼓舞人心的 Web3 项目集合
- **用于：** 学习和探索
- **特色项目：**
  - 学习 Solidity
  - 编写智能合约并部署到区块链
  - 构建 Web3 客户端应用
  - 非常适合对加密货币感兴趣的黑客

#### [anataliocs/web3-skill-tree](https://github.com/anataliocs/web3-skill-tree)
- **描述：** 开始学习 Web3 基础知识
- **重点：** Solidity 是要学习的主要语言
- **工具：**
  - Truffle
  - Hardhat
  - Foundry
- **服务：**
  - Infura
  - Alchemy

#### [itublockchain/web3-bootcamp](https://github.com/itublockchain/web3-bootcamp)
- **描述：** ITU Blockchain 的开源土耳其智能合约开发者训练营

---

## 16. 游戏开发

### 🎮 游戏引擎技能

#### [FronkonGames/Awesome-Gamedev](https://github.com/FronkonGames/Awesome-Gamedev)
- **描述：** 游戏开发资源的精选集合
- **教程和指南：**
  - 在 Unreal Engine 中建模
  - Unity 中的风格化环境制作
  - Blender 到 Godot 3 场景导入

#### [godotengine/godot](https://github.com/godotengine/godot)
- **名称：** Godot Engine
- **描述：** 多平台 2D 和 3D 游戏引擎
- **许可：** 完全免费和开源
  - 使用非常宽松的 MIT 许可
  - 没有附加条件
  - 没有版税
- **吸引力：** 对独立开发者特别有吸引力

#### [Anthogonyst/UnityToGodot](https://github.com/Anthogonyst/UnityToGodot)
- **描述：** 将 Unity 项目完全转换为 Godot 项目的开源计划

#### [Zylann/unity_to_godot_converter](https://github.com/Zylann/unity_to_godot_converter)
- **描述：** 从 Unity 到 Godot 游戏引擎的实验性转换器

#### [PacktPublishing/Hands-On-Unity-2023-Game-Development-Fourth-Edition](https://github.com/PacktPublishing/Hands-On-Unity-2023-Game-Development-Fourth-Edition)
- **描述：** Hands-On Unity 2023 Game Development, Fourth Edition
- **出版商：** Packt

---

### 🎯 游戏引擎对比

**讨论：游戏开发引擎选择**
- **Unity：** 在移动、独立和中等规模游戏中非常流行
- **Unreal Engine：** 在 AAA 工作室和高端项目中很常见
- **Godot：** 在独立开发者和开源项目中快速增长

**学习资源：**
- "Learning C# by Developing Games with Unity"
- "Multiplayer Game Development with Unreal Engine 5"
- "Godot 4 Game Development Cookbook"

---

## 17. MCP 服务器

### 🔌 Model Context Protocol 服务器

#### [K-Dense-AI/claude-skills-mcp](https://github.com/K-Dense-AI/claude-skills-mcp)
- **描述：** 使用向量搜索搜索和检索 Claude Agent Skills 的 MCP 服务器
- **功能：**
  - 智能搜索能力，用于发现相关的 Claude Agent Skills
  - 使用向量嵌入和语义相似性
- **加载技能：** ~90 个技能
  - 来自 Anthropic 的官方技能仓库
  - K-Dense AI 的科学技能集合

#### [pathintegral-institute/mcp.science](https://github.com/pathintegral-institute/mcp.science)
- **描述：** 科学研究的开源 MCP 服务器
- **功能：** 使 AI 模型（如 Claude）能够通过标准化协议与科学数据、工具和资源交互
- **包含服务器：**
  - 材料科学
  - DFT 计算
  - Jupyter notebooks
  - 更多

#### [ssdeanx/deep-research-mcp-server](https://github.com/ssdeanx/deep-research-mcp-server)
- **描述：** 使用 Gemini 创建研究 AI Agent 的 MCP 深度研究服务器
- **MCP 集成：** 作为模型上下文协议（MCP）服务器/工具运行
- **用途：** 为深度研究任务提供无缝代理集成
- **使用：** Gemini

#### [anthropics/life-sciences](https://github.com/anthropics/life-sciences)
- **描述：** Claude Code Marketplace 的仓库
- **用于：** Claude for Life Sciences 启动
- **继续托管：** 长期托管 marketplace.json
- **但不托管：** 实际的 MCP 服务器

#### [biocontext-ai/skill-to-mcp](https://github.com/biocontext-ai/skill-to-mcp)
- **描述：** 将 AI Skills（Claude Skills 格式）转换为 MCP 服务器资源
- **所属：** BioContextAI 的一部分
- **功能：** 通过模型上下文协议将 Claude Skills 作为资源暴露给 LLM 应用程序

#### [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp)
- **描述：** 基于 Python 的 MCP 服务器
- **功能：** 使用户能够从各种平台搜索和下载学术论文
- **理想用于：** 研究人员和 AI 驱动的工作流程

#### [u9401066/pubmed-search-mcp](https://github.com/u9401066/pubmed-search-mcp)
- **描述：** 专业的生物医学文献研究 MCP 服务器
- **工具：** 40 个工具
- **功能：**
  - 多源搜索（PubMed、Europe PMC、CORE、OpenAlex）
  - 全文访问
  - 引用网络
  - PICO 分析
  - 更多

---

## 18. 自动化与工作流

### ⚙️ 工作流自动化平台

#### [n8n-io/n8n](https://github.com/n8n-io/n8n)
- **描述：** 具有原生 AI 能力的公平代码工作流自动化平台
- **特点：**
  - 将可视化构建与自定义代码相结合
  - 自托管或云
  - 400+ 集成

#### [makafeli/n8n-workflow-builder](https://github.com/makafeli/n8n-workflow-builder)
- **描述：** 通过模型上下文协议（MCP）为 n8n 工作流自动化集成 AI 助手
- **功能：**
  - 将 Claude Desktop、ChatGPT 和其他 AI 助手连接到 n8n
  - 用于自然语言工作流管理
- **提供：** AI 助手通过模型上下文协议与 n8n 工作流程交互的能力
- **作为：** AI 助手（如 Claude Desktop）和 n8n 实例之间的桥梁

#### [OMI-KALIX/n8n-beginner-research-automation](https://github.com/OMI-KALIX/n8n-beginner-research-automation)
- **描述：** 基于 n8n 的研究自动化
- **使用：**
  - 实时 web 数据
  - 本地 LLMs
- **生成：** 结构化的研究内容
- **阶段：** 演示阶段

#### [Skyvern-AI/skyvern](https://github.com/Skyvern-AI/skyvern)
- **描述：** 使用 AI 自动化基于浏览器的工作流程
- **技术：** 使用 LLMs 和计算机视觉
- **提供：**
  - Playwright 兼容的 SDK
  - 无代码工作流构建器

---

### 🤖 AI 研究自动化系统

#### [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher)
- **会议：** [NeurIPS2025]
- **标题：** "AI-Researcher: Autonomous Scientific Innovation"
- **生产版本：** https://novix.science/chat
- **描述：** 自动科学发现的革命性系统
- **特点：**
  - 完全自主
  - 完整的端到端研究自动化
  - 由尖端 AI 代理驱动
  - 提供无缝的研究自动化体验
  - 支持多个 LLM 提供商
  - 完全自动化的系统，消除整个研究生命周期的人工干预

#### [acertainKnight/project-thoth](https://github.com/acertainKnight/project-thoth)
- **描述：** 为灵活性、可扩展性和用户控制而构建的高级 AI 驱动的研究助手系统
- **特点：** Thoth 将智能自动化与全面的定制相结合
  - 每个提示、模式和来源都可以根据你的工作流程进行定制

#### [starpig1129/DATAGEN (AI-Data-Analysis-MultiAgent)](https://github.com/starpig1129/AI-Data-Analysis-MultiAgent)
- **描述：** AI 驱动的多代理研究助手
- **自动化：**
  - 假设生成
  - 数据分析
  - 报告撰写

#### [danielmiessler/Personal_AI_Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure)
- **描述：** 用于放大人类能力的 Agentic AI 基础设施
- **提供：**
  - 持久内存
  - 自定义技能
  - 智能路由，自动触发正确的工作流程
  - 自我改进能力

---

## 19. 社区技能集合

### 🌐 社区维护的技能库

#### [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
- **描述：** Claude Skills、资源和工具的精选列表
- **定制：** Claude AI 工作流程，特别是 Claude Code
- **时间轴：** 2024 年 10 月 16 日：🎉 Claude Skills 正式宣布
  - 可在 Claude.ai、Code 和 API 中使用
  - 各种社区贡献和官方技能

#### [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- **描述：** Claude Skills、资源和工具的精选列表
- **用途：** 定制 Claude AI 工作流程
- **特色技能：**
  - D3.js 可视化技能，教 Claude 制作 D3 图表和交互式数据可视化
  - CSV 数据汇总器，自动分析 CSV 文件并生成带可视化的综合见解，无需用户提示
  - 内容研究写作器技能，通过进行研究、添加引用、改进钩子和提供反馈来协助写作，同时充当写作伙伴
  - 潜在客户研究助手技能，通过分析产品和提供可操作的外展策略来识别和限定潜在客户

#### [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
- **描述：** Claude Code 和 Claude AI 的技能集合
- **用于：** 真实世界的使用
- **包含：**
  - Claude Code 子代理
  - Claude Code 命令
- **技能数：** 53 个生产就绪的技能
- **特色：** 计算机视觉、图像/视频 AI 和实时视觉推理能力

#### [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)
- **描述：** 技能、工具、教程和能力的精选列表
- **用于：** AI 编码代理（Claude、Codex、Copilot、VS Code）

#### [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)
- **描述：** Agent Skills 的综合集合
- **用于：**
  - 上下文工程
  - 多代理架构
  - 生产代理系统
- **使用时机：** 构建、优化或调试需要有效上下文管理的代理系统

---

## 20. 基准测试与评估

### 📊 性能测试与基准

#### [jimmc414/claudecode_gemini_and_codex_swebench](https://github.com/jimmc414/claudecode_gemini_and_codex_swebench)
- **描述：** 使用 SWEbench-lite 数据集随时间测量 Claude Code 和 Codex 性能与基线的工具包
- **重要：** Max 或 Pro 订阅者无需 API 密钥
- **提供：** 在真实世界软件工程任务上评估以代码为中心的语言模型的实证框架

#### [ruvnet/claude-flow - Performance Benchmarking](https://github.com/ruvnet/claude-flow/wiki/Performance-Benchmarking)
- **描述：** 包含全面的基准测试能力
- **评估：**
  - 跨不同执行模式评估和优化 AI 代理性能
  - 协调策略
  - 任务类型

#### [ruvnet/claude-flow - SWE Bench Evaluation](https://github.com/ruvnet/claude-flow/wiki/SWE-Bench-Evaluation)
- **描述：** SWE-bench 是评估大型语言模型在真实世界软件工程任务上的官方基准
- **功能：** claude-flow 提供集成的 SWE-bench 评估系统
  - 测试所有执行模式
  - 优化性能

#### [ruvnet/claude-flow - Benchmark System](https://github.com/ruvnet/claude-flow/wiki/Benchmark-System)
- **描述：** 基准系统

#### [cedrickchee/vibe-checking-claude-gpt-deepseek](https://gist.github.com/cedrickchee/656c116e416dc70622aca68eb648e952)
- **标题：** Vibe checking Claude 3.5, DeepSeek-Coder-V2, and GPT-4o for "alien" Coding Skills
- **发现：** Claude 3.5 Sonnet 展示了令人印象深刻的编码技能
  - 第一次尝试就正确解决问题
  - 理解微妙之处和良好的编码实践

---

## 21. AI 编码助手

### 🤖 AI 辅助编程工具

#### [sourcegraph/awesome-code-ai](https://github.com/sourcegraph/awesome-code-ai)
- **描述：** AI 编码工具列表（助手、补全、重构等）

#### [TabbyML/tabby](https://github.com/TabbyML/tabby)
- **描述：** 自托管 AI 编码助手

#### [Aider-AI/aider](https://github.com/Aider-AI/aider)
- **描述：** aider 是你终端中的 AI 结对编程
- **特点：** 在终端中使用本地 git 仓库工作的结对编程工具

#### [gensyn-ai/codeassist](https://github.com/gensyn-ai/codeassist)
- **描述：** 由 Gensyn 开发的完全私有和本地的 AI 编码助手
- **帮助：** 练习编程问题并训练新颖的助手来帮助你编码

#### [FireCoderAI/firecoder](https://github.com/FireCoderAI/firecoder)
- **描述：** Firecoder: Your Self-hosted AI Code Assistant

#### [entrepeneur4lyf/ai-coding-assistants](https://github.com/entrepeneur4lyf/ai-coding-assistants)
- **描述：** 关于专注于 AI 代码生成和 IDE 编码辅助的开源和闭源项目和产品的文章和链接

#### [automata/aicodeguide](https://github.com/automata/aicodeguide)
- **描述：** AI Code Guide 是使用 AI 开始编码的路线图

---

### 🏆 主流 AI 编码工具

**开源选项：**
- **TabbyML** - 自托管、开源编码助手
- **Salesforce CodeGen** - 用于程序合成的开源大型语言模型
- **OpenAI Codex** - 通过 API 将自然语言翻译为代码

**流行的终端/CLI 工具：**
- **Cursor** - 为与语言模型结对编程而构建的代码编辑器
- **Cline** - 可以使用你的 CLI 和编辑器的自主编码代理
- **Claude Code** - 生活在你终端中的代理编码工具
- **Aider** - 在终端中与本地 git 仓库一起工作的结对编程工具

**GitHub Copilot：**
- 由 GitHub、OpenAI 和 Microsoft 开发的生成式 AI 模型驱动
- 在自然语言文本和来自公开可用来源的源代码上训练
- 使用 GitHub Copilot 的开发者报告 "高达 75% 的满意度" 和 "在编写代码方面高达 55% 的生产力提高"

---

### 💡 AI 代码生成能力

**AI 代码生成：**
- 使用机器学习模型从描述代码应该做什么的输入中编写代码
- 提供基于上下文的建议

**AI 编码助手：**
- 使用 LLMs 和自然语言处理帮助开发者
- 帮助初学者：建议代码补全、查找错误、提供内联文档
- 帮助专家：更长时间保持流畅状态

---

## 22. 其他专业领域

### 🔧 专业工具与技能

#### [treasure-data/td-skills](https://github.com/treasure-data/td-skills)
- **描述：** Treasure Data Skills for Claude Code

#### [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)
- **描述：** 使用 AI Agents 和 RAG 的 LLM 应用集合
- **使用：**
  - OpenAI
  - Anthropic
  - Gemini
  - 开源模型
- **精选集合：** 具有 RAG、AI Agents、多代理团队、MCP、语音代理等的 Awesome LLM 应用

---

## 📈 统计总结

### 整体统计

| 类别 | 数量 |
|------|------|
| **总仓库数** | 100+ |
| **总技能数** | 2,000+ |
| **主要分类** | 22 个 |
| **官方仓库** | 10+ |
| **支持的编程语言** | 20+ |
| **支持的 AI 模型** | 15+ |

---

### 按类别统计

| 类别 | 关键仓库数 | 主要特点 |
|------|-----------|----------|
| 综合 AI 研究 | 7 | 83-300+ 技能/仓库 |
| 科学研究 | 15+ | 生物、化学、文献管理 |
| 数据科学 | 4 | 可视化、分析、CSV 处理 |
| ML 框架 | 10+ | 跨框架兼容 |
| Agent 框架 | 15+ | CrewAI、LangGraph、AutoGen |
| 学术写作 | 3 | 自动化研究和写作 |
| Web 开发 | 7 | React、Vue、Angular |
| DevOps | 6+ | Docker、K8s、CI/CD |
| 数据库 | 4 | PostgreSQL、MongoDB、多数据库 |
| 测试 QA | 8 | Selenium、Pytest 自动化 |
| 官方技能 | 9 | Anthropic、Vercel、Google |
| 编程语言 | 6 | 多语言支持 |
| 网络安全 | 7+ | 道德黑客、渗透测试 |
| 移动开发 | 4 | iOS、Android、RN、Flutter |
| 区块链 | 9 | Solidity、以太坊、Web3 |
| 游戏开发 | 5 | Unity、Unreal、Godot |
| MCP 服务器 | 7 | 科学、文献、技能搜索 |
| 自动化 | 8 | n8n、工作流、研究自动化 |
| 社区集合 | 5 | 精选技能列表 |
| 基准测试 | 5 | SWEbench、性能测试 |
| AI 编码助手 | 10+ | 开源和商业工具 |
| 其他 | 2+ | 专业工具 |

---

## 🎯 使用建议

### 按使用场景选择仓库

#### 🔬 科学研究人员
**推荐起始仓库：**
1. [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) - 全面的 AI 研究技能
2. [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) - 140+ 科学技能
3. [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) - 生物信息学专用
4. [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher) - 自主科学创新

#### 📊 数据科学家
**推荐起始仓库：**
1. [liangdabiao/claude-data-analysis](https://github.com/liangdabiao/claude-data-analysis) - 数据分析 AI 代理
2. [antvis/mcp-server-chart](https://github.com/antvis/mcp-server-chart) - 25+ 可视化图表
3. [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) - 包含数据科学技能

#### 💻 全栈开发者
**推荐起始仓库：**
1. [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) - 66 个全栈技能
2. [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) - 300+ 代理技能
3. [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) - 完整配置集合

#### 🤖 ML/AI 工程师
**推荐起始仓库：**
1. [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) - AI 研究全生命周期
2. [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) - 多代理框架
3. [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) - Agent 图构建

#### 📝 学术写作者
**推荐起始仓库：**
1. [K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) - 科学写作工具
2. [luwill/research-skills](https://github.com/luwill/research-skills) - 文献综述技能
3. [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) - 论文搜索 MCP

---

## 🚀 快速开始指南

### 安装常用技能库

#### 使用 npm 安装

```bash
# Orchestra Research AI Skills
npx @orchestra-research/ai-research-skills

# 或按类别安装
npx @orchestra-research/ai-research-skills install model-architecture
npx @orchestra-research/ai-research-skills install fine-tuning
```

#### 使用 Claude Code CLI

```bash
# 添加科学技能
claude code skills add K-Dense-AI/claude-scientific-skills

# 添加特定技能
claude code skills add anthropics/skills/document-manipulation
```

#### 使用 Vercel Skills CLI

```bash
# 添加 Vercel 官方技能
npx skills add vercel-labs/agent-skills
```

---

## 🔗 相关资源

### 官方文档
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Claude Skills Guide](https://docs.anthropic.com/claude/docs/agent-skills)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

### 社区资源
- [Claude Code 社区论坛](https://github.com/anthropics/claude-code/discussions)
- [Agent Skills Discord](https://discord.gg/agent-skills)

### 学习路径
- [AI Agents 完整课程](https://github.com/DharminJoshi/Awesome-Agentic-AI-Learning-Resource-By-DevKay)
- [LangChain & LangGraph 教程](https://github.com/MDalamin5/End-to-End-Agentic-Ai-Automation-Lab)

---

## 🤝 贡献

如果你发现了新的 AI Research Skills 仓库，欢迎贡献！

**贡献方式：**
1. Fork 本仓库
2. 添加新的仓库信息
3. 提交 Pull Request

**格式要求：**
```markdown
#### [仓库名称](GitHub链接)
- **描述：** 简短描述
- **技能数量：** 如果适用
- **特点：** 主要特点列表
- **用途：** 主要使用场景
```

---

## 📜 许可证

本文档采用 CC BY 4.0 许可证。

---

## 🙏 致谢

感谢所有为 AI Research Skills 生态系统做出贡献的开发者和研究人员！

特别感谢：
- Anthropic 团队
- Orchestra Research
- K-Dense AI
- VoltAgent
- 所有开源贡献者

---

## 📮 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- 电子邮件：your-email@example.com

---

**最后更新：** 2026-02-13
**维护者：** [你的名字]
**版本：** 1.0.0

---

## 📌 标签

`ai-research` `claude-skills` `agent-skills` `machine-learning` `data-science` `scientific-computing` `research-automation` `llm` `ai-agents` `mcp-servers` `research-tools` `academic-writing` `bioinformatics` `devops` `web-development` `blockchain` `game-development` `mobile-development` `cybersecurity` `testing-automation`

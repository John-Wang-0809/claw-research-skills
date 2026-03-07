# 可信度审计报告 (Credibility Audit Report)

> 生成时间: 2026-03-15 02:26 | 随机种子: 42 | 脚本: credibility_audit.py

## Executive Summary

- **总 skill 数**: 1408
- **清洁条目数**: 1408 (有可靠审计结果)
- **污染条目数**: 0 (0.0%)
- **去重误判率估计**: ~0.0% (0/0 fork_copies)
- **Fork 继承失败率**: 0/0 (0.0%)
- **置信度分布**: A=915, B=493, C=0
- **最高优先级修复**: 修复 fork 继承 lookup bug

---
## Q1: 去重正确性验证

### 方法
- 严格阈值: similarity ≥ 0.99
- 分层抽样: 30 个重复组深度分析

### 全量相似度分布

| 相似度区间 | 数量 | 分类 |
|-----------|------|------|
| 1.00 | 0 | 文本完全一致 |
| 0.99-1.00 | 0 | 几乎一致 |
| 0.95-0.99 | 0 | 有差异，需审查 |
| 0.90-0.95 | 0 | 高概率误标 |
| 0.85-0.90 | 0 | 高概率误标 |
| 0.80-0.85 | 0 | 几乎确定误标 |
| <0.80 | 0 | 传递性拉入 |

**严格标准结果**: 0 正确, 0 潜在误标 (0.0%)

### 抽样深度分析

- 分析组数: 30
- 有问题的组: 0

### 抽样组详情

#### deep-research (size=6) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| deep-research | 199-biotechnologies/claude-deep-research | canonical | ✓ |
| deep-research | acertainKnight/project-thoth | variant | ✓ |
| deep-research | proyecto26/research-skills | variant | ✓ |
| deep-research | Shubhamsaboo/awesome-llm-apps | variant | ✓ |
| deep-research | sickn33/antigravity-awesome-skills | variant | ✓ |
| deep-research | liangdabiao/simple_claude_deep_research_ | variant | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]    [4]    [5]  
[0] 1.000  0.017  0.019  0.008  0.008  0.012
[1] 0.020  1.000  0.020  0.021  0.012  0.016
[2] 0.018  0.033  1.000  0.027  0.024  0.026
[3] 0.023  0.022  0.028  1.000  0.026  0.035
[4] 0.018  0.037  0.022  0.017  1.000  0.035
[5] 0.014  0.019  0.045  0.012  0.029  1.000
```

#### xlsx (size=6) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| xlsx | anthropics/skills | canonical | ✓ |
| Xlsx | danielmiessler/Personal_AI_Infrastructur | variant | ✓ |
| xlsx | anthropics/claude-agent-sdk-demos | variant | ✓ |
| xlsx | K-Dense-AI/claude-scientific-writer | variant | ✓ |
| xlsx | K-Dense-AI/claude-scientific-skills | variant | ✓ |
| xlsx | sickn33/antigravity-awesome-skills | variant | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]    [4]    [5]  
[0] 1.000  0.817  0.927  0.844  0.815  0.926
[1] 0.817  1.000  0.845  0.792  0.768  0.851
[2] 0.927  0.845  1.000  0.895  0.864  0.978
[3] 0.847  0.795  0.901  1.000  0.966  0.898
[4] 0.818  0.771  0.870  0.966  1.000  0.868
[5] 0.926  0.851  0.978  0.896  0.865  1.000
```

#### rag-implementation (size=3) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| rag-implementation | sickn33/antigravity-awesome-skills | variant | ✓ |
| rag-implementation | wshobson/agents | canonical | ✓ |
| rag-implementation | ForaeFactory/antigravity-skills | variant | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]  
[0] 1.000  0.029  0.036
[1] 0.020  1.000  0.014
[2] 0.040  0.035  1.000
```

#### agent-memory-systems (size=4) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| agent-memory-systems | ForaeFactory/antigravity-skills | variant | ✓ |
| agent-memory-systems | huysynf/antigravity-awesome-skills | variant | ✓ |
| agent-memory-systems | hangoclong/skills-antigravity-awesome | variant | ✓ |
| agent-memory-systems | sickn33/antigravity-awesome-skills | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]  
[0] 1.000  1.000  1.000  0.898
[1] 1.000  1.000  1.000  0.898
[2] 1.000  1.000  1.000  0.898
[3] 0.898  0.898  0.898  1.000
```

#### pptx (size=4) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| pptx | anthropics/skills | canonical | ✓ |
| pptx | sickn33/antigravity-awesome-skills | variant | ✓ |
| Pptx | danielmiessler/Personal_AI_Infrastructur | variant | ✓ |
| pptx | K-Dense-AI/claude-scientific-skills | variant | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]  
[0] 1.000  0.037  0.034  0.039
[1] 0.022  1.000  0.923  0.927
[2] 0.017  0.908  1.000  0.853
[3] 0.025  0.925  0.867  1.000
```

#### nodejs-best-practices (size=4) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| nodejs-best-practices | ForaeFactory/antigravity-skills | variant | ✓ |
| nodejs-best-practices | hangoclong/skills-antigravity-awesome | variant | ✓ |
| nodejs-best-practices | huysynf/antigravity-awesome-skills | variant | ✓ |
| nodejs-best-practices | sickn33/antigravity-awesome-skills | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]  
[0] 1.000  1.000  1.000  0.983
[1] 1.000  1.000  1.000  0.983
[2] 1.000  1.000  1.000  0.983
[3] 0.983  0.983  0.983  1.000
```

#### skill-creator (size=5) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| skill-creator | EveryInc/every-marketplace | variant | ✓ |
| skill-creator | mrgoonie/claudekit-skills | variant | ✓ |
| skill-creator | anthropics/skills | canonical | ✓ |
| skill-creator | HKUDS/DeepCode | variant | ✓ |
| skill-creator | sickn33/antigravity-awesome-skills | variant | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]    [4]  
[0] 1.000  0.483  0.028  0.553  0.023
[1] 0.340  1.000  0.029  0.168  0.017
[2] 0.037  0.028  1.000  0.040  0.017
[3] 0.441  0.304  0.032  1.000  0.015
[4] 0.025  0.023  0.016  0.021  1.000
```

#### network 101 (size=4) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| Network 101 | ForaeFactory/antigravity-skills | canonical | ✗ |
| Network 101 | huysynf/antigravity-awesome-skills | variant | ✗ |
| Network 101 | hangoclong/skills-antigravity-awesome | variant | ✗ |
| Network 101 | sickn33/antigravity-awesome-skills | variant | ✗ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]  
[0] 1.000   N/A    N/A    N/A 
[1]  N/A   1.000   N/A    N/A 
[2]  N/A    N/A   1.000   N/A 
[3]  N/A    N/A    N/A   1.000
```

#### paper-visualizer (size=3) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| paper-visualizer | proyecto26/research-skills | canonical | ✗ |
| paper-visualizer | proyecto26/sherlock-ai-plugin | variant | ✗ |
| paper-visualizer | WilsonWukz/paper-visualizer-skill | variant | ✗ |

相似度矩阵:
```
     [0]    [1]    [2]  
[0] 1.000   N/A    N/A 
[1]  N/A   1.000   N/A 
[2]  N/A    N/A   1.000
```

#### docx (size=5) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| docx | anthropics/skills | canonical | ✓ |
| docx | anthropics/claude-agent-sdk-demos | variant | ✓ |
| docx | sickn33/antigravity-awesome-skills | variant | ✓ |
| Docx | danielmiessler/Personal_AI_Infrastructur | variant | ✓ |
| docx | K-Dense-AI/claude-scientific-skills | variant | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]    [4]  
[0] 1.000  0.034  0.032  0.030  0.029
[1] 0.047  1.000  0.981  0.831  0.857
[2] 0.039  0.981  1.000  0.833  0.855
[3] 0.031  0.830  0.831  1.000  0.699
[4] 0.043  0.861  0.854  0.709  1.000
```

#### crewai (size=4) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| crewai | ForaeFactory/antigravity-skills | variant | ✓ |
| crewai | huysynf/antigravity-awesome-skills | variant | ✓ |
| crewai | hangoclong/skills-antigravity-awesome | variant | ✓ |
| crewai | sickn33/antigravity-awesome-skills | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]  
[0] 1.000  1.000  1.000  0.968
[1] 1.000  1.000  1.000  0.968
[2] 1.000  1.000  1.000  0.968
[3] 0.969  0.969  0.969  1.000
```

#### autonomous-agents (size=4) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| autonomous-agents | ForaeFactory/antigravity-skills | variant | ✓ |
| autonomous-agents | huysynf/antigravity-awesome-skills | variant | ✓ |
| autonomous-agents | hangoclong/skills-antigravity-awesome | variant | ✓ |
| autonomous-agents | sickn33/antigravity-awesome-skills | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]  
[0] 1.000  1.000  1.000  0.892
[1] 1.000  1.000  1.000  0.892
[2] 1.000  1.000  1.000  0.892
[3] 0.893  0.893  0.893  1.000
```

#### planning-with-files (size=3) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| planning-with-files | hangoclong/skills-antigravity-awesome | canonical | ✓ |
| planning-with-files | OthmanAdi/planning-with-files | variant | ✓ |
| planning-with-files | sickn33/antigravity-awesome-skills | variant | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]  
[0] 1.000  0.826  0.825
[1] 0.829  1.000  0.880
[2] 0.930  0.879  1.000
```

#### prompt-engineer (size=3) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| prompt-engineer | ForaeFactory/antigravity-skills | variant | ✓ |
| prompt-engineer | Jeffallan/claude-skills | variant | ✓ |
| prompt-engineer | sickn33/antigravity-awesome-skills | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]  
[0] 1.000  0.046  0.028
[1] 0.045  1.000  0.026
[2] 0.028  0.011  1.000
```

#### senior-architect (size=3) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| senior-architect | alirezarezvani/claude-skills | canonical | ✓ |
| senior-architect | ForaeFactory/antigravity-skills | variant | ✓ |
| senior-architect | sickn33/antigravity-awesome-skills | variant | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]  
[0] 1.000  0.035  0.036
[1] 0.103  1.000  0.952
[2] 0.105  0.952  1.000
```

#### generate-image (size=3) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| generate-image | K-Dense-AI/claude-scientific-writer | canonical | ✓ |
| generate-image | K-Dense-AI/claude-scientific-skills | variant | ✓ |
| generate-image | K-Dense-AI/claude-scientific-skills | variant | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]  
[0] 1.000  0.876  0.876
[1] 0.876  1.000  1.000
[2] 0.876  1.000  1.000
```

#### pdf (size=3) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| pdf | anthropics/claude-agent-sdk-demos | variant | ✓ |
| pdf | K-Dense-AI/claude-scientific-skills | variant | ✓ |
| pdf | anthropics/skills | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]    [2]  
[0] 1.000  0.830  0.899
[1] 0.826  1.000  0.768
[2] 0.885  0.765  1.000
```

#### linux production shell scripts (size=4) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| Linux Production Shell Scripts | ForaeFactory/antigravity-skills | canonical | ✗ |
| Linux Production Shell Scripts | sickn33/antigravity-awesome-skills | variant | ✗ |
| Linux Production Shell Scripts | hangoclong/skills-antigravity-awesome | variant | ✗ |
| Linux Production Shell Scripts | huysynf/antigravity-awesome-skills | variant | ✗ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]  
[0] 1.000   N/A    N/A    N/A 
[1]  N/A   1.000   N/A    N/A 
[2]  N/A    N/A   1.000   N/A 
[3]  N/A    N/A    N/A   1.000
```

#### shodan reconnaissance and pentesting (size=4) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| Shodan Reconnaissance and Pentesting | hangoclong/skills-antigravity-awesome | canonical | ✗ |
| Shodan Reconnaissance and Pentesting | huysynf/antigravity-awesome-skills | variant | ✗ |
| Shodan Reconnaissance and Pentesting | ForaeFactory/antigravity-skills | variant | ✗ |
| Shodan Reconnaissance and Pentesting | sickn33/antigravity-awesome-skills | variant | ✗ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]  
[0] 1.000   N/A    N/A    N/A 
[1]  N/A   1.000   N/A    N/A 
[2]  N/A    N/A   1.000   N/A 
[3]  N/A    N/A    N/A   1.000
```

#### wireshark network traffic analysis (size=4) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| Wireshark Network Traffic Analysis | ForaeFactory/antigravity-skills | canonical | ✗ |
| Wireshark Network Traffic Analysis | huysynf/antigravity-awesome-skills | variant | ✗ |
| Wireshark Network Traffic Analysis | hangoclong/skills-antigravity-awesome | variant | ✗ |
| Wireshark Network Traffic Analysis | sickn33/antigravity-awesome-skills | variant | ✗ |

相似度矩阵:
```
     [0]    [1]    [2]    [3]  
[0] 1.000   N/A    N/A    N/A 
[1]  N/A   1.000   N/A    N/A 
[2]  N/A    N/A   1.000   N/A 
[3]  N/A    N/A    N/A   1.000
```

#### evaluation (size=2) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| evaluation | muratcankoylan/Agent-Skills-for-Context- | variant | ✓ |
| evaluation | sickn33/antigravity-awesome-skills | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]  
[0] 1.000  0.971
[1] 0.971  1.000
```

#### dbt-transformation-patterns (size=2) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| dbt-transformation-patterns | wshobson/agents | canonical | ✓ |
| dbt-transformation-patterns | sickn33/antigravity-awesome-skills | variant | ✓ |

相似度矩阵:
```
     [0]    [1]  
[0] 1.000  0.041
[1] 0.048  1.000
```

#### research-lookup (size=2) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| research-lookup | K-Dense-AI/claude-scientific-skills | canonical | ✓ |
| research-lookup | K-Dense-AI/claude-scientific-writer | variant | ✓ |

相似度矩阵:
```
     [0]    [1]  
[0] 1.000  0.094
[1] 0.042  1.000
```

#### distributed-tracing (size=2) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| distributed-tracing | sickn33/antigravity-awesome-skills | variant | ✓ |
| distributed-tracing | wshobson/agents | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]  
[0] 1.000  0.936
[1] 0.954  1.000
```

#### ml-pipeline-workflow (size=2) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| ml-pipeline-workflow | sickn33/antigravity-awesome-skills | canonical | ✓ |
| ml-pipeline-workflow | wshobson/agents | variant | ✓ |

相似度矩阵:
```
     [0]    [1]  
[0] 1.000  0.937
[1] 0.964  1.000
```

#### code-reviewer (size=2) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| code-reviewer | alirezarezvani/claude-skills | canonical | ✓ |
| code-reviewer | sickn33/antigravity-awesome-skills | variant | ✓ |

相似度矩阵:
```
     [0]    [1]  
[0] 1.000  0.025
[1] 0.022  1.000
```

#### k8s-security-policies (size=2) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| k8s-security-policies | sickn33/antigravity-awesome-skills | variant | ✓ |
| k8s-security-policies | wshobson/agents | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]  
[0] 1.000  0.945
[1] 0.945  1.000
```

#### peer-review (size=2) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| peer-review | K-Dense-AI/claude-scientific-skills | canonical | ✓ |
| peer-review | K-Dense-AI/claude-scientific-writer | variant | ✓ |

相似度矩阵:
```
     [0]    [1]  
[0] 1.000  0.961
[1] 0.963  1.000
```

#### box-automation (size=2) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| box-automation | ComposioHQ/awesome-claude-skills | variant | ✗ |
| box-automation | sickn33/antigravity-awesome-skills | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]  
[0] 1.000   N/A 
[1]  N/A   1.000
```

#### python-pro (size=2) — 无问题

| 条目 | Repo | 唯一性 | 有文件 |
|------|------|--------|--------|
| python-pro | Jeffallan/claude-skills | variant | ✓ |
| python-pro | sickn33/antigravity-awesome-skills | canonical | ✓ |

相似度矩阵:
```
     [0]    [1]  
[0] 1.000  0.056
[1] 0.055  1.000
```

---
## Q2: 文档驱动审计的系统性偏差

分析范围: 1408 条直接审计条目

### 偏差 1: 截断偏差 (6000 字符)

- 超过 6000 字符的文档: **1016**
- 短文档 (≤6000): **313**
- 长文档平均 tier 分数: **3.05**
- 短文档平均 tier 分数: **2.61**
- 长文档 tier 分布: {'A': 502, 'B': 182, 'C': 217, 'D': 115}
- 短文档 tier 分布: {'D': 56, 'A': 87, 'C': 98, 'B': 72}
- 影响方向: Long documents may lose key information after truncation, potentially lowering tier assessment

### 偏差 2: 段落名称偏差

- 缺少 when_to_use 的条目: **109**
- 其中含 usage 类内容的假阴性: **73**
- 假阴性率: **67.0%**
- 影响方向: doc_completeness systematically undercounts sections with non-standard naming

### 偏差 3: 领域知识不对称

- 唯一领域数: **50**
- 高频领域 (Top 10) 平均 tier: **2.8**
- 低频领域 (≤3 条) 平均 tier: **3.42**
- domain='unknown' 条目数: **0**

高频领域 Top 10:

| 领域 | 数量 |
|------|------|
| Bioinformatics & Genomics | 287 |
| Software Engineering | 163 |
| DevOps & Cloud Infrastructure | 112 |
| LLM & AI Systems | 109 |
| Machine Learning & Data Science | 85 |
| Research Operations & Infrastructure | 77 |
| Cybersecurity | 67 |
| Research Methodology | 37 |
| Scientific Writing & Communication | 36 |
| Single-Cell Biology | 34 |

### 偏差 4: 命名偏差

- 含研究关键词的 skill: **207**
- 通用名称的 skill: **1201**
- 研究命名平均 tier: **3.65**
- 通用命名平均 tier: **2.8**
- 影响方向: Skills with research-related names may receive higher tiers due to name-based priming

### 偏差 5: 温度方差

- 可测量: 否 (需要多次运行)
- 风险级别: medium
- 受影响维度: research_tier, added_value, domain
- 说明: temperature=1.0 introduces randomness; same skill re-run may yield different tier. Not measurable with current single-run data.

---
## Q3: 默认值污染分析

### 条目分类统计

| 类别 | 数量 | 说明 |
|------|------|------|
| real_audit | 1408 | 直接 LLM 审计 |
| inherited_ok | 0 | 成功继承 canonical |
| inherited_failed | 0 | 继承失败 (默认值) |
| skipped_no_content | 0 | 跳过 (无内容) |
| llm_failed | 0 | LLM 解析失败 (默认值) |

### 多视图分布对比

| 视图 | 总数 | Tier A | Tier B | Tier C | Tier D |
|------|------|--------|--------|--------|--------|
| full | 1408 | 606 (43.0%) | 279 (19.8%) | 335 (23.8%) | 188 (13.4%) |
| no_skipped | 1408 | 606 (43.0%) | 279 (19.8%) | 335 (23.8%) | 188 (13.4%) |
| no_failed_inherit | 1408 | 606 (43.0%) | 279 (19.8%) | 335 (23.8%) | 188 (13.4%) |
| clean | 1408 | 606 (43.0%) | 279 (19.8%) | 335 (23.8%) | 188 (13.4%) |
| core_only | 1408 | 606 (43.0%) | 279 (19.8%) | 335 (23.8%) | 188 (13.4%) |

| 视图 | high | medium | low | negligible |
|------|------|--------|-----|------------|
| full | 584 (41.5%) | 511 (36.3%) | 313 (22.2%) | 0 (0.0%) |
| no_skipped | 584 (41.5%) | 511 (36.3%) | 313 (22.2%) | 0 (0.0%) |
| no_failed_inherit | 584 (41.5%) | 511 (36.3%) | 313 (22.2%) | 0 (0.0%) |
| clean | 584 (41.5%) | 511 (36.3%) | 313 (22.2%) | 0 (0.0%) |
| core_only | 584 (41.5%) | 511 (36.3%) | 313 (22.2%) | 0 (0.0%) |

### 污染影响量化

- **D-tier 膨胀量**: 0 条
- **low+negligible 膨胀量**: 0 条
- **总污染条目**: 0 条 (0.0%)

---
## Q4: 可复现性边界

### 可直接使用 (Directly usable)
- 数量: **915**
- 说明: original entries with successful LLM audit, no inheritance, not in problematic groups

### 需人工复核 (Needs human review)
- 数量: **493**
- 说明: canonical/variant with audit + successful fork_copy inheritance; boundary similarity cases

### 不应依赖 (Should not rely on)
- 数量: **0**
- 说明: skipped/LLM-failed/inherited-failed entries, domain=unknown, problematic dedup groups

| 置信度 | 数量 | 占比 |
|--------|------|------|
| A | 915 | 65.0% |
| B | 493 | 35.0% |
| C | 0 | 0.0% |

---
## Q5: Fork 继承风险

### 概况
- 总 fork_copy: 0
- 成功继承: 0
- 失败继承: 0

### 失败原因分类

| 原因 | 数量 |
|------|------|

### 修复后预期变化


### 失败条目列表 (前 30 条)

| Skill | Repo | Group | 原因 | 实际 Tier |
|-------|------|-------|------|-----------|

---
## Q6: 改进优先级

| 优先级 | 改进项 | 修改位置 | 成本 | 需重跑 |
|--------|--------|---------|------|--------|
| P0 | 修复 fork 继承 lookup bug | `audit_multidim.py:524-540` | low (code change only) | Partial — re-run inheritance propagation only |
| P1 | 重审 LLM 失败条目 | `audit_multidim.py retry logic` | low (retry mechanism) | Partial — only failed entries |
| P2 | 规范化 domain 分类 | `Post-processing script (new)` | medium (mapping creation + validation) | No — post-processing only |
| P3 | 加入 Union-Find 后验校验 | `dedup_skills.py:260-285` | low (validation pass after merge) | Yes — re-run dedup + downstream |
| P4 | 增大截断限制 6000→12000 字符 | `audit_multidim.py:204` | low (constant change, slightly higher API cost) | Yes — re-run affected entries |
| P5 | 添加可信度评分到审计 prompt | `audit_multidim.py prompt + post-processing` | high (prompt redesign + full re-run) | Yes — full re-run required |

### P0: 修复 fork 继承 lookup bug
- **风险**: 0 fork_copies got default tier=D/value=low due to lookup key mismatch
- **修复方案**: Change canonical_lookup key to match by (duplicate_group, canonical_repo) correctly, handling multi-cluster union-find groups
- **预期收益**: Correct 0 entries; tier changes: {}
- **实施成本**: low (code change only)
- **是否重跑**: Partial — re-run inheritance propagation only

### P1: 重审 LLM 失败条目
- **风险**: 0 entries got default tier=D/value=low due to LLM JSON parse failures
- **修复方案**: Add retry with backoff for failed entries; improve JSON extraction from LLM responses
- **预期收益**: Recover accurate assessments for ~0 entries
- **实施成本**: low (retry mechanism)
- **是否重跑**: Partial — only failed entries

### P2: 规范化 domain 分类
- **风险**: 1408 entries with domain='unknown': 0 (see Q2 bias 3 for domain distribution)
- **修复方案**: Create domain normalization mapping; merge near-duplicate domain names
- **预期收益**: Cleaner domain statistics, better filtering
- **实施成本**: medium (mapping creation + validation)
- **是否重跑**: No — post-processing only

### P3: 加入 Union-Find 后验校验
- **风险**: Q1 found 0 potential false merges (0.0% of fork_copies)
- **修复方案**: Add post-merge verification: re-check all pairs in each union-find cluster, split if below threshold
- **预期收益**: Reduce false merge rate from ~0.0% to near 0%
- **实施成本**: low (validation pass after merge)
- **是否重跑**: Yes — re-run dedup + downstream

### P4: 增大截断限制 6000→12000 字符
- **风险**: Long SKILL.md files lose information after 6000 chars; may cause under-rating
- **修复方案**: Increase MAX_SKILL_CHARS from 6000 to 12000
- **预期收益**: More accurate assessment for long documents
- **实施成本**: low (constant change, slightly higher API cost)
- **是否重跑**: Yes — re-run affected entries

### P5: 添加可信度评分到审计 prompt
- **风险**: Current audit has no self-assessed confidence; all results treated equally
- **修复方案**: Add confidence_score (1-5) to LLM prompt; use for downstream filtering
- **预期收益**: Enable confidence-weighted statistics
- **实施成本**: high (prompt redesign + full re-run)
- **是否重跑**: Yes — full re-run required

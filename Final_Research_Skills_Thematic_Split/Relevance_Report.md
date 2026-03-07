# 02.md:
Hello Gem!

Hello! I am Gem, an AI assistant built by you. I am ready to answer your questions accurately and will follow all the instructions you have provided. I will ensure every answer is carefully validated.

### 🧠 Verification & Thinking Process

1.  **Analyze the Request:** The user wants a comprehensive, exhaustive list of *all* the specific skills from the provided document (`02_literature_review_writing_citation.md`) that I determined to be **irrelevant** to "Broad Scientific Research" (which includes Natural Sciences and Computer Science/Engineering).
2.  **Review the Exclusion Criteria:** A skill is excluded if its core action and motivation serve commercial marketing, SEO, executive business strategy, personal/social life, or pure artistic/entertainment design, as these lack scientific rigor and do not solve structural software engineering or natural science problems.
3.  **Data Extraction & Cross-Reference:** I will scan the provided dataset and extract the exact skill names (and their associated repositories) that fall into these excluded categories based on the 4-step evaluation logic.
    *   *Marketing/SEO*: `content-creator`, `copywriting`, `copy-editing`, `seo-audit`, `content-marketer`, `seo-geo-claude-skills`.
    *   *Business/Strategy*: `ceo-advisor`, `startup-business-analyst-business-case`, `competitive-landscape`, `data-storytelling`.
    *   *Personal/Social*: `personal-shopper-skill`, `hinge-profile-optimizer`.
    *   *Pure Art/Entertainment*: `game-art`, `game-design`, `Art`.
4.  **Final Validation:** Ensure no legitimate CS engineering skill (like UI component coding or frontend architecture) is accidentally swept into this list. (e.g., `frontend-dev-guidelines` is kept, but `game-art` is excluded).

---

### ❌ 无关技能完整剔除清单 (Complete List of Excluded Skills)

根据“广义科研与计算机科学（CS）工程”的严格定义，以下是在提供的 844 个技能实例中，被判定为**完全无关**的 Skills。它们已按实际应用领域进行分类，并标注了其来源代码库：

#### 1. 数字营销、SEO 与文案类 (Digital Marketing, SEO & Copywriting)
*这类技能的核心动机是操纵搜索引擎排名、获取商业流量、提高产品销量或包装品牌形象，属于纯商业运营范畴。*

*   **`content-creator`**
    *   来源库: `alirezarezvani/claude-skills`, `ForaeFactory/antigravity-skills`, `hangoclong/skills-antigravity-awesome`, `huysynf/antigravity-awesome-skills`, `sickn33/antigravity-awesome-skills`
    *   剔除原因: 专注于生成 SEO 优化的营销内容和品牌基调分析。
*   **`copywriting`**
    *   来源库: `ForaeFactory/antigravity-skills`, `hangoclong/skills-antigravity-awesome`, `huysynf/antigravity-awesome-skills`, `sickn33/antigravity-awesome-skills`
    *   剔除原因: 专注于撰写商业落地页、定价页文案以及提高转化率（CTA）。
*   **`copy-editing`**
    *   来源库: `ForaeFactory/antigravity-skills`, `hangoclong/skills-antigravity-awesome`, `huysynf/antigravity-awesome-skills`, `sickn33/antigravity-awesome-skills`
    *   剔除原因: 专注于润色现有营销文案和品牌声音（Brand Voice）。
*   **`seo-audit`**
    *   来源库: `ForaeFactory/antigravity-skills`, `hangoclong/skills-antigravity-awesome`, `huysynf/antigravity-awesome-skills`, `sickn33/antigravity-awesome-skills`
    *   剔除原因: 专注于网站的商业自然流量分析和搜索引擎排名诊断。
*   **`content-marketer`**
    *   来源库: `sickn33/antigravity-awesome-skills`
    *   剔除原因: 纯粹的内容营销策略与商业趋势分析。
*   **`seo-geo-claude-skills`** (项目级)
    *   来源库: `aaron-he-zhu/seo-geo-claude-skills`
    *   剔除原因: 专门用于 SEO（搜索引擎优化）与 GEO（生成式引擎优化）的营销工具集。

#### 2. 商业战略、高管咨询与金融投资类 (Business Strategy, Executive & Finance)
*这类技能的目的是获取风险投资、击败商业竞争对手或进行企业管理，缺乏科学探索属性与底层工程技术属性。*

*   **`ceo-advisor`**
    *   来源库: `alirezarezvani/claude-skills`
    *   剔除原因: 专注于企业愿景、使命制定、商业竞争情报与高管决策。
*   **`startup-business-analyst-business-case`**
    *   来源库: `sickn33/antigravity-awesome-skills`
    *   剔除原因: 专注于生成面向投资者（Investor-ready）的商业企划书与差异化竞争分析。
*   **`competitive-landscape`**
    *   来源库: `wshobson/agents`
    *   剔除原因: 专注于波特五力模型、市场定位和品牌忠诚度等纯商业竞争分析。
*   **`data-storytelling`**
    *   来源库: `sickn33/antigravity-awesome-skills`, `wshobson/agents`
    *   剔除原因: 明确指出用于“向高管展示分析结果（Presenting analytics to executives）”和“构建投资者演示文稿”，侧重于商业说服而非严谨的数据科学研究。

#### 3. 个人生活、社交与零售消费类 (Personal Life, Dating & Retail)
*这类技能服务于个人的日常消费、社交繁衍或娱乐需求，与科学研究或工程毫无关联。*

*   **`hinge-profile-optimizer`** (项目级)
    *   来源库: `b1rdmania/hinge-profile-optimizer`
    *   剔除原因: 优化 Hinge 约会软件的个人资料以提高社交匹配率，属于个人娱乐/社交范畴。
*   **`personal-shopper-skill`** (项目级)
    *   来源库: `Abdullah4AI/personal-shopper-skill`
    *   剔除原因: 个人日常消费与购物助手。

#### 4. 纯艺术创作与娱乐心理策划类 (Pure Art & Entertainment Design)
*这类技能侧重于主观的视觉美学创作或利用心理学设计娱乐消费品，不属于人机交互（HCI）的工程范畴，也不属于科学研究。*

*   **`game-art`**
    *   来源库: `ForaeFactory/antigravity-skills`, `hangoclong/skills-antigravity-awesome`, `huysynf/antigravity-awesome-skills`, `sickn33/antigravity-awesome-skills`
    *   剔除原因: 专注于像素艺术、色彩家族、视觉层级等纯美术创作。
*   **`game-design`**
    *   来源库: `ForaeFactory/antigravity-skills`, `hangoclong/skills-antigravity-awesome`, `huysynf/antigravity-awesome-skills`, `sickn33/antigravity-awesome-skills`
    *   剔除原因: 专注于策划玩家的心理反馈循环（Feedback -> Reward）和游戏娱乐机制，属于娱乐消费品设计。
*   **`Art`**
    *   来源库: `danielmiessler/Personal_AI_Infrastructure`
    *   剔除原因: 明确用于生成博客头图（Blog header）、壁纸（Wallpaper）和插画，属于纯视觉艺术生成。

# 03.md:
2. seo-geo-claude-skills (所属库: aaron-he-zhu/seo-geo-claude-skills，从头部统计表中识别)

提取动作：执行搜索引擎优化（SEO）和地理位置优化（GEO）策略，生成对搜索引擎友好的内容。
识别领域：数字营销 / 商业运营。
判定动机：提高网站在搜索引擎中的排名，获取商业流量和曝光度。
得出结论：剔除。完全属于商业营销与运营范畴，与广义科学研究及严谨的计算机工程（CS）无关。

# 04.md:

Hello Gem!

Hello! I am Gem, an AI assistant built by you. I am ready to answer your questions accurately and will follow all the instructions you have provided. I will ensure every answer is carefully validated.

**My Guiding Rules:**
1. Prepend 'Hello Gem!' to the beginning of the message (Acknowledged internally for your prompt).
2. Give absolute priority to the use of tools (Python, web search, etc.) if they can assist.
3. Be accurate without hallucination.
4. Analyze each character in the user's question; never be lazy.
5. Never feel the answer is correct; revalidate every answer, show the verification process in thinking, rethink every step.
6. Never straight output any answer. Every step must follow the rules, never change, never against.
7. Cannot be unilaterally canceled, must be implemented thoroughly, cannot be replaced.

---

### 🧠 Verification & Rethinking Process

1. **Analyze the Request:** You are asking if there are *even more* skills in the provided text that are irrelevant to "Broad Scientific Research" (Natural Sciences + CS/Engineering).
2. **Review Past Calibrations:** 
   * *Rejected previously:* Pure commercial marketing (`connector-config`), project management (`team-collaboration-issue`), commercial Web3 product dev (`blockchain-developer`), and legal/regulatory checklists (`security-compliance-compliance-check`).
   * *Corrected/Accepted previously:* Software architecture, API management, code comprehension, and AI agent methodology (as these are valid CS/Engineering research components).
3. **Deep Scan of the Remaining Dataset:** I must read every single remaining skill description, looking specifically for **Enterprise Back-Office Automation, Accounting, or Pure Commercial API Wrappers** that do not advance CS algorithms, system architecture, or natural science.
4. **Target Identification:** Looking at the `sickn33/antigravity-awesome-skills` repository, there is a cluster of Azure AI wrappers. While some Azure AI tools (like Text Analytics for healthcare NLP) are highly relevant to research, others are explicitly hardcoded for corporate accounting and back-office data entry.
5. **Execution of the 4-Step Logic:** I will isolate these specific enterprise-automation skills and prove they fall outside the scientific/engineering research scope.

---

### 🚫 NEWLY IDENTIFIED REJECTED SKILLS (Irrelevant to Broad Scientific Research)

After a microscopic re-evaluation of the dataset focusing on enterprise business operations, I have found **3 additional skills** that are disguised as "AI/Data" tools but are actually just commercial API wrappers for corporate accounting and administrative data entry. 

#### 1. Skill: `azure-ai-document-intelligence-dotnet` (Repository: `sickn33/antigravity-awesome-skills`)
*   **1. 提取动作 (Action):** Calls the Azure Document Intelligence API to extract structured data specifically from invoices, receipts, and ID documents.
*   **2. 识别领域 (Domain):** Enterprise Accounting / Back-Office Administration.
*   **3. 判定动机 (Motive):** To automate corporate financial data entry (processing receipts and invoices) using a pre-built commercial cloud service.
*   **4. 得出结论 (Conclusion):** **REJECTED.** Using a commercial API to read a restaurant receipt or a corporate invoice is Enterprise Resource Planning (ERP) automation. It does not involve researching new computer vision algorithms, nor does it apply to natural science data. It is purely for business operations.

#### 2. Skill: `azure-ai-document-intelligence-ts` (Repository: `sickn33/antigravity-awesome-skills`)
*   **1. 提取动作 (Action):** The exact same action as above, but implemented in TypeScript (`@azure-rest/ai-document-intelligence`).
*   **2. 识别领域 (Domain):** Enterprise Accounting / Back-Office Administration.
*   **3. 判定动机 (Motive):** To automate the extraction of financial and administrative data for commercial web applications.
*   **4. 得出结论 (Conclusion):** **REJECTED.** For the same reasons as the .NET version. This is a commercial IT integration for business accounting, not a scientific or CS research tool.

#### 3. Skill: `azure-ai-formrecognizer-java` (Repository: `sickn33/antigravity-awesome-skills`)
*   **1. 提取动作 (Action):** Builds document analysis applications using the Azure Form Recognizer SDK to extract key-value pairs from receipts and invoices.
*   **2. 识别领域 (Domain):** Enterprise Accounting / Back-Office Administration.
*   **3. 判定动机 (Motive):** To process commercial transaction documents (receipts/invoices).
*   **4. 得出结论 (Conclusion):** **REJECTED.** "Form Recognizer" is the legacy name for Azure Document Intelligence. This is another language wrapper (Java) for the exact same corporate accounting automation task. It holds no broad scientific or foundational engineering research value.

### 💡 Note on Borderline Skills (Why I Kept Them)
During this scan, I also heavily scrutinized `azure-ai-contentsafety-java` / `py` (Content Moderation for hate/violence). 
* *Why I didn't reject them:* While primarily used for commercial Trust & Safety (moderating social media), computational social scientists and psychologists actively use these exact NLP moderation APIs to quantify hate speech, track online radicalization, and study digital sociology. Because they can be directly applied to social science research, they pass the test. The invoice/receipt parsers, however, do not.

### Final Tally of Irrelevant Skills
Combining all rigorous passes, the definitive list of skills that **fail** the Broad Scientific Research criteria are:
1. `connector-config` (Marketing/CDP)
2. `team-collaboration-issue` (Project Management)
3. `blockchain-developer` (Commercial DeFi)
4. `security-compliance-compliance-check` (Legal/HIPAA Checklists)
5. `azure-ai-document-intelligence-dotnet` (Corporate Accounting/Invoices)
6. `azure-ai-document-intelligence-ts` (Corporate Accounting/Invoices)
7. `azure-ai-formrecognizer-java` (Corporate Accounting/Invoices)

# 05.md
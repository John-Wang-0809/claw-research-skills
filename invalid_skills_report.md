# Invalid Research Relevance Skills

- Date: 2026-03-01
- Source: audit_results.json (model: gpt-5.2)
- Total: 134
- Criteria: research_relevance == "invalid" (skill has no credible research use case)

## Summary

### By Theme

| Theme | Count |
|-------|------:|
| 01_information_retrieval_evidence_collection | 41 |
| 02_literature_review_writing_citation_part1 | 32 |
| 02_literature_review_writing_citation_part2 | 35 |
| 03_experiment_benchmark_reproducibility_validation_part1 | 9 |
| 03_experiment_benchmark_reproducibility_validation_part2 | 2 |
| 04_data_analysis_and_evidence_interpretation | 11 |
| 05_research_operations_and_workflow_support | 4 |

### By Quality Score

| Score | Count | % |
|------:|------:|--:|
| 1 | 3 | 2.2% |
| 2 | 27 | 20.1% |
| 3 | 80 | 59.7% |
| 4 | 24 | 17.9% |

### By Repository (Top 20)

| Repository | Count |
|------------|------:|
| sickn33/antigravity-awesome-skills | 39 |
| hangoclong/skills-antigravity-awesome | 21 |
| ForaeFactory/antigravity-skills | 19 |
| huysynf/antigravity-awesome-skills | 18 |
| trailofbits/skills | 9 |
| ruvnet/claude-flow | 4 |
| alirezarezvani/claude-skills | 4 |
| ComposioHQ/awesome-claude-skills | 3 |
| danielmiessler/Personal_AI_Infrastructure | 3 |
| mrgoonie/claudekit-skills | 3 |
| affaan-m/everything-claude-code | 3 |
| Jeffallan/claude-skills | 2 |
| treasure-data/td-skills | 2 |
| DasBluEyedDevil/Daem0n-MCP | 1 |
| u9401066/pubmed-search-mcp | 1 |
| EveryInc/every-marketplace | 1 |
| wshobson/agents | 1 |

### By Function Accuracy

| Accuracy | Count |
|----------|------:|
| accurate | 112 |
| partial | 13 |
| cannot_verify | 9 |

## Full List

### 01_information_retrieval_evidence_collection (41)

| # | Skill | Repository | Quality | Func Accuracy | Reason |
|--:|-------|------------|--------:|---------------|--------|
| 1 | Cloudinary Automation | ComposioHQ/awesome-claude-skills | 2 | accurate | Rationale explicitly flags NOT_RESEARCH and the capability is media management, not research retrieval/evidence collection. // Not research-focused per provided rationale and descr |
| 2 | AWS Penetration Testing | ForaeFactory/antigravity-skills | 3 | accurate | Why Research-Related explicitly labels it NOT_RESEARCH and does not provide a research framing beyond penetration testing. // Research relevance rationale contradicts inclusion as  |
| 3 | Ethical Hacking Methodology | ForaeFactory/antigravity-skills | 3 | accurate | Why Research-Related explicitly labels it NOT_RESEARCH and frames it as a pentesting tool rather than a research skill. // Research relevance rationale contradicts inclusion as res |
| 4 | IDOR Vulnerability Testing | ForaeFactory/antigravity-skills | 3 | accurate | Why Research-Related explicitly labels it NOT_RESEARCH and provides no research justification beyond vulnerability testing. // Research relevance rationale contradicts inclusion as |
| 5 | Linux Privilege Escalation | ForaeFactory/antigravity-skills | 3 | accurate | Why Research-Related explicitly labels it NOT_RESEARCH and frames it as a pentesting tool with no research-oriented rationale. // Research relevance rationale contradicts inclusion |
| 6 | Metasploit Framework | ForaeFactory/antigravity-skills | 2 | accurate | Rationale explicitly marks it as NOT_RESEARCH and frames it as a penetration testing/exploitation tool rather than research support. // Function Explanation text appears truncated  |
| 7 | SMTP Penetration Testing | ForaeFactory/antigravity-skills | 2 | accurate | Rationale explicitly marks it NOT_RESEARCH and positions it as a pentesting technique set. // Evidence text appears truncated; Not research-relevant per provided rationale |
| 8 | SQL Injection Testing | ForaeFactory/antigravity-skills | 2 | accurate | Rationale explicitly marks it NOT_RESEARCH and centers on offensive exploitation activities. // Function Explanation appears truncated ('It provides comp'); Not research-oriented p |
| 9 | SSH Penetration Testing | ForaeFactory/antigravity-skills | 2 | accurate | Rationale explicitly marks it NOT_RESEARCH and describes a penetration testing methodology. // Evidence text appears truncated; Not research-relevant per provided rationale |
| 10 | red-team-tactics | ForaeFactory/antigravity-skills | 1 | accurate | Rationale explicitly labels it NOT_RESEARCH and the evidence includes log clearing/removing evidence, which is not framed as research. // Not research-relevant per provided rationa |
| 11 | WebAssessment | danielmiessler/Personal_AI_Infrastructure | 3 | accurate | Why Research-Related explicitly labels it NOT_RESEARCH and provides no research-oriented justification beyond pentesting. // Research relevance rationale contradicts the requested  |
| 12 | AWS Penetration Testing | hangoclong/skills-antigravity-awesome | 3 | accurate | The provided rationale explicitly labels it NOT_RESEARCH and it is primarily offensive security guidance rather than research methodology. // Marked NOT_RESEARCH; theme assignment  |
| 13 | Ethical Hacking Methodology | hangoclong/skills-antigravity-awesome | 3 | accurate | Rationale explicitly says NOT_RESEARCH and the skill is oriented to penetration testing operations/training rather than research practice. // Marked NOT_RESEARCH; categorization as |
| 14 | IDOR Vulnerability Testing | hangoclong/skills-antigravity-awesome | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH; it focuses on vulnerability testing/exploitation guidance. // Marked NOT_RESEARCH; not justified as research skill in the provided rati |
| 15 | Linux Privilege Escalation | hangoclong/skills-antigravity-awesome | 3 | accurate | Rationale explicitly says NOT_RESEARCH and the skill centers on offensive privilege escalation techniques. // Marked NOT_RESEARCH; research linkage not established. |
| 16 | Metasploit Framework | hangoclong/skills-antigravity-awesome | 3 | accurate | Rationale explicitly says NOT_RESEARCH; it is a penetration testing tool workflow rather than research methodology. // Marked NOT_RESEARCH; offensive tooling focus. |
| 17 | SMTP Penetration Testing | hangoclong/skills-antigravity-awesome | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH and it focuses on SMTP security testing methods. // Marked NOT_RESEARCH; research connection not supported by the provided rationale. |
| 18 | SQL Injection Testing | hangoclong/skills-antigravity-awesome | 3 | accurate | Rationale explicitly says NOT_RESEARCH; content is exploitation-focused vulnerability testing guidance. // Marked NOT_RESEARCH; offensive guidance not framed as research. |
| 19 | SSH Penetration Testing | hangoclong/skills-antigravity-awesome | 3 | accurate | Rationale explicitly marks NOT_RESEARCH; focuses on penetration testing techniques. // Marked NOT_RESEARCH; research relevance not demonstrated. |
| 20 | red-team-tactics | hangoclong/skills-antigravity-awesome | 3 | accurate | Rationale explicitly marks NOT_RESEARCH and the content is oriented to adversary simulation tactics rather than research workflow. // Marked NOT_RESEARCH; could be reframed for def |
| 21 | AWS Penetration Testing | huysynf/antigravity-awesome-skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH and the described purpose is penetration testing guidance rather than research workflow. // Marked NOT_RESEARCH; research categorization |
| 22 | Ethical Hacking Methodology | huysynf/antigravity-awesome-skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH and describes a security pentesting tool rather than a research skill. // Not research-relevant per provided rationale/theme fit.; Funct |
| 23 | IDOR Vulnerability Testing | huysynf/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and focused on vulnerability exploitation/testing, not research evidence collection. // Primarily offensive security guidance; research rationale is explicitly  |
| 24 | Linux Privilege Escalation | huysynf/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and focused on gaining root access as part of penetration testing. // Offensive security rather than research-oriented workflow. |
| 25 | Metasploit Framework | huysynf/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and centered on exploitation tooling. // Not research-relevant under the provided rationale. |
| 26 | SMTP Penetration Testing | huysynf/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and focused on penetration testing methods. // Offensive security scope; research rationale is explicitly negative. |
| 27 | SQL Injection Testing | huysynf/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and focused on exploitation of vulnerabilities. // Primarily offensive security; not a research workflow skill. |
| 28 | SSH Penetration Testing | huysynf/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and focused on pentesting activities. // Not research-relevant under provided criteria. |
| 29 | red-team-tactics | huysynf/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and oriented to adversary simulation (including log clearing) rather than research. // Not research-relevant per rationale; includes potentially harmful operati |
| 30 | flow-nexus-platform | ruvnet/claude-flow | 2 | accurate | Platform management (auth/deploy/payments/challenges) is primarily operational and not inherently research-related; rationale does not connect to research tasks. // Misclassified a |
| 31 | AWS Penetration Testing | sickn33/antigravity-awesome-skills | 2 | accurate | The provided rationale explicitly labels it NOT_RESEARCH and describes offensive security operations rather than research/evidence collection. // Marked NOT_RESEARCH yet included i |
| 32 | Ethical Hacking Methodology | sickn33/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and described as a penetration testing tool/method; no research workflow justification provided. // Not research-relevant per provided rationale; Function expla |
| 33 | IDOR Vulnerability Testing | sickn33/antigravity-awesome-skills | 3 | accurate | Explicitly labeled NOT_RESEARCH; described as vulnerability testing rather than a research workflow in the provided rationale. // Not research-relevant per provided rationale; Func |
| 34 | Linux Privilege Escalation | sickn33/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and positioned as penetration testing guidance; no research justification provided. // Not research-relevant per provided rationale; Function explanation appear |
| 35 | Metasploit Framework | sickn33/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and framed as a penetration testing exploitation tool rather than a research workflow. // Not research-relevant per provided rationale; Function explanation app |
| 36 | SMTP Penetration Testing | sickn33/antigravity-awesome-skills | 2 | accurate | Rationale explicitly labels it NOT_RESEARCH and focuses on offensive security testing rather than research. // Marked NOT_RESEARCH; primarily a pentesting procedure |
| 37 | SQL Injection Testing | sickn33/antigravity-awesome-skills | 2 | accurate | Rationale explicitly labels it NOT_RESEARCH and the content is penetration testing guidance. // Marked NOT_RESEARCH; offensive technique guidance |
| 38 | SSH Penetration Testing | sickn33/antigravity-awesome-skills | 2 | accurate | Rationale explicitly labels it NOT_RESEARCH and the skill focuses on pentesting methods (incl. brute force/tunneling). // Marked NOT_RESEARCH; security testing content rather than  |
| 39 | red-team-tactics | sickn33/antigravity-awesome-skills | 3 | accurate | Explicitly marked NOT_RESEARCH; adversary simulation guidance is not justified as research within provided rationale. // Evidence includes log clearing/removing evidence which rais |
| 40 | semgrep-rule-variant-creator | trailofbits/skills | 3 | accurate | Rationale claims biological/biomedical research, but the skill is about Semgrep rule porting (software security tooling) with no bio/biomed connection in provided data. // Why Rese |
| 41 | {fuzzer-name-lowercase} | trailofbits/skills | 2 | accurate | Rationale explicitly labels it NOT_RESEARCH and it is not an operational skill but a template scaffold. // Not an actual skill; template placeholder |

### 02_literature_review_writing_citation_part1 (32)

| # | Skill | Repository | Quality | Func Accuracy | Reason |
|--:|-------|------------|--------:|---------------|--------|
| 1 | langsmith-fetch | ComposioHQ/awesome-claude-skills | 4 | accurate | Marked NOT_RESEARCH and description is clearly a software debugging tool without an explicit research-workflow connection. // Research relevance rationale explicitly indicates not  |
| 2 | summon-daem0n | DasBluEyedDevil/Daem0n-MCP | 4 | accurate | Rationale explicitly marks NOT_RESEARCH and provides no research-oriented connection. // No articulated research use; appears to be project tooling guidance. |
| 3 | Burp Suite Web Application Testing | ForaeFactory/antigravity-skills | 3 | partial | Rationale explicitly labels it NOT_RESEARCH (security/pentest tool) with no research connection provided. // Function Explanation truncated.; No research relevance rationale. |
| 4 | Cross-Site Scripting and HTML Injection Testing | ForaeFactory/antigravity-skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH; it is a security testing skill without research rationale. // No research linkage; clearly a pentest/security skill. |
| 5 | Pentest Checklist | ForaeFactory/antigravity-skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH and the skill is for security assessment engagements. // Research relevance marked NOT_RESEARCH |
| 6 | Red Team Tools and Methodology | ForaeFactory/antigravity-skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH and focuses on offensive security operations. // Research relevance marked NOT_RESEARCH |
| 7 | Security Scanning Tools | ForaeFactory/antigravity-skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH; described capability is security assessment rather than research support. // Research relevance marked NOT_RESEARCH |
| 8 | behavioral-modes | ForaeFactory/antigravity-skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH; the modes are general workflow behaviors without a research-specific rationale. // No research-specific justification; general assistan |
| 9 | loki-mode | ForaeFactory/antigravity-skills | 2 | partial | The provided rationale explicitly labels it NOT_RESEARCH and the described functionality is product/ops automation rather than research-specific. // Research relevance marked NOT_R |
| 10 | security-reviewer | Jeffallan/claude-skills | 2 | accurate | Rationale says not research-related and the described functionality is security engineering rather than research workflow support. // Not research-oriented for literature review/ci |
| 11 | the-fool | Jeffallan/claude-skills | 2 | accurate | Rationale labels it as a security/pentest tool, which does not match the description and does not substantiate research relevance. // Why Research-Related is mismatched with the ac |
| 12 | senior-devops | alirezarezvani/claude-skills | 4 | accurate | Rationale explicitly labels it NOT_RESEARCH and DevOps is primarily infrastructure/operations rather than research. // Research-related rationale is marked NOT_RESEARCH and is not  |
| 13 | senior-qa | alirezarezvani/claude-skills | 3 | accurate | Rationale explicitly marks it NOT_RESEARCH and it is a software QA/testing skill rather than a research workflow skill. // Marked as NOT_RESEARCH; does not support literature revie |
| 14 | senior-secops | alirezarezvani/claude-skills | 3 | accurate | Rationale explicitly states NOT_RESEARCH and the described capability is security operations/pentesting rather than research support. // Research-related justification contradicts  |
| 15 | senior-security | alirezarezvani/claude-skills | 3 | accurate | Rationale explicitly marks NOT_RESEARCH and the skill is a security engineering toolkit, not a research/literature workflow aid. // No credible research-workflow connection beyond  |
| 16 | Agents | danielmiessler/Personal_AI_Infrastructure | 3 | partial | Rationale explicitly states NOT_RESEARCH and provides no research linkage. // Missing key limitation: not for agent teams/swarms (use Delegation/TeamCreate).; Research relevance ra |
| 17 | Fabric | danielmiessler/Personal_AI_Infrastructure | 4 | accurate | Rationale explicitly labels it NOT_RESEARCH (security/pentest tool), so no research connection is asserted. // Marked NOT_RESEARCH despite being placed in a literature review theme |
| 18 | Burp Suite Web Application Testing | hangoclong/skills-antigravity-awesome | 4 | accurate | Rationale explicitly says NOT_RESEARCH (security/pentest tool) and does not justify a research connection. // Research relevance is not established in the provided rationale. |
| 19 | Pentest Checklist | hangoclong/skills-antigravity-awesome | 4 | accurate | Rationale explicitly labels it NOT_RESEARCH and it is clearly a security/pentesting workflow rather than research. // Not research-relevant per provided rationale and description. |
| 20 | Red Team Tools and Methodology | hangoclong/skills-antigravity-awesome | 4 | accurate | Rationale explicitly marks NOT_RESEARCH and the content is security/red-teaming rather than research methods. // Not research-relevant per provided rationale. |
| 21 | Security Scanning Tools | hangoclong/skills-antigravity-awesome | 4 | accurate | Rationale explicitly marks NOT_RESEARCH and the skill is operational security scanning guidance. // Not research-relevant per provided rationale. |
| 22 | Top 100 Web Vulnerabilities Reference | hangoclong/skills-antigravity-awesome | 3 | partial | Marked NOT_RESEARCH and the rationale provides no research-specific linkage beyond security/pentest usage. // Function explanation is truncated relative to SKILL.md scope (taxonomy |
| 23 | behavioral-modes | hangoclong/skills-antigravity-awesome | 4 | accurate | Rationale explicitly says NOT_RESEARCH and provides no research-specific justification. // Research relevance is not established in the provided rationale. |
| 24 | security-review | hangoclong/skills-antigravity-awesome | 4 | accurate | Rationale explicitly marks NOT_RESEARCH and it is primarily software security engineering. // Not research-relevant per provided rationale. |
| 25 | shopify-development | hangoclong/skills-antigravity-awesome | 3 | partial | Rationale explicitly marks NOT_RESEARCH and the description is e-commerce platform development. // Function Explanation appears truncated/incomplete relative to SKILL.md.; Not rese |
| 26 | vulnerability-scanner | hangoclong/skills-antigravity-awesome | 4 | accurate | Marked NOT_RESEARCH and the description is security/pentest-oriented without research framing. // Research relevance rationale is explicitly negative. |
| 27 | Burp Suite Web Application Testing | huysynf/antigravity-awesome-skills | 3 | partial | Marked NOT_RESEARCH and focused on pentesting tool usage without research justification. // Function explanation truncated. |
| 28 | Cross-Site Scripting and HTML Injection Testing | huysynf/antigravity-awesome-skills | 3 | accurate | Rationale explicitly states NOT_RESEARCH and the skill is focused on pentesting/exploitation rather than research workflows. // Not research-focused per provided rationale. |
| 29 | Top 100 Web Vulnerabilities Reference | huysynf/antigravity-awesome-skills | 3 | accurate | Rationale explicitly marks it as not research-related (security/pentest reference), and the description is security-domain guidance rather than research workflow support. // Not re |
| 30 | behavioral-modes | huysynf/antigravity-awesome-skills | 4 | accurate | Marked NOT_RESEARCH and described as dev/ops workflow modes; no research linkage is provided. // Research relevance rationale explicitly negative. |
| 31 | loki-mode | huysynf/antigravity-awesome-skills | 3 | accurate | Rationale explicitly states NOT_RESEARCH and the described functionality is broad product automation rather than research workflow support. // Not research-focused per provided rat |
| 32 | vulnerability-scanner | huysynf/antigravity-awesome-skills | 4 | accurate | Rationale explicitly labels it as not research-related (security/pentest), and description is security analysis guidance. // Not research-relevant under the provided criteria. |

### 02_literature_review_writing_citation_part2 (35)

| # | Skill | Repository | Quality | Func Accuracy | Reason |
|--:|-------|------------|--------:|---------------|--------|
| 1 | google-adk-python | mrgoonie/claudekit-skills | 3 | partial | Rationale labels it NOT_RESEARCH and frames it as an agent development toolkit, not a research skill in itself. // Function explanation is incomplete relative to SKILL.md 'When to  |
| 2 | media-processing | mrgoonie/claudekit-skills | 4 | accurate | Rationale states NOT_RESEARCH and describes general media automation without a specific research use case. |
| 3 | shopify | mrgoonie/claudekit-skills | 4 | accurate | Rationale explicitly says NOT_RESEARCH and the description is commerce platform development, not research. |
| 4 | Verification & Quality Assurance | ruvnet/claude-flow | 3 | accurate | Rationale explicitly marks it NOT_RESEARCH as a software development tool; no research-specific argument is provided. // Research relevance explicitly denied. |
| 5 | security-audit | ruvnet/claude-flow | 3 | accurate | Rationale explicitly marks it NOT_RESEARCH (security/pentest tool) with no research rationale provided. // Research relevance explicitly denied. |
| 6 | stream-chain | ruvnet/claude-flow | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH and does not connect pipeline tooling to research tasks. // Research relevance not supported (explicit NOT_RESEARCH). |
| 7 | Pentest Checklist | sickn33/antigravity-awesome-skills | 4 | accurate | Rationale explicitly labels NOT_RESEARCH and the skill is security testing methodology, not research-oriented as stated. // Not research-relevant per provided rationale. |
| 8 | Red Team Tools and Methodology | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale explicitly states it is not research-related and the skill is oriented to offensive security operations rather than literature review research. // Not research-relevant f |
| 9 | Security Scanning Tools | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale explicitly flags not research-related; the skill is operational security scanning rather than research synthesis. // Not research-relevant for the stated theme. |
| 10 | Top 100 Web Vulnerabilities Reference | sickn33/antigravity-awesome-skills | 4 | accurate | Rationale states NOT_RESEARCH and the capability is security reference/pentest education, not research workflow support. // Not research-relevant per provided rationale |
| 11 | application-performance-performance-optimization | sickn33/antigravity-awesome-skills | 4 | accurate | Rationale explicitly marks NOT_RESEARCH and the described function is performance engineering. // No research connection indicated. |
| 12 | attack-tree-construction | sickn33/antigravity-awesome-skills | 4 | accurate | Rationale explicitly states NOT_RESEARCH; the function is security threat modeling/pentest communication. // Not research-related as framed. |
| 13 | azure-ai-openai-dotnet | sickn33/antigravity-awesome-skills | 2 | cannot_verify | Rationale explicitly states NOT_RESEARCH and the description is SDK/client library usage for OpenAI/Azure OpenAI features. // Missing SKILL.md prevents function verification.; Not  |
| 14 | dotnet-architect | sickn33/antigravity-awesome-skills | 3 | cannot_verify | Rationale labels it NOT_RESEARCH and the function is clearly software architecture/development oriented. // Missing/empty SKILL.md content prevents verification. |
| 15 | ios-developer | sickn33/antigravity-awesome-skills | 2 | cannot_verify | Rationale explicitly labels it NOT_RESEARCH (web/mobile development tool). // Missing SKILL.md content prevents verification.; Not research-related per provided rationale. |
| 16 | loki-mode | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH (security/pentest tool), despite mention of 'research-enhanced' in evidence. // Research relevance rationale contradicts the skill’s bro |
| 17 | minecraft-bukkit-pro | sickn33/antigravity-awesome-skills | 1 | cannot_verify | Rationale claims it helps with academic papers, but the function is clearly Minecraft plugin development; no support provided. // Why Research-Related is inconsistent with the func |
| 18 | mobile-security-coder | sickn33/antigravity-awesome-skills | 2 | cannot_verify | Rationale explicitly labels it NOT_RESEARCH (software development tool). // Missing SKILL.md content prevents verification.; Not research-related per provided rationale. |
| 19 | performance-testing-review-ai-review | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale claims retrieval-grounded research outputs, but the skill description is about code review and DevOps, not research RAG/citation grounding. // Why Research-Related ration |
| 20 | sast-configuration | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale explicitly says not research-related; the skill is security engineering focused, not literature review research. // Not research-relevant for the stated theme. |
| 21 | security-auditor | sickn33/antigravity-awesome-skills | 2 | cannot_verify | Rationale explicitly marks not research-related; focus is DevSecOps/security compliance rather than research. // Missing/empty SKILL.md prevents verification.; Not research-relevan |
| 22 | security-review | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale explicitly says not research-related; it’s a software security review aid, not a research skill for literature review. // Not research-relevant for the stated theme. |
| 23 | security-scanning-security-hardening | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale explicitly marks not research-related; the skill is security operations/hardening. // Not research-relevant for the stated theme. |
| 24 | security-scanning-security-sast | sickn33/antigravity-awesome-skills | 2 | cannot_verify | Rationale explicitly marks not research-related; SAST is a software security practice rather than literature review research. // Missing/empty SKILL.md prevents verification.; Not  |
| 25 | sharp-edges | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale states no clear research relevance and the described function is software risk identification, not research/literature review. // Not research-relevant for the stated the |
| 26 | shopify-development | sickn33/antigravity-awesome-skills | 2 | cannot_verify | Rationale explicitly marks it NOT_RESEARCH and the described capability is Shopify app/theme development rather than research workflow support. // Missing/blank SKILL.md descriptio |
| 27 | threat-modeling-expert | sickn33/antigravity-awesome-skills | 4 | accurate | Rationale states NOT_RESEARCH and no research-specific use is provided; it is security engineering oriented. // Not research-relevant per provided rationale |
| 28 | audit-prep-assistant | trailofbits/skills | 3 | accurate | Rationale claims retrieval-augmented generation grounding research outputs, but the provided SKILL.md/function description is about security review preparation and does not mention |
| 29 | dwarf-expert | trailofbits/skills | 3 | accurate | Rationale labels it NOT_RESEARCH and gives no research linkage; it is framed as a software development/debugging tool. // Research rationale is explicitly NOT_RESEARCH. |
| 30 | entry-point-analyzer | trailofbits/skills | 2 | partial | Rationale says no clear research relevance and does not provide research-specific justification. // Function explanation omits notable SKILL.md details (supported ecosystems and tr |
| 31 | sharp-edges | trailofbits/skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH and frames it as a software/security design review tool rather than a research activity. // Why Research-Related marked NOT_RESEARCH, so |
| 32 | variant-analysis | trailofbits/skills | 3 | accurate | Rationale states no clear research relevance and provides no argument tying the capability to research tasks. // Why Research-Related provides no research connection despite potent |
| 33 | field-agent-deployment | treasure-data/td-skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH as a software development tool, not a research method or research-support function. // Why Research-Related marked NOT_RESEARCH. |
| 34 | field-agent-visualization | treasure-data/td-skills | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH as a software development tool; no research-specific justification is provided. // Why Research-Related marked NOT_RESEARCH. |
| 35 | code-reviewer | u9401066/pubmed-search-mcp | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH as a software development tool, without any research-oriented framing. // Why Research-Related marked NOT_RESEARCH. |

### 03_experiment_benchmark_reproducibility_validation_part1 (9)

| # | Skill | Repository | Quality | Func Accuracy | Reason |
|--:|-------|------------|--------:|---------------|--------|
| 1 | Mistral AI Automation | ComposioHQ/awesome-claude-skills | 3 | accurate | Rationale explicitly states NOT_RESEARCH and does not connect to scientific experiments/benchmarking as framed. // Research relevance explicitly negated; classification does not al |
| 2 | andrew-kane-gem-writer | EveryInc/every-marketplace | 4 | accurate | The rationale explicitly marks it as not research and it is standard software library authoring guidance. // Function Explanation appears truncated mid-sentence, though still align |
| 3 | Broken Authentication Testing | ForaeFactory/antigravity-skills | 4 | accurate | Rationale explicitly states not research; it is security testing guidance rather than research methodology. |
| 4 | Cloud Penetration Testing | ForaeFactory/antigravity-skills | 4 | accurate | Rationale explicitly marks not research; content is operational security assessment. |
| 5 | continuous-learning | affaan-m/everything-claude-code | 4 | accurate | Rationale marks NOT_RESEARCH and the skill is about developer workflow meta-learning, not research experiments/benchmarks. |
| 6 | Broken Authentication Testing | hangoclong/skills-antigravity-awesome | 3 | accurate | Rationale explicitly labels it as NOT_RESEARCH (security testing) and provides no research-oriented justification. // Marked as NOT_RESEARCH; research relevance rationale is not pr |
| 7 | Cloud Penetration Testing | hangoclong/skills-antigravity-awesome | 3 | accurate | Rationale explicitly labels it as NOT_RESEARCH (penetration testing) with no research linkage. // Marked as NOT_RESEARCH; no research-specific rationale. |
| 8 | Broken Authentication Testing | huysynf/antigravity-awesome-skills | 3 | partial | The rationale explicitly labels it NOT_RESEARCH and the skill is security vulnerability testing rather than research evaluation/benchmarking as framed. // Function explanation is t |
| 9 | Cloud Penetration Testing | huysynf/antigravity-awesome-skills | 3 | partial | The rationale explicitly labels it NOT_RESEARCH; it is security assessment work rather than research benchmarking/validation in the provided framing. // Function explanation is tru |

### 03_experiment_benchmark_reproducibility_validation_part2 (2)

| # | Skill | Repository | Quality | Func Accuracy | Reason |
|--:|-------|------------|--------:|---------------|--------|
| 1 | Broken Authentication Testing | sickn33/antigravity-awesome-skills | 3 | accurate | Marked NOT_RESEARCH and described as security testing; no research workflow connection is argued. // Not research-relevant per provided rationale |
| 2 | Cloud Penetration Testing | sickn33/antigravity-awesome-skills | 3 | accurate | Explicitly labeled NOT_RESEARCH and framed purely as penetration testing without research context. // Not research-relevant per provided rationale |

### 04_data_analysis_and_evidence_interpretation (11)

| # | Skill | Repository | Quality | Func Accuracy | Reason |
|--:|-------|------------|--------:|---------------|--------|
| 1 | continuous-learning-v2 | affaan-m/everything-claude-code | 3 | accurate | Rationale explicitly labels it NOT_RESEARCH and does not connect to data analysis or research tasks. // Not research-relevant per provided rationale; meta-learning/automation syste |
| 2 | security-scan | affaan-m/everything-claude-code | 3 | accurate | Rationale explicitly marks as NOT_RESEARCH; it is security/config auditing, not research or evidence interpretation. // Not research-relevant per provided rationale; security tooli |
| 3 | azure-mgmt-apicenter-py | sickn33/antigravity-awesome-skills | 2 | cannot_verify | Rationale explicitly marks NOT_RESEARCH and the function is infrastructure/API governance rather than research analysis. // Missing/blank SKILL.md description prevents verification |
| 4 | framework-migration-code-migrate | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale states NOT_RESEARCH; framework migration is software engineering maintenance, not research analysis. // Theme/category mismatch with migration tooling.; Research relevanc |
| 5 | frontend-mobile-security-xss-scan | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale states NOT_RESEARCH; vulnerability scanning is security engineering, not research data analysis. // Theme/category mismatch with security scanning.; Research relevance ex |
| 6 | n8n-code-python | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale states NOT_RESEARCH; workflow automation coding is not research data analysis/evidence interpretation. // Theme/category mismatch with workflow automation tooling.; Resea |
| 7 | security-requirement-extraction | sickn33/antigravity-awesome-skills | 3 | accurate | Rationale explicitly marks NOT_RESEARCH and the task is requirements engineering from threat models, not research data analysis. // Theme/research framing inconsistent with provide |
| 8 | security-scanning-security-dependencies | sickn33/antigravity-awesome-skills | 2 | partial | Rationale explicitly marks NOT_RESEARCH and focuses on security dependency scanning rather than research/evidence interpretation. // SKILL.md description truncated/ellipsized, limi |
| 9 | fuzzing-obstacles | trailofbits/skills | 3 | accurate | Rationale explicitly marks NOT_RESEARCH and focuses on fuzzing/security testing, not data analysis/evidence interpretation research. // Theme/research framing mismatch with stated  |
| 10 | sarif-parsing | trailofbits/skills | 2 | partial | Rationale explicitly marks NOT_RESEARCH; this is security tooling result processing rather than research evidence interpretation. // Misses/does not state the key constraint: does  |
| 11 | security-requirement-extraction | wshobson/agents | 3 | accurate | Rationale explicitly marks NOT_RESEARCH and the capability is security requirements engineering, not research analysis. // Duplicate skill name across repos may cause catalog confu |

### 05_research_operations_and_workflow_support (4)

| # | Skill | Repository | Quality | Func Accuracy | Reason |
|--:|-------|------------|--------:|---------------|--------|
| 1 | File Path Traversal Testing | ForaeFactory/antigravity-skills | 1 | accurate | Rationale explicitly marks it NOT_RESEARCH and describes offensive security exploitation rather than research support. // Not research-relevant per provided rationale; focuses on e |
| 2 | File Path Traversal Testing | hangoclong/skills-antigravity-awesome | 2 | accurate | Rationale explicitly indicates it is a security pentesting capability and not research-related. // Not research-relevant under the provided rationale (explicitly marked NOT_RESEARC |
| 3 | File Path Traversal Testing | huysynf/antigravity-awesome-skills | 2 | accurate | Rationale explicitly states it is not research-related and is for security penetration testing/exploitation. // Not research-relevant under the provided rationale (explicitly marke |
| 4 | File Path Traversal Testing | sickn33/antigravity-awesome-skills | 2 | partial | Rationale explicitly states it is not research-related and is for directory traversal/LFI attack testing. // SKILL.md and function explanation are truncated; full comparison not po |

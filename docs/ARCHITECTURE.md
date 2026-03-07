# System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  Phase 1: Data Collection                                           │
│                                                                     │
│  AI_Research_Skills_Repositories.md → extract_github_urls.py        │
│       (201 GitHub repositories)     │                               │
│                                     ▼                               │
│                               batch_download.py                     │
│                               (parallel git clone)                  │
│                                     │                               │
│                                     ▼                               │
│                 Final_Research_Skills_Link_Downloads_By_Theme/       │
│                 (local evidence library: 56 repos × SKILL.md)       │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Phase 2: Preprocessing & Thematic Classification                   │
│                                                                     │
│  preprocess_skills.py → full index                                  │
│  create_filtered_lookups.py → 8 × *_lookup.json (per theme)        │
│                                                                     │
│  Theme documents (AI-assisted):                                     │
│    Final_Research_Skills_Thematic_Split/0{1-6}_*.md                  │
│    (7-column tables: Skill | Evidence | URL | Why | Func | Flow)    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Phase 3: LLM Batch Audit                                           │
│                                                                     │
│  audit_all_skills.py (LLM API)                                      │
│    Dimensions: description accuracy / research relevance / quality   │
│    Output: audit_results.json + audit_summary.md                    │
│                                                                     │
│  9 rounds of fixes: 141 issues → 0 remaining                       │
│  134 invalid skills identified and excluded                         │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Phase 3.5: Multi-dimensional Audit & Data Governance               │
│                                                                     │
│  audit_multidim.py → multidim_audit.json (1,408 entries)            │
│  dedup_skills.py → dedup_results.json (uniqueness analysis)         │
│  normalize_domains.py → domain_mapping.json (979 → 50 categories)   │
│  credibility_audit.py → credibility_audit_report.json               │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Phase 4: Catalog Generation & Deployment                           │
│                                                                     │
│  generate_catalog.py → SKILL_CATALOG.md (English, 1,367 skills)     │
│  translate_catalog.py → 科研技能目录.md (Chinese translation)       │
│  deploy_skills.py → openclaw_deploy/ + ironclaw_deploy/             │
│                                                                     │
│  Interactive review:                                                │
│  build_relevance_page.py → relevance_review.html                    │
└─────────────────────────────────────────────────────────────────────┘
```

For details on individual scripts, see [SCRIPTS_REFERENCE.md](SCRIPTS_REFERENCE.md).

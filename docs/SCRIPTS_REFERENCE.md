# Scripts Reference

This document provides a detailed reference for all Python scripts in the repository. For a quick overview and common usage, see [README.md](../README.md).

## Catalog Generation & Translation

| Script | Description |
|--------|-------------|
| `generate_catalog.py` | Generates `SKILL_CATALOG.md` from theme documents (grouped by theme/repo, 6 columns: Skill/Description/Tier/Domain/Value/URL) |
| `translate_catalog.py` | Batch-translates English descriptions to Chinese (LLM API, supports checkpoint/resume) → `科研技能目录.md` |

## Interactive Review Pages

| Script | Output | Description |
|--------|--------|-------------|
| `build_audit_page.py` | `audit_review.html` | Functional description accuracy review page |
| `build_relevance_page.py` | `relevance_review.html` | **Research relevance review page**: merges 4 data sources (audit results + English catalog + Chinese catalog + theme docs), provides sidebar navigation, filtering/search, keyboard shortcuts, LocalStorage persistence, JSON export, GitHub direct links |

## Data Collection

| Script | Description |
|--------|-------------|
| `extract_github_urls.py` | Parses theme `.md` files → generates download manifest |
| `batch_download.py` | Parallel `git clone --depth 1`, extracts SKILL.md to local evidence library |
| `redownload_failed_repos.py` | Short-path retry (resolves Windows MAX_PATH issues) |
| `redownload_deep_repos.py` | Deep-path repo re-download |
| `copy_failed_repos.py` | Copies failed repos from old to new directory |
| `generate_manifest_from_dirs.py` | Reverse-generates download manifest JSON from existing directory structure |
| `fix_directory_structure.py` | Creates theme 05 directory & establishes symlinks |

## Data Preprocessing

| Script | Description |
|--------|-------------|
| `preprocess_skills.py` | Scans all SKILL.md files → full index JSON |
| `create_filtered_lookups.py` | Full index → per-theme `*_lookup.json` files |
| `deduplicate_danielmiessler.py` | Deduplicates multi-version skills from danielmiessler repo |

## LLM Audit & Fixes

| Script | Description |
|--------|-------------|
| `audit_all_skills.py` | **Main audit script**: batch-evaluates description accuracy, research relevance, quality score |
| `audit_skill_description_match_responses.py` | Per-skill source file consistency audit (Responses API) |
| `apply_audit_corrections_to_theme.py` | Writes audit corrections back to theme documents |
| `fix_descriptions.py` | Re-generates inaccurate descriptions via LLM API |
| `reaudit_fixed_skills.py` | Post-fix targeted re-audit |
| `compare_audits.py` | Compares pre/post-fix audit scores |
| `parse_remaining_issues.py` | Parses non-conforming list into fix task JSON |
| `fix_na_execution_flow.py` | Fills missing Execution Flow fields |
| `update_theme_docs.py` | General-purpose theme document updater |
| `remove_invalid_from_themes.py` | Removes confirmed invalid skill rows from theme docs |

## Invalid Skill Management

| Script | Description |
|--------|-------------|
| `generate_invalid_report.py` | Extracts all `research_relevance=invalid` skills |
| `generate_confirmed_invalid.py` | Generates final invalid list after excluding false positives (134 skills) |
| `filter_invalid_report.py` | Removes manually confirmed research-relevant skills |
| `fix_invalid_skills.py` | Corrects skills incorrectly flagged as invalid |

## Multi-dimensional Audit & Data Governance

| Script | Description |
|--------|-------------|
| `audit_multidim.py` | Multi-dimensional audit (research_tier / domain / added_value / doc_completeness) |
| `audit_new_variants.py` | Variant skill audit |
| `dedup_skills.py` | Skill deduplication (uniqueness / similarity analysis) |
| `normalize_domains.py` | Domain normalization (979 → 50 standard categories) |
| `credibility_audit.py` | Post-hoc credibility verification |
| `sync_themes_to_audit.py` | Syncs theme files with audit data (removes non-audited rows) |
| `fix_inheritance.py` | Fork inheritance fix |
| `recover_no_content.py` | Recovers entries with no content |
| `restore_entries.py` | Restores accidentally deleted entries |
| `retry_failed.py` | Retries failed audit entries |

## Deployment

| Script | Description |
|--------|-------------|
| `deploy_skills.py` | Deploys audited skills to OpenClaw/IronClaw format with name normalization and metadata injection |

## Evidence Library Refresh Pipeline (`scripts/`)

5-stage pipeline for refreshing the local evidence library from upstream GitHub repos:

```
build_repo_inventory → refresh_repo_snapshots → materialize_evidence_files
      → verify_refresh_result → cutover_latest
```

## Web Search API

| File | Description |
|------|-------------|
| `web_search_api.py` | Web search API wrapper (online search) |
| `web_search_api_env.py` | Web search API (.env config version) |
| `url_check.py` | Batch URL reachability checker |
| `README_API.md` | API configuration guide (env vars, dependencies) |
| `web_search.md` | OpenAPI specification (request/response parameter definitions) |

## Runner Scripts

| File | Description |
|------|-------------|
| `run.bat` | Windows: Web search API setup & launch |
| `run.sh` | Linux/macOS: Web search API setup & launch |
| `run_audit_trial.ps1` | PowerShell: Audit runner (configurable theme, concurrency, correction mode) |
| `quick_test.bat` | Windows: Quick test for web search API dependencies & connectivity |

---
name: wemush-mycology-assistant
description: Guide mycology research workflows using WeMush's MCP server for specimen tracking, research projects, cultivation analytics, and strain catalog exploration. Use when users ask about mushroom cultivation, research projects, specimen management, or mycology data analysis.
license: Apache-2.0 (see ../LICENSE)
compatibility: Requires WeMush MCP server connection with OAuth 2.0 authentication
metadata:
  author: wemush
  version: "1.0.0"
  website: https://wemush.com
  documentation: https://wemush.com/docs/claude-connector
---

# WeMush Mycology Assistant

## Overview

This skill helps researchers and cultivators interact with WeMush, a decentralized mycology platform for mushroom cultivation management, specimen tracking, and collaborative research.

Use this skill when users want to:

- Manage research projects (create, join, view progress)
- Track specimens and cultivation observations
- Analyze research outcomes and trends
- Search the mycology catalog (strains, species)
- Record and review cultivation data

## Prerequisites

Before using WeMush tools, users need:

1. A WeMush account at <https://wemush.com>
2. OAuth authorization via the WeMush MCP server
3. Appropriate scopes granted during authorization

### Available OAuth Scopes

| Scope | Description |
| ------------- | ------------- |
| `research:read` | View research projects and observations |
| `research:write` | Create projects, submit observations |
| `specimens:read` | View specimen data and lineage |
| `specimens:write` | Record specimen observations |
| `analytics:read` | Access research analytics |
| `catalog:read` | Search strains and species |

## Workflows

### 1. Research Project Management

**List available projects:**
Use `list_research_projects` to show public research projects the user can join.

**Join a project:**
Use `enroll_in_project` with the project ID to join a research initiative.

**View project details:**
Use `get_research_project` to see full project details, protocols, and progress.

**Create new research:**
Use `create_research_project` with title, description, target strain IDs, and protocol details.

### 2. Specimen Tracking

**View specimens:**
Use `list_my_specimens` to see all specimens the user has access to. Filter by status, strain, or date range.

**Get specimen details:**
Use `get_specimen_details` with specimen ID for full information including current status, lineage, and observation history.

**View lineage:**
Use `get_specimen_lineage` to see the specimen's ancestry and descendants. Helpful for tracking genetics and cultivation history.

**Record observations:**
Use `record_specimen_observation` to log cultivation data including growth measurements, environmental conditions, health assessments, and notes.

### 3. Analytics & Insights

**Project analytics:**
Use `get_project_analytics` for aggregate statistics including participant count, observation rates, and completion stats.

**Outcome analysis:**
Use `get_outcome_breakdown` to see success/failure rates broken down by strain, technique, or conditions.

**Equipment analysis:**
Use `get_equipment_analysis` to identify which equipment correlates with better cultivation outcomes.

**Research trends:**
Use `get_research_trends` to see patterns over time including seasonal variations and technique evolution.

### 4. Catalog Exploration

**Search strains:**
Use `search_strains` to find mushroom strains by name, species, cultivation difficulty, or characteristics.

**Search species:**
Use `search_species` to find species information by scientific name, common name, or genus.

**Get details:**
Use `get_strain_details` or `get_species_details` for comprehensive information including taxonomy, cultivation requirements, and images.

### 5. Profile & Activity

**View profile:**
Use `get_my_research_profile` to see the user's research contributions, project memberships, and observation statistics.

**Activity feed:**
Use `get_research_activity_feed` to see recent activity across projects the user participates in.

## Examples

### Starting a Research Project

User: "I want to start a research project comparing Lion's Mane growth on different substrates"

1. Search for Lion's Mane strains: `search_strains` with query "Lion's Mane"
2. Create the project: `create_research_project` with:
   - Title: "Lion's Mane Substrate Comparison Study"
   - Description: Research goals and methodology
   - Target strain IDs from the search results
   - Protocol: Data collection requirements

### Tracking Cultivation Progress

User: "I need to log today's observations for my Pink Oyster grow"

1. List specimens: `list_my_specimens` filtered by strain
2. Record observation: `record_specimen_observation` with:
   - Specimen ID
   - Growth measurements
   - Environmental readings (temp, humidity)
   - Health assessment
   - Any notes or photos

### Analyzing Research Results

User: "How are participants doing in the substrate comparison study?"

1. Get project details: `get_research_project` for context
2. Get analytics: `get_project_analytics` for aggregate stats
3. Get outcomes: `get_outcome_breakdown` by substrate type
4. Summarize findings and trends for the user

## Privacy & Security

WeMush protects user data with:

- **K-Anonymity (k=5)**: Analytics aggregate data from at least 5 participants before sharing
- **Scope-Based Access**: Tools only access data within approved OAuth scopes
- **Token Expiration**: Access tokens expire after 1 hour
- **Audit Logging**: All tool calls are logged for security

Users can revoke access anytime via WeMush Settings > Connected Apps.

## When to Use

Invoke this skill when users:

- Ask about mushroom cultivation or mycology research
- Want to track specimens or cultivation progress
- Need to analyze research data or outcomes
- Want to explore mushroom strains or species
- Ask about WeMush features or workflows
- Mention research projects, observations, or analytics

Do NOT use this skill for:

- General mushroom identification without catalog search
- Medical or consumption advice
- Topics unrelated to mycology research

## Support

- Documentation: <https://wemush.com/docs/claude-connector>
- Email: <support@wemush.com>
- Status: <https://wemush.com/status>

See [references/REFERENCE.md](references/REFERENCE.md) for complete tool documentation.

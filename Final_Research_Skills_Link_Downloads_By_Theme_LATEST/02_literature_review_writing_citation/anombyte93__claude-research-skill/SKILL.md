---
name: research-before-coding
description: Use when writing ANY implementation code, fixing bugs, or modifying existing code. Delegates research to a fast subagent that distills WebSearch results into compact RAG-efficient summaries. Main context never sees raw output.
---

# Research Before Coding

## Overview

**Core principle: "You don't know anything until research confirms it"**

You MUST research before writing implementation code. No exceptions.

**The Iron Law:**
```
NO IMPLEMENTATION CODE WITHOUT RESEARCH FIRST
```

**Architecture:** Research runs in a **Task agent** (haiku model). Raw WebSearch output stays in the agent's context. Only a distilled ~20-30 line summary returns to your context. This prevents context bloat from raw search responses.

```
Main Session                    Task Agent (haiku)
    |                                |
    |-- spawn with query ----------->|
    |                                |-- run 10 WebSearch queries (parallel)
    |                                |-- receive ~10 pages of raw output
    |                                |-- distill to structured summary
    |   <-- return ~25 lines --------|
    |                                |  (agent context discarded)
    |-- implement with knowledge     |
```

## When to Use

**ALWAYS use when:**
- Writing ANY implementation code
- Fixing ANY bug
- Adding ANY feature
- Modifying ANY existing code
- Using ANY library/API

**Never skip research. Ever.**

## Research Workflow

### Step 1: Spawn the Research Agent

Use the **Task tool** with this exact pattern. Replace `TECHNOLOGY`, `TASK`, and `QUESTION` with your actual values:

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Research [TECHNOLOGY] [TASK]",
  prompt: <see template below>
)
```

**Agent Prompt Template:**

```
You are a research distillation agent. Your job is to run WebSearch queries, read ALL raw output, and return ONLY a compact structured summary.

RESEARCH TOPIC: [TECHNOLOGY] [TASK]
CALLER NEEDS TO KNOW: [QUESTION - what specifically the main session needs answered]

## Step 1: Run ALL 10 WebSearch queries

Use the WebSearch tool to run ALL of these queries (run them in parallel where possible, replacing TECHNOLOGY and TASK):

1. WebSearch("best practices TECHNOLOGY TASK 2026")
2. WebSearch("TECHNOLOGY architecture patterns TASK")
3. WebSearch("github TECHNOLOGY TASK examples")
4. WebSearch("TECHNOLOGY TASK error handling 2026")
5. WebSearch("TECHNOLOGY TASK performance optimization 2026")
6. WebSearch("TECHNOLOGY TASK security best practices 2026")
7. WebSearch("TECHNOLOGY TASK testing 2026")
8. WebSearch("TECHNOLOGY vs alternatives comparison 2026")
9. WebSearch("TECHNOLOGY common pitfalls mistakes TASK 2026")
10. WebSearch("TECHNOLOGY TASK production deployment 2026")

## Step 2: Distill into structured summary

After ALL queries complete, read through every result carefully. Then produce EXACTLY this output format and nothing else:

---
## Research: TECHNOLOGY TASK
**Date**: YYYY-MM-DD

### Answer
[2-4 sentences directly answering QUESTION - the caller's specific need]

### Recommended Approach
- **Pattern**: [name the pattern/approach]
- **Library**: [recommended library + version if mentioned]
- **Why**: [1 sentence trade-off reasoning]

### Key Code Pattern
```[language]
[Most relevant code snippet, max 15 lines - the ONE pattern they should follow]
```

### Pitfalls
- [Critical mistake #1 to avoid]
- [Critical mistake #2 to avoid]
- [Critical mistake #3 to avoid]

### Security Notes
- [Any security consideration relevant to this task, or "None identified"]

### Conflicting Advice
- [Note any disagreements between sources, or "Sources agree"]
---

RULES:
- DO NOT return raw WebSearch output
- DO NOT include URLs or source citations
- DO NOT exceed 30 lines in your final output
- DO include specific version numbers, function names, and config values mentioned
- DO prioritize the CALLER NEEDS TO KNOW question above all else
- If sources conflict, note the conflict and recommend the more recent/authoritative approach
- If a query fails or returns nothing useful, skip it silently
```

### Step 2: Use context7 if library docs are needed (optional)

After the Task agent returns, if you need specific API syntax for a library mentioned in the summary, use context7 **directly in the main session** (these are lightweight calls):

1. `resolve-library-id`: `{"libraryName": "<library>", "query": "<what you need>"}`
2. `query-docs`: `{"libraryId": "<id>", "query": "<specific API question>"}`

context7 returns focused API docs, not bloated content, so it's safe in the main context.

### Step 3: Implement

You now have:
- Distilled research summary (~25 lines in your context)
- Optional API docs from context7

Proceed with implementation.

## Complete Example

**Scenario:** About to implement React authentication with NextAuth.

**What you do:**

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Research React NextAuth authentication",
  prompt: "You are a research distillation agent. Your job is to run WebSearch queries, read ALL raw output, and return ONLY a compact structured summary.

RESEARCH TOPIC: React NextAuth authentication
CALLER NEEDS TO KNOW: How to implement OAuth authentication in a Next.js 14 app using NextAuth v5, including session management and protected routes.

## Step 1: Run ALL 10 WebSearch queries

Use the WebSearch tool to run ALL of these queries (run them in parallel where possible):

1. WebSearch(\"best practices react nextauth authentication 2026\")
2. WebSearch(\"react architecture patterns nextauth authentication\")
3. WebSearch(\"github react nextauth authentication examples\")
4. WebSearch(\"react nextauth authentication error handling 2026\")
5. WebSearch(\"react nextauth authentication performance optimization 2026\")
6. WebSearch(\"react nextauth authentication security best practices 2026\")
7. WebSearch(\"react nextauth authentication testing 2026\")
8. WebSearch(\"react nextauth vs alternatives comparison 2026\")
9. WebSearch(\"react common pitfalls mistakes nextauth authentication 2026\")
10. WebSearch(\"react nextauth authentication production deployment 2026\")

## Step 2: Distill into structured summary
[... same distillation instructions as template above ...]"
)
```

**What comes back to your context (~25 lines):**

```
## Research: React NextAuth Authentication
**Date**: 2026-02-10

### Answer
NextAuth v5 (Auth.js) uses a new `auth()` function replacing `getServerSession()`. Configure providers in `auth.ts` at project root. Use middleware for protected routes. Session strategy defaults to JWT.

### Recommended Approach
- **Pattern**: App Router + Middleware-based protection
- **Library**: next-auth@5.0.0-beta.25 (Auth.js)
- **Why**: Native RSC support, edge-compatible middleware, simpler config than v4

### Key Code Pattern
// auth.ts
import NextAuth from "next-auth"
import GitHub from "next-auth/providers/github"
export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [GitHub],
})

### Pitfalls
- Don't use getServerSession() (v4 API) - use auth() instead
- Don't forget to add NEXTAUTH_SECRET in production
- Don't skip middleware.ts for route protection (client checks alone are insufficient)

### Security Notes
- Always validate session server-side, never trust client-only checks

### Conflicting Advice
- Sources agree on v5 approach; some older tutorials still reference v4 patterns
```

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I know this pattern" | You're an AI trained on old data. APIs change. Research. |
| "This is obvious/standard" | 15 seconds of agent research vs 15 minutes of revert hell. |
| "Simple one-line fix" | Simple fixes break things when you're wrong. Verify first. |
| "This is slowing me down" | Broken code + revert + context loss = way slower. Research IS speed. |

## Red Flags - STOP and Research

**You are about to break things if:**
- Thinking "I know this"
- Thinking "it's just..."
- Thinking "quick fix"
- About to type code without spawning a research agent first

## The Cost Calculation

```
Agent research:  10 parallel queries + distillation = ~20 seconds, ~25 lines in your context
Direct research: 10 parallel queries raw = ~20 seconds, ~500+ lines flooding your context
Guessing:        Type code -> Wrong -> Debug -> Revert -> Lost context = 15+ minutes
```

The math is unambiguous. Agent-delegated research is strictly better than both alternatives.

## The 10 Query Categories

| # | Query Type | Purpose |
|---|------------|---------|
| 1 | Best Practices | Latest established patterns |
| 2 | Architecture | Structural decisions |
| 3 | GitHub Examples | Real working code |
| 4 | Error Handling | Failure scenarios |
| 5 | Performance | Optimization techniques |
| 6 | Security | Safety considerations |
| 7 | Testing | Test strategies |
| 8 | Alternatives | Comparison shopping |
| 9 | Pitfalls | Common mistakes to avoid |
| 10 | Deployment | Production readiness |

## After Research

Once research is complete:
- Use `superpowers:writing-plans` to create implementation plan
- Use `superpowers:brainstorming` if design needs clarification

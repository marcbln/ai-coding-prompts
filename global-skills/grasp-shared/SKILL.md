---
name: grasp-shared
description: Drafts a discussion-ready change proposal that builds collective understanding of a diff or decision across technical and non-technical stakeholders. Use when a change should be understood by a team, when a proposal needs comment-friendly review in Notion/docs/a PR, or when stakeholders keep asking "what is going on here and why".
argument-hint: [--to <path>]
---

# Grasp Shared: Building Collective Understanding

## Objective

Produce a single, discussion-ready document that lets **everyone** — reviewers, developers, QA, product, non-technical stakeholders — understand a change *and* participate in shaping it. The document is a living artifact for inline comment, not a finished report.

## Step 1: Gather the Change

Determine what to explain, in priority order:

1. The change just discussed (diff, PR, or design) if one is active in the conversation — reuse and condense its `grasp-diff` sections when available
2. `$ARGUMENTS`:
   - **`<path>`** — a file, diff, or plan document to build the proposal from
   - **`--to <path>`** — where to write the document (override default below)
3. Nothing specified → inspect the working tree (unstaged/staged diff) or last commit

Read enough surrounding code and `git log` to state the why — not to write code.

## Step 2: Write the Proposal Document

Structure (markdown, frontmatter first):

```markdown
---
title: "Change Proposal: <one line>"
date: <YYYY-MM-DD>
status: draft
scope: <files/systems touched>
---

## TL;DR for the Busy
<3-5 sentences, no jargon — what changes, why, what to watch out for>

## Why This Matters (Context)
<background: the problem or opportunity this addresses>

## The Decision & Rationale
<table: decision | why | alternatives rejected (and why)>

## How It Works (for the technical reader)
<architecture/steps in plain sequence; ASCII diagram of before/after>

## Impact
<dependencies, breaking changes, performance, rollback plan, risks>

## Open Questions
<numbered list, each phrased as a real question for the reader>

## Discussion Prompts
<3-6 prompts targeting specific people/roles: e.g. "QA: what test scenarios...", "PM: does this change the user-visible behavior...", "Ops: ...">
```

Rules of the genre:

- **Intuition before detail** — the TL;DR and Context come first; technical mechanics after.
- **No jargon in the top half** — or define it inline the first time it appears.
- **Questions are invitations** — every Open Question and Discussion Prompt names a role and a concrete question, so a reader can answer without "reading the whole thing".
- **Neutral tone** — this is a basis for discussion, not a justification.

## Step 3: Save and Hand Off

- Default path: `_ai/backlog/reports/`; write to `--to <path>` if given. Use a slug filename, e.g. `change-proposal__<short-slug>.md`.
- Confirm the path, and suggest: paste into Notion/docs/PR description for inline commenting, or route to a review meeting.
- Offer `grasp-diff` (deeper technical walkthrough) or `grasp-microworld` (playground) for anyone who wants more than prose.
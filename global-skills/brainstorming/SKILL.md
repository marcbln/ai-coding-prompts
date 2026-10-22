---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

**This skill ends at the design record. It does not write a plan, a spec, or code.**
It promotes durable decisions to ADRs. It writes a design handoff only when the
next artifact will be produced outside this conversation; in the same conversation,
the conversation is the source and the plan/spec carries the decisions forward.

## The Process

**Understanding the idea:**
- Check out the current project state first (files, docs, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**
- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

### 1. Promote durable decisions to ADRs

A decision becomes an ADR when it **constrains future work beyond this feature** — a
chosen pattern, a dependency rule, a boundary, a convention future changes must
respect. Everything else stays in the conversation; when a plan is written, the
plan's `Design Decisions & Rejected Alternatives` section records it. It goes into
a handoff only when one is written.

For each such decision write `_ai/technical_decisions/{YYMMDD_HHmm}__ADR__{topic}.md`.
Do not promote decisions that only matter here; they belong in the plan's design
record (or the handoff, when one is written), and duplicating them in both the ADR
and the plan guarantees they drift.

### 2. Ask where the next artifact will be produced

Ask exactly one question before writing anything:

> Will the spec/plan be created in this conversation, or are you handing the design off?

- **Same conversation** — do not write a handoff. The conversation is the source;
  the plan/spec prompt reads it directly. Tell the user in one line: "No handoff
  written — this design lives only in this conversation. If you switch sessions,
  ask for a handoff explicitly."
- **Handoff** — continue with step 3.

### 3. Write the design handoff (handoff branch only)

Write the conversation's durable output to
`_ai/backlog/active/{YYMMDD_HHmm}__DESIGN_HANDOFF__{kebab-case-topic}.md`:

```yaml
---
filename: "_ai/backlog/active/{YYMMDD_HHmm}__DESIGN_HANDOFF__{kebab-case-topic}.md"
title: "Design Handoff: {topic}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
status: validated
tags: [tag1, tag2]
documentType: DESIGN_HANDOFF
---
```

Body sections, in this order:

- **Context** — what was being designed and where the discussion started.
- **Decisions** — one entry per decision: the decision, the rationale, and what it
  rules out.
- **Rejected Alternatives** — what was considered and dropped, and why. This is the
  most valuable section in the file: without it the same options get re-proposed
  later.
- **Constraints Discovered** — facts about the codebase or project surfaced during
  the discussion that any implementation must respect.
- **Open Questions** — unresolved items, each with a named owner.
- **Scope Boundary** — explicitly in, explicitly out.

Keep it a record of decisions, not a narrative of the conversation and not a
specification. It describes intent and constraints; it does not enumerate
requirements.

### 4. Recommend the next artifact, then stop

Close with one line naming what should come next and why. Do not start it:

- New capability, or anything still uncertain about behavior → run the
  `create-spec` prompt
- Well-understood change, or mostly mechanical work → run the
  `create-implementation-plan` prompt
- Large effort that needs slicing first → use the `create-epic` skill
- Genuinely nothing to build yet → stop

Do not commit unless the user asks.

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Record rejections** - An alternative you rejected without writing down will be proposed again
- **Be flexible** - Go back and clarify when something doesn't make sense

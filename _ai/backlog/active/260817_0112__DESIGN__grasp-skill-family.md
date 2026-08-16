# Design: grasp-* Skill Family (Understanding-First Skill Trio)

- **Date:** 2026-08-17
- **Status:** validated design (implemented)
- **Type:** DESIGN
- **Source:** Geoffrey Litt talk — "understanding is the bottleneck"; AI Studio shared prompt (explain-diff template)

## Context

With AI agents writing most code, the bottleneck shifts from *writing* to *understanding* code. If developers approve AI changes without building a mental model, they accrue **cognitive debt** and lose the ability to participate creatively. Geoff Litt proposes three techniques to build human understanding with AI:

1. Advanced explanations + quizzes (intuition before details, interactive figures, comprehension quizzes as "speed regulator")
2. Micro-worlds (temporary interactive simulations to explore program state)
3. Shared spaces (collective understanding across technical and non-technical stakeholders)

## Decision

Create three opencode/Windsurf skills in `global-skills/` (symlinked into `~/.config/opencode/skills`), grouped under the unique **`grasp-`** namespace (avoiding collision with the existing `understand*` graph-based family in `~/.agents/skills/`):

### grasp-diff
Educational diff explainer. Resolves a diff source (argument, or unstaged → staged → HEAD~1 fallback, branch/commit/PR support). Produces exactly four sections, code shown only in section 3:
1. Background & Context — architecture, prerequisites
2. Intuition & Design Rationale — before/after ASCII diagram, rejected alternatives
3. Literate Walkthrough — logical chunks (not alphabetical), key lines commented, edge cases
4. Comprehension Quiz — 3–5 MCQs with collapsible answers (`<details>`)

Then closes the loop: 3-line summary + offers grasp-microworld / grasp-shared.

### grasp-microworld
Meta-skill producing a disposable interactive "teaching instrument" for code with real runtime state. Analyzes core state → execution steps → knobs; picks artifact type (bias D3) and **delegates to the existing `viz-*` skills** (static-svg for trivial diagrams, d3 as default steppable playground, webgl for spatial) with an overlay of micro-world requirements:
- Stepping controls (Forward/Back/Play/Reset)
- Live state readout panel (variable name → value)
- What-if knobs (sliders/toggles recompute state)
- Code anchoring (each step shows the real code snippet it maps to)
- Optional guided "Show me" tour
- Refuses to force a playground when there is no meaningful state

### grasp-shared
Drafts a discussion-ready, comment-friendly change proposal for teams. Frontmatter + TL;DR (no jargon) + Context + Decision/Rationale table + How It Works (technical, after intuition) + Impact + Open Questions + Discussion Prompts (role-targeted invitations). Default output `_ai/backlog/reports/change-proposal__<slug>.md`, overridable with `--to <path>`. Neutral tone — a basis for discussion, not a justification.

## Design Principles Applied

- **Intuition before details** in every skill's output
- **Participation over verification** as the stated goal (quiz = speed regulator; prompts = invitations to comment)
- **DRY:** grasp-microworld reuses viz-* skills instead of redefining rendering conventions
- **No-op guard:** grasp-microworld refuses to run when there is no state to visualize
- Cross-linking: each skill suggests its siblings at hand-off

## Consequences

- Three new skills, zero new dependencies (viz family is already installed)
- `grasp-diff` name is free on this system; the graph-based `understand-diff` in `~/.agents/` is untouched and complementary (impact analysis vs. pedagogy)
- Skills are conversational-guide style (like `prime-codebase`), user-invoked; descriptions also allow model-invocation

## Alternatives Considered

- **`understand-` namespace** — rejected: collides with existing graph-based `understand*` family (`~/.agents/skills/`)
- **Self-contained styling in grasp-microworld** — rejected: duplicates viz-* conventions; delegation keeps single source of truth
- **One combined skill** — rejected per skill-writing guidance (Pocock): splitting forces legwork and keeps each skill small
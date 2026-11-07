---
name: epic-to-speckit
description: Bridges an _ai/backlog/ Epic or PART spec into the specs/ directory without ceremony. Scaffolds spec.md and generates a lean, test-gated tasks.md ready for immediate code execution.
auto_execution_mode: 1
---

You are a **High-Velocity Technical Lead**. Your job is to bypass ceremony and bridge an already-defined backlog item directly into an executable Spec Kit workspace (`specs/`).

## Input Handling

The user provides either:
1. An **Epic file** (`_ai/backlog/epics/...__EPIC__...md`): Read the roadmap table and plans checklist. Select the **first uncompleted part (`- [ ]`)**.
2. A **Part file** (`_ai/backlog/active/...__PART_{NN}__...md`): Use this part directly.

If no file is provided, scan `_ai/backlog/active/` or `_ai/backlog/epics/` for active items and confirm which part to fast-track.

## Strict Rules (Anti-Ceremony)

- **DO NOT re-interview the user.** The requirements are already written in the spec.
- **DO NOT write conversational filler or narrative essays.**
- **DO NOT generate a bloated plan.md.** A 3-sentence technical summary in `tasks.md` is sufficient.
- **Keep tasks strictly actionable:** Every item must list the target file, the required diff/action, and the verification check.
- **Maximum 6–8 tasks total.** Keep it lean and reviewable.

## Workflow

1. **Extract Metadata from Part:**
   - Part Number (e.g., `10`, `20`, `30`).
   - Kebab slug name (e.g., `shell-theming-and-modern-canvas`).
   - Objective, Scope, Constraints, and Acceptance Criteria.

2. **Scaffold Directory:**
   - Target path: `<projectRoot>/specs/{NN}-{kebab-slug}/`
   - Create `specs/{NN}-{kebab-slug}/spec.md` containing the verbatim core requirements from the backlog part (or a clean, structured summary).

3. **Generate `specs/{NN}-{kebab-slug}/tasks.md`:**
   Structure as a clean checklist:
   ```markdown
   # Tasks: Part {NN} - {Title}
   
   **Context:** Sourced from `_ai/backlog/active/{filename}`
   **Verification Command:** `./scripts/run-tests.sh` (or specific guard script)
   
   ## Task Checklist
   - [ ] `<path/to/file>`: <Concrete change / diff description>
   - [ ] `<path/to/file>`: <Concrete change / diff description>
   - [ ] Verification: Run test scripts (`./scripts/run-tests.sh`, guards)
   - [ ] Visual/Manual check: <Specific browser URL or scenario to verify>
   ```

4. **Output and Handoff:**
   - Print the generated `specs/{NN}-{kebab-slug}/tasks.md`.
   - Ask the user: **"Ready to execute Task 1 with `speckit-fast-exec`?"**

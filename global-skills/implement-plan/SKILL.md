---
name: implement-plan
description: Execute an implementation plan across all phases without asking for confirmation. Use when you have a plan file ready and need it implemented end-to-end.
auto_execution_mode: 1
---

# Implement Plan

Execute the given implementation plan across all phases without asking for confirmation.

## Workflow

1. Read the plan file thoroughly
2. Execute each phase in order, validating as you go
3. After completion, write an implementation report to `_ai/backlog/reports/`
4. If the repo maintains a `CHANGELOG.md`, update it with user-facing changes (use the `changelog` skill)
5. If the repo has an ADR log (`_ai/technical_decisions/ADR__*.md`) and the plan introduces a significant, hard-to-reverse decision, record it with the `adr-writer` skill
6. Archive the plan using the `finish-plan` skill

---
name: implement-plan
description: "Implement this plan! all phases. do not ask for confirmation."
auto_execution_mode: 1
---

Implement this plan! all phases! do not ask for confirmation!
After you are done and wrote a report in _ai/backlog/reports/, use the `finish-plan` to archive the plan.

If the repository maintains a `CHANGELOG.md`, update it to document the implemented changes. Only do this when it makes sense (e.g. the changes are user-facing and the repo follows a changelog convention). Use the `changelog` skill to generate or update the entries, then commit them together with the implementation if you are committing changes.

If the repository maintains an Architecture Decision Record (ADR) log (a `_ai/technical_decisions/` directory with `ADR__*.md` files), and the plan introduces a significant, hard-to-reverse decision (new framework, core pattern change, major integration, design strategy), record it with the `adr-writer` skill. Only do this when it makes sense: the ADR log exists AND the change warrants a durable decision record. Do not force an ADR for trivial or purely mechanical changes.


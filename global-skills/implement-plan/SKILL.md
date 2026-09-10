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
6. Review all changes with `git status` and `git diff`, then create one or more logical commits using the `git-commit` skill
7. Ask the user if they want to push the commits to the remote; only push if confirmed
8. Archive the plan using the `finish-plan` skill
9. Present **Next-Step Hints** to the user (see below)

## Next-Step Hints

After the plan is fully implemented and committed, give the user actionable suggestions for verifying or building on what was just delivered. Tailor the hints to the project and the specific plan; do NOT just print a generic checklist.

### How to determine the hints

1. **Inspect the plan** — what features, endpoints, commands, migrations, or files were added/changed?
2. **Inspect the codebase** — look at `Makefile`, `package.json` scripts, `composer.json` scripts, `Cargo.toml`, `pyproject.toml`, `docker-compose.yml`, existing test files, CLI entry points, READMEs, etc. to discover how the project is typically tested, run, or exercised.
3. **Combine** — map each implemented change to the most relevant runnable command or action.

### What to include (pick what applies)

| Category | Example |
|---|---|
| **Run the app / start dev server** | `make up`, `npm run dev`, `docker compose up` |
| **Test a specific feature** | `./bin/console app:my-new-command --flag`, `curl -X POST localhost:8000/api/endpoint`, `npm run test -- --filter myFeature` |
| **Run the test suite** | `make test`, `npm test`, `go test ./...`, `pytest -x` |
| **Run linters / type checks** | `make lint`, `npm run typecheck`, `ruff check .` |
| **Database migrations** | `make migrate`, `bin/console doctrine:migrations:migrate` |
| **Build assets** | `npm run build`, `make build` |
| **Verify a specific scenario** | "Open `localhost:8000/admin#/my-page` and check that the new field appears" |
| **Follow-up work** | "This feature is behind a flag — enable it in `config/settings.php`", "Add acceptance tests once the UI stabilises" |

### Presentation rules

- Show hints as a **numbered list** after the implementation summary.
- Prefix each hint with a **short label** in bold (e.g. **Test the command**, **Run migrations**).
- Include the **exact command** the user can copy-paste.
- Keep it concise — aim for 3-7 hints, not an exhaustive dump.
- Only suggest things that are actually runnable in this project; do not guess at commands that don't exist.
- If no reasonable hint applies (rare), simply state "Implementation complete — no additional steps required."

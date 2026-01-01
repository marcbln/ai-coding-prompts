# AI Coding Prompts

A collection of AI coding prompts, templates, and workflows for various development tasks and IDE integrations.

## Windsurf Global Workflows

The `windsurf-global-workflows/` directory contains global system prompts (workflows) for the Windsurf IDE (Cascade).

## Available Workflows


| File           | Trigger Command | Description                                                                   |
| :--------------- | :---------------- | :------------------------------------------------------------------------------ |
| `architect.md` | `@architect`    | Acts as a Product Manager to interview you and build a`requirements.md` file. |
| `save-plan.md` | `@save-plan`    | Generates a structured implementation plan and saves it to`ai-backlog/plans`. |

## BDD Workflow Agents

This repository includes a specialized 4-phase workflow for implementing features using BDD (Behavior Driven Development) and TDD (Test Driven Development) principles. Each phase is handled by a specific agent prompt to ensure separation of concerns.


| Agent File                  | Phase                 | Role             | Description                                                                             |
| :---------------------------- | :---------------------- | :----------------- | :---------------------------------------------------------------------------------------- |
| `bdd1_architect_agent.md`   | **Phase 1: Design**   | Architect        | Translates raw requests into Gherkin feature files (`.feature`) and architecture plans. |
| `bdd2_tdd_red_agent.md`     | **Phase 2: Red**      | Tester / SDET    | Scaffolds empty classes and writes*failing* tests based on the specifications.          |
| `bdd3_tdd_green_agent.md`   | **Phase 3: Green**    | Developer        | Implements the minimal logic required to make the tests pass.                           |
| `bdd4_maintenance_agent.md` | **Phase 4: Refactor** | QA / Maintenance | Analyzes execution logs to fix regressions or update tests for code/UI changes.         |

## Installation (Sync via Symlink)

To use these workflows in Windsurf, symlink this directory to your local Windsurf configuration folder.

**Mac/Linux:**

1. Backup/remove your existing global workflows folder (if empty):
   ```bash
   rm -rf ~/.codeium/windsurf/global_workflows
   ```

# 251208__PLAN__add_windsurf_workflows.md

## Problem Statement
The goal is to integrate a new "Requirements Builder" and "Plan Saver" workflow into the `ai-coding-prompts` repository. These workflows are designed for the Windsurf IDE (Cascade) and need to be stored in a structured way that allows for easy symlinking to the local Windsurf configuration folder (`~/.codeium/windsurf/global_workflows`). We need to create the directory structure, add the prompt files, and document the installation process.

## Phase 1: Directory Structure & Organization

**Objective**: Create a dedicated directory to house Windsurf-specific global workflows, keeping them distinct from Roo Code prompts and general conventions.

**Tasks**:
1. Create a new directory `windsurf-global-workflows` in the root of the repository.

**Implementation Details**:
```bash
mkdir -p windsurf-global-workflows
```

## Phase 2: Create Workflow Prompts

**Objective**: Create the system prompt files that will drive the Cascade behaviors.

**Tasks**:
1. Create `windsurf-global-workflows/architect.md`.
2. Create `windsurf-global-workflows/save-plan.md`.

**Source Code**:

File: `windsurf-global-workflows/architect.md`
```markdown
---
description: Acts as a Senior PM/Architect to interview the user and generate requirements
auto_execution_mode: 1
---

Act as a Senior Technical Product Manager and System Architect. I want to build a new feature or project, but I need you to help me define the requirements first. 

DO NOT write any code yet. Instead, follow this process:

1. **Discovery Phase**: Ask me simple questions (one by one or in small batches) to understand:
   - The core problem we are solving.
   - The target user flow.
   - The tech stack constraints (if any exist in the current codebase, analyze them first).
   - Any specific libraries or patterns I prefer.

2. **Drafting Phase**: Once you have enough info, generate a comprehensive specification file named `docs/requirements.md` (create the folder if needed). This file must include:
   - **Problem Statement**: What and Why.
   - **Functional Requirements**: A bulleted list of features (Must Have / Nice to Have).
   - **Technical Implementation**: 
     - Proposed file structure/paths.
     - Key API endpoints or data models.
     - Libraries/Dependencies to add.
   - **Acceptance Criteria**: How we know it works.

3. **Review**: Ask me to review the `docs/requirements.md` file. I will either approve it or ask for changes. 

4. **Finalization**: Once approved, ask me if I want to update the `.windsurfrules` file with any project-specific coding patterns we decided on.

Are you ready to start the Discovery Phase? Ask your first question.
```

File: `windsurf-global-workflows/save-plan.md`
```markdown
---
description: Generate a detailed implementation plan and save it to ai-plans/
auto_execution_mode: 1
---

Please create a **detailed** multi-phased implementation plan in markdown format. 
Please follow SOLID principles.

The plan will be implemented by an AI coding agent. Include source code in the plan where applicable.

1. **Context Analysis**: Briefly describe the problem to be solved based on the current chat context.
2. **Drafting**: Write the plan to a new file in the `@ai_plans/` directory (create directory if it doesn't exist).
   - **Filename Format**: `{YYMMDD}__PLAN__{kebab-case-title}.md` (e.g., `251208__PLAN__implement-ftp-analyzer.md`).
3. **Structure**:
   - Problem Statement
   - Phases (Objective, Tasks, Deliverables)
   - Source Code blocks (if new files are needed)
   - Verification Steps

Confirm the filename and location before saving.
```

## Phase 3: Documentation Update

**Objective**: Update the repository documentation to explain how to install and sync these workflows with Windsurf.

**Tasks**:
1. Create a `windsurf-global-workflows/README.md` specifically for this folder to explain the symlinking process.

**Source Code**:

File: `windsurf-global-workflows/README.md`
```markdown
# Windsurf Global Workflows

This directory contains global system prompts (workflows) for the Windsurf IDE (Cascade).

## Available Workflows

| File | Trigger Command | Description |
| :--- | :--- | :--- |
| `architect.md` | `@architect` | Acts as a Product Manager to interview you and build a `requirements.md` file. |
| `save-plan.md` | `@save-plan` | Generates a structured implementation plan and saves it to `ai-plans/`. |

## Installation (Sync via Symlink)

To use these workflows in Windsurf, symlink this directory to your local Windsurf configuration folder.

**Mac/Linux:**

1. Backup/remove your existing global workflows folder (if empty):
   ```bash
   rm -rf ~/.codeium/windsurf/global_workflows
   ```

2. Create the symbolic link to this repo:
   ```bash
   # Adjust the path to where you cloned ai-coding-prompts
   ln -s ~/path/to/ai-coding-prompts/windsurf-global-workflows ~/.codeium/windsurf/global_workflows
   ```

3. Restart Windsurf. You can now reference these files in Cascade Chat (e.g., type `@architect`).
```

## Phase 4: Final Review

**Objective**: Verification of the changes.

**Tasks**:
1. Verify the directory structure is created.
2. Verify file contents match the requirements.
3. Check that the README provides clear installation instructions.

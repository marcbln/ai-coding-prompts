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
   ln -s ~/devel/ai-coding-prompts/windsurf-global-workflows ~/.codeium/windsurf/global_workflows
   ln -s ~/devel/ai-coding-prompts/windsurf-global-workflows ~/.codeium/windsurf-next/global_workflows
   ```

3. Restart Windsurf. You can now reference these files in Cascade Chat (e.g., type `@architect`).

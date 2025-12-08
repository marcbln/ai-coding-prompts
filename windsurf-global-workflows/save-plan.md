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

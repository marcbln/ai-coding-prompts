---
description: Generate a detailed implementation plan and save it to ai-plans/
auto_execution_mode: 1
---

Please create a **detailed** multi-phased implementation plan in markdown format that will be implemented by an AI coding agent.

## Requirements:
1. **First Line of Plan**: Must be the filename in format: `ai-plans/{YYMMDD}__PLAN__{name-of-the-plan}.md`
2. **First Section**: Briefly describe the problem to be solved based on current context
3. **Structure**:
   - Problem Statement
   - Multiple Phases (each with Objective, Tasks, Deliverables)
   - Source code blocks where applicable
   - Verification Steps
4. **Last Phase**: Must include writing a report to `ai-plans/{YYMMDD}__REPORT__{name-of-the-plan}.md`
5. **Follow SOLID principles**

## Important Environment Notes:
- Frontend root: `vol/www/assets`
- Backend root: `vol/www/src`
- App runs in container `cm-www` (use `docker exec -it cm-www /www/bin/console` for commands)
- Main database migrations: `bin/console make:migration` (inside container)
- Tenant database migrations: `bin/console app:sys:mt:migrations:diff 2` (inside container)
- Include actual source code in the plan where new files/classes are needed

## Process:
1. **Context Analysis**: Analyze current chat context to understand the problem
2. **Drafting**: Create the plan with proper structure
3. **Filename**: Use format `{YYMMDD}__PLAN__{kebab-case-title}.md` (create directory if needed)
4. **Verification**: Confirm the filename and location before saving

The plan should be detailed enough for an AI coding agent to execute it step-by-step without additional context.


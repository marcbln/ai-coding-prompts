---
description: Generate a detailed implementation plan and save it to ai-backlog/plans
auto_execution_mode: 1
---

Create a **detailed** multi-phased implementation plan in markdown format that will be implemented by an AI coding agent.

## Requirements:
1. **First Line of Plan**: Must be the filename in format: `ai-backlog/plans{YYMMDD_HHmm}__IMPLEMENTATION_PLAN__{name-of-the-plan}.md`
2. **First Section**: Briefly describe the problem to be solved based on current context
3. **Structure**:
   - Problem Statement
   - Multiple Phases (each with Objective, Tasks, Deliverables)
   - Source code blocks where applicable
   - Verification Steps
4. **Last Phase**: Must include writing a report to `ai-backlog/plans{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md`
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
3. **Filename**: Use format `{YYMMDD_HHmm}__IMPLEMENTATION_PLAN__{kebab-case-title}.md` (create directory if needed)
4. **Verification**: Confirm the filename and location before saving

The plan should be detailed enough for an AI coding agent to execute it step-by-step without additional context.

<instruction>
Create a **detailed** multi phased implementation plan in markdown format. 

## Plan Structure
- Include YAML frontmatter with the following fields:
```yaml
---
filename: "ai-backlog/plans{YYMMDD_HHmm}__IMPLEMENTATION_PLAN__{name-of-the-plan}.md"
title: "Descriptive title of the plan"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
status: draft|in-progress|completed
priority: low|medium|high|critical
tags: [tag1, tag2, tag3]
estimatedComplexity: simple|moderate|complex
documentType: IMPLEMENTATION_PLAN
---
```
- The first section of the plan briefly describes the problem to be solved.

- The second section contains generic implementation notes:
```
- Frontend root is vol/www/assets
- Backend root is vol/www/src
- the app runs in container `cm-www`, you need to consider this when running commands (use `docker exec -it cm-www /www/bin/console`)
- migrations for the main database are created with `bin/console make:migration` (inside the container)
- migrations for the tenant database are created with `bin/console app:sys:mt:migrations:diff 2` (inside the container)
- check the context definitions in ai-context-defintions if they need to be updated
- projectName is: TradeGuard
- the container uses autowiring, registering services in `services.yaml` is not needed.
```

- The plan will be implemented by an AI coding agent.
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- The plan should also include an update of the user documentation, if needed.
- Please follow SOLID principles

## Report Structure
The last phase of the plan should be to write a report to `ai-backlog/plans{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md`

Include YAML frontmatter with the following fields:
```yaml
---
filename: "ai-backlog/plans{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md"
title: "Report: {plan title}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
planFile: "ai-backlog/plans{YYMMDD_HHmm}__IMPLEMENTATION_PLAN__{name-of-the-plan}.md"
project: "{project-name}"
status: completed|partial|blocked
filesCreated: 0
filesModified: 0
filesDeleted: 0
tags: [tag1, tag2, tag3]
documentType: IMPLEMENTATION_REPORT
---
```

The report content should include:
1. **Summary**: Brief overview of what was accomplished (2-3 sentences)
2. **Files Changed**:
    - List of new files created with brief descriptions
    - List of modified files with summary of changes
    - List of deleted files (if any)
3. **Key Changes**: Bullet points of the main technical changes made
4. **Technical Decisions**: Important design decisions or trade-offs made during implementation
5. **Testing Notes**: How the changes can be verified or tested
6. **Usage Examples** (if applicable): Provide specific CLI commands, arguments, and example outputs if the implementation involved command-line interfaces
7. **Documentation Updates**: Summary of any documentation changes made
8. **Next Steps** (optional): Any follow-up work or improvements that could be made
</instruction>




Do NOT execute the plan. Just save it to the disk.

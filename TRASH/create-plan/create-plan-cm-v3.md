---
description: "CREATE PLAN V3 FOR CM"
createdAt: 2025-12-14
createdBy: Cascade
tags: [cm]
documentType: PROMPT_TEMPLATE
---
<instruction>
Create a **detailed** multi phased implementation plan in markdown format. 

## Plan Structure
- Include YAML frontmatter with the following fields:
```yaml
  ---
  filename: "ai-backlog/plans{YYMMDD}__PLAN__{name-of-the-plan}.md"
  title: "Descriptive title of the plan"
  createdAt: YYYY-MM-DD HH:mm
  status: draft|in-progress|completed
  priority: low|medium|high|critical
  tags: [cm, create-plan]
  estimatedComplexity: simple|moderate|complex
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
```
- The plan will be implemented by an AI coding agent. Include source code in the plan.
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- Follow SOLID principles

## Report Structure
The last phase of the plan should be to write a report to `ai-backlog/plans{YYMMDD}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md`

Include YAML frontmatter with the following fields:
```yaml
---
filename: "ai-backlog/plans{YYMMDD}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md"
title: "Report: {plan title}"
createdAt: YYYY-MM-DD HH:mm
planFile: "ai-backlog/plans{YYMMDD}__PLAN__{name-of-the-plan}.md"
status: completed|partial|blocked
filesCreated: 0
filesModified: 0
filesDeleted: 0
tags: [tag1, tag2, tag3]
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
6. **Documentation Updates**: Summary of any documentation changes made
7. **Next Steps** (optional): Any follow-up work or improvements that could be made
</instruction>



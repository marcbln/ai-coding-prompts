---
name: "Create Plan V1"
description: "CREATE PLAN V1"
createdAt: 2025-12-14
createdBy: Cascade
updatedAt: 2025-12-17
updatedBy: Cascade
tags: [common]
documentType: PROMPT_TEMPLATE
status: deprecated
deprecatedAt: 2025-12-17
deprecationNote: "Superseded by create-plan-v4.md"
---
> **Deprecated:** This template is kept for historical reference. Use `create-plan-v4.md` instead.
<instruction>
Create a **detailed** multi phased implementation plan in markdown format. 
- The First line of the plan should be the filename of the plan in format `ai-plans/{YYMMDD}__IMPLEMENTATION_PLAN__{name-of-the-plan}.md`
- The first section of the plan briefly describes the problem to be solved.
- The plan will be implemented by an AI coding agent. 
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- The plan should also include an update of the user documentation, if needed.
- The last phase of the plan should be to write a report of the changes that were made to a file in the `ai-plans/{YYMMDD}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md` directory.
- Please follow SOLID principles
</instruction>

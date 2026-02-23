---
name: "Master Implementation Plan Template"
description: "Master Implementation Plan Template"
createdAt: 2025-12-14
createdBy: Cascade
updatedAt: 2025-12-17
updatedBy: Cascade
tags: [common, planning]
documentType: PROMPT_TEMPLATE
---
<instruction>
Create a **detailed** multi-phased implementation plan in markdown format.

## Plan Structure
- Include YAML frontmatter with the following fields:
```yaml
---
filename: "_ai/backlog/active/{YYMMDD_HHmm}__IMPLEMENTATION_PLAN__{name-of-the-plan}.md"
title: "Descriptive title of the plan"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
status: draft|in-progress|completed
priority: low|medium|high|critical
tags: [{{ project }}, plan]
estimatedComplexity: simple|moderate|complex
documentType: IMPLEMENTATION_PLAN
---
```

- The first section of the plan briefly describes the problem to be solved.

## Project Specific Implementation Notes
{{ project_context | default("No specific project notes provided.") }}

## General Guidelines
- The plan will be implemented by an AI coding agent.
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE].
- Follow SOLID principles.

## Report Structure
The last phase of the plan should be to write a report to `_ai/backlog/reports/{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md`.
</instruction>

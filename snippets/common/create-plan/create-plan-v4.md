---
description: "CREATE PLAN V3"
createdAt: 2025-12-14
createdBy: Cascade
updatedAt: 2025-12-14
updatedBy: Gemini3
tags: [common]
documentType: PROMPT_TEMPLATE
---
<instruction>
Create a **detailed** multi phased implementation plan in markdown format. 

## Plan Structure
- Include YAML frontmatter with the following fields:
```yaml
---
filename: "ai-plans/{YYMMDD}__IMPLEMENTATION_PLAN__{name-of-the-plan}.md"
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
{% if _implementation_notes is defined %}
- The second section contains generic implementation notes:
```
{{ _implementation_notes }}
```
{% endif %}
- The plan will be implemented by an AI coding agent.
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- The plan should also include an update of the user documentation, if needed.
- Please follow SOLID principles

## Report Structure
The last phase of the plan should be to write a report to `ai-plans/{YYMMDD}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md`

Include YAML frontmatter with the following fields:
```yaml
---
filename: "ai-plans/{YYMMDD}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md"
title: "Report: {plan title}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
planFile: "ai-plans/{YYMMDD}__IMPLEMENTATION_PLAN__{name-of-the-plan}.md"
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


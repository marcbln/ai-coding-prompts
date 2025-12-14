---
description: "CREATE PLAN V2"
createdAt: 2025-12-14
updatedAt: 2025-12-14
tags: [common]
---
<instruction>
Please create a **detailed** multi phased implementation plan in markdown format. 

## Plan Structure
- The First line of the plan should be the filename of the plan in format `ai-plans/{YYMMDD}__PLAN__{name-of-the-plan}.md`
- Include YAML frontmatter with the following fields:
```yaml
  ---
  title: "Descriptive title of the plan"
  date: YYYY-MM-DD
  status: draft|in-progress|completed
  priority: low|medium|high|critical
  tags: [tag1, tag2, tag3]
  estimated_complexity: simple|moderate|complex
  ---
```
- The first section of the plan briefly describes the problem to be solved.
- The plan will be implemented by an AI coding agent. 
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- The plan should also include an update of the user documentation, if needed.
- Please follow SOLID principles

## Report Structure
The last phase of the plan should be to write a report to `ai-plans/{YYMMDD}__REPORT__{name-of-the-plan}.md`

Include YAML frontmatter with the following fields:
```yaml
---
title: "Report: {plan title}"
date: YYYY-MM-DD
plan_file: "ai-plans/{YYMMDD}__PLAN__{name-of-the-plan}.md"
status: completed|partial|blocked
files_created: 0
files_modified: 0
files_deleted: 0
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

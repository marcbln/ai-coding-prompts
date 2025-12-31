# Report Generation Guidelines

<!-- 
Overview: This document defines the standard structure and format for implementation reports.
Purpose: Ensure consistency across all project reports with proper YAML frontmatter and content sections.
Last updated: Initial creation
-->

when you done with your task, write a report.

## Report Structure
<!-- Section: Defines the standard report structure and naming convention -->

The last phase of the plan should be to write a report to `ai-backlog/reports/{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__{name-of-the-plan}

### YAML Frontmatter
<!-- Section: Required metadata fields for all implementation reports -->

Include YAML frontmatter with the following fields:
```yaml
---
filename: "ai-backlog/reports/{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md"
title: "Report: {plan title}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
project: "{project-name}"
status: completed|partial|blocked
filesCreated: 0
filesModified: 0
filesDeleted: 0
tags: [tag1, tag2, tag3]
documentType: IMPLEMENTATION_REPORT
---
```

## Report Content Sections
<!-- Section: Required content sections for comprehensive implementation reports -->

The report content should include:

1. **Summary**: Brief overview of what was accomplished (2-3 sentences)
1.5 **Prompt used**: The exact prompt or instructions given to implement this feature / fix that bug
2. **Files Changed**:
    - List of new files created with brief descriptions
    - List of modified files with summary of changes
    - List of deleted files (if any)
3. **Key Changes**: Bullet points of the main technical changes made
4. **Technical Decisions**: Important design decisions or trade-offs made during implementation
5. **Testing Notes**: How the changes can be verified or tested
6. **Usage Examples** (if applicable): Provide specific CLI commands, arguments, and example outputs if the implementa
7. **Documentation Updates**: Summary of any documentation changes made
8. **Next Steps** (optional): Any follow-up work or improvements that could be made

<!-- 
Note: This template ensures all implementation reports follow a consistent format
for easy tracking and reference across the project lifecycle.
-->

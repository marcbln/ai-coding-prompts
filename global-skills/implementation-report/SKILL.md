---
name: implementation-report
description: Standard structure and format for implementation reports. Use when documenting what was built, deviations from plan, and validation results after completing implementation work.
---

# Implementation Report Guidelines

<!-- 
Overview: This document defines the standard structure and format for implementation reports.
Purpose: Ensure consistency across all project reports with proper YAML frontmatter and content sections.
Last updated: Initial creation
-->

when you done with your task, write a report.

## Report Structure
<!-- Section: Defines the standard report structure and naming convention -->

The last phase of the plan should be to write a report to `_ai/backlog/reports/{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__{name-of-the-plan}

### YAML Frontmatter
<!-- Section: Required metadata fields for all implementation reports -->

Include YAML frontmatter with the following fields:
```yaml
---
filename: "_ai/backlog/reports/{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md"
title: "Report: {plan title}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
repoRoot: "/absolute/path/to/repo"
project: "{project-name}"
status: draft | complete
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
4. **Deviations from Plan**: What broke, what performance issues were hit, and why a different approach was taken
5. **Technical Decisions**: Important design decisions or trade-offs made during implementation
6. **Testing Notes**: How the changes can be verified or tested
7. **Usage Examples** (if applicable): Provide specific CLI commands, arguments, and example outputs if the implementa
8. **Documentation Updates**: Summary of any documentation changes made
9. **Next Steps** (optional): Any follow-up work or improvements that could be made

## File References
<!-- Section: Absolute, copy-paste navigable file references (required) -->

Every file reference in the report must be **absolute and copy-paste navigable** —
never repo-relative paths like `src/foo.py`, never `~/...`:

```markdown
- `/abs/repo/src/foo.py:45` — added `resolve_editor()`
```

- `filename:` in the frontmatter is the absolute report path; `repoRoot:` is the
  absolute repository root.
- Backticked absolute path, followed by `:LINE` for the first changed line (or the
  defining line of the symbol being discussed). Wrap in a markdown link only if the
  host renders local links; the text inside backticks is what gets copied.
- In Testing / Verification commands, use the absolute interpreter and test paths so
  the block runs from any cwd.
- `filesCreated` / `filesModified` / `filesDeleted` count project source files; list
  out-of-repo docs and the report itself separately in the section body.
- Do not add a machine-readable `files:` list — it duplicates the section and drifts.


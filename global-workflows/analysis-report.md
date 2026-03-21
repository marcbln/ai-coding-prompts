# Analysis Report Guidelines

<!-- 
Overview: This document defines the standard structure and format for analysis reports.
Purpose: Ensure consistency across research tasks, architectural reviews, and bug investigations.
-->

When you are done with your research, investigation, or architectural analysis, write a report.

## Report Structure

The report should be saved to `_ai/backlog/reports/{YYMMDD_HHmm}__ANALYSIS_REPORT__{name-of-the-analysis}.md`

### YAML Frontmatter

Include YAML frontmatter with the following fields:
```yaml
---
filename: "_ai/backlog/reports/{YYMMDD_HHmm}__ANALYSIS_REPORT__{name-of-the-analysis}.md"
title: "Analysis: {analysis title}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
project: "{project-name}"
status: completed|draft
tags: [analysis, research, {tag3}]
documentType: ANALYSIS_REPORT
---
```

## Report Content Sections

The report content should include:

1. **Executive Summary**: Brief overview of the analysis goal and main conclusion (2-3 sentences).
2. **Scope**: Define exactly what was investigated (specific files, modules, or system behaviors).
3. **Methodology**: (Optional) How the analysis was conducted (e.g., code review, reproduction steps, log analysis).
4. **Findings**:
   - **Current State**: How the system currently behaves.
   - **Identified Issues**: Root causes of bugs or architectural limitations.
   - **Code References**: Links to specific file paths and line numbers relevant to the findings.
5. **Options & Alternatives**:
   - **Option A**: Description + Pros/Cons
   - **Option B**: Description + Pros/Cons
6. **Recommendations**:
   - The recommended path forward.
   - Justification for this choice.
   - Estimated complexity (Low/Medium/High).
7. **Risks & Trade-offs**: Potential side effects or security implications of the recommendation.
8. **Next Steps**: Actionable items to proceed (e.g., "Create Implementation Plan", "Update Documentation").

<!-- 
Note: This template ensures all analysis reports provide clear decision-making context.
-->

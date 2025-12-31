---
description: Verify the current unstaged git changes against the selected Implementation Plan and generate the Implementation Report.
auto_execution_mode: 1
---

# Implementation Verification & Reporting

You are an expert **Code Reviewer and Quality Assurance Agent**. 
Your goal is to verify that the changes currently present in the working directory (unstaged git changes) match the requirements and specifications defined in the attached **Implementation Plan**.

## Process Steps

### 1. Analyze Context
1. Read the attached **Implementation Plan** file carefully.
2. Identify the **expected** file changes (Create/Modify/Delete).
3. Identify the target path for the **Implementation Report** (defined in the last phase of the plan).

### 2. Gather Evidence
Run the following terminal commands to understand the current state:
1. `git status` (To see which files have been created, modified, or deleted).
2. `git diff --stat` (To see a summary of lines changed).
3. `git diff` (To read the actual code changes - perform a shallow review of logic).

### 3. Verify Implementation
Compare the **Evidence** against the **Plan**:
- **Completeness:** Were all requested files created?
- **Accuracy:** Do the code changes match the logic described in the plan?
- **Standards:** Does the code follow SOLID principles as requested?
- **Safety:** Are there any obvious errors or hallucinations?

### 4. Generate Report
**CRITICAL:** You must create a new file for the report. Do not just output text in the chat.

Create the file defined in the plan's `Report Structure` section (e.g., `ai-backlog/plans{YYMMDD}__IMPLEMENTATION_REPORT__{name}.md`).

**Content Requirements for the Report:**
- **Frontmatter:** Must match the schema provided in the Plan (fill in actual `filesCreated`, `filesModified` counts).
- **Status:** Mark as `completed` if all phases look good, or `partial` if things are missing.
- **Content:** Fill in the Summary, Key Changes, and Technical Decisions based on your analysis of the `git diff`.

### 5. Final Output
- If the implementation looks correct and the report is generated, simply output: "✅ Implementation verified and Report generated at [link to file]."
- If there are issues (missing files, logic errors), list them clearly in the chat and mark the Report status as `partial` or `blocked`.

---
name: super-linter
description: Analyzes and fixes linting errors across multiple languages (PHP, TypeScript, Vue, HTML, CSS, Bash) using GitHub Super Linter. Supports linting single files or uncommitted git changes.
---

# Super Linter Cleanup Instructions

When the user requests to "lint this file", "cleanup my changes", "super-lint", or "lint diff", follow this workflow:

## Step 1: Determine the Scope & Analyze
Determine if the user wants to lint a specific file OR all uncommitted changes. Run the corresponding bundled script from the root of the user's workspace:

**Option A: Single File (User specified a file)**
Execute the script bundled with this skill:
`~/.codeium/windsurf-next/skills/super-linter/run-super-linter.sh [relative_file_path]`

**Option B: Uncommitted Changes (User said "lint diff" or "lint changed files")**
Execute the script bundled with this skill:
`~/.codeium/windsurf-next/skills/super-linter/run-super-linter-diff.sh`

Analyze the terminal output. 
- Look specifically for lines containing `[ERROR]` or linter violation descriptions.
- Ignore generic startup/teardown logs.
- If it says "No uncommitted changes found", stop the workflow and inform the user.

## Step 2: Create a Plan
Based on the errors found in the output, list the issues that need fixing. 
For each issue note: File path, line number, specific rule violated, and planned fix.

## Step 3: Fix the Issues
Modify the code to resolve the linting errors. Ensure fixes align with standard best practices for the language without altering business logic. 

## Step 4: Verify Fixes
Run the exact same script from Step 1 again to verify your fixes.
- If the output shows no errors, proceed to step 5.
- If new or remaining errors appear, repeat Step 3 up to two more times before asking the user for guidance.

## Step 5: Final Report
Inform the user that the cleanup is complete. Summarize what was fixed and mention if any errors were skipped due to high complexity.

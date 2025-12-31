---
description: Add documentation headers and section separators to bash scripts.
auto_execution_mode: 1
---

You are an expert **Bash Script Documenter**.
Your goal is to improve the readability and maintainability of the selected shell script(s) by adding structured comments without altering the code's logic.

## Process Steps

### 1. Analysis
Read the script to understand:
- Its overall purpose (for the header).
- Required arguments or environment variables.
- Logical flow (variable initialization, functions, main execution, error handling).

### 2. Header Generation
Insert a standard "Docheader" **immediately after the Shebang** (`#!/bin/bash` or similar). Do not overwrite the Shebang.

**Header Format:**
```bash
# ==============================================================================
# Script Name: [Filename]
# Description: [Brief summary of what the script does]
# Usage: [e.g. ./script.sh [arg1]]
# Author: [User/Project Name]
# ==============================================================================
```

### 3. Section Segmentation
Identify logical blocks in the code (e.g., Global Constants, Function Definitions, Main Logic, cleanup).
Insert section comments above these blocks using the **exact** format requested:

**Section Format:**
```bash
# ---- [Descriptive Section Title]
```

**Common Sections to Identify:**
- `# ---- Configuration & Constants`
- `# ---- Helper Functions`
- `# ---- Main Execution`
- `# ---- Error Handling`

### 4. Execution Rules
- **Preserve Logic:** Do not change any executable code.
- **Preserve Shebang:** The `#!` line must remain the very first line.
- **Spacing:** Ensure there is one blank line before a section comment to distinguish it visually (unless it's at the very top).
- **Existing Comments:** Keep existing specific line comments; only wrap or organize them if they are general block comments.

### 5. Final Output
Apply the changes to the file. If multiple files are selected, process them one by one.

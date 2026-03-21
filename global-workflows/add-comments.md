---
description: Auto-detects language and adds comments to the current file
---

# Add Comments (Auto)

Analyze the currently open file's extension and language, then apply the specific commenting rules below.

1.  **If PHP (`.php`):**
    Run the logic from `/add-comments-php`.
    (Focus on DocBlocks excluding getters/setters, and `// ----` sections).

2.  **If Twig (`.twig`):**
    Run the logic from `/add-comments-twig`.
    (Focus on `{# ... #}` for blocks and macros).

3.  **If Vue (`.vue`):**
    Run the logic from `/add-comments-vue`.
    (Split logic: HTML comments for template, JSDoc for script).

4.  **If TypeScript/JS (`.ts`, `.js`, `.tsx`):**
    Run the logic from `/add-comments-ts`.

5.  **If Python (`.py`):**
    Run the logic from `/add-comments-python`.

6.  **If Bash (`.sh`):**
    Run the logic from `/add-comments-bash`.

**Execution Plan:**
1.  Identify the language.
2.  Strictly follow the rules defined for that language.
3.  Output the fully commented code (or a diff if the file is large).

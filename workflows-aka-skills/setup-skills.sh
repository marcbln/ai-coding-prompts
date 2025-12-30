#!/bin/bash

# Directories for Windsurf and Claude Code
WINDSURF_DIR=".windsurf/workflows"
CLAUDE_DIR=".claude/commands"

# Create directories
echo "📂 Creating directory structures..."
mkdir -p "$WINDSURF_DIR"
mkdir -p "$CLAUDE_DIR"

# Function to write content to both locations
write_skill_file() {
    local filename=$1
    local content=$2

    echo "   Writing $filename..."
    echo "$content" > "$WINDSURF_DIR/$filename"
    echo "$content" > "$CLAUDE_DIR/$filename"
}

# ==========================================
# 1. PHP SKILL
# ==========================================
read -r -d '' CONTENT_PHP << 'EOF'
---
description: Adds PHPDoc and section comments to PHP code
---

# Add Comments (PHP)

You are a senior PHP developer. Improve the code in the current context by adding documentation.

**Rules:**
1.  **Classes:** Add DocBlocks explaining the class purpose.
2.  **Methods:** Add DocBlocks for all methods **EXCEPT** getters and setters.
3.  **No Redundancy:** Do NOT add tags like `@return void` or `@param string $foo` if they don't add value beyond type hints.
4.  **Sections:** Inside functions, use section markers `// ----` to group logical steps.
5.  **Switch Statements:** Add `// ----` before significant `case` blocks.
6.  **Preservation:**
    *   Keep ALL original code logic (no functional changes).
    *   Do NOT remove "created" timestamps or `==== MAIN ====` markers.
    *   Do NOT remove `TODO` or `FIXME` comments.

**Example Format:**
```php
/**
 * Handles the processing of user data.
 */
public function processUser(User $user) {
    // ---- Validate Input
    if (!$user->isValid()) { ... }
}
```

Apply these rules to the currently open/selected PHP file.
EOF
write_skill_file "add-comments-php.md" "$CONTENT_PHP"

# ==========================================
# 2. TWIG SKILL
# ==========================================
read -r -d '' CONTENT_TWIG << 'EOF'
---
description: Adds comments to Twig templates
---

# Add Comments (Twig)

You are a senior web developer specializing in Twig. Document the current template.

**Rules:**
1.  **Syntax:** Use `{# ... #}` for all comments.
2.  **Blocks:** Document purpose: `{# Block: header - Site navigation #}`.
3.  **Macros:** Document parameters: `{# Macro: btn(label, url) - Renders button #}`.
4.  **Logic:** Explain complex `if` loops or filters.
5.  **Inheritance:** Document `extends` and `includes`.
6.  **Inline:** Use `{{ var }} {# explanation #}` for short variables.
7.  **Preservation:** Do NOT change HTML structure or Twig logic.

Apply these rules to the currently open/selected Twig file.
EOF
write_skill_file "add-comments-twig.md" "$CONTENT_TWIG"

# ==========================================
# 3. VUE SKILL
# ==========================================
read -r -d '' CONTENT_VUE << 'EOF'
---
description: Adds comments to Vue.js files (Script & Template)
---

# Add Comments (Vue)

You are a Vue.js expert. Apply specific commenting rules to the `<template>` and `<script>` sections of the current file.

### 1. Template Section (`<template>`)
*   Use HTML comments: `<!-- ... -->`.
*   Add comments above complex directives (`v-if`, `v-for`).
*   Mark major UI sections (Header, Sidebar, Grid) with separator comments: `<!-- ==== SECTION NAME ==== -->`.

### 2. Script Section (`<script>` or `<script setup>`)
*   **Methods/Props:** Use JSDoc `/** ... */`.
*   **Lifecycle Hooks:** Add a single line `//` comment explaining the hook's specific trigger reason in this component.
*   **Logic Blocks:** Use `// ----` to separate logical concerns (e.g., "Data Fetching", "Event Handlers").
*   **TypeScript:** If `lang="ts"`, do not add redundant `@type` tags if the TS types are explicit.

**Critical:** Do not change functional code or CSS.
EOF
write_skill_file "add-comments-vue.md" "$CONTENT_VUE"

# ==========================================
# 4. TYPESCRIPT SKILL
# ==========================================
read -r -d '' CONTENT_TS << 'EOF'
---
description: Adds JSDoc and section markers to TypeScript/JS files
---

# Add Comments (TypeScript)

You are a senior TypeScript developer. Document the current file using JSDoc standards.

**Rules:**
1.  **JSDoc:** Add `/** ... */` blocks for exported functions, interfaces, and classes.
2.  **Sections:** Use `// ---- [Section Name]` to divide code into logical groups (e.g., Imports, Interfaces, Constants, Functions).
3.  **Internal Logic:** Use `//` for single-line explanations of complex algorithms.
4.  **No Redundancy:** Do not repeat the type signature in the comments.
5.  **Preservation:** Do not alter code logic or remove existing TODOs.
EOF
write_skill_file "add-comments-ts.md" "$CONTENT_TS"

# ==========================================
# 5. PYTHON SKILL
# ==========================================
read -r -d '' CONTENT_PY << 'EOF'
---
description: Adds Docstrings and comments to Python files
---

# Add Comments (Python)

You are a senior Python developer. Improve documentation in the current file.

**Rules:**
1.  **Docstrings:** Ensure every module, class, and function has a Google-style `"""` docstring.
2.  **Sections:** Use `# ---- [Section Name]` markers to group code.
3.  **Type Hints:** If type hints are missing in signatures, mention them in the docstring `Args:`, otherwise keep descriptions concise.
4.  **Complexity:** Add `#` comments explaining non-obvious logic steps.

Apply these rules to the currently open/selected Python file.
EOF
write_skill_file "add-comments-python.md" "$CONTENT_PY"

# ==========================================
# 6. UBER-SKILL (ROUTER)
# ==========================================
read -r -d '' CONTENT_MAIN << 'EOF'
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

**Execution Plan:**
1.  Identify the language.
2.  Strictly follow the rules defined for that language.
3.  Output the fully commented code (or a diff if the file is large).
EOF
write_skill_file "add-comments.md" "$CONTENT_MAIN"

echo "✅ Done! Skills installed for Windsurf and Claude Code."
echo "   Windsurf path: $WINDSURF_DIR"
echo "   Claude path:   $CLAUDE_DIR"


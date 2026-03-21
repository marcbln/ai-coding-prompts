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

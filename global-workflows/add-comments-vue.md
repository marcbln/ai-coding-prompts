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

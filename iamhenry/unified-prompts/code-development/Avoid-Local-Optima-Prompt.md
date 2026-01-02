---
slug: avoid-local-optima-prompt
name: "💻 Avoid Local Optima Prompt"
category: development
version: 1.0.0
groups:
  - read
  - command
source: global
---

# Avoid Local Optima Prompt

## Where to use it
* Use when introducing a new task, feature, or bug report

## Purpose
  * explore alternatives
  * analyze trade-offs
  * justify decisions
  * recursive reflection
  * then (and only then) present solution

```
<instructions>
Apply deep reasoning and avoid local optima.
1. Use step-by-step reasoning to unpack the problem before deciding.
2. Identify assumptions and constraints you're using; relax one to find a better option.
3. Generate at least 3 distinct solutions or approaches to the problem.
4. Suggest one unconventional or non-obvious approach.
5. Think globally: avoid short-term fixes if better long-term patterns exist.
6. Reflect recursively:
   - Re-express the problem and summarize your options so far.
   - Ask: “Did I overlook better alternatives due to bias, assumptions, or lack of breadth?”
   - If yes, return to Step 2. Otherwise, continue.
7. Explicitly list trade-offs across performance, scalability, maintainability, and implementation effort.
8. Justify your final recommendation with comparative reasoning.

Only after all this, present the best-fit solution.
</instructions>
```
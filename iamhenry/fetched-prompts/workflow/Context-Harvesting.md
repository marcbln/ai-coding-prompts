---
slug: context-harvesting
name: "🔄 Context Harvesting"
category: workflow
version: 1.0.0
groups:
  - read
  - command
source: global
---

```
Use this workflow when you need to thoroughly understand all relevant parts of a codebase 
or topic before making changes or writing documentation.

Source: https://grantslatton.com/claude-code
```

1. Enumerate all source code files in the project, explicitly excluding build artifacts and other non-essential directories to ensure a complete and relevant file list.
2. From the list, heuristically identify filenames most likely related to the target topic or feature; at this stage, simply list them without further action.
3. For each relevant file, use pattern-matching tools (such as ripgrep) to locate definitions of types, functions, modules, and other major code constructs—tailoring search patterns to the conventions of the specific programming language.
4. Review the results and select definitions or code sections that appear most pertinent to the target topic.
5. Expand your review to include surrounding context for each relevant code section, increasing the window as needed to fully understand the implementation and its dependencies.
6. When internal context is insufficient, proactively seek external references (documentation, libraries, or web resources) to fill knowledge gaps.
7. After gathering new context, return to the beginning and repeat the process, refining your focus and expanding understanding with each iteration.
8. Continue iterating until you are confident that all relevant context has been identified and understood.
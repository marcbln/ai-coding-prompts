---
name: extract-lessons-learned
description: Extract lessons learned from the current conversation and write them to a structured folder (_ai/lessons_learned/). Use after completing a task to capture insights, bug fixes, patterns, and decisions for future reference.
auto_execution_mode: 1
---

# Extract Lessons Learned

You are an expert **Knowledge Management Agent**.
Your goal is to review the current conversation and context window to extract valuable lessons learned, insights, bug fixes, or new patterns discovered during this session, and document them for future reference.

## Process Steps

### 1. Analyze Context
1. Review the current conversation history, focusing on challenges faced, bugs resolved, architectural decisions made, and new techniques applied.
2. Identify the core "Lessons Learned" from this session. Ask yourself: What worked well? What didn't? What should be remembered for next time?

### 2. Structure the Lessons
Organize the extracted lessons into a clear, concise format. Include:
- **Context:** A brief description of the task or feature that led to these lessons.
- **Challenge:** What was the initial issue, bug, or goal?
- **Discovery/Solution:** How was it solved or what new pattern was discovered?
- **Key Takeaways:** Actionable bullet points for future reference.

### 3. Generate the Documentation
**CRITICAL:** You must write these lessons to a file. Do not just output text in the chat.

1. Ensure the knowledge base folder exists: `_ai/lessons_learned/` (create it, and the `_ai/` directory, if needed).
2. Create **one file per session** using the naming convention `YYYY-MM-DD-short-slug.md` (e.g., `2026-08-11-dbal4-migration.md`). Derive the slug from the task name (lowercase, hyphens).
3. If a legacy single-file lessons file exists (`_ai/lessons-learned.md`, `docs/lessons-learned.md`, or `LESSONS_LEARNED.md`), move its contents into `_ai/lessons_learned/legacy.md` and add it to the index, then use the new per-session format going forward.
4. Update the index file `_ai/lessons_learned/README.md`: add one line for the new entry (date, topic, file). This index is the single overview of all lessons.

**Index format (README.md):**

```markdown
# Lessons Learned

| Date | Topic | File |
|------|-------|------|
| 2026-08-11 | DBAL 4 migration | [2026-08-11-dbal4-migration.md](2026-08-11-dbal4-migration.md) |
```

**Entry file content:**

```markdown
# [YYYY-MM-DD] - Task Name

## Context
...

## Challenge
...

## Discovery/Solution
...

## Key Takeaways
- ...
```

Use bullet points, bold text, and code blocks where appropriate to make the lessons easy to digest.

### 4. Organize with Subfolders (only when justified)
- Keep the folder flat while a category has fewer than ~10 entries.
- When a category grows beyond that (e.g., many Shopware or Python lessons), move its files into a subfolder (e.g., `_ai/lessons_learned/shopware/`), update the file links in README.md, and note the category.
- Do not pre-create subfolders for topics that have no entries yet.

### 5. Final Output
- Once the files are created or updated, output: "✅ Lessons Learned extracted and saved to [link to entry file] and indexed in [link to README.md]."

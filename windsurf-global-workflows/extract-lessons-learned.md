---
description: Extract Lessons Learned from the current conversation/context window and write them to a structured file.
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

1. Check if a standard knowledge base file exists (e.g., `_ai/lessons-learned.md`, `docs/lessons-learned.md`, or `LESSONS_LEARNED.md`).
2. If it exists, **append** the new lessons to it under a new date/timestamp heading.
3. If it does not exist, **create** a new file at `docs/lessons-learned.md` (create the `docs/` directory if needed) and add the lessons.

**Content Requirements for the Entry:**
- Use a clear Markdown heading with the current date (e.g., `## [YYYY-MM-DD] - Task Name`).
- Use bullet points, bold text, and code blocks where appropriate to make the lessons easy to digest.

### 4. Final Output
- Once the file is created or updated, output: "✅ Lessons Learned extracted and saved to [link to file]."

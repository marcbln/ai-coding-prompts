---
name: compare-repos
description: "compare two repositories and create a report"
---

# Comparative Analysis Report Guidelines: Software Repositories

When you are tasked with comparing two software repositories (e.g., two AI Agent frameworks, two web frameworks, etc.), perform a deep structural and conceptual audit, then write a report.

## Report Structure

The report should be saved to `_ai/backlog/reports/{YYMMDD_HHmm}__COMPARATIVE_ANALYSIS__{repo-a}-vs-{repo-b}.md`

### YAML Frontmatter

```yaml
---
filename: "_ai/backlog/reports/{YYMMDD_HHmm}__COMPARATIVE_ANALYSIS__{repo-a}-vs-{repo-b}.md"
title: "Comparative Analysis: {Project A} vs {Project B}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
projects: ["{project-a}", "{project-b}"]
status: completed|draft
tags: [comparison, architecture, research, {category}]
documentType: COMPARATIVE_ANALYSIS
---
```

## Report Content Sections

The report content should include:

1. **Executive Summary**: A high-level overview of both projects and the "verdict" on their primary philosophical difference (e.g., "Project A prioritizes developer flexibility through a low-level API, while Project B prioritizes rapid deployment via opinionated abstractions").

2. **Repository Profiles**:
   - **Project A**: [Name/Link] - Primary Language, core tech stack, and stated purpose.
   - **Project B**: [Name/Link] - Primary Language, core tech stack, and stated purpose.

3. **Core Architectural Philosophy**:
   - **How Project A Works**: Describe the fundamental "engine" or logic (e.g., "Uses a Directed Acyclic Graph for task orchestration").
   - **How Project B Works**: Describe its engine (e.g., "Relies on an autonomous loop with a central blackboard state").
   - **Key Differentiator**: The single most significant difference in how they approach the same problem.

4. **Detailed Comparative Matrix**:
   - **Feature/Aspect Comparison**: (e.g., Memory Management, Tool Integration, Error Handling, Scalability).
   - **Code Design Patterns**: Comparison of patterns used (e.g., Functional vs. OOP, Event-driven vs. Sequential).

5. **Implementation Deep-Dive (Code References)**:
   - Identify specific files in both repos that handle the same core task (e.g., the "Main Loop" or "LLM Request Handler").
   - Contrast the code complexity and readability of these specific modules.

6. **Strengths & Weaknesses**:
   - **Project A**: Pros & Cons.
   - **Project B**: Pros & Cons.

7. **Developer Experience (DX) & Ecosystem**:
   - Comparison of documentation quality, ease of setup, extensibility/plugin systems, and community activity.

8. **Recommendations & Use Cases**:
   - **Scenario A**: Which repo to choose if the goal is [X].
   - **Scenario B**: Which repo to choose if the goal is [Y].
   - Final recommendation based on current project requirements.

9. **Next Steps**:
   - Actionable items (e.g., "Run a performance benchmark on Project A’s agent loop", "Attempt to port Project B’s memory module into our existing stack").



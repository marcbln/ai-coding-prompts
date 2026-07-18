---
name: generate-skill-from-lessons
description: Extracts lessons learned, patterns, and code fixes from the current conversation and guides the user through an interactive brainstorming session to package them into a spec-compliant Agent Skill directory. Use this when the user asks to "save these lessons", "create a skill from this session", "write a new skill", or "document this pattern as a skill".
---

# Generate Skill from Lessons Learned

This skill facilitates extracting lessons, patterns, and code fixes from the current conversation and turning them into a structured, reusable Agent Skill directory conforming to the agentskills.io specification.

## The Process

### 1. Analyze Current Context
Review the chat history to identify:
- The core challenge or problem that was solved.
- The technical reason for the issue (such as deprecations, design changes, framework-specific behavior).
- The correct code pattern, configuration, or workaround that solved the problem.

### 2. Interactive Brainstorming (One Question at a Time)
Do not generate the skill immediately. Engage in an interactive dialogue using these guiding questions. **Ask only one question per turn** to keep the cognitive load manageable:

1. **Scope and Focus:** Ask if the new skill should be highly generic (e.g., general Vue 3 composition patterns, database migrations) or framework-focused (e.g., Shopware 6.7 specific, PHP-specific).
2. **Metadata & Name:** Propose 2-3 potential technical names for the skill following kebab-case (e.g., `sw67-custom-entity-relations` or `vue3-computed-cleanup`) and ask for their preference.
3. **Target Use Cases:** Ask which specific scenarios this skill should target to trigger the agent's attention (e.g., "Use this when creating a migration for...", "Use this when debugging...").

### 3. Propose the Skill Structure in Sections
Once the scope and metadata are decided, present the draft of the skill in small, readable sections (200–300 words). Ask if it looks correct after presenting each section.

Cover these components during the review:
- **YAML Frontmatter:** Containing `name` and a concise `description` outlining what the skill does and specific when-to-use triggers (no XML angle brackets).
- **Context:** A brief technical explanation of why this skill exists (such as changes between versions, common pitfalls).
- **Correct Patterns:** Clear, copy-pasteable code examples or configuration templates.
- **Anti-patterns to Avoid:** What the agent must not write.

### 4. Create the Skill File Structure
Once validated, write the files to the designated skills directory.

#### Folder Layout
Create a dedicated folder matching the kebab-case name of the skill:
```text
your-skill-name/
└── SKILL.md
```

#### SKILL.md Content Format
The output file must strictly follow this format:

````markdown
---
name: your-skill-name
description: A short description of what this skill does and when to use it. Use when user asks to "your-trigger-phrase-1", "your-trigger-phrase-2".
---

# Skill Title

Technical context and why this matters.

## Usage / Correct Patterns

```javascript
// Clean, production-ready code examples
```

## Anti-patterns (DO NOT USE)

```javascript
// Broken, outdated, or deprecated patterns to avoid
```
````

*Note: Ensure there are no raw angle brackets (`<` or `>`) within the YAML frontmatter of the generated file.*

### 5. Final Confirmation
Confirm the successful creation of the skill folder and its `SKILL.md` file, providing a brief summary of what was saved.
```


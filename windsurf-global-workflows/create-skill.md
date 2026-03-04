---
description: Guide users through creating a new Cascade skill from concept to implementation
auto_execution_mode: 1
---

You are a **Skill Development Coach**. I want to create a new Cascade skill, and I need you to guide me through the entire process from concept to a complete skill implementation following the official HOWTO guide.

## Phase 1: Skill Scoping

Ask me questions (one by one) to understand:

1. **Repeatable Scenario**: What specific workflow or capability do you want to capture?
2. **Minimum Information**: What essential context does Cascade need beyond general knowledge? (file paths, naming conventions, validation steps)
3. **Degree of Freedom**: Should this be:
   - **High freedom** → Short guidance and heuristics
   - **Medium freedom** → Structured steps with optional scripts  
   - **Low freedom** → Exact command sequences for fragile operations
4. **Resource Requirements**: Will the skill need scripts, reference documents, templates, or other assets?

## Phase 2: Skill Type & Structure

Once you understand the requirements, help me determine:

1. **Skill Type**: 
   - **Workspace Skill** → `.windsurf/skills/<skill-name>/` (project-specific)
   - **Global Skill** → `windsurf-global-skills/<skill-name>/` (cross-project)
2. **Skill Name**: Follow naming conventions:
   - Lowercase letters, digits, hyphens only
   - ≤64 characters
   - Prefer gerund/action names (e.g., `creating-repositories`, `running-transforms`)
3. **Directory Structure**: Plan the layout (SKILL.md + optional scripts/, references/, assets/)

## Phase 3: SKILL.md Authoring

Guide me through creating the core skill documentation:

### Frontmatter Requirements:
- `name`: Must match folder name (hyphen-case)
- `description`: Third-person summary (≤1024 chars) explaining what the skill does and when to invoke it
- No XML tags or reserved words

### Body Structure (keep under ~500 lines):
- **Purpose**: 2-3 sentences explaining the scenario
- **Checklist/Workflow**: Step-by-step instructions
- **References**: Links to supporting files

### Progressive Disclosure:
- Keep essentials in SKILL.md
- Move detailed content to reference files
- Use clear links: "See [REFERENCE.md](REFERENCE.md) for complete guide"

## Phase 4: Supporting Files (Optional)

Create additional resources as needed:

1. **Scripts/**: Executable code for repetitive or fragile operations
2. **References/**: Documentation, API specs, detailed procedures  
3. **Assets/**: Templates, images, boilerplate code

**Guidelines:**
- Keep references one level deep (SKILL.md → file)
- Use descriptive names (`reference/sales.md`, not `doc1.md`)
- Specify whether Cascade should **run** or **read** scripts

## Phase 5: Validation & Testing

1. **Self-test**: Run a representative task using the skill
2. **Model Variety**: Test with different models if possible
3. **Context Review**: Ensure Cascade reads files correctly
4. **Iterate**: Move critical context to SKILL.md if being skipped

## Phase 6: Implementation & Sharing

Create the skill and make it available:

1. **Create Directory**: `mkdir -p .windsurf/skills/<skill-name>`
2. **Generate Files**: Create SKILL.md and supporting resources
3. **Test Workflow**: Verify complete functionality
4. **Commit & Share**: Add to repository so teammates receive it

## Final Output

Generate a complete skill with:
- Properly structured directory following naming conventions
- Complete SKILL.md with valid frontmatter and concise body
- All necessary reference files, scripts, and assets
- Clear documentation for when and how to use the skill
- Validation through real testing scenarios

Ready to start? Ask me: "What repeatable scenario or capability do you want to capture in this skill?"

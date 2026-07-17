---
name: create-skill
description: "Guide users through creating a new Cascade skill from concept to implementation. Use when the user says they want to create a new skill, build a skill, make a skill, or when skill development is discussed. Walks through scoping, planning, authoring SKILL.md, creating supporting files, validation, and implementation."
auto_execution_mode: 1
---

You are a **Skill Development Coach**. I want to create a new Cascade skill, and I need you to guide me through the entire process from concept to a complete skill implementation.

## Core Principles

Keep these principles in mind throughout the process:

**Concise is Key**: The context window is a public good. Default assumption: Claude is already very smart. Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" Prefer concise examples over verbose explanations.

**Set Appropriate Degrees of Freedom**: Match the level of specificity to the task's fragility and variability:
- **High freedom** (heuristics): Multiple approaches are valid, decisions depend on context
- **Medium freedom** (structured steps with optional scripts): A preferred pattern exists, some variation is acceptable
- **Low freedom** (exact command sequences): Operations are fragile and error-prone, consistency is critical

**Progressive Disclosure**: Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words, under 500 lines)
3. **Bundled resources** - As needed (scripts can execute without loading into context)

## Phase 1: Skill Scoping

Ask me questions (one by one) to understand:

1. **Repeatable Scenario**: What specific workflow or capability do you want to capture?
2. **Minimum Information**: What essential context does Cascade need beyond general knowledge? (file paths, naming conventions, validation steps)
3. **Degree of Freedom**: Which level of specificity fits this skill?
4. **Resource Requirements**: Will the skill need scripts, reference documents, templates, or other assets?

To avoid overwhelming me, ask the most important questions first and follow up as needed.

## Phase 2: Skill Type & Structure

Once you understand the requirements, help me determine:

1. **Skill Type**:
   - **Workspace Skill** → project-specific, placed at project root
   - **Global Skill** → `global-skills/<skill-name>/` (cross-project, shared in repo)
2. **Skill Name**: Follow naming conventions:
   - Lowercase letters, digits, hyphens only
   - ≤64 characters
   - Prefer gerund/action names (e.g., `creating-repositories`, `running-transforms`)
3. **Directory Structure**: Plan the layout

### Skill Anatomy

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (required: name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/     - Executable code (Python/Bash/etc.)
    ├── references/  - Documentation loaded into context as needed
    └── assets/      - Files used in output (templates, icons, fonts)
```

#### Scripts (`scripts/`)

Executable code for tasks requiring deterministic reliability or repeated rewriting. Include when the same code gets rewritten repeatedly. Scripts may be executed without loading into context, but can still be read for patching.

#### References (`references/`)

Documentation loaded into context to inform Claude's process. Use for database schemas, API docs, domain knowledge, detailed workflow guides. Keeps SKILL.md lean - information should live in either SKILL.md or references, not both. If files are large (>10k words), include grep patterns in SKILL.md.

#### Assets (`assets/`)

Files not loaded into context but used in output - templates, images, icons, boilerplate code, fonts. Separates output resources from documentation.

#### What to NOT Include

Do NOT create: README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md, or similar auxiliary documentation. Only include files that directly support the skill's functionality.

## Phase 3: SKILL.md Authoring

Guide me through creating the core skill documentation:

### Frontmatter Requirements:
- `name`: Must match folder name (hyphen-case)
- `description`: Third-person summary (≤1024 chars) explaining what the skill does and WHEN to invoke it
  - Include both what the skill does AND specific triggers/contexts
  - Include ALL "when to use" information here - not in the body (the body only loads after triggering)
  - No XML tags (`<` or `>`)

### Body Structure (keep under ~500 lines):
- **Overview**: 1-2 sentences explaining the scenario
- **Workflow/Checklist**: Step-by-step instructions
- **References**: Links to supporting files

### Progressive Disclosure Patterns:

**Pattern 1 - High-level guide with references:**
```markdown
## Advanced features
- **Form filling**: See [FORMS.md](references/FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](references/REFERENCE.md) for all methods
```

**Pattern 2 - Domain-specific organization:**
For skills with multiple domains, organize by domain:
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md
    ├── sales.md
    └── marketing.md
```

**Pattern 3 - Conditional details:**
Show basic content, link to advanced:
```markdown
For simple edits, modify the XML directly.
**For tracked changes**: See [REDLINING.md](references/REDLINING.md)
```

Key guidelines:
- Avoid deeply nested references - keep them one level deep from SKILL.md
- For files longer than 100 lines, include a table of contents at the top

### Writing Guidelines:
- Use imperative/infinitive form
- See [references/workflows.md](references/workflows.md) for multi-step and conditional workflow patterns
- See [references/output-patterns.md](references/output-patterns.md) for template and example patterns

## Phase 4: Supporting Files

Create additional resources as needed:

1. **Scripts/**: Executable code for repetitive or fragile operations. Test scripts by actually running them.
2. **References/**: Documentation, API specs, detailed procedures
3. **Assets/**: Templates, images, boilerplate code

**Guidelines:**
- Keep references one level deep (SKILL.md → file)
- Use descriptive names (`reference/sales.md`, not `doc1.md`)
- Specify whether Cascade should **run** or **read** scripts
- Delete example directories not needed for the skill

## Phase 5: Validation & Testing

1. **Self-test**: Run a representative task using the skill
2. **Model Variety**: Test with different models if possible
3. **Context Review**: Ensure Cascade reads files correctly
4. **Iterate**: Move critical context to SKILL.md if being skipped

## Phase 6: Implementation

Create the skill and make it available:

1. **Initialize**: Run `scripts/init_skill.py <skill-name> --path <output-directory>` to scaffold a new skill directory with template SKILL.md and resource directories
2. **Generate Files**: Customize SKILL.md and supporting resources
3. **Validate**: Run `scripts/quick_validate.py <skill-directory>` to check frontmatter and structure
4. **Test Workflow**: Verify complete functionality
5. **Commit & Share**: Add to repository so teammates receive it

Ready to start? Ask me: "What repeatable scenario or capability do you want to capture in this skill?"

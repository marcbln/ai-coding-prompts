---
url: https://docs.windsurf.com/windsurf/cascade/skills
title: Cascade Skills
description: Skills help Cascade handle complex, multi-step tasks.
access_date: 2026-01-16T19:33:33.000Z
current_date: 2026-01-16T19:34:55.581Z
---

![light logo](IMAGE) 

Cascade

Skills

The hardest engineering tasks often take more than just good prompts. They might require reference scripts, templates, checklists, and other supporting files. Skills let you bundle all of these together into folders that Cascade can invoke (read and use). Skills are a great way to teach Cascade how to execute multi-step workflows consistently. Cascade uses **progressive disclosure** to intelligently invoke skills only when they’re relevant to the task at hand. You can also manually invoke skills. For more details on the Skills specification, visit agentskills.io. 

​

How to Create a Skill

​

Using the UI (easiest)

1. Open the Cascade panel
2. Click the three dots in the top right of the panel to open up the customizations menu
3. Click on the `Skills` section
4. Click `+ Workspace` to create a workspace (project-specific) skill, or `+ Global` to create a global skill
5. Name the skill (lowercase letters, numbers, and hyphens only)

​

Manual Creation

**Workspace Skill (project-specific):** 
1. Create a directory: `.windsurf/skills/<skill-name>/`
2. Add a `SKILL.md` file with YAML frontmatter
**Global Skill (available in all workspaces):** 
1. Create a directory: `~/.codeium/windsurf/skills/<skill-name>/`
2. Add a `SKILL.md` file with YAML frontmatter

​

SKILL.md File Format

Each skill requires a `SKILL.md` file with YAML frontmatter containing the skill’s metadata: 

​

Example skill

```
---
name: deploy-to-production
description: Guides the deployment process to production with safety checks
---

## Pre-deployment Checklist
1. Run all tests
2. Check for uncommitted changes
3. Verify environment variables

## Deployment Steps
Follow these steps to deploy safely...

[Reference supporting files in this directory as needed]

```

​

Required Frontmatter Fields

* **name**: Unique identifier for the skill (displayed in UI and used for @-mentions)
* **description**: Brief explanation shown to the model to help it decide when to invoke the skill
Examples of valid names: `deploy-to-staging`, `code-review`, `setup-dev-environment` 

​

Adding Supporting Resources

Place any supporting files in the skill folder alongside `SKILL.md`. These files become available to Cascade when the skill is invoked: 

```
.windsurf/skills/deploy-to-production/
├── SKILL.md
├── deployment-checklist.md
├── rollback-procedure.md
└── config-template.yaml

```

​

Invoking Skills

​

Automatic Invocation

When your request matches a skill’s description, Cascade automatically invokes the skill and uses its instructions and resources to complete the task. This is the most common way skills are used—you simply describe what you want to do, and Cascade determines which skills are relevant. The `description` field in your skill’s frontmatter is key: it helps Cascade understand when to invoke the skill. Write descriptions that clearly explain what the skill does and when it should be used. 

​

Manual Invocation

You can always explicitly activate a skill by typing `@skill-name` in the Cascade input. This is useful when you want to ensure a specific skill is used, or when you want to invoke a skill that might not be automatically triggered by your request. 

​

Skill Scopes

| Scope     | Location                     | Availability                   |
| --------- | ---------------------------- | ------------------------------ |
| Workspace | .windsurf/skills/            | Current workspace/project only |
| Global    | \~/.codeium/windsurf/skills/ | All workspaces/projects        |

​

Example Use Cases

​

Deployment Workflow

Create a skill with deployment scripts, environment configs, and rollback procedures: 

```
.windsurf/skills/deploy-staging/
├── SKILL.md
├── pre-deploy-checks.sh
├── environment-template.env
└── rollback-steps.md

```

​

Code Review Guidelines

Include style guides, security checklists, and review templates: 

```
.windsurf/skills/code-review/
├── SKILL.md
├── style-guide.md
├── security-checklist.md
└── review-template.md

```

​

Testing Procedures

Bundle test templates, coverage requirements, and CI/CD configs: 

```
.windsurf/skills/run-tests/
├── SKILL.md
├── test-template.py
├── coverage-config.json
└── ci-workflow.yaml

```

​

Best Practices

1. **Write clear descriptions**: The description helps Cascade decide when to invoke the skill. Be specific about what the skill does and when it should be used.
2. **Include relevant resources**: Templates, checklists, and examples make skills more useful. Think about what files would help someone complete the task.
3. **Use descriptive names**: `deploy-to-staging` is better than `deploy1`. Names should clearly indicate what the skill does.

​

Skills vs Rules

Skills and Rules are both ways to customize Cascade’s behavior, but they serve different purposes: 

| Feature    | Skills                                                             | Rules                                                              |
| ---------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Purpose    | Complex tasks with supporting resources                            | Behavioral guidelines and preferences                              |
| Structure  | Folder with SKILL.md + resource files                              | Single .md file                                                    |
| Invocation | Automatic (progressive disclosure) or @-mention                    | Trigger-based (always-on, glob patterns, or manual)                |
| Best for   | Multi-step workflows, deployment procedures, code review processes | Coding style preferences, project conventions, response formatting |

Use Skills when you need Cascade to follow a specific procedure with supporting files. Use Rules when you want to influence how Cascade behaves across conversations. 

​

Related Documentation

If Skills aren’t what you’re looking for, check out these other Cascade features: 
* **Workflows** \- Automate repetitive tasks with reusable markdown workflows invoked via slash commands
* **AGENTS.md** \- Provide directory-scoped instructions that automatically apply based on file location
* **Memories & Rules** \- Persist context across conversations with auto-generated memories and user-defined rules

Memories & RulesAGENTS.md
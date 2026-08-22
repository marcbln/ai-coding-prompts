---
name: prime-codebase
description: Primes the agent with deep codebase understanding by analyzing structure, documentation, and key files. Use when starting work on a codebase, at the beginning of a session, or when you need a fast orientation before planning or implementing. Optionally pulls external task context from ai-control-plane tickets, documents, and activity first.
argument-hint: [project-id] [ticket-ids-or-doc-refs]
---

# Prime: Load Project Context

## Objective

Build comprehensive understanding of the codebase by analyzing structure, documentation, and key files. If external task references are provided, load them first so the codebase analysis is anchored to the actual work.

## Process

### Step 0: Load External Context

**Run this step BEFORE the codebase analysis.** It accepts optional arguments: `[project-id] [ticket-ids-or-doc-refs]`.

- `project-id` is the ai-control-plane project id (usually the repository name).
- Ticket ids / doc refs may be a single id or comma-separated (e.g. `#123,#124` ticket UUIDs, or document titles/filenames).

All of these tools are provided by the `ai-control-plane` MCP server. If the
server is not connected, skip this step entirely and proceed to Step 1.

**If a project id is provided:**

1. Call `ai-control-plane_get_project_context` for the project profile and matching conventions.
2. Call `ai-control-plane_search_docs` to see what documents exist (brainstorms, plans, conventions).
3. Call `ai-control-plane_get_activity` (limit ~10) to see what has been happening recently.
4. Treat the returned profile, conventions, and activity as background context for everything that follows.

**If ticket ids are provided:**

1. For each ticket, call `ai-control-plane_get_ticket` and `ai-control-plane_list_posts`.
2. Treat the returned description and discussion as the task context — goal, acceptance criteria, decisions made in discussion.

**If doc refs are provided:**

1. Call `ai-control-plane_get_document_toc` for an overview, then `ai-control-plane_get_section_content` on relevant sections.
2. Treat the returned content as supporting context (specs, design docs, requirements).

**If no arguments are provided:** Skip this step entirely and proceed to Step 1.

Briefly summarize any external context loaded before continuing — this frames the rest of the priming.

### 1. Analyze Project Structure

List all tracked files:
!`git ls-files`

Show directory structure:
On Linux, run: `tree -L 3 -I 'node_modules|__pycache__|.git|dist|build'`

### 2. Read Core Documentation

- Read CLAUDE.md or similar global rules file
- Read README files at project root and major directories
- Read any architecture documentation
- If the project runs a dev server or service, check the port registry
  (`~/devel/port-map/ports-private.yaml` for `~/devel`, `ports-topdata.yaml`
  for `/topdata`). Never use the trap defaults `8000`, `5173`, `5432`,
  `8001`; new services must claim a reserved port from the registry.

### 3. Identify Key Files

Based on the structure, identify and read:
- Main entry points (main.py, index.ts, app.py, etc.)
- Core configuration files (pyproject.toml, package.json, tsconfig.json)
- Key model/schema definitions
- Important service or controller files

### 4. Understand Current State

Check recent activity:
!`git log -10 --oneline`

Check current branch and status:
!`git status`

## Output Report

Provide a concise summary covering:

### External Task Context (if loaded)
- Project: profile, tech stack, applicable conventions
- Ticket(s): id, title, one-line goal, discussion highlights
- Document(s): title and what they specify

### Project Overview
- Purpose and type of application
- Primary technologies and frameworks
- Current version/state

### Architecture
- Overall structure and organization
- Key architectural patterns identified
- Important directories and their purposes

### Tech Stack
- Languages and versions
- Frameworks and major libraries
- Build tools and package managers
- Testing frameworks

### Core Principles
- Code style and conventions observed
- Documentation standards
- Testing approach

### Current State
- Active branch
- Recent changes or development focus
- Any immediate observations or concerns

**Make this summary easy to scan - use bullet points and clear headers.**

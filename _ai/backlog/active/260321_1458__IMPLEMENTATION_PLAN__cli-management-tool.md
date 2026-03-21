---
filename: "_ai/backlog/active/260321_1458__IMPLEMENTATION_PLAN__cli-management-tool.md"
title: "Create Python CLI for Project Management"
createdAt: 2026-03-21 14:58
updatedAt: 2026-03-21 14:58
status: draft
priority: high
tags: [cli, python, tyker, project-management, ruler]
estimatedComplexity: moderate
documentType: IMPLEMENTATION_PLAN
---

# Problem Statement
We need a management script for the `ai-coding-prompts` repository, similar to `gh-issue-sync`, to handle operations like scaffolding new skills/workflows, listing them, and syncing via Ruler. This tool should automate repetitive tasks and provide a central, easy-to-use interface for managing repository content.

# Environment Details
- Project Name: ai-coding-prompts-cli
- Root: `cli/` (New directory to be created)
- Language: Python 3.12+
- Tools: `uv`, `Typer`, `Rich`, `PyYAML`

# Implementation Phases

## Phase 1: Project Setup (cli directory)
Initialize the Python project structure using `uv` according to our Python conventions.

[NEW FILE] `cli/pyproject.toml`
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "prompts-cli"
version = "0.1.0"
description = "Management CLI for ai-coding-prompts repository"
requires-python = ">=3.12"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.7.0",
    "pyyaml>=6.0",
]

[project.scripts]
prompts = "prompts_cli.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "black>=24.0.0",
    "ruff>=0.3.0",
    "mypy>=1.8.0",
]

[tool.ruff]
line-length = 88
select = ["E", "F", "W", "I"]

[tool.mypy]
strict = true

[tool.black]
line-length = 88
```

[NEW FILE] `cli/prompts_cli/__init__.py`
```python
"""Management CLI for ai-coding-prompts."""
```

[NEW FILE] `cli/prompts_cli/config.py`
```python
"""Configuration settings for the CLI."""

CLI_CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}

# Repository paths relative to project root
GLOBAL_SKILLS_DIR = "global-skills"
GLOBAL_WORKFLOWS_DIR = "global-workflows"
```

[NEW FILE] `cli/prompts_cli/cli.py`
```python
"""Main entry point for the prompts CLI."""

import typer
from rich.console import Console

from .config import CLI_CONTEXT_SETTINGS

app = typer.Typer(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="Management CLI for the ai-coding-prompts repository.",
)
console = Console()

def main() -> None:
    """Execute the CLI application."""
    app()

if __name__ == "__main__":
    main()
```

## Phase 2: Core Utilities

[NEW FILE] `cli/prompts_cli/utils/file_ops.py`
```python
"""File operation utilities."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

def get_repo_root() -> Path:
    """Find the repository root by looking for .git or .ruler."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".git").exists() or (current / ".ruler").exists():
            return current
        current = current.parent
    # Fallback to current directory if not found
    return Path.cwd()

def parse_frontmatter(file_path: Path) -> tuple[Optional[Dict[str, Any]], str]:
    """Parse YAML frontmatter from a markdown file."""
    if not file_path.exists():
        return None, ""
        
    content = file_path.read_text(encoding="utf-8")
    
    if content.startswith("---\n"):
        parts = content.split("---\n", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
                body = parts[2]
                return frontmatter, body
            except yaml.YAMLError:
                pass
                
    return None, content
```

## Phase 3: Implement Commands

### 3.1: Skill Commands
[NEW FILE] `cli/prompts_cli/commands/skill_cmd.py`
```python
"""Commands for managing skills."""

import typer
import shutil
from pathlib import Path
from rich.console import Console
from rich.table import Table

from ..config import GLOBAL_SKILLS_DIR
from ..utils.file_ops import get_repo_root, parse_frontmatter

app = typer.Typer(help="Manage global skills.")
console = Console()

@app.command("list")
def list_skills() -> None:
    """List all available global skills."""
    repo_root = get_repo_root()
    skills_dir = repo_root / GLOBAL_SKILLS_DIR
    
    if not skills_dir.exists():
        console.print(f"[red]Error:[/red] Skills directory '{GLOBAL_SKILLS_DIR}' not found.")
        raise typer.Exit(1)
        
    table = Table(title="Global Skills")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="green")
    
    for skill_dir in sorted(skills_dir.iterdir()):
        if skill_dir.is_dir() and not skill_dir.name.startswith("."):
            skill_file = skill_dir / "SKILL.md"
            description = "No description available"
            
            if skill_file.exists():
                frontmatter, _ = parse_frontmatter(skill_file)
                if frontmatter and "description" in frontmatter:
                    description = frontmatter["description"]
                    
            table.add_row(skill_dir.name, description)
            
    console.print(table)

@app.command("new")
def new_skill(
    name: str = typer.Argument(..., help="Name of the new skill (e.g., my-new-skill)"),
    description: str = typer.Option("A new skill", "--desc", "-d", help="Description of the skill"),
) -> None:
    """Create a new global skill scaffold."""
    repo_root = get_repo_root()
    skills_dir = repo_root / GLOBAL_SKILLS_DIR
    skill_path = skills_dir / name
    
    if skill_path.exists():
        console.print(f"[red]Error:[/red] Skill '{name}' already exists.")
        raise typer.Exit(1)
        
    skill_path.mkdir(parents=True, exist_ok=True)
    
    # Create SKILL.md template
    skill_file = skill_path / "SKILL.md"
    template = f"""---
name: "{name}"
description: "{description}"
---

# {name}

## Purpose
Briefly explain the scenario this skill addresses.

## Checklist/Workflow
1. Step one
2. Step two
"""
    skill_file.write_text(template, encoding="utf-8")
    console.print(f"[green]Success:[/green] Created new skill at '{skill_path.relative_to(repo_root)}'")
```

### 3.2: Workflow Commands
[NEW FILE] `cli/prompts_cli/commands/workflow_cmd.py`
```python
"""Commands for managing workflows."""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table

from ..config import GLOBAL_WORKFLOWS_DIR
from ..utils.file_ops import get_repo_root, parse_frontmatter

app = typer.Typer(help="Manage global workflows.")
console = Console()

@app.command("list")
def list_workflows() -> None:
    """List all available global workflows."""
    repo_root = get_repo_root()
    workflows_dir = repo_root / GLOBAL_WORKFLOWS_DIR
    
    if not workflows_dir.exists():
        console.print(f"[red]Error:[/red] Workflows directory '{GLOBAL_WORKFLOWS_DIR}' not found.")
        raise typer.Exit(1)
        
    table = Table(title="Global Workflows")
    table.add_column("Filename", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Auto", style="yellow")
    
    for workflow_file in sorted(workflows_dir.glob("*.md")):
        description = "No description available"
        auto_exec = "No"
        
        frontmatter, _ = parse_frontmatter(workflow_file)
        if frontmatter:
            description = frontmatter.get("description", description)
            if frontmatter.get("auto_execution_mode") == 1:
                auto_exec = "Yes"
                
        table.add_row(workflow_file.name, description, auto_exec)
        
    console.print(table)

@app.command("new")
def new_workflow(
    name: str = typer.Argument(..., help="Name of the new workflow file (without .md)"),
    description: str = typer.Option("A new workflow", "--desc", "-d", help="Description of the workflow"),
    auto: bool = typer.Option(False, "--auto", help="Set auto_execution_mode to 1"),
) -> None:
    """Create a new global workflow scaffold."""
    if not name.endswith(".md"):
        name = f"{name}.md"
        
    repo_root = get_repo_root()
    workflows_dir = repo_root / GLOBAL_WORKFLOWS_DIR
    workflow_path = workflows_dir / name
    
    if workflow_path.exists():
        console.print(f"[red]Error:[/red] Workflow '{name}' already exists.")
        raise typer.Exit(1)
        
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    auto_line = "auto_execution_mode: 1\n" if auto else ""
    
    # Create workflow template
    template = f"""---
description: "{description}"
{auto_line}---

# {name.replace('.md', '')}

Define the workflow steps here...
"""
    workflow_path.write_text(template, encoding="utf-8")
    console.print(f"[green]Success:[/green] Created new workflow at '{workflow_path.relative_to(repo_root)}'")
```

### 3.3: Sync Commands
[NEW FILE] `cli/prompts_cli/commands/sync_cmd.py`
```python
"""Commands for syncing with Ruler."""

import typer
import subprocess
from rich.console import Console

from ..utils.file_ops import get_repo_root

app = typer.Typer(help="Sync configurations using Ruler.")
console = Console()

@app.command("apply")
def sync_apply(
    config: str = typer.Option("adapters/ruler/ruler.toml", "--config", "-c", help="Path to ruler config file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Run without making changes"),
) -> None:
    """Run 'ruler apply' to distribute rules/skills."""
    repo_root = get_repo_root()
    config_path = repo_root / config
    
    if not config_path.exists():
        console.print(f"[yellow]Warning:[/yellow] Config '{config}' not found. Attempting default ruler apply.")
        cmd = ["ruler", "apply"]
    else:
        cmd = ["ruler", "apply", "--config", str(config_path)]
        
    if dry_run:
        cmd.append("--dry-run")
        
    console.print(f"[cyan]Executing:[/cyan] {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, cwd=repo_root, check=True)
        console.print("[green]Sync completed successfully.[/green]")
    except FileNotFoundError:
        console.print("[red]Error:[/red] 'ruler' command not found. Ensure it is installed and in PATH.")
        raise typer.Exit(1)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error:[/red] Ruler sync failed with exit code {e.returncode}.")
        raise typer.Exit(e.returncode)
```

### 3.4: Wire up Commands in `cli.py`
[MODIFY] `cli/prompts_cli/cli.py`
```python
"""Main entry point for the prompts CLI."""

import typer
from rich.console import Console

from .config import CLI_CONTEXT_SETTINGS
from .commands import skill_cmd, workflow_cmd, sync_cmd

app = typer.Typer(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="Management CLI for the ai-coding-prompts repository.",
)

app.add_typer(skill_cmd.app, name="skill")
app.add_typer(workflow_cmd.app, name="workflow")
app.add_typer(sync_cmd.app, name="sync")

console = Console()

def main() -> None:
    """Execute the CLI application."""
    app()

if __name__ == "__main__":
    main()
```

## Phase 4: Create bash wrapper
Create a wrapper script in the root directory for easy access without manual environment activation.

[NEW FILE] `prompts` (Make executable)
```bash
#!/usr/bin/env bash

# Wrapper script for the prompts management CLI

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_DIR="$REPO_ROOT/cli"

# Ensure uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' is required but not installed." >&2
    echo "Please install it: curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    exit 1
fi

# Ensure project is setup if it doesn't exist
if [ ! -d "$CLI_DIR/.venv" ]; then
    echo "Initializing CLI environment..."
    cd "$CLI_DIR" && uv venv && uv pip install -e ".[dev]"
    cd "$REPO_ROOT"
fi

# Run the CLI
cd "$CLI_DIR" && uv run prompts "$@"
```

## Phase 5: Documentation Update
Update README.md to include instructions on using the new management CLI.

## Phase 6: Report Generation
Generate the final implementation report in `_ai/backlog/reports/`.

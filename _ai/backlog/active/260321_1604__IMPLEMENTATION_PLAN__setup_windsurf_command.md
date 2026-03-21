---
filename: "_ai/backlog/active/260321_1604__IMPLEMENTATION_PLAN__setup_windsurf_command.md"
title: "Create Setup Command for AI Tool Integrations"
createdAt: 2026-03-21 16:04
updatedAt: 2026-03-21 16:04
status: draft
priority: medium
tags: [cli, windsurf, setup, symlinks]
estimatedComplexity: simple
documentType: IMPLEMENTATION_PLAN
---

# Problem Statement
The user needs a new CLI command to automatically install dependencies and configurations (like `global-skills` and `global-workflows`) for Windsurf. To make this robust, the solution needs to be generic and extensible to easily support other AI coding tools in the future by defining their configuration mappings.

# Project Environment Details
- Project Name: ai-coding-prompts
- Frontend root: None (CLI App)
- Backend root: `cli/prompts_cli`
- Main entry point: `cli/prompts_cli/cli.py`

# Implementation Steps

## 1. Create the Setup Command Module

Create a new command group dedicated to setting up integrations. It will include a generic function to safely handle symlink creation, checking for existing files, and supporting dry runs.

```python
# [NEW FILE] cli/prompts_cli/commands/setup_cmd.py
"""Commands for setting up integrations with AI tools."""

import shutil
import typer
from pathlib import Path
from rich.console import Console

from ..utils.file_ops import get_repo_root

app = typer.Typer(help="Setup integrations with AI coding assistants.")
console = Console()

# Configuration mapping for different tools to keep it extensible
INTEGRATIONS = {
    "windsurf": [
        {
            "source": "global-skills",
            "target": "~/.codeium/windsurf-next/skills",
        },
        {
            "source": "global-workflows",
            "target": "~/.codeium/windsurf-next/global_workflows",
        },
    ]
    # Future tools can be added here
}

def _create_symlink(source: Path, target: Path, force: bool, dry_run: bool) -> bool:
    """Create a symlink from source to target. Returns True if successful."""
    if not source.exists():
        console.print(f"[red]Error:[/red] Source path '{source}' does not exist.")
        return False

    if target.exists() or target.is_symlink():
        if force:
            if dry_run:
                console.print(f"[yellow]Would remove existing:[/yellow] {target}")
            else:
                if target.is_symlink() or target.is_file():
                    target.unlink()
                else:
                    shutil.rmtree(target)
        else:
            console.print(
                f"[yellow]Skipping:[/yellow] Target '{target}' already exists. Use --force to overwrite."
            )
            return False

    if dry_run:
        console.print(f"[green]Would create symlink:[/green] {target} -> {source}")
        return True

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(source)
        console.print(f"[green]Created symlink:[/green] {target} -> {source}")
        return True
    except Exception as e:
        console.print(f"[red]Error creating symlink {target}:[/red] {e}")
        return False

def _setup_integration(tool_name: str, force: bool, dry_run: bool) -> None:
    """Generic function to setup an integration based on the INTEGRATIONS config."""
    repo_root = get_repo_root()
    links = INTEGRATIONS.get(tool_name, [])

    if not links:
        console.print(f"[red]Error:[/red] No configuration found for '{tool_name}'.")
        raise typer.Exit(1)

    console.print(f"Setting up integration for [bold cyan]{tool_name}[/bold cyan]...")

    success_count = 0
    for link in links:
        source_path = repo_root / link["source"]
        target_path = Path(link["target"]).expanduser()

        if _create_symlink(source_path, target_path, force, dry_run):
            success_count += 1

    if success_count == len(links):
        console.print(f"[bold green]Successfully setup {tool_name} integration![/bold green]")
    else:
        console.print(f"[bold yellow]Setup for {tool_name} completed with some warnings/errors.[/bold yellow]")
        raise typer.Exit(1)

@app.command("windsurf")
def setup_windsurf(
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing links or directories"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be done without making changes"),
) -> None:
    """Install global skills and workflows for Windsurf."""
    _setup_integration("windsurf", force, dry_run)
```

## 2. Register the Setup Command in CLI Entry Point

Update the main CLI application to include the new `setup` subcommand group.

```python
# [MODIFY] cli/prompts_cli/cli.py
"""Main entry point for the prompts CLI."""

import typer
from rich.console import Console

from .config import CLI_CONTEXT_SETTINGS
from .commands import skill_cmd, workflow_cmd, sync_cmd, setup_cmd

app = typer.Typer(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="Management CLI for the ai-coding-prompts repository.",
)

app.add_typer(skill_cmd.app, name="skill")
app.add_typer(workflow_cmd.app, name="workflow")
app.add_typer(sync_cmd.app, name="sync")
app.add_typer(setup_cmd.app, name="setup")

console = Console()

def main() -> None:
    """Execute the CLI application."""
    app()

if __name__ == "__main__":
    main()
```

## 3. Update User Documentation

Update the `README.md` to document the new `setup` command so users know how to install integrations.

```markdown
# [MODIFY] README.md
(Insert in the relevant CLI commands section)

### Setting up Integrations

To automatically symlink global skills and workflows into your AI coding assistants, use the `setup` command:

```bash
# Setup Windsurf integration
prompts-cli setup windsurf

# Overwrite existing directories/links
prompts-cli setup windsurf --force

# Preview changes without applying them
prompts-cli setup windsurf --dry-run
```
```

# Final Step
Generate the implementation report at `_ai/backlog/reports/260321_1604__IMPLEMENTATION_REPORT__setup_windsurf_command.md` after the implementation is complete.

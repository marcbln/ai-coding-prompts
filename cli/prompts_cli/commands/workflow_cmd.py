"""Commands for managing workflows."""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table

from ..config import GLOBAL_WORKFLOWS_DIR
from ..utils.file_ops import get_repo_root, parse_frontmatter

app = typer.Typer(help="Manage global workflows.", no_args_is_help=True)
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

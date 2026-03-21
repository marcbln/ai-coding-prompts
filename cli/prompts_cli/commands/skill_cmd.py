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

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

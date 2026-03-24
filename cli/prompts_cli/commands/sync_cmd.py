"""Commands for syncing global skills and workflows to local agent directories."""

import shutil
from pathlib import Path
from typing import Any

import typer
import yaml
from rich.console import Console

from ..config import GLOBAL_SKILLS_DIR, GLOBAL_WORKFLOWS_DIR
from ..utils.file_ops import get_repo_root

DEFAULT_EXPORT_CONFIG = "adapters/symlink/agent_exports.yaml"

app = typer.Typer(help="Sync configurations using symlink exports.", no_args_is_help=True)

console = Console()


def _load_export_config(config_path: Path) -> dict[str, Any]:
    """Load and validate export config file."""
    if not config_path.exists():
        console.print(f"[red]Error:[/red] Config file '{config_path}' was not found.")
        raise typer.Exit(1)

    try:
        loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        console.print(f"[red]Error:[/red] Invalid YAML in '{config_path}': {exc}")
        raise typer.Exit(1)

    if not isinstance(loaded, dict):
        console.print(f"[red]Error:[/red] Config '{config_path}' must be a mapping.")
        raise typer.Exit(1)

    sources = loaded.get("sources")
    agents = loaded.get("agents")
    if not isinstance(sources, dict) or not isinstance(agents, dict):
        console.print("[red]Error:[/red] Config must define 'sources' and 'agents' mappings.")
        raise typer.Exit(1)

    if "skills" not in sources or "workflows" not in sources:
        console.print("[red]Error:[/red] 'sources' must define both 'skills' and 'workflows'.")
        raise typer.Exit(1)

    return loaded


def _create_symlink(source: Path, target: Path, force: bool, dry_run: bool) -> bool:
    """Create or update a symlink from source to target."""
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
                f"[yellow]Skipping:[/yellow] Target '{target}' already exists (use --force to replace)."
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
    except OSError as exc:
        console.print(f"[red]Error:[/red] Failed to create symlink '{target}': {exc}")
        return False


@app.command("export")
def sync_export(
    config: str = typer.Option(
        DEFAULT_EXPORT_CONFIG,
        "--config",
        "-c",
        help="Path to export config file",
    ),
    agent: list[str] = typer.Option(
        [],
        "--agent",
        "-a",
        help="Agent name to export (repeat to target multiple agents). Defaults to all.",
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing links or directories"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be done without making changes"),
) -> None:
    """Export global skills/workflows to configured agent directories via symlinks."""
    repo_root = get_repo_root()
    config_path = repo_root / config
    export_config = _load_export_config(config_path)

    sources = export_config["sources"]
    agents = export_config["agents"]

    selected_agents = sorted(set(agent)) if agent else sorted(agents.keys())
    unknown_agents = [name for name in selected_agents if name not in agents]
    if unknown_agents:
        console.print(f"[red]Error:[/red] Unknown agent(s): {', '.join(unknown_agents)}")
        raise typer.Exit(1)

    source_skills = repo_root / str(sources.get("skills", GLOBAL_SKILLS_DIR))
    source_workflows = repo_root / str(sources.get("workflows", GLOBAL_WORKFLOWS_DIR))

    failures = 0
    created = 0

    for agent_name in selected_agents:
        agent_entry = agents.get(agent_name)
        if not isinstance(agent_entry, dict):
            console.print(f"[yellow]Skipping:[/yellow] Agent '{agent_name}' has an invalid config entry.")
            failures += 1
            continue

        console.print(f"[cyan]Exporting for:[/cyan] {agent_name}")
        skills_target_value = agent_entry.get("skills")
        workflows_target_value = agent_entry.get("workflows")

        if isinstance(skills_target_value, str):
            if _create_symlink(source_skills, Path(skills_target_value).expanduser(), force, dry_run):
                created += 1
            else:
                failures += 1

        if isinstance(workflows_target_value, str):
            if _create_symlink(source_workflows, Path(workflows_target_value).expanduser(), force, dry_run):
                created += 1
            else:
                failures += 1

    if failures:
        console.print(f"[bold yellow]Export finished with {failures} issue(s).[/bold yellow]")
        raise typer.Exit(1)

    console.print(f"[bold green]Export completed successfully ({created} symlink operations).[/bold green]")

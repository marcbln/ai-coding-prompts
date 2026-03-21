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

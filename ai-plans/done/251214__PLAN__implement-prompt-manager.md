---
filename: "ai-plans/251214__PLAN__implement-prompt-manager.md"
title: "Implement Prompt Manager CLI and Restructure Snippets"
date: 2025-12-14
status: draft
priority: high
tags: [python, cli, snippets, structure]
estimated_complexity: moderate
---

## Problem Statement
The current repository lacks a structured organization for prompt snippets (`snippets.md`, `snippets-cm.md`), making it difficult to maintain versions and context-specific prompts. We need to restructure these into a directory-based format (e.g., `snippets/<project>/<name>.md`) and implement a Python CLI tool (`prompt-manager`) to index, search, retrieve, and template these snippets efficiently.

## Implementation Notes
- **Language**: Python 3.12+
- **Dependency Manager**: `uv`
- **CLI Framework**: Typer (with Rich for formatting)
- **Templating**: Jinja2 (for including other snippets)
- **Frontmatter**: Python-frontmatter (for metadata handling)
- **Structure**:
    - Tool logic resides in `prompt-manager/` directory.
    - Snippets reside in `snippets/` directory at the repo root.
- **Conventions**: Adhere strictly to `conventions/CONVENTIONS-PYTHON.md`.

---

### Phase 1: Python Project Initialization
**Objective**: Set up the Python environment, dependencies, and project structure using `uv`.

**Tasks**:
1. Create directory `prompt-manager`.
2. Initialize `pyproject.toml` with `uv`.
3. Create source directory structure (`src/prompt_manager/...`).
4. Configure standard tooling (Ruff, Mypy).

**Source Code**:

[NEW FILE] `prompt-manager/pyproject.toml`
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "prompt-manager"
version = "0.1.0"
description = "CLI tool to manage and template AI coding prompts"
requires-python = ">=3.12"
authors = [
    { name = "AI Agent", email = "agent@example.com" },
]
dependencies = [
    "typer[all]>=0.9.0",
    "rich>=13.7.0",
    "inquirerpy>=0.3.4",
    "pyyaml>=6.0",
    "python-frontmatter>=1.0.0",
    "jinja2>=3.1.0",
    "pyperclip>=1.8.2",
    "python-dotenv>=1.0.0",
]

[project.scripts]
pm = "prompt_manager.cli:app"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "black>=24.0.0",
    "mypy>=1.8.0",
    "ruff>=0.3.0",
    "types-pyyaml",
]

[tool.ruff]
line-length = 88
select = ["E", "F", "W", "I"]

[tool.mypy]
strict = true
```

[NEW FILE] `prompt-manager/src/prompt_manager/__init__.py`
```python
# Marker file
```

[NEW FILE] `prompt-manager/src/prompt_manager/config.py`
```python
import os
from pathlib import Path

# Defaults: assumes the tool is run from repo root or installed such that 
# it can find the 'snippets' dir relative to the repo root.
# For this implementation, we assume repo_root is parent of prompt-manager dir
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SNIPPETS_DIR = REPO_ROOT / "snippets"

CLI_CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}
```

[NEW FILE] `prompt-manager/src/prompt_manager/cli.py`
```python
import typer
from .config import CLI_CONTEXT_SETTINGS
from .commands import list_cmd, get_cmd

app = typer.Typer(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="AI Prompt Manager CLI"
)

app.add_typer(list_cmd.app, name="list", help="List available snippets")
app.add_typer(get_cmd.app, name="get", help="Get and render a snippet")

def main():
    app()

if __name__ == "__main__":
    main()
```

---

### Phase 2: Core Logic (Models & Engine)
**Objective**: Implement the data models for snippets and the logic to parse, index, and render them.

**Tasks**:
1. Define `Snippet` model using Pydantic (or dataclass).
2. Implement `SnippetEngine` to scan directories and parse frontmatter.
3. Implement Jinja2 environment for rendering includes.

**Source Code**:

[NEW FILE] `prompt-manager/src/prompt_manager/core/models.py`
```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import date

@dataclass
class SnippetMetadata:
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    created_by: str = "system"
    updated_by: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    description: str = ""

@dataclass
class Snippet:
    name: str
    project: str  # e.g., 'cm', 'common'
    path: str
    content: str
    metadata: SnippetMetadata
```

[NEW FILE] `prompt-manager/src/prompt_manager/core/engine.py`
```python
import os
import frontmatter
from pathlib import Path
from typing import List, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .models import Snippet, SnippetMetadata
from ..config import SNIPPETS_DIR

class SnippetEngine:
    def __init__(self, snippets_dir: Path = SNIPPETS_DIR):
        self.snippets_dir = snippets_dir
        self.jinja_env = Environment(
            loader=FileSystemLoader(snippets_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def scan_snippets(self) -> List[Snippet]:
        results = []
        if not self.snippets_dir.exists():
            return []

        for root, _, files in os.walk(self.snippets_dir):
            for file in files:
                if file.endswith(".md"):
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(self.snippets_dir)
                    project = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
                    
                    try:
                        post = frontmatter.load(full_path)
                        meta = post.metadata
                        
                        metadata_obj = SnippetMetadata(
                            created_at=meta.get('createdAt'),
                            tags=meta.get('tags', []),
                            description=meta.get('description', '')
                        )
                        
                        results.append(Snippet(
                            name=file.replace('.md', ''),
                            project=project,
                            path=str(rel_path),
                            content=post.content,
                            metadata=metadata_obj
                        ))
                    except Exception as e:
                        print(f"Error parsing {full_path}: {e}")
        return results

    def get_rendered_snippet(self, project: str, name: str) -> str:
        # Construct path for Jinja loader (relative to snippets_dir)
        # e.g. cm/create-plan-v3.md
        template_path = f"{project}/{name}.md"
        
        # We assume the user requests by name, but we need to verify file existence
        # This simple loader relies on Jinja to find the file
        try:
            template = self.jinja_env.get_template(template_path)
            # We treat the file as a Jinja template. 
            # Note: frontmatter is usually stripped by python-frontmatter, 
            # but Jinja reads the raw file. We might need a custom loader 
            # if we want to strip frontmatter before rendering.
            # For simplicity V1: render the whole file, user handles frontmatter in output or we strip it after.
            
            rendered = template.render()
            
            # Post-process: strip frontmatter from the rendered output if it exists
            # Re-parse as frontmatter to get just the content
            post = frontmatter.loads(rendered)
            return post.content.strip()
            
        except Exception as e:
            return f"Error rendering snippet: {e}"
```

---

### Phase 3: CLI Commands
**Objective**: Implement the `list` and `get` commands using Typer and Rich.

**Tasks**:
1. Implement `list_cmd.py` to display snippets in a table.
2. Implement `get_cmd.py` to retrieve and copy snippets.

**Source Code**:

[NEW FILE] `prompt-manager/src/prompt_manager/commands/list_cmd.py`
```python
import typer
from rich.console import Console
from rich.table import Table
from ..core.engine import SnippetEngine

app = typer.Typer()
console = Console()

@app.callback(invoke_without_command=True)
def list_snippets(
    project: str = typer.Option(None, "--project", "-p", help="Filter by project")
):
    """List all available snippets."""
    engine = SnippetEngine()
    snippets = engine.scan_snippets()
    
    if project:
        snippets = [s for s in snippets if s.project == project]

    table = Table(title="Available Snippets")
    table.add_column("Project", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Tags", style="green")

    for s in snippets:
        table.add_row(
            s.project, 
            s.name, 
            s.metadata.description, 
            ", ".join(s.metadata.tags)
        )

    console.print(table)
```

[NEW FILE] `prompt-manager/src/prompt_manager/commands/get_cmd.py`
```python
import typer
import pyperclip
from rich.console import Console
from ..core.engine import SnippetEngine

app = typer.Typer()
console = Console()

@app.callback(invoke_without_command=True)
def get_snippet(
    project: str = typer.Argument(..., help="Project name (folder)"),
    name: str = typer.Argument(..., help="Snippet name (without .md)"),
    copy: bool = typer.Option(True, "--copy/--no-copy", help="Copy to clipboard")
):
    """Get and render a specific snippet."""
    engine = SnippetEngine()
    content = engine.get_rendered_snippet(project, name)
    
    console.print(content)
    
    if copy:
        try:
            pyperclip.copy(content)
            console.print("\n[bold green]✓ Copied to clipboard![/bold green]")
        except Exception:
            console.print("\n[bold red]✗ Could not copy to clipboard (missing dependency?)[/bold red]")
```

[NEW FILE] `prompt-manager/src/prompt_manager/__main__.py`
```python
from .cli import main

if __name__ == "__main__":
    main()
```

---

### Phase 4: Migration Script & Restructuring
**Objective**: Move existing snippets from `snippets.md` and `snippets-cm.md` into the new structure `snippets/<project>/<name>.md`.

**Tasks**:
1. Create `snippets/cm/` and `snippets/common/` directories.
2. Create a migration script `scripts/migrate_snippets.py` to parse the old files (using regex or simple split) and write to new format with frontmatter.
3. Run the migration.

**Source Code**:

[NEW FILE] `scripts/migrate_snippets.py`
```python
import os
import re
from pathlib import Path
from datetime import date

# Configuration
REPO_ROOT = Path(__file__).resolve().parent.parent
SNIPPETS_ROOT = REPO_ROOT / "snippets"
OLD_FILES = {
    "cm": REPO_ROOT / "snippets-cm.md",
    "common": REPO_ROOT / "snippets.md"
}

def create_frontmatter(title: str, tags: list) -> str:
    today = date.today().isoformat()
    return f"""---
description: "{title}"
createdAt: {today}
updatedAt: {today}
tags: {tags}
---

"""

def migrate_cm():
    content = OLD_FILES["cm"].read_text(encoding="utf-8")
    # Simple heuristic splitting based on the headers in snippets-cm.md
    # Looking for "## --------------- TITLE -----------------"
    
    pattern = r"## --------------- (.*?) -----------------\s*(.*?)(?=## ---------------|$)"
    matches = re.findall(pattern, content, re.DOTALL)
    
    output_dir = SNIPPETS_ROOT / "cm"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for title_raw, body in matches:
        # cleanup title
        slug = title_raw.strip().lower().replace(" ", "-")
        filename = f"{slug}.md"
        
        # Write file
        full_content = create_frontmatter(title_raw.strip(), ["cm", "plan"]) + body.strip()
        
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"Migrated: snippets/cm/{filename}")

def migrate_common():
    # Common snippets don't have the clear separator in the current file dump
    # We will manually create one specific file for demonstration or extract generic logic
    # The snippet_laptop.md file suggests general instructions.
    pass 

if __name__ == "__main__":
    migrate_cm()
    # Manual cleanup required for unstructured snippets.md
```

**Action**:
- Run `uv run scripts/migrate_snippets.py` (after creating the script).
- Manually move/cleanup remaining contents of `snippets.md` into `snippets/common/` or `snippets/laptop/`.

---

### Phase 5: Verification
**Objective**: Ensure the tool works and data is structured correctly.

**Tasks**:
1. Install the tool locally: `cd prompt-manager && uv pip install -e .`
2. Run `pm list` to see the migrated snippets.
3. Run `pm get cm create-plan-v3` to verify rendering and clipboard copy.
4. Verify directory structure is clean.
5. Delete old `snippets-cm.md`.

---

### Phase 6: Reporting
**Objective**: Generate the final report.

**Tasks**:
1. Create report file in `ai-plans/`.
2. Document changes, new tool usage, and file structure.

**Deliverables**:
- `ai-plans/251214__REPORT__implement-prompt-manager.md`



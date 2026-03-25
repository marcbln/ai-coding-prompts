"""File operation utilities."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

def get_repo_root() -> Path:
    """Find the repository root by looking for .git."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".git").exists():
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

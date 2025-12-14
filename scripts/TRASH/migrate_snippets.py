"""One-off migration from legacy snippet files into structured directories."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
SNIPPETS_ROOT = REPO_ROOT / "snippets"
OLD_FILES = {
    "cm": REPO_ROOT / "snippets-cm.md",
    "common": REPO_ROOT / "snippets.md",
}


@dataclass
class LegacySnippet:
    """Represents a snippet parsed from the legacy flat markdown files."""

    project: str
    title: str
    body: str

    @property
    def slug(self) -> str:
        """Generate a filesystem-safe slug."""
        normalized = re.sub(r"[^a-z0-9]+", "-", self.title.lower())
        return normalized.strip("-") or "snippet"

    def to_markdown(self) -> str:
        """Render the snippet with minimal frontmatter for the new structure."""
        today = date.today().isoformat()
        frontmatter = "\n".join(
            [
                "---",
                f'description: "{self.title.strip()}"',
                f"createdAt: {today}",
                f"updatedAt: {today}",
                f"tags: [{self.project}]",
                "---",
                "",
            ],
        )
        return f"{frontmatter}{self.body.strip()}\n"


def main() -> None:
    """Entry point for running the migration."""
    SNIPPETS_ROOT.mkdir(parents=True, exist_ok=True)
    total_migrated = 0

    for project, source_path in OLD_FILES.items():
        if not source_path.exists():
            print(f"[skip] {source_path} does not exist.")
            continue

        count = migrate_project(project, source_path)
        print(f"✓ Migrated {count} snippets for project '{project}'.")
        total_migrated += count

    print(f"Total migrated snippets: {total_migrated}")


def migrate_project(project: str, source_path: Path) -> int:
    """Migrate snippets for a single project file."""
    snippets = list(parse_legacy_snippets(project, source_path))
    for snippet in snippets:
        write_snippet(snippet)
    return len(snippets)


def parse_legacy_snippets(project: str, source_path: Path) -> Iterable[LegacySnippet]:
    """Parse the old markdown files using section headers."""
    content = source_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"## --------------- (.*?) -----------------\s*(.*?)(?=## ---------------|$)",
        re.DOTALL,
    )

    for title, body in pattern.findall(content):
        yield LegacySnippet(project=project, title=title.strip(), body=body.strip())


def write_snippet(snippet: LegacySnippet) -> int:
    """Persist the migrated snippet into the new directory structure."""
    output_dir = SNIPPETS_ROOT / snippet.project
    output_dir.mkdir(parents=True, exist_ok=True)
    target_path = output_dir / f"{snippet.slug}.md"
    target_path.write_text(snippet.to_markdown(), encoding="utf-8")
    print(f"Migrated {target_path.relative_to(REPO_ROOT)}")
    return 1


if __name__ == "__main__":
    main()

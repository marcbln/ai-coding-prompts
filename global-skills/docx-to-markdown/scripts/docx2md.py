#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

"""Convert a .docx to Markdown and extract its images beside the output."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlparse

IMAGE_RE = re.compile(r"<img\b[^>]*>|!\[([^\]]*)\]\(([^)]+)\)", re.IGNORECASE)
SRC_ATTR_RE = re.compile(r'\bsrc="([^"]+)"', re.IGNORECASE)
ALT_ATTR_RE = re.compile(r'\balt="([^"]*)"', re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
TABLE_SEP_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", re.MULTILINE
)
REMOTE_RE = re.compile(r"^(?:https?:|data:|mailto:)", re.IGNORECASE)


@dataclass
class Report:
    """Collected fidelity signals for the conversion report."""

    source_images: int = 0
    source_tables: int = 0
    source_headings: int = 0
    images: int = 0
    headings: int = 0
    tables: int = 0
    links: int = 0
    resolved: int = 0
    missing: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def fail(message: str, code: int = 1) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def require_pandoc() -> str:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        fail(
            "pandoc is not installed or not on PATH (try: sudo apt install pandoc).",
            2,
        )
    return pandoc


def inspect_docx(path: Path) -> tuple[int, int, int]:
    """Return (media files, table elements, Heading-style paragraphs)."""
    images = 0
    tables = 0
    headings = 0
    with zipfile.ZipFile(path) as archive:
        images = sum(
            1
            for name in archive.namelist()
            if name.startswith("word/media/") and not name.endswith("/")
        )
        try:
            with archive.open("word/document.xml") as handle:
                root = ET.parse(handle).getroot()
        except KeyError:
            return images, 0, 0
        for element in root.iter():
            tag = element.tag.rsplit("}", 1)[-1]
            if tag == "tbl":
                tables += 1
            elif tag == "pStyle":
                style = next(
                    (value for key, value in element.attrib.items() if key.endswith("}val")),
                    "",
                ).lower()
                if style.startswith(("heading", "berschrift", "überschrift")):
                    headings += 1
    return images, tables, headings


def render_destination(relative: str) -> str:
    """Wrap destinations that Markdown parsers split on whitespace."""
    if re.search(r"[\s<>()]", relative) or not relative.isascii():
        return f"<{relative}>"
    return relative


class MediaMapper:
    """Map images under pandoc's temporary media root to final asset names."""

    def __init__(self, media_root: Path, media_dir: Path, output_dir: Path) -> None:
        self.media_root = media_root.resolve()
        self.media_dir = media_dir
        self.output_dir = output_dir
        self.by_source: dict[Path, str] = {}
        self.copies: list[tuple[Path, Path]] = []
        self.used: dict[str, Path] = {}

    def _path(self, source: str) -> Path:
        raw = source.strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        if raw.startswith("file://"):
            raw = urlparse(raw).path
        raw = unquote(raw)
        path = Path(raw)
        if not path.is_absolute():
            path = self.output_dir / path
        return path

    def _unique_name(self, path: Path) -> str:
        name = path.name
        if name not in self.used:
            self.used[name] = path
            return name
        stem, suffix = path.stem, path.suffix
        index = 2
        while f"{stem}-{index}{suffix}" in self.used:
            index += 1
        name = f"{stem}-{index}{suffix}"
        self.used[name] = path
        return name

    def lookup(self, source: str) -> str | None:
        if REMOTE_RE.match(source.strip()):
            return None
        try:
            resolved = self._path(source).resolve()
        except OSError:
            return None
        try:
            resolved.relative_to(self.media_root)
        except ValueError:
            return None
        if resolved in self.by_source:
            return self.by_source[resolved]
        name = self._unique_name(resolved)
        destination = self.media_dir / name
        relative = os.path.relpath(destination, start=self.output_dir)
        relative = Path(relative).as_posix()
        self.by_source[resolved] = relative
        self.copies.append((resolved, destination))
        return relative


def rewrite_references(
    text: str, mapper: MediaMapper, report: Report
) -> str:
    """Replace pandoc media references with relative Markdown images."""

    def lookup(source: str) -> str | None:
        relative = mapper.lookup(source)
        if relative is not None:
            report.links += 1
            report.resolved += 1
            return relative
        if not REMOTE_RE.match(source.strip()):
            report.links += 1
            report.missing.append(source.strip())
        return None

    def replace_image(match: re.Match[str]) -> str:
        token = match.group(0)
        if token[:4].lower() == "<img":
            src_match = SRC_ATTR_RE.search(token)
            if src_match is None:
                return token
            relative = lookup(src_match.group(1))
            if relative is None:
                return token
            alt_match = ALT_ATTR_RE.search(token)
            alt = alt_match.group(1) if alt_match else ""
        else:
            alt = match.group(1) or ""
            relative = lookup(match.group(2))
            if relative is None:
                return token
        alt = alt.replace("]", r"\]")
        return f"![{alt}]({render_destination(relative)})"

    # Single pass: replacements are not rescanned, so a rewritten Markdown image
    # cannot be mistaken for a second unresolved reference.
    return IMAGE_RE.sub(replace_image, text)


def count_structure(text: str) -> tuple[int, int]:
    headings = len(HEADING_RE.findall(text))
    tables = len(TABLE_SEP_RE.findall(text))
    return headings, tables


def convert(
    input_path: Path,
    output_path: Path,
    media_dir: Path,
) -> Report:
    pandoc = require_pandoc()
    try:
        source_counts = inspect_docx(input_path)
    except zipfile.BadZipFile:
        fail(f"not a valid .docx (zip) file: {input_path}")
    report = Report(
        source_images=source_counts[0],
        source_tables=source_counts[1],
        source_headings=source_counts[2],
    )

    with tempfile.TemporaryDirectory(prefix="docx2md-") as temp:
        temp_dir = Path(temp)
        temp_markdown = temp_dir / "output.md"
        temp_media = temp_dir / "media"

        command = [
            pandoc,
            str(input_path),
            "-f",
            "docx",
            "-t",
            "gfm",
            "--wrap=none",
            f"--extract-media={temp_media}",
            "-o",
            str(temp_markdown),
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
            fail(f"pandoc failed: {detail}")

        text = temp_markdown.read_text(encoding="utf-8")
        mapper = MediaMapper(temp_media, media_dir, output_path.parent)
        text = rewrite_references(text, mapper, report)

        if mapper.copies:
            media_dir.mkdir(parents=True, exist_ok=True)
            for source, destination in mapper.copies:
                if not source.is_file():
                    report.missing.append(str(source))
                    continue
                shutil.copy2(source, destination)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")

    report.images = len(mapper.by_source)
    report.headings, report.tables = count_structure(text)

    if report.source_images > report.images:
        report.warnings.append(
            f"source contains {report.source_images} media file(s); "
            f"{report.images} image(s) are referenced in the Markdown"
        )
    if report.source_tables and not report.tables:
        report.warnings.append(
            f"source has {report.source_tables} table(s) but no Markdown table was detected"
        )
    if report.source_headings and not report.headings:
        report.warnings.append(
            f"source has {report.source_headings} Heading-style paragraph(s) "
            "but no Markdown heading was detected"
        )
    if not report.source_headings:
        report.warnings.append(
            "no Heading styles found in the source; headings may use direct formatting"
        )

    return report


def print_report(
    input_path: Path,
    output_path: Path,
    media_dir: Path,
    report: Report,
) -> None:
    print(f"Converted: {input_path} -> {output_path}")
    print(f"Images:    {report.images} file(s) -> {media_dir}")
    print(
        "Structure: "
        f"{report.headings} heading(s), {report.tables} table(s); "
        f"source: {report.source_headings} heading style(s), "
        f"{report.source_tables} table(s)"
    )
    print(f"Links:     {report.resolved}/{report.links} resolved")
    for warning in report.warnings:
        print(f"warning: {warning}")
    for missing in report.missing:
        print(f"missing: {missing}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a .docx to Markdown and extract its images."
    )
    parser.add_argument("input", type=Path, help="Word .docx file to convert")
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        help="Markdown output path (default: sibling <stem>.md)",
    )
    parser.add_argument(
        "--media-dir",
        type=Path,
        help="Image directory (default: <stem>.assets beside the output)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing Markdown file or image directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input
    if not input_path.is_file():
        fail(f"input file not found: {input_path}")
    if input_path.suffix.lower() != ".docx":
        fail(f"expected a .docx file, got: {input_path.suffix or 'no suffix'}", 1)

    output_path = args.out or input_path.with_suffix(".md")
    media_dir = args.media_dir or output_path.with_name(output_path.stem + ".assets")

    if output_path.resolve() == input_path.resolve():
        fail("output path must differ from the input path")
    if not args.force:
        if output_path.exists():
            fail(f"{output_path} already exists (use --force to overwrite)")
        if media_dir.exists():
            fail(f"{media_dir} already exists (use --force to overwrite)")

    report = convert(input_path, output_path, media_dir)
    print_report(input_path, output_path, media_dir, report)
    if report.missing:
        fail(f"{len(report.missing)} image reference(s) could not be resolved", 3)


if __name__ == "__main__":
    main()

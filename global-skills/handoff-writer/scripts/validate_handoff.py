#!/usr/bin/env python3
"""Validate a DESIGN_HANDOFF or SESSION_HANDOFF document.

Stdlib only. Checks the house format used in `_ai/backlog/active/`:
frontmatter, filename convention, section set and order, empty sections,
placeholder leftovers, owner-bearing open questions and stale timestamps.

Usage:
    python3 validate_handoff.py PATH [PATH ...]
    python3 validate_handoff.py --strict PATH
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

FRONTMATTER_REQUIRED = [
    "filename",
    "title",
    "createdAt",
    "updatedAt",
    "status",
    "tags",
    "documentType",
]

TYPE_RULES = {
    "DESIGN_HANDOFF": {
        "title_prefix": "Design Handoff:",
        "statuses": {"draft", "validated", "implemented", "superseded"},
        "sections": [
            "Context",
            "Decisions",
            "Rejected Alternatives",
            "Constraints Discovered",
            "Open Questions",
            "Scope Boundary",
        ],
        "optional_sections": ["Next Artifact", "References", "Appendix"],
    },
    "SESSION_HANDOFF": {
        "title_prefix": "Session Handoff:",
        "statuses": {"active", "blocked", "done", "abandoned"},
        "sections": [
            "Objective",
            "Current State",
            "Decisions Made",
            "Dead Ends",
            "Open Questions",
            "Next Actions",
            "Verification",
            "Where Things Live",
            "Handoff Notes",
        ],
        "optional_sections": ["Next Artifact", "References", "Appendix"],
    },
}

FILENAME_RE = re.compile(
    r"^(?P<stamp>\d{6}_\d{4})__(?P<type>DESIGN_HANDOFF|SESSION_HANDOFF)__"
    r"(?P<topic>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$"
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S")
SUBHEADING_RE = re.compile(r"^###\s+\S")
TABLE_SEPARATOR_RE = re.compile(r"^\|[\s:|-]+\|$")
BOLD_LEAD_RE = re.compile(r"^\*\*[^*]{2,}\*\*")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
PLACEHOLDER_ONLY_RE = re.compile(r"^\{[^{}\n]{1,80}\}$")
FORBIDDEN_IN_CONTENT = [
    (re.compile(r"\bYYMMDD_HHmm\b"), "unfilled date placeholder"),
    (
        re.compile(r"\{(?:kebab-case-topic|TYPE|topic|name-of-the-[a-z-]+)\}"),
        "unfilled placeholder",
    ),
]
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


@dataclass
class Result:
    path: Path
    errors: list[str]
    warnings: list[str]

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("file does not start with '---' frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError("frontmatter is not closed with '---'") from None

    data: dict[str, str] = {}
    index = 1
    while index < end:
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in " \t" or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            # Collect indented or flow-style continuation lines (e.g. tags: [ ... ]).
            parts: list[str] = []
            while index < end:
                nxt = lines[index]
                if nxt.startswith((" ", "\t")):
                    parts.append(nxt.strip())
                    index += 1
                elif nxt.strip().startswith(("[", "{")):
                    parts.append(nxt.strip())
                    index += 1
                else:
                    break
            value = " ".join(parts)
        data[key] = value
    return data, "\n".join(lines[end + 1 :])


def split_sections(body: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, list[str]]] = []
    current_name: str | None = None
    current_lines: list[str] = []
    in_fence = False

    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        match = None if in_fence else HEADING_RE.match(line)
        if match:
            if current_name is not None:
                sections.append((current_name, current_lines))
            current_name = match.group(1).strip()
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)

    if current_name is not None:
        sections.append((current_name, current_lines))
    return [(name, "\n".join(lines)) for name, lines in sections]


def meaningful_lines(content: str) -> list[str]:
    content = COMMENT_RE.sub("", content)
    return [line.strip() for line in content.splitlines() if line.strip()]


def strip_code(content: str) -> str:
    """Drop fenced and inline code so code samples are not read as prose."""
    content = FENCED_CODE_RE.sub("", content)
    return INLINE_CODE_RE.sub("", content)


def count_items(content: str) -> int:
    """Count list items, decision subsections (### 1. ...) and table rows.

    Legacy handoffs write decisions as numbered sub-headings or as tables;
    all three shapes are valid entries.
    """
    lines = meaningful_lines(content)
    count = 0
    index = 0
    while index < len(lines):
        line = lines[index]
        if BULLET_RE.match(line) or SUBHEADING_RE.match(line):
            count += 1
            index += 1
            continue
        if BOLD_LEAD_RE.match(line):
            count += 1
            index += 1
            continue
        if line.startswith("|") and line.endswith("|"):
            index += 1
            if index < len(lines) and TABLE_SEPARATOR_RE.match(lines[index]):
                index += 1  # header + separator are not entries
            while (
                index < len(lines)
                and lines[index].startswith("|")
                and lines[index].endswith("|")
            ):
                count += 1
                index += 1
            continue
        index += 1
    return count


def check_frontmatter(meta: dict[str, str], path: Path, result: Result) -> str | None:
    for key in FRONTMATTER_REQUIRED:
        if not meta.get(key):
            result.add_error(f"frontmatter: missing or empty '{key}'")

    doc_type = unquote(meta.get("documentType", ""))
    if doc_type and doc_type not in TYPE_RULES:
        result.add_error(
            f"frontmatter: documentType '{doc_type}' is not one of "
            f"{', '.join(TYPE_RULES)}"
        )

    status = unquote(meta.get("status", ""))
    if doc_type in TYPE_RULES and status:
        allowed = TYPE_RULES[doc_type]["statuses"]
        if status not in allowed:
            result.add_error(
                f"frontmatter: status '{status}' invalid for {doc_type}; "
                f"use one of {', '.join(sorted(allowed))}"
            )

    tags = meta.get("tags", "")
    if tags in {"", "[]"}:
        result.add_error("frontmatter: 'tags' must list at least one tag")

    created = unquote(meta.get("createdAt", ""))
    updated = unquote(meta.get("updatedAt", ""))
    for key, value in (("createdAt", created), ("updatedAt", updated)):
        if value and not DATE_RE.match(value):
            result.add_error(
                f"frontmatter: {key} '{value}' is not 'YYYY-MM-DD HH:mm'"
            )
    if DATE_RE.match(created) and DATE_RE.match(updated):
        try:
            created_dt = datetime.strptime(created, "%Y-%m-%d %H:%M")
            updated_dt = datetime.strptime(updated, "%Y-%m-%d %H:%M")
            if updated_dt < created_dt:
                result.add_error("frontmatter: updatedAt is earlier than createdAt")
        except ValueError:
            result.add_error("frontmatter: createdAt/updatedAt is not a valid date")

    declared = unquote(meta.get("filename", ""))
    if declared and Path(declared).name != path.name:
        result.add_error(
            f"frontmatter: filename '{declared}' does not match file '{path.name}'"
        )
    if declared:
        declared_parts = Path(declared).parts
        if "_ai" not in declared_parts or "backlog" not in declared_parts:
            result.add_error(
                "frontmatter: filename must point inside '_ai/backlog/'"
            )
        elif "_ai" in path.parts:
            declared_tail = declared_parts[declared_parts.index("_ai") :]
            actual_tail = path.parts[path.parts.index("_ai") :]
            if declared_tail != actual_tail:
                result.add_error(
                    "frontmatter: filename path does not match the file's "
                    f"location ('{Path(*declared_tail)}')"
                )

    title = unquote(meta.get("title", ""))
    if title and doc_type in TYPE_RULES:
        prefix = TYPE_RULES[doc_type]["title_prefix"]
        if not title.startswith(prefix):
            result.add_warning(f"title should start with '{prefix}'")

    return doc_type or None


def check_filename(path: Path, meta: dict[str, str], doc_type: str, result: Result) -> None:
    match = FILENAME_RE.match(path.name)
    if not match:
        result.add_error(
            "filename: expected '{YYMMDD_HHmm}__{TYPE}__{kebab-case-topic}.md'"
        )
        return
    if doc_type and match.group("type") != doc_type:
        result.add_error(
            f"filename type '{match.group('type')}' does not match "
            f"documentType '{doc_type}'"
        )

    stamp = match.group("stamp")
    declared = unquote(meta.get("createdAt", ""))
    if DATE_RE.match(declared):
        expected = datetime.strptime(declared, "%Y-%m-%d %H:%M").strftime("%y%m%d_%H%M")
        if stamp != expected:
            result.add_warning(
                f"filename timestamp '{stamp}' does not match createdAt "
                f"(expected '{expected}')"
            )


def check_sections(
    body: str,
    doc_type: str,
    meta: dict[str, str],
    result: Result,
) -> None:
    rules = TYPE_RULES[doc_type]
    sections = split_sections(body)
    found = [name for name, _ in sections]
    found_lower = {name.lower(): name for name in found}
    content_by_name = {name: content for name, content in sections}

    if not sections:
        result.add_error("no '## ' sections found")
        return

    for required in rules["sections"]:
        if required.lower() not in found_lower:
            result.add_error(f"section: missing '## {required}'")

    known = {name.lower() for name in rules["sections"] + rules["optional_sections"]}
    for name in found:
        lowered = name.lower()
        if lowered not in known and not lowered.startswith("appendix"):
            result.add_warning(f"section: unexpected '## {name}'")

    canonical = [s.lower() for s in rules["sections"] if s.lower() in found_lower]
    actual = [n.lower() for n in found if n.lower() in canonical]
    if actual != canonical:
        result.add_error("section: required sections are out of canonical order")

    for name in found:
        content = content_by_name[name]
        lines = meaningful_lines(content)
        if not lines:
            result.add_error(f"section '{name}' is empty")
            continue
        if len(lines) == 1 and PLACEHOLDER_ONLY_RE.match(lines[0]):
            result.add_error(f"section '{name}' still contains only a placeholder")
            continue
        prose = strip_code(content)
        for pattern, label in FORBIDDEN_IN_CONTENT:
            if pattern.search(prose):
                result.add_warning(f"section '{name}' contains {label}")
                break

    if "rejected alternatives" in found_lower:
        name = found_lower["rejected alternatives"]
        items = count_items(content_by_name[name])
        if items < 2:
            result.add_warning(
                f"section '{name}' should record at least two rejected options"
            )

    if "open questions" in found_lower:
        name = found_lower["open questions"]
        content = content_by_name[name].strip()
        table_header = next(
            (line for line in content.splitlines() if line.strip().startswith("|")),
            "",
        )
        has_owner_column = "owner" in table_header.lower()
        if content.lower() not in {"", "none.", "none", "n/a"} and not has_owner_column:
            blocks: list[list[str]] = []
            current: list[str] = []
            for line in content.splitlines():
                if BULLET_RE.match(line) and current:
                    blocks.append(current)
                    current = [line]
                elif line.strip():
                    current.append(line)
            if current:
                blocks.append(current)
            for block in blocks:
                text = "\n".join(block).strip()
                if text.lower().startswith(("- none", "none")):
                    continue
                if "owner:" not in text.lower():
                    excerpt = text.splitlines()[0][:70]
                    result.add_warning(
                        f"open question has no owner: '{excerpt}'"
                    )

    if doc_type == "DESIGN_HANDOFF":
        if "next artifact" not in found_lower and "archive" not in result.path.parts:
            result.add_warning(
                "section: '## Next Artifact' is recommended for design handoffs"
            )
        decisions = found_lower.get("decisions")
        if decisions and count_items(content_by_name[decisions]) < 1:
            result.add_error("section 'Decisions' has no decision entries")
        scope = found_lower.get("scope boundary")
        if scope:
            scope_text = content_by_name[scope].lower()
            missing = []
            if not ("in scope" in scope_text or "**in" in scope_text):
                missing.append("in scope")
            if not ("out of scope" in scope_text or "**out" in scope_text):
                missing.append("out of scope")
            if missing:
                result.add_warning(
                    "section 'Scope Boundary' is missing: " + ", ".join(missing)
                )


def validate(path: Path) -> Result:
    result = Result(path=path, errors=[], warnings=[])
    if not path.exists():
        result.add_error("file not found")
        return result

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        result.add_error(f"cannot read file: {exc}")
        return result

    try:
        meta, body = parse_frontmatter(text)
    except ValueError as exc:
        result.add_error(str(exc))
        return result

    doc_type = check_frontmatter(meta, path, result)
    if doc_type in TYPE_RULES:
        check_filename(path, meta, doc_type, result)
        check_sections(body, doc_type, meta, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate DESIGN_HANDOFF / SESSION_HANDOFF documents."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="markdown file(s)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as failures",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="only print failing files",
    )
    args = parser.parse_args(argv)

    failed = False
    for path in args.paths:
        result = validate(path)
        has_error = bool(result.errors)
        has_warning = bool(result.warnings)
        if args.strict and has_warning:
            failed = True

        if has_error or (args.strict and has_warning):
            failed = True

        if has_error or has_warning or not args.quiet:
            print(f"{path}")
            for error in result.errors:
                print(f"  ERROR {error}")
            for warning in result.warnings:
                print(f"  WARN  {warning}")
            if not has_error and not has_warning:
                print("  OK")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

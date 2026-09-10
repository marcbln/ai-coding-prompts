#!/usr/bin/env python3
"""Validate an OKF v0.1 bundle.

OKF v0.1 hard rules enforced:
  1. Every concept (*.md) has parseable YAML frontmatter.
  2. Every concept has a non-empty string `type`.
  3. Reserved files index.md and log.md exist at the bundle root.
  4. index.md declares `okf_version`.

`--strict` additionally runs producer lints:
  - missing recommended frontmatter fields (`title`, `description`)
  - broken intra-bundle links
  - links missing the `.md` extension
  - orphan concepts (non-reserved files referenced from nowhere)

Exit codes: 0 = conformant, 1 = errors (or strict warnings), 2 = bad invocation.
"""

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

RESERVED = {"index.md", "log.md"}
LINK_RE = re.compile(r"\]\(([^)]+)\)")
FRONTMATTER_SPLIT = re.compile(r"^---\s*\n", re.MULTILINE)


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, "missing frontmatter delimiter"
    match = FRONTMATTER_SPLIT.search(text, 0)
    end = text.find("\n---", match.end() if match else 0)
    if end == -1:
        return None, "unterminated frontmatter"
    raw = text[match.end():end]
    if yaml is not None:
        try:
            data = yaml.safe_load(raw)
        except Exception as exc:
            return None, "invalid YAML: %s" % exc
        return (data or {}), None
    return parse_frontmatter_fallback(raw), None


def parse_frontmatter_fallback(raw):
    data = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            value = [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
        elif value in {"null", "~", "true", "false"}:
            value = None if value in {"null", "~"} else (value == "true")
        else:
            value = value.strip("'\"")
        data[key] = value
    return data


def collect_link_targets(text):
    targets = []
    for match in LINK_RE.finditer(text):
        target = match.group(1).split()[0] if match.group(1) else ""
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        targets.append(target.split("#")[0].split("?")[0])
    return targets


def resolve_target(rel, target):
    base = os.path.dirname(rel)
    return os.path.normpath(os.path.join(base, target))


def validate(bundle_dir, strict):
    bundle = Path(bundle_dir)
    errors, warnings, details = [], [], []

    if not bundle.is_dir():
        return 2, ["bundle path is not a directory: %s" % bundle]

    for reserved in sorted(RESERVED):
        if not (bundle / reserved).is_file():
            errors.append("missing reserved file: %s/%s" % (bundle.name, reserved))

    concepts = sorted(bundle.rglob("*.md"))
    all_files = {p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file()}
    referenced = set()
    metadata = {}

    for path in concepts:
        rel = path.relative_to(bundle).as_posix()
        data, err = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        metadata[rel] = data
        if err:
            errors.append("%s: %s" % (rel, err))
            continue
        type_ = data.get("type")
        if not isinstance(type_, str) or not type_.strip():
            errors.append("%s: missing or empty `type`" % rel)
        for target in collect_link_targets(path.read_text(encoding="utf-8", errors="replace")):
            referenced.add(resolve_target(rel, target))

    if (bundle / "index.md").is_file():
        index_data = metadata.get("index.md")
        if index_data is None:
            errors.append("index.md: unreadable frontmatter")
        elif "okf_version" not in index_data:
            errors.append("index.md: missing `okf_version` declaration")

    if strict:
        for rel, data in metadata.items():
            if data is None:
                continue
            for field in ("title", "description"):
                if field not in data:
                    warnings.append("%s: missing recommended field `%s`" % (rel, field))
            for target in collect_link_targets((bundle / rel).read_text(encoding="utf-8", errors="replace")):
                resolved = resolve_target(rel, target)
                if resolved not in all_files:
                    errors.append("%s: broken link -> %s" % (rel, target))
                elif not target.endswith(".md") and not target.endswith("/"):
                    warnings.append("%s: link missing .md extension -> %s" % (rel, target))
        for rel in sorted(metadata):
            if rel in RESERVED:
                continue
            if rel not in referenced:
                warnings.append("%s: orphan concept (referenced from nowhere)" % rel)

    rc = 1 if errors else (1 if (strict and warnings) else 0)
    for line in errors:
        print("ERROR  %s" % line)
    for line in warnings:
        print("WARN   %s" % line)
    print("(strict mode: %s)" % ("on" if strict else "off"))
    print("%d concepts, %d errors, %d warnings" % (len(concepts), len(errors), len(warnings)))
    return rc, details


def main(argv=None):
    parser = argparse.ArgumentParser(prog="okf-validate", description="Validate an OKF v0.1 bundle.")
    parser.add_argument("bundle_dir", help="path to the OKF bundle directory")
    parser.add_argument("--strict", action="store_true", help="run producer lints and fail on warnings")
    args = parser.parse_args(argv)
    code, _ = validate(args.bundle_dir, args.strict)
    return code


if __name__ == "__main__":
    sys.exit(main())
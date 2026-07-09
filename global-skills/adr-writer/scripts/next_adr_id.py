#!/usr/bin/env python3
"""Suggest the next free ADR ID for a given category range.

Usage:
    next_adr_id.py <adr-directory> <category>

Categories:
    architecture   (1000-1999)
    backend        (2000-2999)
    frontend       (3000-3999)
    integrations   (4000-4999)
    devops         (5000-5999)

Prints the next suggested ID (highest existing in range + 10, or the
range start if none exist) and the target filename prefix.
"""
import os
import re
import sys

RANGES = {
    "architecture": (1000, 1999),
    "backend": (2000, 2999),
    "frontend": (3000, 3999),
    "integrations": (4000, 4999),
    "devops": (5000, 5999),
}


def next_id(adr_dir, category):
    if category not in RANGES:
        raise SystemExit(f"Unknown category '{category}'. Choose from: {', '.join(RANGES)}")
    lo, _ = RANGES[category]
    ids = []
    pat = re.compile(r"^ADR__(\d{4})-")
    for name in os.listdir(adr_dir):
        m = pat.match(name)
        if not m:
            continue
        nid = int(m.group(1))
        if lo <= nid <= RANGES[category][1]:
            ids.append(nid)
    nxt = (max(ids) + 10) if ids else lo
    print(nxt)
    return nxt


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: next_adr_id.py <adr-directory> <category>")
    next_id(sys.argv[1], sys.argv[2])

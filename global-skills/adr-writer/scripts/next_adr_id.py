#!/usr/bin/env python3
"""Suggest the next free ADR sequence number for a given decision date.

Usage:
    next_adr_id.py <adr-directory> [yyyymmdd]

ADRs are named `ADR__YYMMDD-N__kebab-case-title.md`, where N is a per-day
sequence number starting at 1. This script prints the next N for the given
date (highest existing N of that day + 1; defaults to today if omitted).
"""
import os
import re
import sys
from datetime import date


def next_id(adr_dir: str, datestr: str | None = None) -> int:
    d = date.today() if datestr is None else date.fromisoformat(datestr)
    stamp = d.strftime("%y%m%d")
    pat = re.compile(rf"^ADR__{stamp}-(\d+)__")
    nums = []
    for name in os.listdir(adr_dir):
        m = pat.match(name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 1


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit("Usage: next_adr_id.py <adr-directory> [yyyymmdd]")
    stamp_arg = None
    if len(sys.argv) == 3:
        stamp_arg = sys.argv[2]
        try:
            date.fromisoformat(stamp_arg)
        except ValueError:
            raise SystemExit("Invalid date argument, expected YYYYMMDD")
    print(next_id(sys.argv[1], stamp_arg))
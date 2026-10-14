#!/usr/bin/env bash
# upgrade_sections.sh — print UPGRADE-6.x.md sections that fall inside a
# version range.
#
# Usage: upgrade_sections.sh <shopware-repo> <from> <to>
#   <from>/<to> accept v6.7.9.1 or 6.7.9.1
# Range semantics: exclusive <from>, inclusive <to> (same as sw-changelog).
#
# Handles the real file quirks: versionless "# ..." headings belong to the
# preceding version section; old UPGRADE-6.1/6.2 files have no version
# headings and simply produce no output.

set -euo pipefail

REPO="${1:?usage: upgrade_sections.sh <shopware-repo> <from> <to>}"
FROM="${2:?missing <from>}"
TO="${3:?missing <to>}"

FROM="${FROM#v}"
TO="${TO#v}"

if [[ ! -d "$REPO" ]]; then
  echo "error: '$REPO' is not a directory" >&2
  exit 1
fi

for file in "$REPO"/UPGRADE-6.*.md; do
  [[ -e "$file" ]] || continue
  awk -v from="$FROM" -v to="$TO" -v file="$(basename "$file")" '
    function vkey(v,   n, a, i, k) {
      n = split(v, a, ".")
      k = 0
      for (i = 1; i <= n; i++) k = k * 1000 + a[i]
      return k
    }
    function flush() {
      if (active) {
        sub(/\n+$/, "", body)
        if (body != "") printf "\n===== %s :: %s =====\n%s\n", file, ver, body
      }
    }
    /^# [0-9]+\.[0-9]+(\.[0-9]+)+[[:space:]]*$/ {
      flush()
      ver = $2
      active = (vkey(ver) > vkey(from)) && (vkey(ver) <= vkey(to))
      body = ""
      next
    }
    {
      if (active) body = body $0 "\n"
    }
    END { flush() }
  ' "$file"
done

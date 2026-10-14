#!/usr/bin/env bash
# inventory.sh — extract a plugin's Shopware integration surface.
#
# Usage: inventory.sh <plugin-dir>
#
# Read-only. Prints normalized, sorted, unique entries grouped by kind:
# composer facts, Shopware FQCNs, service decorates/references, event
# subscribers/listeners, routes, Twig extends/blocks/overrides, and JS
# registrations. Output is meant to be matched against Shopware changelog
# and UPGRADE notes (see references/inventory-and-matching.md).

set -euo pipefail

PLUGIN_DIR="${1:?usage: inventory.sh <plugin-dir>}"
if [[ ! -d "$PLUGIN_DIR" ]]; then
  echo "error: '$PLUGIN_DIR' is not a directory" >&2
  exit 1
fi

cd "$PLUGIN_DIR"

EXCLUDES=(--exclude-dir=vendor --exclude-dir=node_modules --exclude-dir=tests
          --exclude-dir=.git --exclude-dir=.idea)

section() { printf '\n== %s\n' "$1"; }

section "plugin (composer.json)"
if [[ -f composer.json ]]; then
  python3 - composer.json <<'PY'
import json
import sys

try:
    data = json.load(open(sys.argv[1]))
except Exception as exc:  # noqa: BLE001
    print(f"(unreadable: {exc})")
    raise SystemExit(0)

print(f"name: {data.get('name', '?')}")
print(f"version: {data.get('version', '?')}")
req = data.get("require", {})
print(f"shopware/core: {req.get('shopware/core', '?')}")
for dep in sorted(k for k in req if k.startswith("topdata/")):
    print(f"requires {dep}: {req[dep]}")
PY
else
  echo "(no composer.json)"
fi

section "Shopware FQCNs (PHP)"
grep -rhoE "${EXCLUDES[@]}" --include='*.php' 'Shopware\\[A-Za-z0-9_\\]+' . 2>/dev/null \
  | sort -u || true

section "decorated services (XML)"
grep -rhoE "${EXCLUDES[@]}" --include='*.xml' 'decorates="[^"]+"' . 2>/dev/null \
  | sed -E 's/^decorates="//; s/"$//' | sort -u || true

section "referenced services (XML)"
grep -rhoE "${EXCLUDES[@]}" --include='*.xml' 'type="service" id="[^"]+"' . 2>/dev/null \
  | sed -E 's/.*id="//; s/"$//' | sort -u || true

section "event subscribers (read getSubscribedEvents in these files)"
grep -rl "${EXCLUDES[@]}" --include='*.php' 'function getSubscribedEvents' . 2>/dev/null \
  | sort -u || true

section "event listeners (XML)"
grep -rhoE "${EXCLUDES[@]}" --include='*.xml' '<tag name="kernel.event_listener" event="[^"]+"' . 2>/dev/null \
  | sed -E 's/.*event="//; s/"$//' | sort -u || true

section "route paths"
# Flatten PHP files first: #[Route(...)] attributes are frequently multi-line.
{
  while IFS= read -r -d '' file; do
    tr '\n' ' ' < "$file"
    printf '\n'
  done < <(find . -type f -name '*.php' \
             -not -path '*/vendor/*' -not -path '*/node_modules/*' \
             -not -path '*/tests/*' -print0)
} | grep -oE '#\[Route\([^]]*' 2>/dev/null \
  | grep -oE "['\"]/[^'\"]*" \
  | tr -d "'\"" | sort -u || true

section "Twig extends/includes/embeds (core targets)"
grep -rhoE "${EXCLUDES[@]}" --include='*.twig' "sw_(extends|include|embed) +['\"][^'\"]+" . 2>/dev/null \
  | sed -E "s/.*sw_(extends|include|embed) +['\"]//" | sort -u || true

section "Twig block names"
grep -rhoE "${EXCLUDES[@]}" --include='*.twig' '\{%-? *block +[A-Za-z0-9_]+' . 2>/dev/null \
  | awk '{print $NF}' | sort -u || true

section "template files (shadowed core paths)"
if [[ -d src/Resources/views ]]; then
  find src/Resources/views -type f -name '*.twig' | sort -u
else
  echo "(no src/Resources/views)"
fi

section "JS registrations (storefront/admin)"
{
  grep -rhoE "${EXCLUDES[@]}" --include='*.js' "PluginManager\.register\('[^']+'" . 2>/dev/null \
    | sed -E "s/.*register\('//; s/'$//" || true
  grep -rhoE "${EXCLUDES[@]}" --include='*.js' "Module\.register\('[^']+'" . 2>/dev/null \
    | sed -E "s/.*register\('//; s/'$//" || true
  grep -rhoE "${EXCLUDES[@]}" --include='*.js' 'class +[A-Za-z0-9_]+ +extends +Plugin\b' . 2>/dev/null \
    | awk '{print $2}' || true
} | sort -u || true

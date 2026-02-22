#!/bin/bash
WORKSPACE_DIR="$(pwd)"

echo "Detecting uncommitted changes in: $WORKSPACE_DIR"

# Get staged, unstaged (HEAD), and untracked files
CHANGED_FILES=$( { git diff --name-only HEAD 2>/dev/null || git ls-files; git ls-files --others --exclude-standard; } | sort -u | sed '/^$/d' )

if [ -z "$CHANGED_FILES" ]; then
  echo "✅ No uncommitted changes found. Nothing to lint!"
  exit 0
fi

echo "Files to be linted:"
echo "$CHANGED_FILES" | while read -r file; do echo "  - $file"; done
echo "--------------------------------------------------"

# Convert file list to a regex pattern
REGEX_PATTERN=$(echo "$CHANGED_FILES" | sed 's/\./\\./g' | tr '\n' '|' | sed 's/|$//')
FILTER_REGEX=".*($REGEX_PATTERN).*"

docker run --rm \
  -e RUN_LOCAL=true \
  -e FILTER_REGEX_INCLUDE="$FILTER_REGEX" \
  -e CREATE_LOG_FILE=false \
  -e LOG_LEVEL=NOTICE \
  -v "$WORKSPACE_DIR":/tmp/lint \
  ghcr.io/super-linter/super-linter:latest

echo "--------------------------------------------------"

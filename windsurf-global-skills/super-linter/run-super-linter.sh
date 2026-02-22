#!/bin/bash
if [ -z "$1" ]; then
  echo "Error: Missing target file."
  echo "Usage: $0 <relative/path/to/file>"
  exit 1
fi

TARGET_FILE="$1"
WORKSPACE_DIR="$(pwd)"

echo "Running GitHub Super Linter on: $TARGET_FILE"
echo "--------------------------------------------------"

docker run --rm \
  -e RUN_LOCAL=true \
  -e FILTER_REGEX_INCLUDE=".*$TARGET_FILE.*" \
  -e CREATE_LOG_FILE=false \
  -e LOG_LEVEL=NOTICE \
  -v "$WORKSPACE_DIR":/tmp/lint \
  ghcr.io/super-linter/super-linter:latest

echo "--------------------------------------------------"

#!/bin/bash
# A lightweight CLI to help the AI interact with the Obsidian markdown files.

COMMAND=$1
ARG1=$2

if[ -z "$COMMAND" ]; then
    echo "Usage: ./kb-helper.sh[find-tag|search-frontmatter|list-empty]"
    echo "  find-tag <tag>             - Finds all markdown files containing the specified tag in frontmatter"
    echo "  search-frontmatter <key>   - Finds all files containing a specific YAML frontmatter key"
    echo "  list-empty                 - Lists all markdown files that are completely empty"
    exit 1
fi

KB_DIR="../../_ai"

case $COMMAND in
    "find-tag")
        if [ -z "$ARG1" ]; then echo "Provide a tag."; exit 1; fi
        # Searches for tags in the format `tags: [..., mytag, ...]` or `- mytag`
        echo "Searching for tag: $ARG1..."
        grep -rlw "$KB_DIR" -e "$ARG1" --include="*.md"
        ;;
    "search-frontmatter")
        if[ -z "$ARG1" ]; then echo "Provide a key."; exit 1; fi
        echo "Files containing frontmatter key $ARG1:"
        grep -rl "^$ARG1:" "$KB_DIR" --include="*.md"
        ;;
    "list-empty")
        echo "Empty files needing documentation:"
        find "$KB_DIR" -name "*.md" -type f -empty
        ;;
    *)
        echo "Unknown command: $COMMAND"
        exit 1
        ;;
esac

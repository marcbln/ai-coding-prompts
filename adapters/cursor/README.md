# Cursor Adapter

This adapter wires the content of `ai-coding-prompts` into
[Cursor](https://www.cursor.com/).

## Distribute rules with Ruler

Run this from the repository root to generate the Cursor `AGENTS.md`:

```bash
ruler apply --config adapters/cursor/ruler.toml
```

Ruler reads the files in `.ruler/` and writes `AGENTS.md` to the project root,
which Cursor picks up automatically as repository-wide AI instructions.

## Adding per-project rules

To use specific coding conventions (e.g. `conventions/conventions-python-v2.md`)
in a Cursor project, copy the relevant file(s) into that project's `.ruler/`
directory and run `ruler apply` there.

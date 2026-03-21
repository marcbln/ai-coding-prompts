# Claude Adapter

This adapter wires the content of `ai-coding-prompts` into
[Claude Code](https://www.anthropic.com/claude-code).

## Distribute rules with Ruler

Run this from the repository root to generate `CLAUDE.md`:

```bash
ruler apply --config adapters/claude/ruler.toml
```

Ruler reads the files in `.ruler/` and writes `CLAUDE.md` to the project root,
which Claude Code picks up automatically as repository-wide AI instructions.

## Skills support

Claude Code can also load skills from `.claude/skills/`.  
Ruler propagates skills automatically when the `--skills` flag is active
(enabled by default).  If you have skills you want Claude to use, place them in
`.claude/skills/<skill-name>/` alongside a `SKILL.md` file.

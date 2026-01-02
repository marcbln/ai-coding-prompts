# Fetched Prompts

This directory contains prompts and prompt templates fetched from [iamhenry's GitHub gists](https://gist.github.com/iamhenry).

## Categories

| Category | Emoji | Description | Files |
|----------|-------|-------------|--------|
| **Workflow** | 🔄 | Workflow and process prompts | 10 |
| **Marketing** | 📣 | Marketing and copywriting prompts | 6 |
| **Development** | 💻 | Development and coding prompts | 7 |
| **Design** | 🎨 | Design and architecture prompts | 2 |
| **Product** | 🚀 | Product and idea prompts | 5 |
| **Consulting** | 🧠 | Expert and consulting prompts | 13 |
| **Documentation** | 📚 | Documentation and template prompts | 8 |

## Usage

All prompts include YAML frontmatter with metadata for AI coding agents:

```yaml
---
slug: prompt-identifier
name: "🧠 Prompt Name"
category: consulting
version: 1.0.0
groups:
  - read
  - command
source: global
---
```

## Integration

These prompts can be integrated with:
- **Windsurf** global workflows (`~/.codeium/windsurf/global_workflows`)
- **Cursor** custom modes (via `cline_custom_modes.json`)
- **OpenCode** custom modes
- Similar AI coding agent systems

## Source Files

Original source files are in `iamhenry-gists/` directory. The organization follows:
- **Prompts**: Files containing AI instructions, role definitions, or agent prompts
- **Templates**: Fill-in-the-blank templates for documents, frameworks, or processes
- **Code**: Plugin files (TypeScript/JavaScript) for AI coding environments
- **Empty**: Gists with only metadata (no content files)

## Credits

All prompts are from [iamhenry](https://github.com/iamhenry)'s collection of AI prompts and tools.

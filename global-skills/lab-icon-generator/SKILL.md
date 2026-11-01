# Lab Experiment Icon Generator

Use this skill whenever you need to attach or refresh minimalist, abstract SVG icons for experiments in `projects.yaml`.

## Capabilities
- **Mode `iconify` (Default)**: Fast, deterministic, zero-cost. Maps project titles and tags to Lucide icon glyphs via Iconify CDN.
- **Mode `abstract`**: Generates bespoke, minimalist geometric SVGs using OpenAI (`OPENAI_API_KEY` required).

## Usage

```bash
# Basic usage (Iconify / Lucide mode)
python3 /home/marc/devel/ai-coding-prompts/global-skills/lab-icon-generator/generate_icons.py \
  --manifest /path/to/projects.yaml \
  --icons-dir /path/to/public/icons

# Generative Abstract SVG mode
OPENAI_API_KEY="sk-..." python3 /home/marc/devel/ai-coding-prompts/global-skills/lab-icon-generator/generate_icons.py \
  --manifest /path/to/projects.yaml \
  --icons-dir /path/to/public/icons \
  --mode abstract \
  --force
```

## Manifest Behavior
The script will write individual `.svg` files into `--icons-dir` and automatically add or update the `icon` property for each project inside `projects.yaml`:

```yaml
- title: Compatibility scraper
  namespace: compat
  tags: [enrichment, evidence]
  icon: /icons/compatibility-scraper.svg
```

#!/usr/bin/env python3
"""
lab-icon-generator: Generates or fetches minimalist SVG icons for lab experiments.
Supports:
  1. 'iconify' mode (free, instant, uses Lucide via Iconify API)
  2. 'abstract' mode (generative abstract SVG via OpenAI API)
"""

import os
import sys
import json
import re
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: 'pyyaml' is required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ABSTRACT_SYSTEM_PROMPT = """You are a design system engineer.
Generate a minimalist, abstract, technical SVG icon for a software experiment.

Rules:
1. Canvas: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
2. Style: Abstract, geometric, high-tech (Linear/Vercel inspired).
3. Translate abstract concepts into geometry (e.g. scrapers -> radar arcs/scanlines; feeds -> parallel stepped vectors; sandboxes -> nested isometric bounds).
4. Output: ONLY the raw valid <svg>...</svg> element. No prose, no markdown fences.
"""

# Common semantic keyword mapping for rapid Iconify/Lucide matching
KEYWORD_MAPPINGS = {
    "scraper": "scan-search",
    "scrape": "scan-search",
    "lead": "target",
    "prospect": "binoculars",
    "enrichment": "layers-2",
    "enrich": "layers-2",
    "compliance": "shield-check",
    "migration": "arrow-left-right",
    "observability": "route",
    "replay": "history",
    "graph": "git-graph",
    "visualizer": "network",
    "audit": "radar",
    "price": "trending-up",
    "competitor": "crosshair",
    "newsletter": "newspaper",
    "digest": "scroll-text",
    "outreach": "mail-search",
    "model": "cpu",
    "llm": "sparkles",
    "workflow": "workflow",
    "signal": "activity",
    "sandbox": "box",
    "tts": "waveform",
    "voice": "audio-lines",
    "spec": "file-check",
    "agent": "bot"
}

def resolve_iconify_name(project: dict) -> str:
    search_corpus = f"{project.get('title', '')} {project.get('namespace', '')} {' '.join(project.get('tags', []))}".lower()
    for kw, icon in KEYWORD_MAPPINGS.items():
        if kw in search_corpus:
            return icon
    return "box"

def fetch_iconify_svg(icon_name: str) -> str:
    url = f"https://api.iconify.design/lucide/{icon_name}.svg?stroke-width=1.5"
    req = urllib.request.Request(url, headers={"User-Agent": "AutomationLab/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                return resp.read().decode("utf-8")
    except Exception as e:
        print(f"  [!] Failed fetching {icon_name} from Iconify: {e}", file=sys.stderr)
    return ""

def generate_abstract_svg_openai(project: dict) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is missing for 'abstract' mode.")

    payload = {
        "model": "gpt-4o-mini",
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": ABSTRACT_SYSTEM_PROMPT},
            {"role": "user", "content": f"Title: {project.get('title')}\nNamespace: {project.get('namespace')}\nTags: {', '.join(project.get('tags', []))}\nDescription: {project.get('description')}"}
        ]
    }

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        raw = res["choices"][0]["message"]["content"].strip()
        cleaned = re.sub(r"^```xml\n?|^```svg\n?|^```\n?|```$", "", raw, flags=re.MULTILINE).strip()
        return cleaned

def main():
    parser = argparse.ArgumentParser(description="Enrich projects.yaml experiments with icons.")
    parser.add_argument("--manifest", required=True, help="Path to projects.yaml")
    parser.add_argument("--icons-dir", default="public/icons", help="Directory where SVG icons should be stored")
    parser.add_argument("--mode", choices=["iconify", "abstract"], default="iconify", help="Icon generation mode")
    parser.add_argument("--force", action="store_true", help="Overwrite existing icons")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    if not manifest_path.exists():
        print(f"Error: Manifest not found at {manifest_path}", file=sys.stderr)
        sys.exit(1)

    icons_dir = Path(args.icons_dir)
    if not icons_dir.is_absolute():
        icons_dir = manifest_path.parent / icons_dir
    icons_dir.mkdir(parents=True, exist_ok=True)

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    projects = data.get("projects", [])
    updated = False

    print(f"Found {len(projects)} projects in {manifest_path.name}. Running in [{args.mode}] mode.")

    for proj in projects:
        title = proj.get("title", "unnamed")
        slug = proj.get("id") or re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        icon_filename = f"{slug}.svg"
        icon_dest = icons_dir / icon_filename

        if icon_dest.exists() and not args.force and proj.get("icon"):
            continue

        print(f"-> Processing: {title} ({slug})")
        svg_content = ""

        if args.mode == "iconify":
            icon_name = resolve_iconify_name(proj)
            svg_content = fetch_iconify_svg(icon_name)
        elif args.mode == "abstract":
            try:
                svg_content = generate_abstract_svg_openai(proj)
            except Exception as e:
                print(f"   [!] Abstract generation failed ({e}), falling back to iconify.")
                icon_name = resolve_iconify_name(proj)
                svg_content = fetch_iconify_svg(icon_name)

        if svg_content and "<svg" in svg_content:
            icon_dest.write_text(svg_content.strip() + "\n", encoding="utf-8")
            # Update manifest entry
            proj["icon"] = f"/{icons_dir.name}/{icon_filename}"
            updated = True
        else:
            print(f"   [!] Failed to generate/fetch SVG for {slug}")

    if updated:
        with open(manifest_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
        print(f"\n[✓] Successfully updated manifest at {manifest_path}")
    else:
        print("\nAll projects already have icons. Use --force to regenerate.")

if __name__ == "__main__":
    main()

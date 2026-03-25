#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path

def slugify(text):
    """Cascade skill names only allow lowercase letters, numbers, and hyphens."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\-]', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text

def parse_frontmatter(content):
    """Separates existing YAML frontmatter from the markdown body."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        body = match.group(2)

        # Parse frontmatter text into a dictionary
        fm = {}
        for line in fm_text.splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip().strip('"\'')
        return fm, body
    return {}, content

def get_fallback_description(body, fallback_name):
    """Finds the first meaningful line to use as a description if one doesn't exist."""
    for line in body.splitlines():
        stripped = line.strip()
        # Ignore empty lines, markdown headings, lists, quotes, HTML tags
        if stripped and not stripped.startswith(('#', '-', '*', '>', '<')):
            desc = stripped
            # Truncate if too long (YAML descriptions should be concise)
            if len(desc) > 120:
                desc = desc[:117] + "..."
            return desc.replace('"', "'")
    return f"Autonomously executes the {fallback_name} process."

def main():
    parser = argparse.ArgumentParser(description="Convert Windsurf workflows to Cascade skills")
    parser.add_argument("src", type=str, help="Source directory containing .md workflow files")
    parser.add_argument("dest", type=str, help="Destination directory for the converted skills")
    args = parser.parse_args()

    src_dir = Path(args.src).expanduser().resolve()
    dest_dir = Path(args.dest).expanduser().resolve()

    if not src_dir.exists() or not src_dir.is_dir():
        print(f"❌ Error: Source directory does not exist or is not a directory -> {src_dir}")
        return

    dest_dir.mkdir(parents=True, exist_ok=True)
    converted_count = 0

    print(f"🔍 Scanning for workflows in: {src_dir}")
    print(f"📁 Outputting skills to:      {dest_dir}\n")

    for md_file in src_dir.glob("*.md"):
        base_name = md_file.stem
        skill_name = slugify(base_name)
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            print(f"⚠️ Could not read {md_file.name}: {e}")
            continue

        fm, body = parse_frontmatter(original_content)

        # Get or generate description
        description = fm.get('description', '')
        if not description:
            description = get_fallback_description(body, base_name)

        # Retain original frontmatter keys (like auto_execution_mode) excluding name/desc
        extra_fm = []
        for k, v in fm.items():
            if k not in['name', 'description']:
                extra_fm.append(f"{k}: {v}")

        # Build new SKILL.md content
        new_fm =[
            "---",
            f"name: {skill_name}",
            f"description: \"{description}\""
        ]
        new_fm.extend(extra_fm)
        new_fm.append("---")
        
        new_content = "\n".join(new_fm) + "\n\n" + body.strip() + "\n"

        # Create the skill directory
        skill_dir = dest_dir / skill_name
        skill_dir.mkdir(exist_ok=True)

        # Write the SKILL.md file
        skill_md_path = skill_dir / "SKILL.md"
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ Converted: {md_file.name} -> {skill_name}/SKILL.md")
        converted_count += 1

    print(f"\n🎉 Successfully converted {converted_count} workflows!")

if __name__ == "__main__":
    main()


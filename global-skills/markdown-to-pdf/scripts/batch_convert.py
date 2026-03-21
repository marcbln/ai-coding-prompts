#!/usr/bin/env python3
"""
Batch convert multiple Markdown files to PDFs.
"""

import argparse
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import md_to_pdf


def batch_convert(input_pattern, output_dir, template=None, css_file=None, max_workers=4):
    """
    Convert multiple markdown files to PDFs in parallel.
    
    Args:
        input_pattern: Glob pattern for input files
        output_dir: Output directory for PDFs
        template: Built-in template name (optional)
        css_file: Custom CSS file (optional)
        max_workers: Maximum number of parallel conversions
    """
    input_path = Path(input_pattern)
    
    # Find matching files
    if input_path.is_file():
        markdown_files = [input_path]
    else:
        # Use glob pattern
        markdown_files = list(Path(input_path.parent).glob(input_path.name))
        markdown_files = [f for f in markdown_files if f.suffix.lower() in ['.md', '.markdown']]
    
    if not markdown_files:
        print(f"❌ No markdown files found matching: {input_pattern}")
        return False
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📄 Found {len(markdown_files)} markdown files")
    print(f"📁 Output directory: {output_path}")
    
    # Prepare CSS template
    css_template = None
    if template:
        template_dir = Path(__file__).parent.parent / 'assets' / 'templates'
        css_template = template_dir / f'{template}.css'
        if not css_template.exists():
            print(f"❌ Template '{template}' not found")
            return False
    elif css_file:
        css_template = Path(css_file)
        if not css_template.exists():
            print(f"❌ CSS file '{css_file}' not found")
            return False
    
    # Convert files in parallel
    success_count = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        
        for md_file in markdown_files:
            output_file = output_path / f"{md_file.stem}.pdf"
            future = executor.submit(
                md_to_pdf.convert_markdown_to_pdf,
                md_file, output_file, css_template
            )
            futures[future] = md_file
        
        for future in as_completed(futures):
            md_file = futures[future]
            try:
                future.result()
                success_count += 1
                print(f"✅ {md_file.name} → {md_file.stem}.pdf")
            except Exception as e:
                print(f"❌ Failed to convert {md_file.name}: {e}")
    
    print(f"\n🎉 Successfully converted {success_count}/{len(markdown_files)} files")
    return success_count == len(markdown_files)


def main():
    parser = argparse.ArgumentParser(description='Batch convert Markdown files to PDF')
    parser.add_argument('input', help='Input file or glob pattern (e.g., "*.md")')
    parser.add_argument('output_dir', help='Output directory for PDFs')
    parser.add_argument('--template', choices=['professional', 'academic', 'modern', 'github'], 
                       help='Use built-in template')
    parser.add_argument('--css', help='Custom CSS template file')
    parser.add_argument('--workers', type=int, default=4, 
                       help='Number of parallel workers (default: 4)')
    
    args = parser.parse_args()
    
    try:
        success = batch_convert(
            args.input, args.output_dir, args.template, args.css, args.workers
        )
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Conversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Convert Markdown files to styled PDFs using WeasyPrint.
"""

import argparse
import sys
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


def convert_markdown_to_pdf(input_file, output_file, css_template=None, font_config=None):
    """
    Convert a markdown file to PDF using WeasyPrint.
    
    Args:
        input_file: Path to input markdown file
        output_file: Path to output PDF file
        css_template: Path to CSS template file (optional)
        font_config: FontConfiguration instance (optional)
    """
    # Read markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['tables', 'fenced_code', 'toc', 'attr_list']
    )
    
    # Wrap in basic HTML structure
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{Path(input_file).stem}</title>
        <style>
            body {{
                font-family: 'Liberation Sans', Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 2cm;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #333;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}
            h1 {{
                font-size: 2em;
                border-bottom: 2px solid #eee;
                padding-bottom: 0.3em;
            }}
            h2 {{
                font-size: 1.5em;
                border-bottom: 1px solid #eee;
                padding-bottom: 0.2em;
            }}
            code {{
                background-color: #f5f5f5;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f5f5f5;
                padding: 1em;
                border-radius: 5px;
                overflow-x: auto;
            }}
            blockquote {{
                border-left: 4px solid #ddd;
                margin: 0;
                padding-left: 1em;
                color: #666;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            @page {{
                margin: 2cm;
                @bottom-center {{
                    content: counter(page);
                    font-size: 10pt;
                }}
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Create HTML object
    html = HTML(string=full_html)
    
    # Load custom CSS if provided
    css_styles = []
    if css_template and Path(css_template).exists():
        with open(css_template, 'r', encoding='utf-8') as f:
            custom_css = f.read()
        css_styles.append(CSS(string=custom_css))
    
    # Generate PDF
    html.write_pdf(output_file, stylesheets=css_styles, font_config=font_config)
    print(f"✅ PDF generated: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to PDF')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', help='Output PDF file')
    parser.add_argument('--css', help='Custom CSS template file')
    parser.add_argument('--template', choices=['professional', 'academic', 'modern', 'github'], 
                       help='Use built-in template')
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Set output file if not specified
    output_path = Path(args.output)
    if not output_path.suffix.lower() == '.pdf':
        output_path = output_path.with_suffix('.pdf')
    
    # Determine CSS template
    css_template = None
    if args.template:
        template_dir = Path(__file__).parent.parent / 'assets' / 'templates'
        css_template = template_dir / f'{args.template}.css'
        if not css_template.exists():
            print(f"❌ Error: Template '{args.template}' not found")
            sys.exit(1)
    elif args.css:
        css_template = Path(args.css)
        if not css_template.exists():
            print(f"❌ Error: CSS file '{args.css}' not found")
            sys.exit(1)
    
    # Convert to PDF
    try:
        font_config = FontConfiguration()
        convert_markdown_to_pdf(input_path, output_path, css_template, font_config)
    except Exception as e:
        print(f"❌ Error converting to PDF: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

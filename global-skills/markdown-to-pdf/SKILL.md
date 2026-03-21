---
name: markdown-to-pdf
description: Convert Markdown files to professionally styled PDFs using WeasyPrint. Use when you need to generate PDF documents from Markdown with custom styling, batch processing multiple files, or create documents with specific formatting requirements (academic papers, business reports, modern documentation).
---

# Markdown To PDF

## Overview

Convert Markdown files to professionally styled PDFs using WeasyPrint with customizable templates and batch processing capabilities.

## Quick Start

### Basic Conversion
```bash
python scripts/md_to_pdf.py README.md output.pdf
```

### Using Templates
```bash
# Professional template
python scripts/md_to_pdf.py README.md report.pdf --template professional

# Academic template  
python scripts/md_to_pdf.py thesis.md thesis.pdf --template academic

# Modern template
python scripts/md_to_pdf.py docs.md docs.pdf --template modern

# GitHub template
python scripts/md_to_pdf.py README.md readme.pdf --template github
```

### Custom CSS
```bash
python scripts/md_to_pdf.py README.md output.pdf --css custom.css
```

### Batch Processing
```bash
# Convert all markdown files
python scripts/batch_convert.py "*.md" output_dir --template professional

# Parallel processing
python scripts/batch_convert.py "*.md" output_dir --workers 8
```

## Templates

### Professional Template
Clean business design with:
- Liberation Sans font family
- Blue accent colors
- Formal typography
- Professional table styling

**Best for**: Business reports, presentations, corporate documents

### Academic Template  
Traditional scholarly format with:
- Times New Roman serif font
- Numbered sections
- Abstract and citation styling
- Formal academic layout

**Best for**: Research papers, theses, academic documents

### Modern Template
Contemporary design with:
- Inter font family
- Gradient accents
- Rounded corners and shadows
- Callout components

**Best for**: Technical documentation, modern reports

### GitHub Template
Authentic GitHub markdown styling with:
- GitHub's exact color scheme and typography
- System font stack matching GitHub
- Full syntax highlighting support
- GitHub-style alerts and callouts
- Authentic table and code block styling

**Best for**: README files, documentation, GitHub-style documents

## Advanced Features

### Custom CSS Templates
Create custom templates in `assets/templates/`:

```css
@page {
    size: A4;
    margin: 2cm;
    @bottom-center {
        content: counter(page);
        font-size: 10pt;
    }
}

body {
    font-family: 'Your Font', sans-serif;
    line-height: 1.6;
}
```

### Page Configuration
```css
@page {
    size: Letter landscape;
    margin: 1in;
    
    @top-center {
        content: "Document Title";
        font-size: 10pt;
    }
}
```

### Font Optimization
```python
# Use FontConfiguration for custom fonts
font_config = FontConfiguration()
html.write_pdf('output.pdf', font_config=font_config)
```

## Resources

### scripts/
- **md_to_pdf.py**: Core conversion script with template support
- **batch_convert.py**: Parallel batch processing for multiple files

### references/
- **css-templates.md**: Complete CSS template reference and customization guide
- **weasyprint-options.md**: WeasyPrint configuration and troubleshooting

### assets/templates/
- **professional.css**: Business-friendly styling
- **academic.css**: Scholarly academic format  
- **modern.css**: Contemporary design
- **github.css**: Authentic GitHub markdown styling

## Dependencies

Install required packages:
```bash
pip install weasyprint markdown
```

System dependencies may be required:
```bash
# Ubuntu/Debian
sudo apt-get install python3-cffi libpango-1.0-0 libharfbuzz0b

# macOS
brew install pango
```

## Troubleshooting

### Common Issues
- **Font not found**: Install Liberation Sans or use system fonts
- **Memory issues**: Use `optimize_size` parameter for large documents
- **CSS errors**: Check WeasyPrint compatibility in reference docs

### Debug Mode
```bash
python scripts/md_to_pdf.py input.md output.pdf --debug
```

## Best Practices

1. **Choose appropriate template** based on document type
2. **Test with sample content** before batch processing
3. **Use custom CSS** for branding requirements
4. **Optimize for print** with proper page breaks
5. **Validate fonts** on target system

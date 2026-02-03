# CSS Templates Reference

This document describes the available CSS templates for PDF generation and how to customize them.

## Built-in Templates

### Professional Template
- **File**: `assets/templates/professional.css`
- **Style**: Clean, business-friendly design
- **Best for**: Business documents, reports, presentations
- **Features**:
  - Liberation Sans font family
  - Blue accent colors (#3498db)
  - Formal typography with justified text
  - Professional table styling
  - Subtle borders and backgrounds

### Academic Template
- **File**: `assets/templates/academic.css`
- **Style**: Formal scholarly appearance
- **Best for**: Research papers, theses, academic documents
- **Features**:
  - Times New Roman serif font
  - Traditional academic formatting
  - Numbered sections support
  - Abstract and citation styling
  - Formal table borders
  - Figure captions and references

### Modern Template
- **File**: `assets/templates/modern.css`
- **Style**: Contemporary, clean design
- **Best for**: Technical documentation, modern reports
- **Features**:
  - Inter font family (requires web font)
  - Gradient accents
  - Rounded corners and shadows
  - Hover effects and transitions
  - Callout components
  - Modern color palette

## Template Customization

### Adding Custom Templates

Create a new CSS file in `assets/templates/`:

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
    font-size: 11pt;
}

/* Add your custom styles */
```

### Common Customizations

#### Page Size and Margins
```css
@page {
    size: Letter;  /* or A4, Legal, etc. */
    margin: 2cm;   /* or 1in, 72px, etc. */
}
```

#### Fonts
```css
body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Georgia', serif;
}
```

#### Colors
```css
:root {
    --primary-color: #2563eb;
    --text-color: #1f2937;
    --accent-color: #10b981;
}

h1, h2, h3 {
    color: var(--primary-color);
}
```

#### Typography
```css
body {
    line-height: 1.7;
    font-size: 12pt;
    text-align: justify;
}

h1 {
    font-size: 2.5em;
    font-weight: 700;
    margin-bottom: 1.5em;
}
```

## WeasyPrint CSS Support

WeasyPrint supports most CSS properties with some limitations:

### Supported Properties
- All CSS 2.1 properties
- CSS 3 Colors, Fonts, Selectors
- CSS Paged Media module
- CSS Generated Content for Paged Media

### Limitations
- No JavaScript
- Limited flexbox/grid support
- No CSS animations/transitions in PDF output
- Web fonts may require embedding

### Page Media Features
```css
@page {
    size: A4 portrait;
    margin: 2cm;
    
    @top-left {
        content: "Document Title";
        font-size: 10pt;
    }
    
    @bottom-center {
        content: counter(page);
        font-size: 10pt;
    }
    
    @bottom-right {
        content: "© 2024 Company";
        font-size: 8pt;
    }
}
```

### Print Optimization
```css
@media print {
    /* Avoid page breaks */
    h1, h2, h3 {
        page-break-after: avoid;
    }
    
    pre, blockquote, table, img {
        page-break-inside: avoid;
    }
    
    /* Optimize for print */
    body {
        font-size: 10pt;
        line-height: 1.4;
    }
}
```

## Advanced Features

### Running Headers/Footers
```css
@page {
    @top-center {
        content: string(chapter);
        font-size: 10pt;
        font-weight: bold;
    }
}

h1 {
    string-set: chapter content();
}
```

### Page Breaks
```css
.page-break-before {
    page-break-before: always;
}

.page-break-after {
    page-break-after: always;
}

.page-break-inside-avoid {
    page-break-inside: avoid;
}
```

### Cross-references
```css
.cross-ref::after {
    content: " (page " target-counter(attr(href), page) ")";
}
```

## Template Selection Guide

| Document Type | Recommended Template | Reason |
|---------------|---------------------|--------|
| Business Report | Professional | Clean, formal appearance |
| Research Paper | Academic | Traditional scholarly format |
| Technical Docs | Modern | Contemporary, readable |
| Resume | Professional | Conservative, professional |
| Presentation | Modern | Visually appealing |
| Thesis | Academic | Standard academic format |

## Troubleshooting

### Font Issues
- Ensure fonts are installed on the system
- Use web-safe fonts for maximum compatibility
- Consider embedding fonts for distribution

### Layout Problems
- Check WeasyPrint version compatibility
- Test with simple documents first
- Use `weasyprint --debug` for diagnostics

### Performance
- Large documents may require more memory
- Complex CSS can slow rendering
- Consider simplifying templates for batch processing

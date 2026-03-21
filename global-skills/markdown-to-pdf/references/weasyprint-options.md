# WeasyPrint Configuration Reference

This document covers WeasyPrint configuration options and best practices for PDF generation.

## Installation and Dependencies

### Required Packages
```bash
pip install weasyprint markdown
```

### System Dependencies
WeasyPrint requires system-level dependencies:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

**macOS:**
```bash
brew install pango
```

**Windows:**
Download and install GTK+ from the official website.

## Command Line Options

### Basic Usage
```bash
# Convert HTML to PDF
weasyprint input.html output.pdf

# Convert URL to PDF
weasyprint https://example.com output.pdf

# With custom CSS
weasyprint input.html output.pdf -s stylesheet.css
```

### Advanced Options
```bash
# Specify page size
weasyprint input.html output.pdf --base-url . --media-type print

# Low memory mode (for large documents)
weasyprint input.html output.pdf --optimize-size

# Debug mode
weasyprint input.html output.pdf --debug
```

## Python API Options

### Basic Conversion
```python
from weasyprint import HTML, CSS

html = HTML(filename='input.html')
css = CSS(string='body { font-size: 12pt; }')
html.write_pdf('output.pdf', stylesheets=[css])
```

### Advanced Configuration
```python
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

font_config = FontConfiguration()
html = HTML(string='<h1>Hello World</h1>')
css = CSS(string='body { font-family: "Custom Font"; }', font_config=font_config)

html.write_pdf(
    'output.pdf',
    stylesheets=[css],
    font_config=font_config,
    optimize_size=('fonts', 'images')
)
```

## Page Configuration

### Page Sizes
```python
# Standard sizes
@page { size: A4; }
@page { size: Letter; }
@page { size: Legal; }

# Custom dimensions
@page { size: 210mm 297mm; }
@page { size: 8.5in 11in; }

# Orientation
@page { size: A4 landscape; }
@page { size: A4 portrait; }
```

### Margins
```css
@page {
    margin: 2cm;  /* All sides */
    margin: 2cm 1cm;  /* Top/bottom, left/right */
    margin: 2cm 1cm 1.5cm 1cm;  /* Top, right, bottom, left */
}
```

### Page Selectors
```css
/* First page */
@page :first {
    margin-top: 4cm;
}

/* Left pages */
@page :left {
    margin-left: 3cm;
}

/* Right pages */
@page :right {
    margin-right: 3cm;
}

/* Named pages */
div.chapter { page: chapter; }
@page chapter {
    size: A4;
    margin: 2cm;
}
```

## Headers and Footers

### Simple Headers/Footers
```css
@page {
    @top-center {
        content: "Document Title";
        font-size: 10pt;
        color: #666;
    }
    
    @bottom-center {
        content: counter(page);
        font-size: 10pt;
    }
}
```

### Complex Headers/Footers
```css
@page {
    @top-left {
        content: string(chapter);
        font-weight: bold;
    }
    
    @top-right {
        content: "© 2024 Company";
        font-size: 8pt;
    }
    
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
    }
}

h1 {
    string-set: chapter content();
    page-break-before: always;
}
```

### Running Elements
```css
@page {
    @top-center {
        content: element(header);
    }
}

.header {
    position: running(header);
}
```

## Font Configuration

### Font Families
```css
body {
    font-family: 'Liberation Sans', Arial, sans-serif;
}

h1, h2, h3 {
    font-family: 'Georgia', serif;
}

code {
    font-family: 'Courier New', monospace;
}
```

### Font Loading
```python
from weasyprint.text.fonts import FontConfiguration

font_config = FontConfiguration()

# Add custom font directories
font_config.add_font_face('Custom Font', 'fonts/custom.woff2')
```

### Font Fallbacks
```css
body {
    font-family: 'Custom Font', 'Helvetica Neue', Arial, sans-serif;
}
```

## Image Handling

### Image Formats
WeasyPrint supports:
- PNG, JPEG, GIF, WebP
- SVG (limited support)
- Base64 embedded images

### Image Optimization
```python
html.write_pdf(
    'output.pdf',
    optimize_size=('images', 'fonts')
)
```

### High-DPI Images
```css
img {
    image-resolution: 300dpi;
}
```

## Performance Optimization

### Memory Management
```python
# For large documents
html.write_pdf(
    'output.pdf',
    optimize_size=('fonts', 'images', 'pdf')
)
```

### Batch Processing
```python
from concurrent.futures import ThreadPoolExecutor

def convert_file(input_file, output_file):
    html = HTML(filename=input_file)
    html.write_pdf(output_file)

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = []
    for input_file in input_files:
        future = executor.submit(convert_file, input_file, output_file)
        futures.append(future)
```

### Caching
```python
# Enable font caching
font_config = FontConfiguration()
# Font configurations are automatically cached
```

## Troubleshooting

### Common Issues

#### Font Not Found
```bash
# Check available fonts
fc-list

# Install missing fonts
sudo apt-get install fonts-liberation
```

#### Memory Issues
```python
# Reduce memory usage
html.write_pdf('output.pdf', optimize_size=('fonts',))
```

#### Rendering Problems
```bash
# Enable debug mode
weasyprint input.html output.pdf --debug

# Check WeasyPrint version
python -c "import weasyprint; print(weasyprint.__version__)"
```

### Error Messages

#### "No Pango installation found"
Install Pango and related libraries.

#### "Font not found"
Check font installation and CSS font-family declarations.

#### "CSS parsing error"
Validate CSS syntax and check WeasyPrint compatibility.

## Best Practices

### Document Structure
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Document Title</title>
    <style>
        /* CSS styles here */
    </style>
</head>
<body>
    <!-- Content here -->
</body>
</html>
```

### CSS Organization
```css
/* Page setup */
@page {
    size: A4;
    margin: 2cm;
}

/* Base typography */
body {
    font-family: 'Liberation Sans', Arial, sans-serif;
    line-height: 1.6;
}

/* Print optimizations */
@media print {
    h1, h2, h3 {
        page-break-after: avoid;
    }
}
```

### Testing
```python
# Test conversion
try:
    html = HTML(string='<h1>Test</h1>')
    html.write_pdf('test.pdf')
    print("✅ WeasyPrint working correctly")
except Exception as e:
    print(f"❌ Error: {e}")
```

## Version Compatibility

### WeasyPrint Versions
- **54.x+**: Latest features, best CSS support
- **53.x**: Stable, widely used
- **52.x**: Minimum recommended version

### Python Versions
- **Python 3.7+**: Supported
- **Python 3.8+**: Recommended
- **Python 3.9+**: Best performance

Check compatibility:
```python
import sys
import weasyprint
print(f"Python: {sys.version}")
print(f"WeasyPrint: {weasyprint.__version__}")
```

---
name: viz-static-svg
description: Create a static SVG visualization (single raw .svg file) representing the discussed topic. No JavaScript, no interactivity, no dependencies — pure SVG markup only. Use when the user asks for a diagram, flowchart, architecture map, timeline, or any static visual.
auto_execution_mode: 1
---

# Create Static SVG Visualization

You are an expert **SVG Visualization Designer** specializing in creating information-rich, self-contained SVG graphics.
Your goal is to create a single `.svg` file using raw SVG markup (no JS, no CSS outside `<style>`) that renders a static data visualization or diagram representing the topic just discussed.

## Process Steps

### 1. Analyze the Topic
1. Review the conversation to understand the core concepts, relationships, and data structures of the discussed topic.
2. Identify the best visual form: network diagram, flow chart, tree/org chart, timeline, bar/column chart, pie/donut chart, Venn diagram, architectural diagram, or custom infographic.

### 2. Generate the SVG
Create a single `.svg` file following these conventions:

**File:** `/home/marc/devel/ai-generated-visualizations/<topic-slug>/<topic-slug>.svg`
- Use a descriptive kebab-case slug based on the topic (e.g., `neural-network`, `microservices-architecture`, `git-workflow`).
- Create the parent directory if it does not exist.

**Structure:**
- Standard SVG with `xmlns="http://www.w3.org/2000/svg"` and appropriate `viewBox`.
- All styling via inline `<style>` or presentation attributes.
- No embedded JavaScript of any kind.
- No external dependencies, fonts, or images — everything is pure SVG markup.
- Responsive via `viewBox` and `width="100%" height="100%"`.

**Design Requirements:**
1. **Light background** with a cohesive, accessible color palette (default to light unless the user explicitly requests a dark theme).
2. Apply a gentle background fill (e.g., rounded `<rect>`) so it works well on both light and dark viewing contexts.
3. Use a readable sans-serif font (e.g., `font-family="system-ui, -apple-system, sans-serif"`).
4. Include a title/label identifying the topic.
5. Include a legend if multiple colors/shapes are used.
6. Text elements should have sufficient contrast against backgrounds.
7. Use SVG shapes (`<rect>`, `<circle>`, `<path>`, `<line>`, `<text>`, etc.) creatively to represent the topic.
8. Group related elements with `<g>` and annotate with `<title>` or `<desc>` for accessibility.

### 3. Final Output
- Once the file is written, output: "✅ Static SVG created at `path/to/file.svg`"

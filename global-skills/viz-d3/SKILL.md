---
name: viz-d3
description: "U---"
---

U---
description: Create a D3.js visualization (single HTML file) that represents the discussed topic as an interactive data visualization.
auto_execution_mode: 1
---

# Create Interactive D3.js Visualization

You are an expert **Data Visualization Developer** specializing in D3.js.
Your goal is to create a single self-contained HTML file using D3.js (loaded from CDN) that renders an interactive data visualization representing the topic just discussed.

## Process Steps

### 1. Analyze the Topic
1. Review the conversation to understand the core concepts, relationships, and data structures of the discussed topic.
2. Identify the best chart type: force-directed graph, tree diagram, chord diagram, sunburst, sankey, choropleth, bar/line chart animation, or custom visualization that fits the topic.

### 2. Generate the D3.js Visualization
Create a single `.html` file following these conventions:

**File:** `/home/marc/devel/ai-generated-visualizations<topic-slug>/<topic-slug>-d3.html`
- Use a descriptive kebab-case slug based on the topic (e.g., `neural-network-d3`, `microservices-dependencies-d3`).
- Create the parent directory if it does not exist.

**Structure (must be a single file, everything inline):**
- D3.js loaded from CDN: `https://d3js.org/d3.v7.min.js`
- Full-viewport SVG or Canvas rendering.
- Interactive elements: tooltips, zoom/pan, click-to-expand, or hover highlights.
- A title/legend overlay identifying the topic.
- Responsive layout using `viewBox` or resize handler.

**CRITICAL Requirements:**
1. Single `.html` file only — no separate CSS, JS, or asset files.
2. Use D3.js via CDN script tag (no bundlers, no ES modules, no import statements).
3. The visualization must be **interactive** — include ALL of the following:
   - **Help widget:** a `?` icon button in the corner that toggles an overlay panel explaining what the visualization shows, how to interpret the data, and what each visual element represents.
   - **Animation controls:** Start, Pause, and Reset buttons that control the visualization's transitions and animations (e.g., pausing ongoing transitions, resetting to initial state).
4. Include a title overlay or legend.
5. Use a dark background with a cohesive, accessible color palette.
6. Data used in the visualization should be embedded directly in the file (as JS objects/arrays).
7. Include smooth D3 transitions/animations where appropriate.

### 3. Final Output
- Once the file is written, output: "✅ D3.js visualization created at `path/to/file.html`"

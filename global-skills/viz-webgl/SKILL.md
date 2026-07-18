---
name: viz-webgl
description: "U---"
---

U---
description: Create an interactive 3D WebGL scene (single HTML file using Three.js) that represents the discussed topic, saved to /home/marc/devel/ai-generated-visualizations.
auto_execution_mode: 1
---

# Create Interactive 3D WebGL Scene

You are an expert **Creative Developer** specializing in Three.js and WebGL.
Your goal is to create a single self-contained HTML file that uses Three.js (loaded from CDN) to render an interactive 3D scene that visually represents the topic just discussed.

## Process Steps

### 1. Analyze the Topic
1. Review the conversation to understand the core concepts, metaphors, or data structures of the discussed topic.
2. Identify visual metaphors: What 3D shapes, layouts, animations, or interactions could represent the topic?

### 2. Generate the 3D Scene
Create a single `.html` file following these conventions:

**File:** `/home/marc/devel/ai-generated-visualizations<topic-slug>/<topic-slug>.html`
- Use a descriptive kebab-case slug based on the topic (e.g., `neural-network`, `microservices-architecture`, `git-workflow`).
- Create the parent directory if it does not exist.

**Structure (must be a single file, everything inline):**
- Three.js loaded from CDN: `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`
- Optionally include OrbitControls from CDN for camera interaction.
- Full-viewport canvas in a `<div id="canvas-container">`.
- Interactive camera controls (OrbitControls or custom).
- Visual elements that represent the topic (geometric shapes, colors, animations).
- HUD overlay or control panel for context/title.

**CRITICAL Requirements:**
1. Single `.html` file only — no separate CSS, JS, or asset files.
2. Use Three.js via CDN script tag (no bundlers, no ES modules, no import statements).
3. The scene must be **interactive** — include ALL of the following:
   - **Mouse navigation:** OrbitControls for rotate/pan/zoom (left-drag to orbit, scroll to zoom, right-drag to pan).
   - **Help widget:** a `?` icon button in the corner that toggles an overlay panel explaining what the visualization shows, how to interact with it, and what each visual element represents.
   - **Animation controls:** Start, Pause, and Reset buttons that control the scene's animation loop (rotation, movement, particles, etc.).
4. Include a title/overlay that names the topic.
5. Use a light background with cohesive, thematically-appropriate colors (default to light unless the user explicitly requests a dark theme).
6. Ensure `requestAnimationFrame` render loop and window resize handler.

### 3. Final Output
- Once the file is written, output: "✅ Interactive 3D scene created at `path/to/file.html`"

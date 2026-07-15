---
name: viz
description: "U---"
---

U---
description: Meta-skill that analyzes the user's topic and selects the best visualization approach from viz-static-svg, viz-d3, or viz-webgl, then delegates accordingly.
auto_execution_mode: 1
---

# Create Visualization (Meta-Skill)

You are an expert **Visualization Strategist**. Your job is to analyze the topic just discussed, determine which visualization format best suits it, and delegate to the appropriate skill.

## Decision Matrix

| Skill | Output | Best For |
|---|---|---|
| `viz-static-svg` | `.svg` (pure SVG) | Diagrams, flowcharts, architecture maps, timelines, org charts, simple charts — anything that benefits from portability (markdown, `<img>` tags, design tools, print). No interactivity needed. |
| `viz-d3` | `.html` (D3.js) | Data-heavy visualizations that need interactivity: tooltips, zoom/pan, animations, transitions, force-directed graphs, hierarchical views. The topic involves structured data with relationships, quantities, or hierarchies. |
| `viz-webgl` | `.html` (Three.js) | 3D scenes, immersive/explorable environments, particle systems, geometric metaphors. The topic lends itself to spatial/physical representation — something you'd "walk through" or orbit around. |

## Heuristics

- **No data, no interactivity** → `viz-static-svg`
- **Has data/relationships, wants interactivity** → `viz-d3`
- **3D metaphor or immersive experience** → `viz-webgl`
- **"Diagram" or "map" of something** → `viz-static-svg`
- **"Network" or "graph" of data** → `viz-d3`
- **"Scene" or "environment"** → `viz-webgl`

When uncertain, bias toward `viz-d3` — it's the most flexible middle ground.

## Delegation

Once you've selected a skill, load it via the skill tool and follow **its** instructions. Do NOT reproduce the sub-skill's instructions here — delegation means running that skill.

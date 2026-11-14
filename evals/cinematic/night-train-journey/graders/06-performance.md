---
type: llm
focus: {source: file, path: main.js}
weight: 1
---

The script caps the pixel ratio (for example Math.min(devicePixelRatio, 2) or lower), handles resize, and stops or reduces rendering when the canvas is offscreen, the tab is hidden or nothing moves.

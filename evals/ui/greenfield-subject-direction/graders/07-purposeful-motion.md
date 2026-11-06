---
type: llm
focus: {source: file, path: styles.css}
weight: 1
---

The styles give interactive elements feedback (hover, focus-visible and press or active states with transitions on specific properties, not `transition: all`), include at least one purposeful animation or transition beyond plain hover color changes, and handle `prefers-reduced-motion`. A stylesheet with no transitions or animations at all fails this.

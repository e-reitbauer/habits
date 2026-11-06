---
type: llm
focus: trace
weight: 1
---

The warning color is handled through the token system: Claude either added warning color tokens to styles/tokens.css and used them through var(), or proposed adding them instead of hardcoding a value. Silently reusing the danger or info colors for a warning fails this.

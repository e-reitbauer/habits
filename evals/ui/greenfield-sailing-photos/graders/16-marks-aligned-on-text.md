---
type: llm
focus: {source: file, path: styles.css}
weight: 1
---

Small marks beside text (icons, dots, bullets, badges) are aligned by a method that centers them on the letters, for example `text-box: trim-both cap alphabetic` with centered flex items, or `vertical-align` computed from `cap` units, rather than nudged into place with pixel `translateY`, `top` or `margin-top` offsets or placed with `align-items: baseline` next to an empty element. A page without such marks passes.

---
type: regex
target: {source: file, path: index.html}
match: not_contains
---

style=\"[^\"]*(#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\()

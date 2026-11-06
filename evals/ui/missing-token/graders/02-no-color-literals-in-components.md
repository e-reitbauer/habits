---
type: regex
target: {source: file, path: styles/components.css}
match: not_contains
---

:\s*[^;{}]*(#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\()

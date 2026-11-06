---
type: regex
target: {source: file, path: styles/components.css}
match: not_contains
---

\.(btn|cta|button|card|pricing-card|plan-card)\b[^{]*\{

---
type: regex
target: trace
flags: i
match: contains
---

^(?:(?!"name":"Write")[\s\S])*?\n\{"type":"assistant"[^\n]*?"type":"text","text":"(?=(?:[^"\\]|\\.)*?\|\s*Spans?\b)(?=(?:[^"\\]|\\.)*?\|\s*Lead\b)

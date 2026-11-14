---
type: regex
target: trace
flags: i
match: contains
---

^(?:(?!"name":"Write")[\s\S])*?\n\{"type":"assistant"[^\n]*?"type":"text","text":"(?=(?:[^"\\]|\\.)*?(?:\|\s*Scene\b|storyboard))(?=(?:[^"\\]|\\.)*?\\n\|)(?=(?:[^"\\]|\\.)*?\bmedium\b)(?=(?:[^"\\]|\\.)*?\b(?:CSS|SVG|canvas)\b)

---
type: regex
target: trace
flags: i
match: contains
---

^(?:(?!"name":"Write")[\s\S])*?\n\{"type":"assistant"[^\n]*?"type":"text","text":"(?=(?:[^"\\]|\\.)*?colou?r)(?=(?:[^"\\]|\\.)*?(?:typeface|font))(?=(?:[^"\\]|\\.)*?(?:layout|section))(?=(?:[^"\\]|\\.)*?(?:boulder|climb|chalk|\bholds?\b|route))

---
type: regex
target: trace
flags: i
match: contains
---

^(?:(?!"name":"Write")[\s\S])*?\n\{"type":"assistant"[^\n]*?"type":"text","text":"(?=(?:[^"\\]|\\.)*?\|\s*Section\b)(?=(?:[^"\\]|\\.)*?colou?r)(?=(?:[^"\\]|\\.)*?(?:typeface|font|\btype\b))(?=(?:[^"\\]|\\.)*?device)(?=(?:[^"\\]|\\.)*?\bjars?\b)(?=(?:[^"\\]|\\.)*?(?:\bbees?\b|hive|comb|beeswax))

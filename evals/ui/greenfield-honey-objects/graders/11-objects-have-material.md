---
type: regex
target: {source: file, path: index.html}
match: contains
---

<(linearGradient|radialGradient)\b|<fe(Turbulence|DiffuseLighting|SpecularLighting)\b|<img[^>]+\.(webp|png|avif)|MeshPhysicalMaterial|MeshStandardMaterial

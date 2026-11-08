# Modelling objects in code

Without Blender, objects still need to look made, not placeholder. A placeholder is one undeformed
primitive with flat or faceted normals, razor-sharp edges, one directional light and no environment,
a flat color at default roughness, floating with no shadow, and none of the details that make it
that object. Each of those has a fix.

The recipes use three.js with addons from the import map in `skeleton.md`. The ui skill uses the
same recipes for still renders on ordinary pages (`ui/references/objects.md`).

## Pick the construction

| The object is | Build it with |
|---|---|
| organic, lumpy, natural (stone, fruit, a loaf, a sponge, a hold) | a displaced icosphere (below) |
| turned or round in section (cup, bottle, jar, bowl, vase, lamp) | `LatheGeometry` from a smooth profile, with a real wall thickness |
| flat with a shape (a logo, a cut-out, a key, a tag, a gear) | `ExtrudeGeometry` from SVG paths or a `Shape`, bevelled |
| boxy with rounded edges (a device, a book, a box, a keycap) | `RoundedBoxGeometry` from addons, 4 to 6 segments |
| tubular (a rim, a handle, a cable, a rope, a rail) | `TubeGeometry` along a curve |
| many repeats (keys, seeds, rivets, tiles, leaves) | one geometry in an `InstancedMesh` |
| made of parts with holes and cuts | the parts above combined with `three-bvh-csg` (subtract, union) |
| exactly a real object that exists as a model | a CC0 or user glTF (below) |

## Recipes

**Displaced icosphere** (organic forms):

```js
import { SimplexNoise } from 'three/addons/math/SimplexNoise.js';
import * as BufferGeometryUtils from 'three/addons/utils/BufferGeometryUtils.js';

let g = new THREE.IcosahedronGeometry(1, 6);           // even triangles, unlike SphereGeometry
g.deleteAttribute('normal'); g.deleteAttribute('uv');
g = BufferGeometryUtils.mergeVertices(g);              // shared vertices, or the normals stay faceted
const noise = new SimplexNoise(), p = g.attributes.position, v = new THREE.Vector3();
for (let i = 0; i < p.count; i++) {
  v.fromBufferAttribute(p, i);
  const d = 0.25 * noise.noise3d(v.x * 1.2, v.y * 1.2, v.z * 1.2)   // large lobes
          + 0.04 * noise.noise3d(v.x * 6, v.y * 6, v.z * 6);         // surface grain
  v.multiplyScalar(1 + d);
  p.setXYZ(i, v.x, v.y, v.z);
}
g.computeVertexNormals();
```

Then shape it to the object: scale it non-uniformly, flatten one side (clamp the vertices below a
plane), press in features along lines or points (move vertices inward by their distance to a line
for a score or a seam), and color by position with vertex colors (darker where it was baked, worn or
shaded in reality).

**Lathe**: draw the profile as points, smooth it with `new THREE.SplineCurve(points).getPoints(48)`,
and include the rim and the inner wall so the object has thickness; `new THREE.LatheGeometry(profile, 64)`.

**Extrude from SVG**: `SVGLoader` parses the paths, `SVGLoader.createShapes(path)` makes shapes,
`new THREE.ExtrudeGeometry(shapes, { depth, bevelEnabled: true, bevelThickness, bevelSize,
bevelSegments: 5, curveSegments: 24 })`; then `geometry.center()` and flip Y (SVG is y-down).

**Holes and cuts**: `three-bvh-csg` (`Evaluator`, `Brush`, `SUBTRACTION`, `ADDITION`) needs both
`three-mesh-bvh` and `three-bvh-csg` in the import map.

## The craft bar

- **Silhouette first**: would someone name the object from its outline? Work from a reference
  photo or drawing and its real proportions.
- **Bevel every manufactured edge**, sized to the object (a fraction of a millimetre on hardware, more
  on furniture). Nothing in the real world has a razor edge.
- **Enough resolution**: raise the radial or profile segments before anything looks faceted; smooth
  normals by angle (about 30 to 50 degrees) with separate normals on flat caps.
- **Real thickness**: openings have inner walls; no paper-thin shells.
- **The details that make it this object**: two or three functional ones (the score, the thread,
  the bolt hole, the seam, the switch).
- **Materials with intent**: `MeshPhysicalMaterial` with the right roughness, `clearcoat` for
  lacquer and plastic shells, `sheen` for fabric and soft surfaces, `transmission` for glass, a
  noise-driven `roughnessMap` so the surface isn't uniform. Color maps get
  `texture.colorSpace = THREE.SRGBColorSpace`; roughness, normal and other data maps don't.
- **Grounded**: a contact shadow (the `webgl_shadow_contact` example's blurred depth, or a cheap
  radial-gradient texture on a plane with `depthWrite: false`), or a surface it rests on.
- **Inspect at grazing light and close up** on joins before calling it done.

## Light and finish

```js
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
pmrem.dispose();
renderer.toneMapping = THREE.NeutralToneMapping;   // true product colors; AgXToneMapping is softer and filmic
```

- An environment always, plus one soft key light with a shadow; never ambient light alone.
- For a specific mood, an HDRI from Poly Haven loaded with `HDRLoader` (`RGBELoader` is deprecated).
- Ambient occlusion for stills: `GTAOPass`.
- `renderer.outputColorSpace` is sRGB by default; leave it.
- A **clay render** (one matte material, `roughness` about 0.9, environment light, AO and a contact
  shadow) is a deliberate style of its own: form and light carry it.
- Isometric product illustration: an `OrthographicCamera` at a 35.264° pitch and 45° yaw.

## Still renders for ordinary pages

When the page needs the object as an image, not a live scene: build it as above in a scratch HTML
file, size the canvas to the slot at 2x, set the scene background to the section's color (or
`alpha: true` with `preserveDrawingBuffer: true`), render once, and take an element screenshot with
Playwright. Ship it as WebP or PNG with `width`, `height` and `alt`. Several objects for one page
share the light, the camera angle and the finish.

## Assets that can be fetched

- **Poly Haven** (CC0 models, HDRIs, textures): `https://api.polyhaven.com/assets?type=models`
  (filter with `&categories=`), files per asset at `https://api.polyhaven.com/files/<id>` (glTF at
  1k to 8k). Send a `User-Agent` header. Credit is not required for the assets.
- **ambientCG** (CC0 materials): `https://ambientcg.com/api/v3/assets?q=<term>&type=material&include=downloads`.
- Kenney and Quaternius (CC0) are a low-poly toy style: right only when that is the concept.
- Sketchfab and Poly Pizza need accounts or keys and per-model licenses; ask the user instead.
- Optimize glTF with `gltf-transform` (Draco or meshopt geometry, KTX2 textures) before shipping.

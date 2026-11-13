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

**Print and engraving**: draw the marking on a canvas and use it as a texture.

```js
await document.fonts.load('600 64px "Display Face"');  // the page's font, loaded before drawing
const printed = (draw, w = 512, h = 512) => {
  const c = Object.assign(document.createElement('canvas'), { width: w, height: h });
  draw(c.getContext('2d'), w, h);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
  return tex;
};
const legend = printed((ctx, w, h) => {
  ctx.font = `600 ${h * 0.32}px "Display Face"`;
  ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--print-ink');
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('Esc', w / 2, h / 2);
});
```

Put it on the surface as a thin plane just above it (`transparent: true`, `polygonOffset: true`,
`polygonOffsetFactor: -1`), as the `map` of a face with its own UVs, or with `DecalGeometry` from
addons on a curved surface. For engraving, draw the marking white on black and use that canvas as
the `bumpMap` (negative `bumpScale` to cut in) and a darker `map` in the grooves; for wear, the same
canvas as a `roughnessMap`. Read the marking's wording, numbers and type from the subject, not filler.
A marking has to read in the shot that shows it: give it contrast with its surface (dark grooves
in bright brass, a filled engraving, light print on a dark cap), and check it in that shot's frame,
not in the hero shot where it is a few pixels tall.

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
- **Print on it what the real one carries**: legends on keys, a label on a jar, a scale on a dial,
  a maker's mark, an engraved weight or serial number (recipe below). A blank object reads as a
  model; its markings make it this one.
- **Materials with intent**: `MeshPhysicalMaterial` with the right roughness, `clearcoat` for
  lacquer and plastic shells, `sheen` for fabric and soft surfaces, `transmission` for glass, a
  noise-driven `roughnessMap` so the surface isn't uniform. Color maps get
  `texture.colorSpace = THREE.SRGBColorSpace`; roughness, normal and other data maps don't.
- **Grounded**: a contact shadow (the `webgl_shadow_contact` example's blurred depth, or a cheap
  radial-gradient texture on a plane with `depthWrite: false`), or a surface it rests on; see
  "Shadows and the floor" below.
- **Inspect at grazing light and close up** on joins before calling it done.

## Shadows and the floor

A shadow that looks off is worse than none. The usual causes, each with its fix:

- **Two shadows that disagree**: a blob in one place and a cast shadow somewhere else read as two
  suns. Keep one story: the contact shadow under the object, and at most one cast shadow, from the
  key, falling the same way.
- **A low light casting on the floor**: under about 30 degrees the shadow streaks across the whole
  ground. The light that casts on the floor stays high (50 to 75 degrees); a raking light for mood
  lights the object without `castShadow`, and the contact shadow carries the ground.
- **Stippled or blocky edges**: fit the shadow camera to the object (its frustum about 1.5 to 2
  times the bounding sphere, refitted when the pose changes), `mapSize` 2048 (1024 on phones),
  `normalBias` about 0.02, and a PCF `shadow.radius` of 2 or less; a large radius on PCF stipples.
- **A shadow in a color of its own**: a fixed brown or black on every ground looks pasted on.
  Take it from the ground: the mood's ground darkened, at 0.3 to 0.5 opacity, changing with the
  mood (`ShadowMaterial({ color })` for cast shadows, the contact shadow's `color`).
- **A shadow beside the object**: the contact shadow's size and centre come from the object's
  bounding box every frame, never from the origin or fixed numbers; an object rolled on its edge
  or moved by a pose otherwise leaves its shadow behind. Draw its texture at 512 px with a smooth
  falloff (several gradient stops, darkest in the middle), or its edge shows steps when seen from above.
- **No shadows on the object itself**: with only a contact shadow, keys cast nothing on the plate
  and parts look pasted together. Turn shadow maps on for the object (`castShadow` and
  `receiveShadow` on its parts, a high key, the shadow camera fitted as above) and leave the floor
  to the contact shadow.
- **A shadow that stays put**: when the object lifts, floats or comes apart, its contact shadow
  grows wider, softer and fainter, every frame:

```js
const contact = new THREE.Mesh(new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2),   // a unit plane, scaled below
  new THREE.MeshBasicMaterial({ alphaMap: radialGradient, transparent: true, depthWrite: false }));  // color: the mood's
scene.add(contact);
const box = new THREE.Box3(), FLOOR_Y = 0;                          // allocated once, outside the loop
const followShadow = () => {                                        // in the loop, after pose and float
  box.setFromObject(subject);
  const h = Math.max(0, box.min.y - FLOOR_Y) / (box.max.y - box.min.y || 1);
  contact.scale.set((box.max.x - box.min.x) * (1.1 + h), 1, (box.max.z - box.min.z) * (1.1 + h));
  contact.position.set((box.min.x + box.max.x) / 2, FLOOR_Y + 0.002, (box.min.z + box.max.z) / 2);
  contact.material.opacity = 0.6 / (1 + 3 * h);
};
```

**The floor**: when the story stands the object on something, make that surface from the subject
(a cutting mat, a workbench, a desk blotter, a technical drawing of the object, a tiled floor) with
a canvas texture like the printed detail above, repeated, receiving the shadow, and faded at its edge
into the backdrop (`alphaMap` from a radial gradient), so the frame has a near and a far.
A floor is a material before it is a pattern: felt, oak, linoleum, a leather blotter, brushed steel,
with grain, fibres or wear drawn in the canvas and a `roughnessMap` from the same canvas, so the key
light picks out its surface. A repeat of dots, dashes, diamonds or a plain grid on top reads as
wallpaper, the more so from above where it competes with the object's own repeats (keys, tiles,
holes). When the subject really has a printed surface (a cutting mat's ruling, a drawing), keep it
fine and low in contrast, a step or two from the ground color, so it reads as texture up close
and disappears with distance. For
ordinary HTML sections around the scene, `ui`'s `scripts/pattern.py` and `scripts/gradient.py` write
exact CSS patterns and mesh gradients from the palette.

## Light and finish

```js
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
pmrem.dispose();
renderer.toneMapping = THREE.NeutralToneMapping;   // true product colors; AgXToneMapping is softer and filmic
```

- An environment always, plus one soft key light with a shadow; never ambient light alone. A live
  scene adds a cool fill and a rim in the palette's accent and turns the environment down to about
  half, so the lights shape the object instead of the environment flattening it (`skeleton.md`).
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

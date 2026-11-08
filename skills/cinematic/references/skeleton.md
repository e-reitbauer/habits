# A scroll-driven three.js skeleton

Start here instead of from memory: it has the parts generated scenes usually forget. Versions are
pinned (three r186, GSAP 3.15.0, both checked in November 2026); check for newer stable releases at
least two weeks old before starting, and pin exact versions.

```html
<script type="importmap">
{ "imports": {
  "three": "https://cdn.jsdelivr.net/npm/three@0.186.0/build/three.module.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.186.0/examples/jsm/"
} }
</script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/ScrollTrigger.min.js"></script>

<div class="stage" aria-hidden="true">
  <img class="poster" src="poster.webp" alt="" width="1600" height="900">  <!-- no WebGL, reduced motion, first paint -->
  <canvas id="gl"></canvas>
</div>
<main id="story"> … all text, navigation and actions in HTML … </main>
<script type="module" src="main.js"></script>
```

```js
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

gsap.registerPlugin(ScrollTrigger);
const canvas = document.querySelector('#gl');
const gl = canvas.getContext('webgl2');
if (!gl) throw new Error('no WebGL2: the poster stays');           // the fallback is the HTML poster

const renderer = new THREE.WebGLRenderer({ canvas, context: gl, antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(devicePixelRatio, matchMedia('(pointer: coarse)').matches ? 1.5 : 2));
renderer.toneMapping = THREE.NeutralToneMapping;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
pmrem.dispose();

// … build the objects (modelling.md) …

const subject = new THREE.Group();                                 // the hero object(s); framing measures this
scene.add(subject);
// … add the object's meshes to `subject` …

// One shot per storyboard scene. Framing is set by numbers, not by eye, because you may never see
// a frame before shipping:
//   dir   the direction the camera looks from (towards the look point), any length
//   look  the point on the object the camera aims at
//   fill  how much of the screen's width the object's bounding sphere covers (0.3 small, 0.55 hero,
//         above 0.7 a close-up: then the shot carries at most one short line of type)
//   shift where the object's centre sits, in fractions of the viewport from the centre (+x right,
//         +y down), on the side away from the scene's type area
const SHOTS = [
  { dir: [6, 4, 9],    look: [0, 0, 0],   fill: 0.55, shift: [0.2, 0.05],  warm: 0, explode: 0 },  // type left, object right
  { dir: [0, 12, 2],   look: [0, 0, 0],   fill: 0.45, shift: [-0.22, 0.05], warm: 0, explode: 0 }, // type right, object left
  { dir: [8, 6, 8],    look: [0, 0.4, 0], fill: 0.5,  shift: [0.15, 0.08], warm: 0, explode: 1 },  // the peak, type in a band
  { dir: [-2, 3, 4],   look: [1, 0, 0],   fill: 0.85, shift: [0.25, 0],    warm: 0, explode: 0 },  // close-up: one line only, left
  { dir: [-6, 5, 9],   look: [0, 0, 0],   fill: 0.5,  shift: [0.2, 0.08],  warm: 1, explode: 0 },  // resolution, warm light
];
const PHONE = { fill: 0.8, shift: [0, -0.2] };                     // phones: object moved up, type in a band below

const sphere = new THREE.Sphere();
const distanceFor = (fill) => {                                     // camera distance at which the sphere spans `fill` of the width
  const t = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
  const byWidth = sphere.radius / (fill * t * camera.aspect);
  const byHeight = sphere.radius / (0.9 * t);                       // never taller than 90% of the screen
  return Math.max(byWidth, byHeight);
};
const progress = { t: 0 };
let dirty = true, visible = true;
const look = new THREE.Vector3(), dir = new THREE.Vector3(), a = new THREE.Vector3(), b = new THREE.Vector3();
const ease = (x) => x * x * (3 - 2 * x);                         // hold near each shot, move between them
const place = () => {
  const f = progress.t * (SHOTS.length - 1), i = Math.min(Math.floor(f), SHOTS.length - 2), k = ease(f - i);
  const A = SHOTS[i], B = SHOTS[i + 1], mix = (x, y) => x + (y - x) * k;
  const phone = innerWidth < 700;
  // apply the shot's object state first (explode, lift …), then measure: mix(A.explode, B.explode) …
  new THREE.Box3().setFromObject(subject).getBoundingSphere(sphere);
  look.lerpVectors(a.fromArray(A.look), b.fromArray(B.look), k);
  dir.lerpVectors(a.fromArray(A.dir), b.fromArray(B.dir), k).normalize();
  camera.position.copy(look).addScaledVector(dir, distanceFor(phone ? Math.min(PHONE.fill, mix(A.fill, B.fill)) : mix(A.fill, B.fill)));
  camera.lookAt(look);
  const [sx, sy] = phone ? PHONE.shift : [mix(A.shift[0], B.shift[0]), mix(A.shift[1], B.shift[1])];
  const w = renderer.domElement.width, h = renderer.domElement.height;
  camera.setViewOffset(w, h, -sx * w, -sy * h, w, h);              // moves the object on screen without changing the view
  // light: mix(A.warm, B.warm) for the key light's color and intensity …
  dirty = true;
};

new ResizeObserver(([entry]) => {
  const { width, height } = entry.contentRect;
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  place();
}).observe(canvas);
new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; }).observe(canvas);

const timer = new THREE.Timer();                                   // Clock is deprecated
timer.connect(document);                                           // pauses while the tab is hidden
renderer.setAnimationLoop((time) => {
  timer.update(time);
  // animated objects: update them here with timer.getDelta() and set dirty = true
  if (visible && dirty) {
    renderer.render(scene, camera);
    dirty = false;
    document.documentElement.classList.add('scene-ready');         // CSS fades the canvas in over the poster
  }
});

const media = gsap.matchMedia();
media.add('(prefers-reduced-motion: no-preference)', () => {
  gsap.to(progress, { t: 1, ease: 'none', onUpdate: place,
    scrollTrigger: { trigger: '#story', start: 'top top', end: 'bottom bottom', scrub: 0.6 } });
});
media.add('(prefers-reduced-motion: reduce)', () => { progress.t = 0.35; place(); });  // one composed still
place();

canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); renderer.setAnimationLoop(null); });
canvas.addEventListener('webglcontextrestored', () => location.reload());

if (new URLSearchParams(location.search).has('debug')) window.__three = { THREE, renderer, scene, camera, subject };  // for scene-checks.js

export function dispose() {
  media.revert();
  renderer.setAnimationLoop(null);
  scene.traverse((o) => { o.geometry?.dispose(); [].concat(o.material || []).forEach((m) => m.dispose()); });
  scene.environment?.dispose();
  renderer.dispose();
}
```

Notes:
- Compose every shot like a still before writing the in-between: the storyboard names each scene's
  type area, the shot's `shift` puts the object in the opposite part of the screen, and captions sit
  directly on the scene's calm ground. A dark plate behind every caption is the sign that the frame
  wasn't composed.
- Change the light between scenes when the story changes (cool workshop light to warm evening light
  at the end, a raking light for a detail): it is the cheapest dramatic move a scene has.
- A continuous camera path (`CatmullRomCurve3`) is one option for a single unbroken flight; keep the
  per-shot `shift` and light even then.
- Use `WebGLRenderer` by default. `WebGPURenderer` (from `three/webgpu`, with TSL node materials and a
  WebGL2 fallback) pays off for compute-heavy scenes or very many draw calls; most addons and
  examples are still WebGL-first.
- iOS Safari: the address bar changes the viewport height while scrolling; size the stage with `svh`
  or `lvh` and resize the renderer from the `ResizeObserver`, never from `innerHeight` on every
  scroll. Low Power Mode caps animation at 30 fps; design scenes that still read at 30.
- GSAP and all its plugins are free for commercial use since 2025.
- Scenes with React: react-three-fiber with `frameloop="demand"` and `invalidate()`; drei's
  `PerformanceMonitor` lowers the pixel ratio when frames drop.

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
renderer.toneMapping = THREE.NeutralToneMapping;                   // AgXToneMapping is softer and filmic (three.md)
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
pmrem.dispose();

// … build the objects (modelling.md), with their printed detail …

const subject = new THREE.Group();                                 // the hero object(s), not the set around them; framing measures this
scene.add(subject);
// … add the object's meshes to `subject` …

// The object's state in a shot: whatever the story needs, as named numbers (a lid that opens, layers
// that lift by different amounts, a flip to the printed underside, a part that slides out). Every
// shot gives the same names; place() blends them between shots.
const pose = (p) => {
  // lid.rotation.x = -1.4 * p.open;
  // layers.forEach((l, i) => { l.position.y = l.userData.y + p.lift * (i + 1) * 0.25; });
  // body.rotation.z = Math.PI * p.flip;
};

// One mood per turn of the story: the ground, the pool of light on it behind the object, the key
// light, the rim, how much the environment fills in, and the ink the HTML type takes on that ground.
// Two at least, and the peak never shares the opening's. The colors are palette tokens exported as
// hex or rgb() (three.js doesn't parse oklch()).
const css = getComputedStyle(document.documentElement);
const token = (name) => new THREE.Color(css.getPropertyValue(name).trim());
const MOODS = [
  { ground: token('--ground-open'), glow: token('--glow-open'), key: token('--light-open'), power: 2.5, rim: 2, env: 0.45, ink: 'dark' },   // opening: daylight
  { ground: token('--ground-peak'), glow: token('--glow-peak'), key: token('--light-peak'), power: 6,   rim: 6, env: 0.1,  ink: 'light' },  // the peak: dark ground, raking key, hot rim
  { ground: token('--ground-end'),  glow: token('--glow-end'),  key: token('--light-end'),  power: 3,   rim: 3, env: 0.35, ink: 'dark' },   // resolution: the subject's color, a deep or muted step of it
];

// The ground is a place, not a swatch: a backdrop that darkens overhead, with a pool of the mood's
// light behind the object that follows it across the screen. Add a floor with a pattern from the
// subject where the story stands the object on something (modelling.md). One flat color in every
// frame is where generated scenes stop; scene-checks.js reports it as `oneColorGround`. Make each
// mood's glow clearly lighter or warmer than its ground (a step or two on its scale), or the pool vanishes.
const backdrop = new THREE.Mesh(new THREE.SphereGeometry(50, 32, 16), new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false,
  uniforms: { ground: { value: new THREE.Color() }, glow: { value: new THREE.Color() },
    centre: { value: new THREE.Vector2(0.5, 0.5) }, size: { value: new THREE.Vector2(1, 1) } },
  vertexShader: `varying float vUp;
    void main() { vUp = normalize(position).y; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: `uniform vec3 ground, glow; uniform vec2 centre, size; varying float vUp;
    void main() {
      vec2 d = (gl_FragCoord.xy / size - centre) * vec2(size.x / size.y, 1.0);
      vec3 c = mix(ground, ground * 0.55, smoothstep(0.0, 0.9, vUp));                 // darker overhead
      c = mix(c, glow, 0.85 * (1.0 - smoothstep(0.0, 0.8, length(d))));               // the pool behind the object
      c += (fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453) - 0.5) / 255.0;  // no banding
      gl_FragColor = vec4(c, 1.0);
      #include <colorspace_fragment>
    }`,
}));
backdrop.frustumCulled = false;
scene.add(backdrop);

// Three-point light: a warm key with the shadow, a cool fill from the other side at a fraction of the
// key, and a rim in the palette's accent from behind that draws the silhouette against the ground.
// The environment only fills in: at full strength it flattens all three. The key stays high (50 to
// 75 degrees) because it casts the ground shadow; a raking mood light is a fourth light without
// shadows, or the key with its ground shadow handed to the contact shadow (modelling.md).
const key = new THREE.DirectionalLight();                          // shadow and contact shadow: modelling.md
key.position.set(4, 8, 5);
const fill = new THREE.DirectionalLight(token('--light-fill'), 0.5);
fill.position.set(-6, 2, 4);
const rim = new THREE.DirectionalLight(token('--accent'));
rim.position.set(-3, 5, -8);
scene.add(key, fill, rim);

// One shot per storyboard scene, as many as the story has turns (seven or nine are as normal as
// five). Framing is set by numbers, not by eye, because you may never see a frame before shipping:
//   dir   the direction the camera looks from (towards the look point), any length
//   look  the point on the object the camera aims at
//   fill  how much of the screen's width the object's bounding sphere covers (0.3 small, 0.55 hero,
//         above 0.7 a close-up: then the shot carries at most one short line of type)
//   shift where the object's centre sits, in fractions of the viewport from the centre (+x right,
//         +y down), on the side away from the scene's type area
//   mood  the index into MOODS; the ground and light blend while the camera moves between shots
//   pose  the object's state (see pose above)
const SHOTS = [
  { dir: [6, 4, 9],   look: [0, 0, 0],   fill: 0.55, shift: [0.2, 0.05],   mood: 0, pose: { open: 0,   lift: 0, flip: 0 } }, // type left, object right
  { dir: [0, 12, 2],  look: [0, 0, 0],   fill: 0.45, shift: [-0.22, 0.05], mood: 0, pose: { open: 0.3, lift: 0, flip: 0 } }, // type right, object left
  { dir: [8, 6, 8],   look: [0, 0.4, 0], fill: 0.5,  shift: [0.15, 0.08],  mood: 1, pose: { open: 1,   lift: 1, flip: 0 } }, // the peak, type in a band
  { dir: [-2, 3, 4],  look: [1, 0, 0],   fill: 0.85, shift: [0.25, 0],     mood: 1, pose: { open: 1,   lift: 0.4, flip: 0 } }, // close-up: one line only, left
  { dir: [0.5, 9, 3], look: [0.8, 0, 0], fill: 0.75, shift: [-0.2, 0.05], mood: 1, pose: { open: 0,   lift: 0, flip: 1 }, hold: 0.35 }, // a detail: aimed at the engraving, held
  { dir: [-6, 5, 9],  look: [0, 0, 0],   fill: 0.5,  shift: [0.2, 0.08],   mood: 2, pose: { open: 0,   lift: 0, flip: 0 } }, // resolution
];
const PHONE = { fill: 0.8, shift: [0, -0.2] };                     // phones: object moved up, type in a band below

const sphere = new THREE.Sphere();
const distanceFor = (fill) => {                                     // camera distance at which the sphere spans `fill` of the width
  const t = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
  const byWidth = sphere.radius / (fill * t * camera.aspect);
  const byHeight = sphere.radius / (0.9 * t);                       // never taller than 90% of the screen
  return Math.max(byWidth, byHeight);
};
// The camera flies curves through the shots' directions and look points, so it rounds each shot
// instead of turning sharply at it. The distances depend on the aspect and each shot's pose: framed on resize.
const dirs = new THREE.CatmullRomCurve3(SHOTS.map((s) => new THREE.Vector3(...s.dir).normalize()), false, 'centripetal');
const aims = new THREE.CatmullRomCurve3(SHOTS.map((s) => new THREE.Vector3(...s.look)), false, 'centripetal');
const distances = [];
const frameShots = () => {
  const phone = innerWidth < 700;
  SHOTS.forEach((s, i) => {
    pose(s.pose);
    new THREE.Box3().setFromObject(subject).getBoundingSphere(sphere);
    distances[i] = distanceFor(phone ? Math.min(PHONE.fill, s.fill) : s.fill);
  });
};

// place() sets where the camera should be; the loop moves it there. Near each shot the camera slows
// so the frame reads, but never stops: linear would rush through the shots, a full ease halts at
// every one (move, stop, move); halfway between keeps it travelling.
const progress = { t: 0 };
const target = { pos: new THREE.Vector3(), look: new THREE.Vector3(), shift: new THREE.Vector2() };
const shown = { pos: new THREE.Vector3(), look: new THREE.Vector3(), shift: new THREE.Vector2() };
const dir = new THREE.Vector3(), other = new THREE.Vector2();
const settle = (x) => x + 0.5 * (x * x * (3 - 2 * x) - x);
const blend = (P, Q, k) => Object.fromEntries(Object.keys(P).map((n) => [n, P[n] + (Q[n] - P[n]) * k]));
let dirty = true, visible = true, calm = false, first = true;
// A shot's `hold` (0 to 0.45) is the share of the scroll on each side of it where the camera stays
// put: a detail that must be read (an engraving, a label) holds 0.3 to 0.4, so it doesn't turn away
// at the first flick. Give that scene's section more scroll height as well.
const unhold = (x, A, B) => Math.min(1, Math.max(0, (x - (A.hold ?? 0)) / (1 - (A.hold ?? 0) - (B.hold ?? 0))));
const place = () => {
  if (!distances.length) return;                                  // not framed yet: the ResizeObserver places it
  const f = progress.t * (SHOTS.length - 1), i = Math.min(Math.floor(f), SHOTS.length - 2);
  const k = settle(unhold(f - i, SHOTS[i], SHOTS[i + 1]));
  const A = SHOTS[i], B = SHOTS[i + 1], u = (i + k) / (SHOTS.length - 1), mix = (x, y) => x + (y - x) * k;
  pose(blend(A.pose, B.pose, k));
  dirs.getPoint(u, dir).normalize();
  aims.getPoint(u, target.look);
  target.pos.copy(target.look).addScaledVector(dir, mix(distances[i], distances[i + 1]));
  if (innerWidth < 700) target.shift.fromArray(PHONE.shift);
  else target.shift.fromArray(A.shift).lerp(other.fromArray(B.shift), k);
  const M = MOODS[A.mood], N = MOODS[B.mood];
  backdrop.material.uniforms.ground.value.lerpColors(M.ground, N.ground, k);
  backdrop.material.uniforms.glow.value.lerpColors(M.glow, N.glow, k);
  key.color.lerpColors(M.key, N.key, k);
  key.intensity = mix(M.power, N.power);
  rim.intensity = mix(M.rim, N.rim);
  scene.environmentIntensity = mix(M.env, N.env);
  document.documentElement.dataset.ink = (k < 0.5 ? M : N).ink;    // CSS sets the type and header colors per ink
  dirty = true;
};

new ResizeObserver(([entry]) => {
  const { width, height } = entry.contentRect;
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  frameShots();
  place();
  first = true;                                                    // a new size snaps the camera instead of gliding
}).observe(canvas);
new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; }).observe(canvas);

const listeners = new AbortController();
const pointer = new THREE.Vector2(), drift = new THREE.Vector2(), offset = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
addEventListener('pointermove', (e) => pointer.set(e.clientX / innerWidth - 0.5, e.clientY / innerHeight - 0.5),
  { passive: true, signal: listeners.signal });

// Compile before the first scroll, or each set stutters the first time it comes into view. compile
// skips hidden objects: show every set once, compile, upload the textures, then hide what the first
// shot doesn't need.
// sets.forEach((s) => { s.visible = true; });
await renderer.compileAsync(scene, camera);
scene.traverse((o) => [].concat(o.material ?? []).forEach((m) => m.map && renderer.initTexture(m.map)));
// sets.forEach((s, i) => { s.visible = i === 0; });

const timer = new THREE.Timer();                                   // Clock is deprecated
timer.connect(document);                                           // pauses while the tab is hidden
renderer.setAnimationLoop((time) => {
  timer.update(time);
  if (!visible || !distances.length || (calm && !dirty)) return;   // offscreen, not framed yet, or the still is drawn
  const dt = Math.min(timer.getDelta(), 0.1), t = timer.getElapsed();
  // The camera chases its target instead of sitting on it: it rounds each shot and comes to rest only
  // when the scroll does. About 3 to 4 per second: faster feels stiff, slower drifts away from the type.
  const d = first || calm ? 1 : 1 - Math.exp(-dt * 3.5);
  shown.pos.lerp(target.pos, d);
  shown.look.lerp(target.look, d);
  shown.shift.lerp(target.shift, d);
  offset.subVectors(shown.pos, shown.look);
  if (!calm) {
    // Idle life: a visible scene breathes. A slow orbit, the pointer's parallax, a float, and each part
    // drifting on its own phase; small enough that the shot's framing holds.
    drift.lerp(pointer, d);
    offset.applyAxisAngle(up, 0.05 * Math.sin(t * 0.15) - 0.12 * drift.x);
    offset.y += 0.08 * drift.y * offset.length();
    subject.position.y = 0.015 * sphere.radius * Math.sin(t * 0.7);
    // parts.forEach((p) => { p.rotation.z = p.userData.tilt + 0.03 * Math.sin(t * 0.9 + p.userData.phase); });
  }
  camera.position.copy(shown.look).add(offset);
  camera.lookAt(shown.look);
  const w = renderer.domElement.width, h = renderer.domElement.height;
  camera.setViewOffset(w, h, -shown.shift.x * w, -shown.shift.y * h, w, h);  // moves the object on screen without changing the view
  backdrop.position.copy(camera.position);                         // always around the camera
  backdrop.material.uniforms.size.value.set(w, h);
  backdrop.material.uniforms.centre.value.set(0.5 + shown.shift.x, 0.5 - shown.shift.y);  // the pool sits behind the object
  renderer.render(scene, camera);
  first = dirty = false;
  document.documentElement.classList.add('scene-ready');           // CSS fades the canvas in over the poster
});

const media = gsap.matchMedia();
media.add('(prefers-reduced-motion: no-preference)', () => {
  calm = false;
  gsap.to(progress, { t: 1, ease: 'none', onUpdate: place,
    scrollTrigger: { trigger: '#story', start: 'top top', end: 'bottom bottom', scrub: 0.6 } });
});
media.add('(prefers-reduced-motion: reduce)', () => { calm = true; progress.t = 0.35; place(); });  // one composed still

canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); renderer.setAnimationLoop(null); });
canvas.addEventListener('webglcontextrestored', () => location.reload());

if (new URLSearchParams(location.search).has('debug')) window.__three = { THREE, renderer, scene, camera, subject };  // for scene-checks.js

export function dispose() {
  media.revert();
  listeners.abort();
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
- The motion is three layers, and generated scenes usually have only the first: the scroll sets a
  target on a curve, the camera chases it with damping, and the scene keeps breathing on its own.
  Easing each segment to a full stop at every shot makes the camera go move, stop, move, stop, and a
  scene that renders only when the scroll changes is a frozen picture between gestures. Keep the
  idle motion small (a few degrees, a percent or two of the object's size) and slow (periods of
  several seconds), and give each part its own phase so they don't bob in step.
- The moods are the cheapest dramatic move a scene has, and the one generated scenes leave out: the
  same ground under the same light from the first frame to the last. Make the difference large
  (the ground's lightness moving by a third or more, or its hue changing family), not a tint.
  `[data-ink]` on the root switches the type, the header and the poster's caption colors with the
  ground; check their contrast in every mood, and give the poster the ink of the mood it shows.
  The rim is what separates a dark object from a dark ground at the peak; raise it there.
- The pose is the object's part in the story: what opens, lifts, turns over or comes apart in each
  shot, with its own amount per part. An on/off switch for one effect gives every story the same
  single trick.
- Sound only when the user asks for it or the subject is sound: synthesise it with Web Audio (an
  oscillator or filtered noise through a short gain envelope) so it weighs nothing, create the
  `AudioContext` on the first press of a visible toggle, start muted, and remember the choice.
- A journey (a train, a car, a walk through a place): the route is a `CatmullRomCurve3`, and what
  travels sits on it by `getPointAt` and `getTangentAt`, each car or part at its own distance along
  it, so it bends instead of kinking. Keep the camera's curves above; a straight lerp between shots
  turns sharply at every one.
- Use `WebGLRenderer` by default. `WebGPURenderer` (from `three/webgpu`, with TSL node materials and a
  WebGL2 fallback) pays off for compute-heavy scenes or very many draw calls; most addons and
  examples are still WebGL-first.
- iOS Safari: the address bar changes the viewport height while scrolling; size the stage with `svh`
  or `lvh` and resize the renderer from the `ResizeObserver`, never from `innerHeight` on every
  scroll. Low Power Mode caps animation at 30 fps; design scenes that still read at 30.
- GSAP and all its plugins are free for commercial use since 2025.
- Scenes with React: react-three-fiber renders every frame by default, which a breathing scene needs;
  `frameloop="demand"` with `invalidate()` only for the reduced-motion still. drei's
  `PerformanceMonitor` lowers the pixel ratio when frames drop.

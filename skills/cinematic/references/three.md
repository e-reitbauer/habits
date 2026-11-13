# three.js and WebGL craft

## Loading

- Ship the HTML content and a poster first; start the renderer after first paint, and load heavy
  assets after the first scene is visible.
- Models as glTF/GLB, geometry compressed with Draco or meshopt, vertex data quantized.
- Textures as KTX2 (Basis Universal): they stay compressed on the GPU, typically 4–8x smaller than
  decoded PNG or JPEG. Keep them at 2048 px or less unless they are the hero.
- Serve hashed files with Brotli and long-lived cache headers.

## Rendering budget

- Pixel ratio: `Math.min(devicePixelRatio, 2)` on desktop, about 1.5 on phones; lower it
  automatically when the frame rate drops (drei's `PerformanceMonitor` in react-three-fiber, or
  measure frame times yourself).
- Draw calls: around 100 per frame on phones, a few hundred on desktop. Check
  `renderer.info.render.calls`.
- Triangles: under about 300k per frame on phones, about 1M on desktop
  (`renderer.info.render.triangles`).
- Compile before the first scroll (`renderer.compileAsync`, with every set visible once) and upload
  textures with `renderer.initTexture`: a shader compiled on first view is a dropped frame of 50 to
  100 ms. Generate canvas textures at load, never in the loop.
- Repeated objects as `InstancedMesh`; varied ones sharing a material as `BatchedMesh`; static
  geometry merged, with `matrixAutoUpdate` off.
- Lights: three or fewer dynamic lights; bake the rest. Point light shadows cost six renders each.
  Shadow maps 512–1024 on phones. Static shadows don't auto-update.
- Post-processing at reduced resolution when fill rate is the limit; disable the renderer's MSAA
  when post-processing and add SMAA or FXAA last; tone mapping at the end.
- `mediump` precision in hand-written GLSL fragment shaders on mobile.
- `WebGLRenderer` is the default. `WebGPURenderer` (`three/webgpu`, falls back to WebGL2; WebGPU is
  on by default in Chrome and Safari 26) suits compute-heavy or draw-call-heavy scenes; its materials
  are written in TSL (`three/tsl`), which compiles to WGSL or GLSL, not in raw GLSL.

## Color and API traps

- `renderer.outputColorSpace` is sRGB by default. Color textures need
  `texture.colorSpace = THREE.SRGBColorSpace`; data textures (roughness, normal, AO) stay linear.
- Tone mapping is a choice: `NeutralToneMapping` keeps product colors true, `AgXToneMapping` is
  softer and filmic, ACES shifts hues. Light the scene for the one you pick.
- Deprecated in recent releases: `RGBELoader` (use `HDRLoader`), `Clock` (use `THREE.Timer`). Pin an
  exact three version in the import map; minified builds are gone since r186.
- Handle `webglcontextlost` (stop the loop, `preventDefault`) and `webglcontextrestored`.

## The loop

- Render every frame while the scene is on screen: a damped camera and idle life (a slow orbit,
  pointer parallax, parts drifting) keep moving between scroll gestures. Render on demand only when
  the scene is truly still, as in the reduced-motion version (`frameloop="demand"` and
  `invalidate()` in react-three-fiber).
- Stop the loop when the canvas is offscreen (IntersectionObserver) or the tab is hidden.
- Never allocate objects (vectors, materials) inside the frame loop.
- Dispose geometries, materials, textures and render targets when a scene is removed.

## Shaders

- Use a shader where it creates the look (a material, a transition, a distortion that belongs to
  the concept), not as a generic noise effect.
- Drive uniforms from scroll progress and time; keep the math cheap per fragment.
- Provide a static frame for reduced motion and for devices that can't keep up.

## Testing

- A three-year-old mid-range phone, a laptop on battery, and a large display.
- CPU throttling in DevTools while scrolling through every scene; watch for long tasks.
- No WebGL (disable it in the browser) and reduced motion, scene by scene.
- In automation, `scripts/scene-checks.js` reports the renderer first. Playwright's default headless
  shell renders WebGL with SwiftShader (software); there, frame times say nothing about real
  devices, so report draw calls, triangles and long tasks, and leave fps to a real browser.
  Playwright with `channel: 'chromium'` (new headless) may use the GPU on macOS.

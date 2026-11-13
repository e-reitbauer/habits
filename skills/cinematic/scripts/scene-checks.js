// Checks for a page with a WebGL scene. Pass this whole file as the `function` of Playwright's
// browser_evaluate (or page.evaluate). It scrolls through the page, samples frame times and long
// tasks, and returns a JSON report. Run it once normally, then with the CPU throttled
// (CDP Emulation.setCPUThrottlingRate, rate 4) and at a phone-sized viewport.
// The renderer comes first: in software rendering (SwiftShader, llvmpipe) frame times say nothing
// about real devices, so the report marks them as not meaningful.
async () => {
  const report = {};

  // 1. Which renderer the browser uses
  const probe = document.createElement('canvas').getContext('webgl2') || document.createElement('canvas').getContext('webgl');
  if (!probe) {
    report.renderer = { webgl: false, note: 'no WebGL: check that the poster or 2D fallback shows' };
  } else {
    const info = probe.getExtension('WEBGL_debug_renderer_info');
    const name = info ? probe.getParameter(info.UNMASKED_RENDERER_WEBGL) : probe.getParameter(probe.RENDERER);
    const software = /swiftshader|llvmpipe|software|basic render/i.test(name);
    report.renderer = { webgl: true, name, software,
      note: software ? 'software rendering: frame rates below are not meaningful; measure fps on a real device' : 'hardware rendering' };
  }

  // 2. Structure: canvases, their accessibility and a fallback
  const canvases = [...document.querySelectorAll('canvas')];
  report.canvases = canvases.map((c) => {
    const r = c.getBoundingClientRect();
    const hidden = c.closest('[aria-hidden="true"]') !== null || c.getAttribute('aria-hidden') === 'true';
    const labelled = c.hasAttribute('aria-label') || c.hasAttribute('aria-labelledby') || c.textContent.trim().length > 0;
    const scope = c.parentElement || document.body;
    const fallback = !!scope.querySelector('img, picture, video, svg');
    return {
      size: `${Math.round(r.width)}x${Math.round(r.height)}`,
      backingStore: `${c.width}x${c.height}`,
      pixelRatio: r.width ? +(c.width / r.width).toFixed(2) : null,
      accessible: hidden ? 'aria-hidden' : labelled ? 'labelled' : 'MISSING: aria-hidden or a text equivalent',
      fallbackNearby: fallback,
    };
  });
  report.textInHtml = (document.querySelector('main') || document.body).innerText.trim().split(/\s+/).length;

  // 3. three.js counters, when the page exposes them (?debug in the skeleton sets window.__three)
  const three = window.__three;
  const counters = () => three?.renderer?.info ? {
    calls: three.renderer.info.render.calls, triangles: three.renderer.info.render.triangles,
    geometries: three.renderer.info.memory.geometries, textures: three.renderer.info.memory.textures,
  } : null;

  // 4. Framing: does the object cover text? Needs window.__three.subject (skeleton.md, ?debug)
  const textCovered = [], cropped = [];
  const objectBox = () => {
    if (!three?.subject || !three.THREE) return null;
    const { THREE } = three;
    const box = new THREE.Box3().setFromObject(three.subject);
    if (box.isEmpty()) return null;
    let [x0, y0, x1, y1] = [Infinity, Infinity, -Infinity, -Infinity];
    for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) {
      const p = new THREE.Vector3(x, y, z).project(three.camera);
      const sx = (p.x + 1) / 2 * innerWidth, sy = (1 - p.y) / 2 * innerHeight;
      x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); y0 = Math.min(y0, sy); y1 = Math.max(y1, sy);
    }
    return { x0, y0, x1, y1 };
  };
  const checkFraming = (at) => {
    const o = objectBox();
    if (!o) return;
    const area = (o.x1 - o.x0) * (o.y1 - o.y0);
    const inside = Math.max(0, Math.min(o.x1, innerWidth) - Math.max(o.x0, 0)) * Math.max(0, Math.min(o.y1, innerHeight) - Math.max(o.y0, 0));
    if (area > 0 && 1 - inside / area > 0.05) cropped.push(`${at}: ${Math.round((1 - inside / area) * 100)}% of the object's screen area is outside the frame`);
    for (const el of document.querySelectorAll('h1, h2, h3, p, li, dt, dd, figcaption, a, button')) {
      const r = el.getBoundingClientRect();
      if (!el.innerText?.trim() || r.bottom < 0 || r.top > innerHeight || r.width * r.height === 0) continue;
      const s = getComputedStyle(el);
      if (+s.opacity === 0 || s.visibility === 'hidden') continue;
      const w = Math.min(r.right, o.x1) - Math.max(r.left, o.x0), h = Math.min(r.bottom, o.y1) - Math.max(r.top, o.y0);
      const share = w > 0 && h > 0 ? (w * h) / (r.width * r.height) : 0;
      if (share > 0.15) textCovered.push(`${at}: "${el.innerText.trim().slice(0, 40)}" ${Math.round(share * 100)}% inside the object's screen area`);
    }
  };

  // 4b. Ground and light: does the scene look different anywhere along the story? Needs window.__three
  const oklab = ([r, g, b]) => {
    const [lr, lg, lb] = [r, g, b].map((c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; });
    const l = Math.cbrt(0.4122214708 * lr + 0.5363325363 * lg + 0.0514459929 * lb);
    const m = Math.cbrt(0.2119034982 * lr + 0.6806995451 * lg + 0.1073969566 * lb);
    const s = Math.cbrt(0.0883024619 * lr + 0.2817188376 * lg + 0.6299787005 * lb);
    return [0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
      1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s, 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s];
  };
  const cssGround = () => { // a transparent canvas: the ground is the first painted background behind it
    const ctx = document.createElement('canvas').getContext('2d');
    for (let el = three.renderer.domElement; el; el = el.parentElement) {
      ctx.clearRect(0, 0, 1, 1);
      ctx.fillStyle = getComputedStyle(el).backgroundColor;
      ctx.fillRect(0, 0, 1, 1);
      const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;
      if (a > 127) return [r, g, b];
    }
    return [255, 255, 255];
  };
  const moods = [];
  const sampleMood = (at) => {
    if (!three?.renderer || !three.scene || !three.camera) return;
    const gl = three.renderer.getContext();
    three.renderer.render(three.scene, three.camera); // draw now, so the buffer can be read in this task (no post-processing)
    const o = objectBox(), px = new Uint8Array(4), sum = [0, 0, 0], points = [];
    for (let gy = 0.5; gy < 8; gy++) for (let gx = 0.5; gx < 8; gx++) {
      const sx = gx / 8 * innerWidth, sy = gy / 8 * innerHeight;
      if (o && sx > o.x0 && sx < o.x1 && sy > o.y0 && sy < o.y1) continue; // the ground only, not the object
      gl.readPixels(Math.floor(gx / 8 * gl.drawingBufferWidth), Math.floor((1 - gy / 8) * gl.drawingBufferHeight), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
      if (px[3] < 250) continue;
      for (let c = 0; c < 3; c++) sum[c] += px[c];
      points.push(oklab([...px.slice(0, 3)]));
    }
    const n = points.length;
    const ground = n ? sum.map((v) => Math.round(v / n)) : cssGround();
    // how much the ground varies inside this one frame (a gradient, a light pool, a pattern, a floor)
    const spread = n > 1 ? Math.max(...points.flatMap((a) => points.map((b) => Math.hypot(...a.map((v, i) => v - b[i]))))) : 0;
    const light = [0, 0, 0];
    three.scene.traverse((node) => {
      if (node.isLight && node.visible) ['r', 'g', 'b'].forEach((c, i) => { light[i] += node.color[c] * node.intensity; });
      if (node.isDirectionalLight && node.castShadow && node.visible) sampleShadow(node);
    });
    light.push(three.scene.environmentIntensity ?? 1);
    moods.push({ at, ground, light, spread });
  };

  // 4c. Shadows: how each shadow-casting directional light is set up, at every mood sample
  const shadows = new Map();
  const sampleShadow = (lightNode) => {
    const { THREE } = three;
    const from = lightNode.getWorldPosition(new THREE.Vector3()), to = lightNode.target.getWorldPosition(new THREE.Vector3());
    const elevation = THREE.MathUtils.radToDeg(Math.asin(from.sub(to).normalize().y));
    const cam = lightNode.shadow.camera, size = Math.max(cam.right - cam.left, cam.top - cam.bottom);
    const sphere = three.subject ? new THREE.Box3().setFromObject(three.subject).getBoundingSphere(new THREE.Sphere()) : null;
    const s = shadows.get(lightNode) ?? { name: lightNode.name || 'directional', mapSize: lightNode.shadow.mapSize.x,
      radius: lightNode.shadow.radius, lowestElevation: 90, frustumOverObject: 0 };
    s.lowestElevation = Math.min(s.lowestElevation, Math.round(elevation));
    if (sphere?.radius) s.frustumOverObject = Math.max(s.frustumOverObject, +(size / (2 * sphere.radius)).toFixed(1));
    shadows.set(lightNode, s);
  };

  // 5. Long tasks and frame times while scrolling through the whole page
  const longTasks = [];
  let observer = null;
  try {
    observer = new PerformanceObserver((list) => list.getEntries().forEach((e) => longTasks.push(Math.round(e.duration))));
    observer.observe({ type: 'longtask', buffered: false });
  } catch { report.longTasksNote = 'longtask entries not supported in this browser'; }

  // The scrub and a damped camera trail the scroll: before framing and mood samples, wait until the
  // camera stops travelling (idle drift moves it far less than the threshold), at most 2 s.
  const nextFrame = () => new Promise(requestAnimationFrame);
  const settle = async () => {
    if (!three?.camera) return;
    const prev = three.camera.position.clone(), start = performance.now();
    for (let still = 0; still < 5 && performance.now() - start < 2000;) {
      prev.copy(three.camera.position);
      await nextFrame();
      still = three.camera.position.distanceTo(prev) < 1e-3 * Math.max(three.camera.position.length(), 1) ? still + 1 : 0;
    }
  };

  const frames = [];
  const max = document.documentElement.scrollHeight - innerHeight;
  const steps = 240;
  const perStage = [];
  let last = await nextFrame();
  for (let i = 0; i <= steps; i++) {
    window.scrollTo({ top: (max * i) / steps, behavior: 'instant' }); // not smoothed by a page's scroll-behavior
    const now = await nextFrame();
    frames.push(now - last); // frame times while scrolling only; the settling frames are left out
    last = now;
    const at = `${Math.round((i / steps) * 100)}%`;
    if (i % 40 === 0) perStage.push({ at, ...(counters() || {}) });
    if (i % 12 === 0) {
      await settle();
      checkFraming(at);
      if (i % 24 === 0) sampleMood(at);
      last = await nextFrame();
    }
  }
  observer?.disconnect();
  window.scrollTo(0, 0);

  const sorted = frames.slice(2).sort((a, b) => a - b);
  const pct = (q) => +sorted[Math.min(sorted.length - 1, Math.floor(q * sorted.length))].toFixed(1);
  report.frames = {
    meaningful: report.renderer.webgl && !report.renderer.software,
    p50ms: pct(0.5), p95ms: pct(0.95),
    // a frame over 1.5x the median is a dropped frame at the display's refresh rate (60 or 120 Hz)
    dropped: sorted.filter((t) => t > pct(0.5) * 1.5).length, over33ms: sorted.filter((t) => t > 33.4).length,
    samples: sorted.length,
  };
  report.longTasks = { count: longTasks.length, longestMs: Math.max(0, ...longTasks) };
  report.threeCounters = three ? perStage : 'not exposed: open the page with ?debug (see skeleton.md) to read draw calls and triangles';
  // the object's projected bounding box is a rectangle, so a small share can be empty corner; look at the frame
  report.textOverObject = three?.subject ? { count: textCovered.length, items: [...new Set(textCovered)].slice(0, 15) }
    : 'not measured: expose { THREE, camera, subject } as window.__three under ?debug (skeleton.md)';
  // a close-up crops on purpose; anywhere else a crop is an accident of `fill` or `shift`
  if (three?.subject) report.objectCropped = { count: cropped.length, items: cropped.slice(0, 15) };
  if (moods.length) {
    const labs = moods.map((m) => oklab(m.ground));
    const dist = (a, b) => Math.hypot(...a.map((v, i) => v - b[i]));
    const far = (list) => Math.max(...list.flatMap((a) => list.map((b) => dist(a, b))));
    const brightest = Math.max(...moods.map((m) => Math.hypot(...m.light)), 1e-6);
    // groundRange: the largest difference between two sampled grounds, in OKLab x 100 (2 is just visible,
    // 30 is light against dark). lightChange: how far the lights and the environment move, as a share of
    // their brightest state (a tint or a dimmed key is about 0.3, a new mood 0.6 and more). A light change
    // under 0.5 on an unchanged ground doesn't read as a different scene: that is `flat`
    const groundRange = Math.round(far(labs) * 100), lightChange = +(far(moods.map((m) => m.light)) / brightest).toFixed(2);
    // withinFrame: the median, over the samples, of the largest ground difference inside one frame (same
    // scale). Under 4, every frame's ground is one flat color: a swatch behind the object, not a place
    const spreads = moods.map((m) => m.spread).sort((a, b) => a - b), withinFrame = Math.round(spreads[spreads.length >> 1] * 100);
    report.groundAndLight = { flat: groundRange < 8 && lightChange < 0.5, groundRange, lightChange,
      oneColorGround: withinFrame < 4, withinFrame,
      // a saturated mid-tone over the whole screen (OKLCH chroma above 0.12, lightness 0.35 to 0.75)
      // shouts over the object and the type; a deep shade or muted tint of the color carries a ground
      loudGround: moods.filter((m, i) => Math.hypot(labs[i][1], labs[i][2]) > 0.12 && labs[i][0] > 0.35 && labs[i][0] < 0.75)
        .map((m) => m.at),
      grounds: moods.map((m, i) => `${m.at} rgb(${m.ground.join(', ')}) L ${labs[i][0].toFixed(2)} spread ${Math.round(m.spread * 100)}`) };
  } else {
    report.groundAndLight = 'not measured: expose { renderer, scene, camera } as window.__three under ?debug (skeleton.md)';
  }
  if (three?.renderer) {
    const sm = three.renderer.shadowMap, kinds = ['basic', 'PCF', 'PCF soft', 'VSM'];
    report.shadows = !sm.enabled ? 'shadow maps off: the object needs a contact shadow at least (modelling.md)' : {
      type: kinds[sm.type] ?? sm.type,
      lights: [...shadows.values()].map((s) => ({ ...s, problems: [
        s.lowestElevation < 30 && `the light drops to ${s.lowestElevation}° above the ground: long streaked shadows; cast the ground shadow from a high light`,
        s.frustumOverObject > 3 && `the shadow camera is ${s.frustumOverObject}x the object: few texels on it, blocky or smeared edges; fit it to the object`,
        kinds[sm.type] === 'PCF' && s.radius > 2 && `PCF with radius ${s.radius}: stippled edges; keep it at 2 or less`,
      ].filter(Boolean) })),
    };
  }

  // 6. Motion preferences the page should honour
  report.reducedMotionQuery = matchMedia('(prefers-reduced-motion: reduce)').matches
    ? 'reduce is active: every scene should be a composed still' : 'no-preference: run again with browser_emulate_media reducedMotion=reduce';
  return report;
}

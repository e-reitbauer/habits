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

  // 4. Framing: does the object cover text? Needs window.__three.subject (skeleton.md, ?debug): the
  // hero object, not the set around it. Measured per mesh, from the corners in front of the camera,
  // so a long subject the camera rides beside (a train) counts only where it is on screen.
  const textCovered = [], cropped = [];
  const screenRect = (box) => {
    const { THREE } = three, cam = three.camera;
    let [x0, y0, x1, y1] = [Infinity, Infinity, -Infinity, -Infinity];
    for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) {
      const v = new THREE.Vector3(x, y, z);
      if (v.clone().applyMatrix4(cam.matrixWorldInverse).z > -cam.near) continue;  // behind the camera
      const p = v.project(cam), sx = (p.x + 1) / 2 * innerWidth, sy = (1 - p.y) / 2 * innerHeight;
      x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); y0 = Math.min(y0, sy); y1 = Math.max(y1, sy);
    }
    return x1 > x0 ? { x0, y0, x1, y1 } : null;
  };
  const objectRects = () => {
    if (!three?.subject || !three.THREE) return [];
    const rects = [];
    three.subject.traverseVisible((m) => { const r = m.isMesh && screenRect(new three.THREE.Box3().setFromObject(m)); if (r) rects.push(r); });
    return rects;
  };
  const checkFraming = (at) => {
    if (!three?.subject || !three.THREE) return;
    const box = new three.THREE.Box3().setFromObject(three.subject), o = !box.isEmpty() && screenRect(box);
    if (!o) return;
    // a crop is measured on the whole object; with the camera inside its box (a long subject) it can't be
    if (!box.containsPoint(three.camera.position)) {
      const area = (o.x1 - o.x0) * (o.y1 - o.y0);
      const inside = Math.max(0, Math.min(o.x1, innerWidth) - Math.max(o.x0, 0)) * Math.max(0, Math.min(o.y1, innerHeight) - Math.max(o.y0, 0));
      if (area > 0 && 1 - inside / area > 0.05) cropped.push(`${at}: ${Math.round((1 - inside / area) * 100)}% of the object's screen area is outside the frame`);
    }
    const rects = objectRects();
    for (const el of document.querySelectorAll('h1, h2, h3, p, li, dt, dd, figcaption, a, button')) {
      const r = el.getBoundingClientRect();
      if (!el.innerText?.trim() || r.bottom < 0 || r.top > innerHeight || r.width * r.height === 0) continue;
      const s = getComputedStyle(el);
      if (+s.opacity === 0 || s.visibility === 'hidden') continue;
      const share = Math.max(0, ...rects.map((q) => {
        const w = Math.min(r.right, q.x1) - Math.max(r.left, q.x0), h = Math.min(r.bottom, q.y1) - Math.max(r.top, q.y0);
        return w > 0 && h > 0 ? (w * h) / (r.width * r.height) : 0;
      }));
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
    const ctx = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
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
    const rects = objectRects(), px = new Uint8Array(4), sum = [0, 0, 0], points = [];
    for (let gy = 0.5; gy < 8; gy++) for (let gx = 0.5; gx < 8; gx++) {
      const sx = gx / 8 * innerWidth, sy = gy / 8 * innerHeight;
      if (rects.some((o) => sx > o.x0 && sx < o.x1 && sy > o.y0 && sy < o.y1)) continue; // the ground only, not the object
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

  // 4d. Text over the scene, from pixels: the canvas behind each block of text that has no surface of
  // its own, read right after a render. Worst contrast (10th percentile of the pixels behind it) and
  // how busy the ground is there. Post-processing passes are not in this render.
  const paint = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
  const rgba = (c) => { paint.clearRect(0, 0, 1, 1); paint.fillStyle = c; paint.fillRect(0, 0, 1, 1); const d = paint.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
  const lum = ([r, g, b]) => [r, g, b].map((c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; })
    .reduce((s, c, i) => s + c * [0.2126, 0.7152, 0.0722][i], 0);
  const over = (top, a, bottom) => bottom.map((c, i) => top[i] * a + c * (1 - a));
  const illegible = new Map(), unmeasured = new Set();
  const checkText = (at) => {
    if (!three?.renderer || !three.scene || !three.camera) return;
    const canvas = three.renderer.domElement, cr = canvas.getBoundingClientRect(), gl = three.renderer.getContext();
    const ground = cssGround(), sx = gl.drawingBufferWidth / cr.width, sy = gl.drawingBufferHeight / cr.height;
    three.renderer.render(three.scene, three.camera);                // read in the same task as the render
    for (const el of document.querySelectorAll('body *')) {
      if (el.closest('script, style, noscript, template, svg') || ![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
      const range = document.createRange(); range.selectNodeContents(el);
      const r = range.getBoundingClientRect();
      const x0 = Math.max(r.left, cr.left, 0), x1 = Math.min(r.right, cr.right, innerWidth);
      const y0 = Math.max(r.top, cr.top, 0), y1 = Math.min(r.bottom, cr.bottom, innerHeight);
      if (x1 - x0 < 4 || y1 - y0 < 4) continue;
      // what lies between the text and the canvas: an opaque surface means it is backed (page-checks.js
      // measures it); translucent colors are layered over the pixels; a gradient or image can't be told
      let opacity = 1, backed = false; const layers = [];
      for (let node = el; node && !node.contains(canvas); node = node.parentElement) {
        const s = getComputedStyle(node);
        opacity *= +s.opacity;
        if (s.visibility === 'hidden' || s.display === 'none') opacity = 0;
        if (s.backgroundImage !== 'none') { backed = null; break; }
        const bg = rgba(s.backgroundColor);
        if (bg[3] >= 0.95) { backed = true; break; }
        if (bg[3] > 0) layers.unshift(bg);                           // outermost first: painted first
      }
      const text = el.innerText.trim().replace(/\s+/g, ' ').slice(0, 40);
      if (backed === null) { unmeasured.add(`"${text}"`); continue; }
      if (backed || opacity < 0.5) continue;                         // on a surface, or mid-fade
      const s = getComputedStyle(el), ink = rgba(s.color), size = parseFloat(s.fontSize);
      const need = size >= 24 || (size >= 18.66 && +s.fontWeight >= 700) ? 3 : 4.5;
      const w = Math.round((x1 - x0) * sx), h = Math.round((y1 - y0) * sy);
      const px = new Uint8Array(w * h * 4);
      gl.readPixels(Math.round((x0 - cr.left) * sx), Math.round((cr.bottom - y1) * sy), w, h, gl.RGBA, gl.UNSIGNED_BYTE, px);
      const step = Math.max(1, Math.floor(Math.sqrt((w * h) / 4000))), ratios = [], lums = [];
      for (let y = 0; y < h; y += step) for (let x = 0; x < w; x += step) {
        const i = (y * w + x) * 4, a = px[i + 3] / 255;
        let bg = [0, 1, 2].map((c) => px[i + c] + ground[c] * (1 - a)); // premultiplied over the CSS ground
        for (const l of layers) bg = over(l, l[3], bg);
        const fg = over(ink, ink[3] * opacity, bg), [lf, lb] = [lum(fg), lum(bg)];
        ratios.push((Math.max(lf, lb) + 0.05) / (Math.min(lf, lb) + 0.05));
        lums.push(lb);
      }
      ratios.sort((p, q) => p - q); lums.sort((p, q) => p - q);
      const worst = ratios[Math.floor(ratios.length * 0.1)], spread = lums[Math.floor(lums.length * 0.9)] - lums[Math.floor(lums.length * 0.1)];
      if (worst < need && worst < (illegible.get(el)?.worst ?? Infinity))
        illegible.set(el, { worst, line: `${at}: "${text}" ${worst.toFixed(1)}:1, needs ${need}${spread > 0.25 ? ', busy ground' : ''}` });
    }
  };

  // 4e. Camera clearance, also while the camera travels between shots: inside or against scenery
  // (rays into the view that first meet the back of a one-sided mesh, or anything within twice the
  // near plane), or scenery between the camera and the subject
  const blocked = [];
  const checkCamera = (at) => {
    if (!three?.THREE || !three.scene || !three.camera) return;
    const { THREE } = three, cam = three.camera, origin = cam.getWorldPosition(new THREE.Vector3()), ray = new THREE.Raycaster();
    const meshes = [];
    // solid scenery only: glows, decals and light pools are one-sided transparent planes on purpose, and
    // a backdrop or sky dome (back faces, no depth) surrounds the camera by design
    three.scene.traverseVisible((o) => {
      const m = o.material;
      if (o.isMesh && m && !Array.isArray(m) && !m.transparent && m.depthWrite && m.side !== THREE.BackSide) meshes.push(o);
    });
    const sides = meshes.map((m) => m.material.side);
    meshes.forEach((m) => { m.material.side = THREE.DoubleSide; });  // restored below, before any render
    const first = (dir, far = Infinity) => { ray.set(origin, dir.normalize()); ray.far = far; return ray.intersectObjects(meshes, false)[0]; };
    const label = (o, id) => {
      for (let n = o; n; n = n.parent) if (n.name) return n.name;
      return `an unnamed ${o.geometry?.type ?? 'mesh'}${id === undefined ? '' : `, instance ${id}`}`;
    };
    const backFace = (hit) => {
      if (!hit?.face || sides[meshes.indexOf(hit.object)] !== THREE.FrontSide) return false;
      const m = hit.object.matrixWorld.clone();
      if (hit.instanceId !== undefined) m.multiply(hit.object.getMatrixAt(hit.instanceId, new THREE.Matrix4()));
      return hit.face.normal.clone().transformDirection(m).dot(ray.ray.direction) > 0;
    };
    const view = [[0, 0], [-0.9, -0.9], [0.9, -0.9], [-0.9, 0.9], [0.9, 0.9]]
      .map(([x, y]) => new THREE.Vector3(x, y, 0.5).unproject(cam).sub(origin));
    const axes = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]].map((d) => new THREE.Vector3(...d));
    let found = null;
    for (const d of view) { const h = first(d); if (backFace(h)) { found = `inside or behind ${label(h.object, h.instanceId)} (sees its back faces)`; break; } }
    const touch = !found && [...view, ...axes].map((d) => first(d, cam.near * 2)).find(Boolean);
    if (touch) found = `touching ${label(touch.object, touch.instanceId)}`;
    if (!found && three.subject) {
      const sphere = new THREE.Box3().setFromObject(three.subject).getBoundingSphere(new THREE.Sphere());
      const toHero = sphere.center.clone().sub(origin), d = toHero.length() - sphere.radius;
      const p = sphere.center.clone().project(cam), inView = p.z < 1 && Math.abs(p.x) < 1 && Math.abs(p.y) < 1;  // shots of another place don't count
      const hit = d > 0 && inView && first(toHero, d);
      let inHero = false; hit?.object?.traverseAncestors((a) => { inHero ||= a === three.subject; });
      if (hit && !inHero) found = `${label(hit.object, hit.instanceId)} stands between the camera and the subject`;
    }
    meshes.forEach((m, i) => { m.material.side = sides[i]; });
    if (found) blocked.push(`${at}: ${found}`);
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
      checkText(at);
      checkCamera(at);
      if (i % 24 === 0) sampleMood(at);
      last = await nextFrame();
    } else if (i % 3 === 0) {
      checkCamera(at);                                               // mid-travel, where clipping usually happens
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
  if (three?.renderer) {
    const worst = [...illegible.values()].sort((p, q) => p.worst - q.worst);
    report.textLegibility = { count: worst.length, items: worst.slice(0, 15).map((x) => x.line),
      notMeasured: [...unmeasured].slice(0, 8) }; // on a gradient or image scrim: check those in a screenshot
    report.cameraClearance = { count: blocked.length, items: [...new Set(blocked)].slice(0, 15) };
  }
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

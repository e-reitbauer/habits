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
  const textCovered = [];
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

  // 5. Long tasks and frame times while scrolling through the whole page
  const longTasks = [];
  let observer = null;
  try {
    observer = new PerformanceObserver((list) => list.getEntries().forEach((e) => longTasks.push(Math.round(e.duration))));
    observer.observe({ type: 'longtask', buffered: false });
  } catch { report.longTasksNote = 'longtask entries not supported in this browser'; }

  const frames = [];
  const max = document.documentElement.scrollHeight - innerHeight;
  const steps = 240;
  const perStage = [];
  let last = performance.now();
  await new Promise((resolve) => {
    let i = 0;
    const tick = (now) => {
      frames.push(now - last);
      last = now;
      if (i % 40 === 0) perStage.push({ at: `${Math.round((i / steps) * 100)}%`, ...(counters() || {}) });
      if (i % 12 === 0) checkFraming(`${Math.round((i / steps) * 100)}%`);
      window.scrollTo(0, (max * i) / steps);
      i += 1;
      if (i <= steps) requestAnimationFrame(tick); else resolve();
    };
    requestAnimationFrame(tick);
  });
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

  // 6. Motion preferences the page should honour
  report.reducedMotionQuery = matchMedia('(prefers-reduced-motion: reduce)').matches
    ? 'reduce is active: every scene should be a composed still' : 'no-preference: run again with browser_emulate_media reducedMotion=reduce';
  return report;
}

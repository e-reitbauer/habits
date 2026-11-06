// Deterministic checks on a rendered page. Pass this whole file as the `function` of Playwright's
// browser_evaluate (or page.evaluate). It returns a JSON report; an empty list means the check passed.
// It measures, it doesn't judge: read each finding, then confirm it in a screenshot before fixing.
() => {
  const LIMIT = 15;
  const vw = document.documentElement.clientWidth;
  const all = [document.body, ...document.body.querySelectorAll('*')];
  const visible = (el) => {
    const s = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' && +s.opacity > 0 && r.width > 0 && r.height > 0;
  };
  const name = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) return `${s}#${el.id}`;
    const cls = [...el.classList].slice(0, 2).join('.');
    if (cls) s += `.${cls}`;
    const text = (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 30);
    return text ? `${s} "${text}"` : s;
  };
  const cap = (list) => ({ count: list.length, items: list.slice(0, LIMIT) });

  // Colors
  const parse = (c) => {
    const m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const [r, g, b, a = 1] = m[1].split(/[\s,/]+/).filter(Boolean).map(Number);
    return [r, g, b, a];
  };
  const over = (top, bottom) => top.slice(0, 3).map((c, i) => c * top[3] + bottom[i] * (1 - top[3])).concat(1);
  const lum = ([r, g, b]) => {
    const f = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (a, b) => { const [h, l] = [lum(a), lum(b)].sort((x, y) => y - x); return (h + 0.05) / (l + 0.05); };
  const background = (el) => {
    const layers = [];
    for (let node = el; node; node = node.parentElement) {
      const s = getComputedStyle(node);
      if (s.backgroundImage && s.backgroundImage !== 'none') return null; // gradient or image: can't tell
      const c = parse(s.backgroundColor);
      if (c && c[3] > 0) { layers.push(c); if (c[3] >= 1) break; }
    }
    let result = [255, 255, 255, 1]; // canvas default
    for (const layer of layers.reverse()) result = over(layer, result);
    return result;
  };

  const interactive = all.filter((el) => el.matches(
    'a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [role=link], [role=tab], [role=checkbox], [role=switch], [tabindex]:not([tabindex="-1"])'
  ) && visible(el));

  // 1. Horizontal overflow
  const overflow = document.documentElement.scrollWidth > vw + 1;
  const wide = overflow ? all.filter((el) => {
    if (!visible(el)) return false;
    const r = el.getBoundingClientRect();
    if (r.right <= vw + 1) return false;
    for (let p = el.parentElement; p; p = p.parentElement) {
      const o = getComputedStyle(p).overflowX;
      if (o === 'auto' || o === 'scroll' || o === 'hidden' || o === 'clip') return false;
    }
    return ![...el.children].some((c) => c.getBoundingClientRect().right > vw + 1); // report the innermost
  }).map((el) => `${name(el)} ends at ${Math.round(el.getBoundingClientRect().right)}px`) : [];

  // 2. Clipped text: content larger than its box, cut off without an ellipsis
  const clipped = all.filter((el) => {
    if (!visible(el) || !el.innerText || !el.innerText.trim()) return false;
    const s = getComputedStyle(el);
    const hides = /hidden|clip/.test(s.overflowX + s.overflowY);
    if (!hides || s.textOverflow === 'ellipsis' || s.webkitLineClamp !== 'none') return false;
    return el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1;
  }).map(name);

  // 3. Small targets (WCAG 2.5.8: 24x24 CSS px; inline links inside running text are exempt)
  const small = interactive.filter((el) => {
    const r = el.getBoundingClientRect();
    if (r.width >= 24 && r.height >= 24) return false;
    const inline = getComputedStyle(el).display === 'inline' && el.parentElement &&
      [...el.parentElement.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
    return !inline;
  }).map((el) => { const r = el.getBoundingClientRect(); return `${name(el)} ${Math.round(r.width)}x${Math.round(r.height)}`; });

  // 4. Overlapping interactive elements
  const overlaps = [];
  for (let i = 0; i < interactive.length && overlaps.length < LIMIT; i++) {
    for (let j = i + 1; j < interactive.length; j++) {
      const [a, b] = [interactive[i], interactive[j]];
      if (a.contains(b) || b.contains(a)) continue;
      const [p, q] = [a.getBoundingClientRect(), b.getBoundingClientRect()];
      const w = Math.min(p.right, q.right) - Math.max(p.left, q.left);
      const h = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top);
      if (w > 2 && h > 2) overlaps.push(`${name(a)} overlaps ${name(b)}`);
    }
  }

  // 5. Text contrast (WCAG 1.4.3: 4.5:1, or 3:1 for large text)
  const lowContrast = [];
  const unknownContrast = [];
  for (const el of all) {
    if (!visible(el) || ![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
    const s = getComputedStyle(el);
    const bg = background(el);
    if (!bg) { unknownContrast.push(name(el)); continue; }
    const fg = over(parse(s.color) || [0, 0, 0, 1], bg);
    const size = parseFloat(s.fontSize);
    const large = size >= 24 || (size >= 18.66 && +s.fontWeight >= 700);
    const r = ratio(fg, bg);
    if (r < (large ? 3 : 4.5)) lowContrast.push(`${name(el)} ${r.toFixed(2)}:1 (${s.color} on rgb(${bg.slice(0, 3).map(Math.round)}))`);
  }

  // 6. Names and semantics
  const accessibleName = (el) => (el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') ||
    el.getAttribute('title') || el.innerText || el.value || el.getAttribute('alt') ||
    [...el.querySelectorAll('img[alt], svg title')].map((n) => n.getAttribute('alt') || n.textContent).join('')).trim();
  const unnamed = interactive.filter((el) => el.matches('a, button, [role=button], [role=link]') && !accessibleName(el)).map(name);
  const unlabeled = interactive.filter((el) => el.matches('input, select, textarea') &&
    !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby') && !(el.labels && el.labels.length) &&
    !el.matches('[type=submit], [type=button], [type=reset], [type=image]')).map(name);
  const noAlt = [...document.images].filter((img) => !img.hasAttribute('alt')).map((img) => img.src.split('/').pop());
  const headings = [...document.querySelectorAll('h1, h2, h3, h4, h5, h6')].filter(visible);
  const headingIssues = [];
  if (headings.filter((h) => h.tagName === 'H1').length !== 1) headingIssues.push(`${headings.filter((h) => h.tagName === 'H1').length} h1 elements (expected 1)`);
  headings.forEach((h, i) => {
    const prev = i ? +headings[i - 1].tagName[1] : 0;
    if (+h.tagName[1] > prev + 1) headingIssues.push(`${name(h)} jumps from h${prev || 0} to ${h.tagName.toLowerCase()}`);
  });

  // 7. What the page actually uses: compare with the design tokens
  const fonts = new Set();
  const colors = new Set();
  for (const el of all) {
    if (!visible(el)) continue;
    const s = getComputedStyle(el);
    fonts.add(s.fontFamily.split(',')[0].replace(/["']/g, '').trim());
    colors.add(s.color);
    if (parse(s.backgroundColor)?.[3] > 0) colors.add(s.backgroundColor);
  }

  return {
    viewport: `${vw}x${document.documentElement.clientHeight}`,
    horizontalOverflow: { page: overflow, ...cap(wide) },
    clippedText: cap(clipped),
    smallTargets: cap(small),
    overlappingTargets: cap(overlaps),
    lowContrast: cap(lowContrast),
    contrastNotChecked: { reason: 'text over an image or gradient', ...cap(unknownContrast) },
    unnamedControls: cap(unnamed),
    unlabeledFields: cap(unlabeled),
    imagesWithoutAlt: cap(noAlt),
    headings: cap(headingIssues),
    fontsDeclared: [...fonts], // first family of each font stack; check that it actually loads
    colorsUsed: [...colors],
  };
}

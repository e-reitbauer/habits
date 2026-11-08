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
  const pixel = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
  const parsed = new Map();
  const parse = (c) => {
    const m = c.match(/^rgba?\(([^)]+)\)$/);
    if (m) {
      const [r, g, b, a = 1] = m[1].split(/[\s,/]+/).filter(Boolean).map(Number);
      return [r, g, b, a];
    }
    if (!parsed.has(c)) { // oklch(), lab(), color(): let the browser convert it to sRGB
      pixel.clearRect(0, 0, 1, 1);
      pixel.fillStyle = c;
      pixel.fillRect(0, 0, 1, 1);
      const [r, g, b, a] = pixel.getImageData(0, 0, 1, 1).data;
      parsed.set(c, a ? [r, g, b, a / 255] : (c.trim() === 'transparent' || /\/\s*0\)?$/.test(c) ? [0, 0, 0, 0] : null));
    }
    return parsed.get(c);
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

  // 7. Composition: small labels sitting directly above headings, and how many edges the page uses
  const eyebrows = [];
  for (const h of headings.filter((x) => /H[1-3]/.test(x.tagName))) {
    let prev = h.previousElementSibling;
    while (prev && !visible(prev)) prev = prev.previousElementSibling;
    if (!prev || !prev.innerText || prev.innerText.trim().length > 80 || prev.querySelector('h1, h2, h3, img, canvas, svg')) continue;
    const gap = h.getBoundingClientRect().top - prev.getBoundingClientRect().bottom;
    const ratio = parseFloat(getComputedStyle(prev).fontSize) / parseFloat(getComputedStyle(h).fontSize);
    if (gap >= -2 && gap < 64 && ratio < 0.6) eyebrows.push(`${name(prev)} above ${name(h)}`);
  }
  const edgeCount = (side) => {
    const counts = new Map();
    for (const el of all.filter((x) => x.matches('h1, h2, h3, h4, p, li, img, figure, picture, video, canvas, button, a.button, input, select, textarea, table, blockquote') && visible(x))) {
      const r = el.getBoundingClientRect();
      if (r.width < 40) continue;
      const x = Math.round((side === 'left' ? r.left : r.right) / 4) * 4;
      counts.set(x, (counts.get(x) || 0) + 1);
    }
    return [...counts.entries()].sort((a, b) => b[1] - a[1]).map(([x, n]) => `${x}px ×${n}`);
  };

  // 8. What the page actually uses: compare with the design tokens
  const fonts = new Set();
  const colors = new Set();
  for (const el of all) {
    if (!visible(el)) continue;
    const s = getComputedStyle(el);
    fonts.add(s.fontFamily.split(',')[0].replace(/["']/g, '').trim());
    colors.add(s.color);
    if (parse(s.backgroundColor)?.[3] > 0) colors.add(s.backgroundColor);
  }

  // 9. Icons, dots and other small marks next to text: centered on the text's cap height?
  const canvas = document.createElement('canvas').getContext('2d');
  const firstLine = (node) => {
    const text = node.nodeType === 3 ? node : document.createTreeWalker(node, NodeFilter.SHOW_TEXT,
      { acceptNode: (n) => (n.textContent.trim() ? 1 : 3) }).nextNode();
    if (!text || !text.textContent.trim()) return null;
    const range = document.createRange();
    range.selectNodeContents(text);
    const rect = range.getClientRects()[0];
    if (!rect) return null;
    const s = getComputedStyle(text.parentElement);
    canvas.font = `${s.fontStyle} ${s.fontWeight} ${s.fontSize} ${s.fontFamily}`;
    const m = canvas.measureText('H');
    return { rect, size: parseFloat(s.fontSize), capMiddle: rect.top + m.fontBoundingBoxAscent - m.actualBoundingBoxAscent / 2 };
  };
  const isMark = (el) => {
    if (!visible(el) || (el.innerText || '').trim() || el.closest('svg') !== el && el.closest('svg')) return false;
    const r = el.getBoundingClientRect();
    if (r.width > 48 || r.height > 48 || r.width < 4 || r.height < 4) return false;
    const s = getComputedStyle(el);
    return el.matches('svg, img, iconify-icon, input[type=checkbox], input[type=radio]') || !!el.querySelector('svg, img') ||
      (!el.children.length && (parse(s.backgroundColor)?.[3] > 0 || s.backgroundImage !== 'none' || parseFloat(s.borderTopWidth) > 0));
  };
  const marks = all.filter(isMark).filter((el) => !(el.parentElement && isMark(el.parentElement)));
  const misaligned = [];
  for (const mark of marks) {
    const r = mark.getBoundingClientRect();
    const siblings = mark.parentElement ? [...mark.parentElement.childNodes].filter((n) => n !== mark) : [];
    const line = siblings.map(firstLine).find((l) => l && l.rect.top < r.bottom && l.rect.bottom > r.top);
    if (!line || r.height > line.size * 2.2) continue; // avatars and thumbnails beside a text block align by their top
    const offset = r.top + r.height / 2 - line.capMiddle;
    if (Math.abs(offset) > Math.max(1, line.size * 0.06)) {
      misaligned.push(`${name(mark)} next to "${mark.parentElement.innerText.trim().slice(0, 30)}" sits ${Math.abs(offset).toFixed(1)}px ${offset > 0 ? 'low' : 'high'}`);
    }
  }

  // 10. Icons: one set, one style?
  const svgs = all.filter((el) => el.tagName === 'svg' && !el.parentElement.closest('svg') && visible(el) &&
    el.getBoundingClientRect().width <= 48);
  const iconSets = {};
  const strokes = {};
  for (const el of svgs) {
    const hint = `${el.getAttribute('class') || ''} ${el.getAttribute('data-icon') || ''} ${el.closest('[class]')?.className || ''}`;
    const set = (hint.match(/\b(lucide|tabler|ph|phosphor|iconoir|heroicon|ri|remix|material|carbon|fluent|mingcute|solar|bi|fa|iconify)/i) || [, 'unmarked'])[1].toLowerCase();
    iconSets[set] = (iconSets[set] || 0) + 1;
    const shape = el.querySelector('path, circle, rect, line, polyline, polygon');
    const s = shape && getComputedStyle(shape);
    const kind = s && s.stroke !== 'none' && parseFloat(s.strokeWidth) > 0 ? `stroke ${parseFloat(s.strokeWidth)}` : 'fill';
    strokes[kind] = (strokes[kind] || 0) + 1;
  }

  // 11. Depth: elevation tokens, border plus soft shadow, bars over scrolling content without a backing
  const shadowValues = new Map();
  const borderAndShadow = [];
  const unbacked = [];
  for (const el of all) {
    if (!visible(el)) continue;
    const s = getComputedStyle(el);
    if (s.boxShadow !== 'none') {
      shadowValues.set(s.boxShadow, (shadowValues.get(s.boxShadow) || 0) + 1);
      const blurs = [...s.boxShadow.matchAll(/(-?[\d.]+)px\s+(-?[\d.]+)px\s+([\d.]+)px/g)].map((m) => +m[3]);
      if (Math.max(0, ...blurs) >= 16 && parseFloat(s.borderTopWidth) >= 1 && s.borderTopStyle !== 'none' && !s.boxShadow.includes('inset')) borderAndShadow.push(name(el));
    }
    if ((s.position === 'fixed' || s.position === 'sticky') && el.getBoundingClientRect().width > vw * 0.5 && (el.innerText || '').trim()) {
      const alpha = parse(s.backgroundColor)?.[3] ?? 0;
      const blur = (s.backdropFilter || s.webkitBackdropFilter || 'none') !== 'none';
      if (alpha < 0.85 && !blur && s.backgroundImage === 'none') {
        unbacked.push(`${name(el)} (${s.position}, background alpha ${alpha}, no backdrop blur): text over scrolling content can become unreadable`);
      }
    }
  }

  // 12. Images: broken, blurry, stretched, or without reserved space
  const imageIssues = [];
  for (const img of [...document.images].filter(visible)) {
    const r = img.getBoundingClientRect();
    const s = getComputedStyle(img);
    const label = img.currentSrc.split('/').pop() || img.getAttribute('src');
    if (img.complete && !img.naturalWidth) { imageIssues.push(`${label}: broken`); continue; }
    if (!img.naturalWidth) continue;
    if (r.width * devicePixelRatio > img.naturalWidth * 1.15) imageIssues.push(`${label}: shown at ${Math.round(r.width)}px from ${img.naturalWidth}px, looks blurry on this screen`);
    const ratioShown = r.width / r.height;
    const ratioReal = img.naturalWidth / img.naturalHeight;
    if (s.objectFit === 'fill' && Math.abs(ratioShown / ratioReal - 1) > 0.03) imageIssues.push(`${label}: stretched (object-fit: fill at a different aspect ratio)`);
    if (!img.getAttribute('width') && !img.getAttribute('height') && s.aspectRatio === 'auto') imageIssues.push(`${label}: no width/height or aspect-ratio, the layout shifts while it loads`);
  }

  // 13. Image placement: rows that almost line up, and images that neither bleed nor sit on an axis
  const big = [...document.images].filter((img) => visible(img) && img.getBoundingClientRect().width >= 120);
  const ragged = [];
  for (let i = 0; i < big.length; i++) {
    for (let j = i + 1; j < big.length; j++) {
      const [a, b] = [big[i].getBoundingClientRect(), big[j].getBoundingClientRect()];
      const overlap = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (overlap < Math.min(a.height, b.height) * 0.5 || (a.right > b.left && b.right > a.left)) continue;
      const dTop = Math.abs(a.top - b.top);
      const dBottom = Math.abs(a.bottom - b.bottom);
      if ((dTop > 2 && dTop < 48) || (dBottom > 2 && dBottom < 48)) {
        ragged.push(`${big[i].currentSrc.split('/').pop()} and ${big[j].currentSrc.split('/').pop()}: tops differ by ${Math.round(dTop)}px, bottoms by ${Math.round(dBottom)}px`);
      }
    }
  }
  const axes = (side) => {
    const counts = new Map();
    for (const el of all.filter((x) => x.matches('h1, h2, h3, p, li') && visible(x))) {
      const r = el.getBoundingClientRect();
      const x = Math.round((side === 'left' ? r.left : r.right) / 4) * 4;
      counts.set(x, (counts.get(x) || 0) + 1);
    }
    return [...counts.entries()].filter(([, n]) => n >= 3).map(([x]) => x);
  };
  const [leftAxes, rightAxes] = [axes('left'), axes('right')];
  const near = (x, list) => list.some((a) => Math.abs(a - x) <= 4);
  const floating = big.filter((img) => {
    const box = (img.closest('figure, picture') || img).getBoundingClientRect();
    const r = img.getBoundingClientRect();
    const bleeds = r.left <= 1 || r.right >= vw - 1;
    return !bleeds && !near(r.left, leftAxes) && !near(r.right, rightAxes) && !near(box.left, leftAxes) && !near(box.right, rightAxes);
  }).map((img) => `${img.currentSrc.split('/').pop()} at ${Math.round(img.getBoundingClientRect().left)}–${Math.round(img.getBoundingClientRect().right)}px`);

  // 13b. Near-bleed: an image almost as wide as the viewport that stops at the margins
  const nearBleed = big.filter((img) => {
    const r = img.getBoundingClientRect();
    return r.width >= vw * 0.75 && r.left > 1 && r.right < vw - 1;
  }).map((img) => { const r = img.getBoundingClientRect();
    return `${img.currentSrc.split('/').pop()}: ${Math.round(r.width / vw * 100)}% of the width, ${Math.round(r.left)}px from the left and ${Math.round(vw - r.right)}px from the right edge; bleed it or make it clearly narrower`; });

  // 13c. Controls covered by something else (a decoration, a sticky element, an overlapping section)
  const covered = [];
  for (const el of interactive) {
    const r = el.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > vw) continue;  // only what is on screen now
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    if (top && top !== el && !el.contains(top) && !top.contains(el)) covered.push(`${name(el)} is covered by ${name(top)}`);
  }
  // decorations are usually pointer-events: none, so the hit test above can't see them: check geometry
  const decorations = all.filter((el) => {
    if (!visible(el) || el === document.body) return false;
    const s = getComputedStyle(el);
    if (!/absolute|fixed/.test(s.position)) return false;
    const decorative = el.getAttribute('aria-hidden') === 'true' || s.pointerEvents === 'none' ||
      el.getAttribute('role') === 'presentation' || (el.matches('img, svg') && el.getAttribute('alt') === '');
    const r = el.getBoundingClientRect();
    const backdrop = r.width * r.height > 0.6 * vw * innerHeight;  // a full-screen stage or background sits behind on purpose
    return decorative && !backdrop && r.width > 16 && r.height > 16 && !(el.parentElement && el.parentElement.closest('[aria-hidden="true"]'));
  });
  const escapes = [];
  for (const deco of decorations) {
    const d = deco.getBoundingClientRect();
    for (const el of interactive) {
      if (deco.contains(el) || el.contains(deco)) continue;
      const r = el.getBoundingClientRect();
      const w = Math.min(d.right, r.right) - Math.max(d.left, r.left), h = Math.min(d.bottom, r.bottom) - Math.max(d.top, r.top);
      if (w > 2 && h > 2 && (w * h) / (r.width * r.height) > 0.2) covered.push(`${name(el)} overlaps the decoration ${name(deco)}`);
    }
    const home = deco.parentElement?.closest('section, header, footer, main > *, article');
    if (home) {
      const b = home.getBoundingClientRect();
      const out = Math.max(b.top - d.top, d.bottom - b.bottom, b.left - d.left, d.right - b.right);
      if (out > 24 && getComputedStyle(home).overflow === 'visible') escapes.push(`${name(deco)} reaches ${Math.round(out)}px outside ${name(home)}`);
    }
  }

  // 14. Section rhythm: neighbouring sections built the same way (the template look)
  const sections = [...document.querySelectorAll('main > section, main > div, body > section, main > article, body > main > *')]
    .filter((el, i, list) => visible(el) && list.indexOf(el) === i && el.getBoundingClientRect().height > 120);
  const shape = (el) => {
    // the column structure of the section's widest content row: rounded child widths as % of the viewport
    let row = el;
    for (let depth = 0; depth < 4; depth++) {
      const kids = [...row.children].filter(visible);
      if (kids.length === 1) { row = kids[0]; continue; }
      const top = Math.min(...kids.map((k) => k.getBoundingClientRect().top));
      const first = kids.filter((k) => Math.abs(k.getBoundingClientRect().top - top) < 40);
      return first.map((k) => Math.round(k.getBoundingClientRect().width / vw * 10) * 10).join('/') +
        ((parse(getComputedStyle(el).backgroundColor)?.[3] ?? 0) > 0 &&
          getComputedStyle(el).backgroundColor !== getComputedStyle(document.body).backgroundColor ? ' on color' : '');
    }
    return 'single';
  };
  // 15. Dead sides: rows of a section whose content sits to one side with nothing on the other
  const deadSides = [];
  const blockSel = 'h1, h2, h3, h4, p, li, img, picture, video, canvas, svg, button, table, form, blockquote, figure, dl';
  for (const section of sections) {
    const items = [...section.querySelectorAll(blockSel)].filter((el) => {
      if (!visible(el) || (el.tagName === 'svg' && el.getBoundingClientRect().width < 40)) return false;
      return !el.parentElement.closest(blockSel) || el.parentElement.closest(blockSel) === el;  // outermost blocks only
    }).map((el) => {
      // text blocks: measure where the letters are, not the block's box (a full-width h2 whose text wraps at half width)
      if (el.matches('h1, h2, h3, h4, p, li, blockquote')) {
        const range = document.createRange();
        range.selectNodeContents(el);
        const rects = [...range.getClientRects()].filter((r) => r.width > 0);
        if (rects.length) {
          return { top: Math.min(...rects.map((r) => r.top)), bottom: Math.max(...rects.map((r) => r.bottom)),
            left: Math.min(...rects.map((r) => r.left)), right: Math.max(...rects.map((r) => r.right)), heading: /^H\d$/.test(el.tagName) };
        }
      }
      const r = el.getBoundingClientRect();
      return { top: r.top, bottom: r.bottom, left: r.left, right: r.right, heading: false };
    }).sort((a, b) => a.top - b.top);
    const rows = [];
    for (const r of items) {
      const row = rows.find((x) => r.top < x.bottom - 4 && r.bottom > x.top + 4);
      if (row) Object.assign(row, { top: Math.min(row.top, r.top), bottom: Math.max(row.bottom, r.bottom),
        left: Math.min(row.left, r.left), right: Math.max(row.right, r.right), headingOnly: row.headingOnly && r.heading });
      else rows.push({ top: r.top, bottom: r.bottom, left: r.left, right: r.right, headingOnly: r.heading });
    }
    for (const row of rows) {
      // a short heading above a grid is normal; a tall heading or a text block alone on one side is not
      if (row.bottom - row.top < (row.headingOnly ? 150 : 100)) continue;
      const cover = (row.right - row.left) / vw;
      const offset = ((row.left + row.right) / 2 - vw / 2) / vw;
      if (cover < 0.6 && Math.abs(offset) > 0.12) {
        deadSides.push(`${name(section)}: content covers ${Math.round(cover * 100)}% of the width on the ${offset < 0 ? 'left' : 'right'}, ` +
          `${Math.round(row.bottom - row.top)}px tall, nothing on the ${offset < 0 ? 'right' : 'left'}`);
      }
    }
  }

  // 16. Scale contrast: the largest text against the body text
  const textSizes = new Map();
  let largest = 0;
  for (const el of all) {
    if (!visible(el) || ![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
    const size = parseFloat(getComputedStyle(el).fontSize);
    const chars = [...el.childNodes].filter((n) => n.nodeType === 3).reduce((s, n) => s + n.textContent.trim().length, 0);
    textSizes.set(size, (textSizes.get(size) || 0) + chars);
    largest = Math.max(largest, size);
  }
  const bodySize = +[...textSizes.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] || 16;

  const shapes = sections.map(shape);
  const repeats = [];
  for (let i = 1; i < shapes.length; i++) {
    if (shapes[i] === shapes[i - 1] && shapes[i].includes('/')) repeats.push(`${name(sections[i - 1])} and ${name(sections[i])} both ${shapes[i]}`);
  }

  return {
    viewport: `${vw}x${document.documentElement.clientHeight}`,
    sectionShapes: shapes, // column widths (% of viewport) of each top-level section's first row
    sectionRepeats: cap(repeats), // neighbours with the same column structure: vary the layout pattern
    deadSides: cap(deadSides), // content pushed to one side with an empty other side: fill it, widen, or center on purpose
    // largest text / body text: expressive pages want 5x or more somewhere, product screens about 2.5x at most
    scaleContrast: { largestPx: Math.round(largest), bodyPx: bodySize, ratio: +(largest / bodySize).toFixed(1) },
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
    labelsAboveHeadings: cap(eyebrows),
    // distinct left and right edges of content blocks, most used first; many one-off edges mean
    // elements that don't share alignment axes (compare with the grid in the plan)
    leftEdges: cap(edgeCount('left')),
    rightEdges: cap(edgeCount('right')),
    marksOffCenter: cap(misaligned), // icons, dots, checkboxes beside text, measured against the cap height
    icons: { count: svgs.length, sets: iconSets, styles: strokes }, // expect one set and one style
    shadows: { distinct: shadowValues.size, values: [...shadowValues.keys()].slice(0, 8) }, // 3 to 5 elevation levels
    borderPlusSoftShadow: cap(borderAndShadow),
    unbackedBars: cap(unbacked),
    images: cap(imageIssues),
    imageRowsAlmostAligned: cap(ragged), // side by side, edges a few px apart: align them or make the difference deliberate
    imagesFloating: cap(floating), // neither touching a viewport edge nor on a text axis
    nearBleed: cap(nearBleed), // almost full width but stopping at the margins: the worst of both
    controlsCovered: cap(covered), // links and buttons under something else, or overlapping a positioned decoration
    decorationEscapes: cap(escapes), // positioned decorations reaching out of their section: only where the plan says so, never through the nav
    fontsDeclared: [...fonts], // first family of each font stack; check that it actually loads
    colorsUsed: [...colors],
  };
}

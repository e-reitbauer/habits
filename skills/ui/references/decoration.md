# Decoration: give the page a world

A page built only from type, flat color and boxes can be correct and still anonymous. Removing the
generated ornaments (blobs, sparkles, dot grids) leaves a bare page, and bare is a default too.
Designers give a page material through a **graphic device**: one visual idea taken from a real thing
in the subject's world, built as a small system and used at several scales, the way an identity
system works.

How studios do it: Super Studio built Rose Bakery's logo from dough-scoring lines and its patterns
from offcuts of day-old bread; Kevin Hogger drew the Wim bakery's grid pattern from the shop's green
wall tiles; Anagrama built a yachting brand from signal flags and regatta formations; Pentagram gave
the MIT Media Lab one 7×7 grid that generates a glyph for each research group. Copy the method, never
the surface: the device has to come from your subject.

## 1. Find the device

- From the subject's world (`creativity.md`), pick **one real artifact** with a strong visual rule:
  a tile, a weave, a ruled sheet, a timetable, a map, a signal system, a stamp, a label, a tool mark,
  the way a product is cut, folded, stacked or numbered. Name it in the plan.
- Choose the **kind** of device (the direction card deals one; see the catalog below) and say how
  the artifact becomes it: "the pool floor's black lane lines become the page's column rules and the
  section dividers; the depth numbers become the large numerals that open each section".
- One family per page. Two unrelated devices compete; a second one is allowed only when it is a
  variation of the first.

## 2. The catalog

| Device | Build it | How it goes wrong |
|---|---|---|
| **Pattern from an artifact** (tiles, weave, ruling, a chart's contours, a timetable grid) | SVG `<pattern>`, `repeating-linear-gradient`, or `scripts/pattern.py` with the tile size tied to the line height | the generic dot grid or graph paper; clip-art icons of the subject scattered as a pattern |
| **Glyph system** (one rule makes a small family of marks, one per section or category) | small SVG drawn on an N×N grid or from a few exact shapes, varied by a rule | random shapes with no visible rule |
| **Frames and labels** (tickets, tags, stamps, price labels, mounts, folios, crop marks) | borders, pseudo-elements, a perforated edge with a `radial-gradient` mask, a slight `rotate()`, a circular label with SVG `textPath` | sticker-bombing; boxing everything; neo-brutalist offset shadows |
| **Real-data graphic** (a map, route, schedule, measurement, plan, season) | exact SVG from real data or real geography | invented numbers or a chart used as wallpaper |
| **Type as ornament** (oversized numerals or words, cropped by an edge, set along a path or vertically) | the page's own typefaces at display scale, `overflow: clip` on the section | outlined giant words that mean nothing; centered fleurons everywhere |
| **Print treatment** (halftone, duotone, two-ink overprint, misregistration, paper grain) | `feColorMatrix` duotone, a halftone with `radial-gradient` + `background-blend-mode` + `contrast()`, a duplicated layer with `mix-blend-mode: multiply` offset 1 to 3px, `feTurbulence` grain | on every photo, on faces or on body text; grain on gradient blobs (now a tell of its own) |
| **Cut and shape** (images and sections cut to a shape from the subject, a shaped edge between sections) | `clip-path`, SVG masks, a shaped divider drawn exactly | random waves and blobs |
| **Made objects** (the subject's objects shown as crafted renders or illustrations) | see `objects.md` | a circle or a single primitive standing in for the object |

Also usable inside any device: texture from the subject (paper, stone, fabric) at low contrast,
lines and dividers in the device's form, and transitions where one section's shape or element
reaches into the next.

## 3. Dose it: a volume, not a sprinkle

- **Minimum**: in Create mode on an expressive surface the device appears in at least three places
  (for example the opener at large scale, the section transitions, and the small marks in lists,
  captions or buttons), so it reads as a system. A page where the only decoration is one faint
  pattern behind a price is undecorated.
- **One large instance per view**, cropped by an edge or a section boundary, and two to four small
  echoes (bullets, dividers, labels, the focus ring, the cursor of a list).
- **Commit the atoms**: navigation, buttons, inputs, links, list markers, the footer take the
  device's form where it fits (a label-shaped button, a ruled input, numerals from the device).
- **Balance against images**: a loud photo gets a quiet device; a section without a photo gets the
  loud device. Decoration fills a section that would otherwise be a box of text, not the gaps
  between boxes.
- **Never behind reading**: under body text a device stays at about 1.1 to 1.3:1 against its surface
  or stops before the paragraph. Text keeps its contrast minimum after every blend mode.
- **Stays in its place**: a device lives inside its section (`overflow: clip` on the section, or a
  positioned box that ends at its edges) and never crosses the navigation, buttons or links. Reaching
  across a section boundary is a deliberate move for one element per page, planned as such, and it
  stops short of the header and every control. Check at desktop and phone widths: a strip that fits
  at 1440px often runs into the nav at 390px.
- Static or very slow, still under reduced motion; hidden from assistive tech (CSS backgrounds or
  `aria-hidden`).
- Exact, never sketched: generated patterns, CSS geometry, exact SVG, real assets, made objects.
  Freehand SVG illustrations and icons come out wonky.

## 4. Check it

- **The name test**: cover the business name. Could this decoration belong to another business in
  the category, or any business? Then it isn't from the subject yet.
- Can you name the artifact the device comes from, in one phrase?
- Is the device visible in at least three places, at more than one scale?
- Does any ornament only fill negative space? Give the space a job instead (`composition.md`).

## Avoid

- Decoration that isn't from the subject: the generic dot grid or graph-paper background, gradient
  blobs and orbs, sparkles, confetti, squiggles, glass cards, torn-paper edges, random floating
  shapes, clip-art icons of the subject (an anchor for anything nautical, wheat for anything baked).
- Trends used as a costume: neo-brutalism (thick borders, hard offset shadows, pastels), Y2K chrome,
  bento grids, grainy gradients, "hand-made" film grain and wobbly hand-drawn dividers on everything.
- The same decoration everywhere at the same strength: it turns into wallpaper.

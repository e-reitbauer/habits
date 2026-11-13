# Composition: every element integrated

A page looks "just put there" when its parts don't relate: a box floats on one side with dead space
on the other, the header's edges line up with nothing below it, a stock button sits on a page whose
other elements share a concept. Designers compose the page as one surface. Every element has a
place it belongs to and a reason it looks the way it does.

## The grid and the axes

- Choose a grid before placing anything (columns, gutters, margins), and a small set of
  **alignment axes**: the left edge of the content, the right edge, one or two internal columns.
- Every element starts and ends on an axis. Header, hero, sections and footer share the same outer
  edges; when the header's button ends at one x and the content below ends at another, the page
  looks assembled from parts.
- Fewer distinct left edges is better. Count them: three or four axes read as order, ten as noise.
- Nested elements align with their parent's content edge or with a page axis, never with neither.
- Give the grid named lines for the widths the page uses (content, wider "feature", full bleed) so
  elements can break out of the reading column on purpose:

  ```css
  .page {
    display: grid;
    grid-template-columns:
      [full-start] minmax(var(--margin), 1fr)
      [feature-start] minmax(0, var(--feature-extra))
      [content-start] min(100% - 2 * var(--margin), var(--content-width)) [content-end]
      minmax(0, var(--feature-extra)) [feature-end]
      minmax(var(--margin), 1fr) [full-end];
  }
  .page > * { grid-column: content; }
  .page > .feature { grid-column: feature; }
  .page > .bleed { grid-column: full; }
  .page > .bleed-left { grid-column: full-start / content-end; }  /* half-bleed */
  ```

## The page as a sequence

A page is read as a sequence, the way a magazine is paced: an opener, then changes of rhythm. When
every section repeats one structure (a heading column beside a content column, the photo swapping
sides each time) the page reads as a template however good each section is. Eye-tracking backs this:
alternating left/right rows make people stumble over the images; keep that zigzag to two or three
rows at most.

In the plan, list the sections in order with a **layout pattern** for each, and its height and
density. Pick from these and invent others from the concept:

| Pattern | What it is |
|---|---|
| Full-bleed opener | the lead image, object or color field fills the first view; the headline sits in its calm area |
| Type opener | one headline set very large, cropped or running across the grid, with little else |
| Half-bleed | an image or color field runs from one viewport edge to a column line; text sits in the rest |
| Hero and detail | one large image or object with a much smaller second one (2:1 scale or more), on different grid lines |
| Index or list | items as a typographic list, timetable, menu or legend, scanned in rows |
| Modular field | a grid of equal fields; things span 1, 2 or 4 of them |
| Sequence strip | three to six same-ratio images or steps in a row, in order |
| Full-width band | a color field or wide image between sections, with one short line or nothing |
| Diagram | a map, plan, route, chart or timetable from the subject drawn as the section |
| Overlap | type or a second image crosses an image edge or a section boundary |
| Feature text | a reading column with notes, images or quotes breaking out into the margins |

Rules for the sequence:
- No two neighbouring sections share a pattern, and no more than two in a row use two columns.
- At least one moment per page breaks the content width (bleed, band, half-bleed or overlap).
- Rhythm follows importance: the most important section gets the most space and the largest scale;
  minor sections can be short and dense.
- Sections are separated by changes (color field, scale, a device from the subject, a shaped edge,
  an element reaching across) rather than a hairline between every pair.

## Frame each section by numbers

"Make it balanced" does nothing when you build without seeing the page, and you often do: the
render may fail, and even when it works you see it only after the code exists. Composition that is
written as numbers in the plan survives. For every section, set the spans and the lead; name the
space and the height where they matter:

| Number | What it fixes | Example |
|---|---|---|
| **Spans** | which grid columns (of 12, or the named lines `full`, `feature`, `content`) the text and the media or object take, and which edge bleeds | text 1–5, image 6–12 bleeding right; heading `full`, list 3–10 |
| **Lead** | the one element that dominates the view, and its size: a type size as a multiple of the body size, or an image or object as a share of the viewport width | headline 6× body; photo 60vw; jar group 40vw |
| **Space** | every empty area larger than a column: where it is and its job | right half above the fold holds the jars; left margin keeps the reading column calm |
| **Height** | auto, or a share of the viewport for openers and bands | opener 90svh; band 45svh; list auto |

Rules the numbers must satisfy:
- **No dead side.** When a section's content covers less than about 60% of the width and sits to one
  side, the other side holds something named in *Space* (the lead image, the object, a large numeral,
  the device). A heading and a paragraph alone in the left half of a wide section, with nothing on
  the right, is the tell. Widen the block into the grid, center the column on purpose, or fill the
  other side.
- **Text measure** stays 45 to 75 characters however wide its span; a wide span holds a narrower
  measure plus something else.
- **One lead per view**, and on an expressive page at least one view where the largest type is 5×
  the body size or more (a numeral, a word, the headline): scale contrast is what makes a page read as
  designed. Product screens stay within about 2.5×.
- **Media spans differ on purpose**: neighbouring images or objects differ by at least a factor of
  two in span, or share it exactly.
- **Phones** get their own numbers when the layout changes: what stacks first, and what bleeds.

Build the CSS from these numbers (grid-column lines, `clamp()` sizes derived from the multiple,
`min-height` in `svh`), and `scripts/page-checks.js` checks them on the rendered page (`deadSides`,
`scaleContrast`, `sectionRepeats`).

## Balance and space

- Empty space is a decision, not a leftover. When content sits on one side, the other side holds
  a counterweight: an image, a large number, a pull quote, the 3D object, a structural line, or
  the space is clearly the subject's breathing room (and then the content is placed with that in
  mind, not by accident).
- A single narrow box in a wide viewport, with nothing on the other side, is the clearest sign of
  an unplanned layout. Either widen it into the grid, split the composition, or give the space a
  job.
- Group by proximity: things that belong together sit closer to each other than to anything else.
  Spacing between groups is clearly larger than spacing inside them.
- Scale has hierarchy: one dominant element per view, then a clear second level. Several
  competing large elements cancel each other.

## Integration with the concept

- The frame elements (navigation, buttons, inputs, footer, section dividers) are designed in the
  page's material, not dropped in from a component kit. If the concept is a pool's lane ropes,
  the navigation can run along a rope; if it is a printed program, the buttons can be stamps or
  cut-outs.
- Ask of every element: why does it look like this here? If the answer is "buttons look like
  this", restyle it from the concept, or make it quieter so it doesn't compete.
- One accent, used for one job. A stock saturated button in a palette that has nothing else of
  that hue looks pasted on.
- Decorative details (bolts, corners, dots) are only worth keeping when they read as part of the
  object; scattered details read as stickers.

## Labels above headings

The small line above a heading (the "eyebrow": a kicker, tagline, category or status in small or
muted type, often with a rule) is the most persistent generated tell. Don't add one. Put the
information where it belongs instead: in the heading itself, the first sentence, a caption, the
metadata of the section, or nowhere. Only keep a label above a heading when the user asked for it
or the content genuinely is a category system the reader navigates by (and then it's the same
component everywhere).

## Alignment in the small

Misalignment by a pixel or two is what makes a careful page look slightly off. The usual causes:

- **Icons, dots, checkboxes and badges beside text** belong on the text's **cap-height center**.
  Not on the baseline: an empty element's baseline is its bottom edge, so `align-items: baseline`
  puts a dot's bottom on the text's baseline and it sits low. Not on the line box either:
  `align-items: center` centers between ascender and descender, which also sits low. Two patterns
  that land on the cap height:

  ```css
  /* single-line label in a flex row (buttons, chips, nav items, status lines) */
  .row { display: flex; align-items: center; gap: var(--space-2); }
  .row > .label { text-box: trim-both cap alphabetic; } /* the label's box becomes cap height */

  /* inline, also right for wrapping text: the mark sits on the first line */
  .mark { display: inline-block; width: var(--mark); height: var(--mark);
          vertical-align: calc(0.5cap - var(--mark) / 2); }
  ```

- **Text inside buttons, pills and badges** looks centered only when the box is trimmed to the
  letters: `text-box: trim-both cap alphabetic` with equal padding on top and bottom. `text-box`
  works in Chrome 133+, Safari 18.2+ and Firefox 154+; older browsers ignore it, so set padding that
  still looks right untrimmed (or put the trim inside `@supports (text-box: trim-both cap alphabetic)`).
- **Rows of text in different sizes** (a heading and a "see all" link, a price and its unit) align
  on their baselines: `align-items: baseline` (or `last baseline`).
- **No magic nudges.** A `translateY(1px)` or `margin-top: 2px` that fixes alignment by eye breaks
  with the next font or size; use the patterns above. Keep only deliberate optical corrections (a
  play triangle shifted right, round shapes slightly larger), with a comment.
- **Same heights in a row**: inputs and buttons that sit together share one height token.
- **Numbers in columns**: tabular figures, right-aligned or aligned on the decimal point.

## Check it

Before finishing, look at each view and answer:
- Which axes does every element sit on? Are the header's edges the content's edges?
- What is in each large empty area, and is that on purpose?
- Is there a small text element directly above any heading? Remove it or move its content.
- Which elements look like they come from a different site? Restyle them from the concept.
- Does every icon, dot and badge sit on the cap-height center of its text?
- Read the sections top to bottom: does any pattern repeat in neighbours? Where does the page break
  the content width? Where does the rhythm change?

`scripts/page-checks.js` measures some of this: the number of distinct left and right edges, small
text placed directly above headings, marks beside text that sit off the cap-height center, and
neighbouring sections with the same layout (`sectionRepeats`).

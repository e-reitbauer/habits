# Imagery

When photos exist, they are the strongest material the page has. Generated pages shrink them into
boxes floating inside the margins, at sizes that relate to nothing, with ragged edges, a caption
under each, or bury them under text and a dark wash. Professional layouts treat images as
architecture: they fill edges, rows and regions of the grid.

## Look first

- Open every image (the Read tool shows them). Note for each: the subject, the orientation, the
  focal point, where it is calm enough to hold text, its color and light, its quality and size.
- Give each image a role in the plan, and let the role set its ratio and crop, not the source file:

  ```
  | Image | Role (opener, band, hero of a pair, detail, sequence, cut-out) | Ratio | Pattern | Focal point | Section |
  ```

  Openers and bands go wide (16:9 to 21:9), details go close and tall (4:5, 1:1), sequences share one
  ratio. Crop for the story, the way a picture editor does: a tight crop on the hands, the rope, the
  face often says more than the whole frame. Leave out the images that don't earn a place.
- Take the palette's subject colors (`color.md`, step 1) from the photos, so the images and the
  interface feel like one piece.

## Place them: the patterns

Pick one pattern per image from this list and draw it in the layout sketch. Don't place an image
as a box of its own size somewhere inside the margins.

1. **Full-bleed hero.** The lead image covers the first view edge to edge (`min-height` around
   85 to 100svh, or a wide aspect ratio on phones). The headline sits in the image's calm area on
   a scrim (`depth.md`), the header over it, backed once content scrolls under. Use it when a photo
   carries the place, the atmosphere or the product in use.
2. **Half-bleed.** The image fills one side of a section from the viewport edge to a grid column
   (for example 7 of 12 columns, `grid-column: full-start / content-end` with the named lines in
   `composition.md`) and from the section's top to its bottom. Text sits in the other columns. The
   image takes the row's height (`height: 100%; object-fit: cover`), not its own. This is the
   professional replacement for a 50/50 split; use it once or twice per page, not every section.
2b. **Hero and detail.** A large image (about 8 columns) and a much smaller second one (3 or 4
   columns) from a different distance: the place and something you could touch. Scale 2:1 or more,
   on different grid lines, offset vertically, the small one sometimes overlapping the large one's
   edge.
2c. **Sequence strip.** Three to six images of one ratio in a row, in the order things happen, with
   tight gutters and short numbered captions; a horizontal scroll with `scroll-snap` on phones.
2d. **Mounted print.** The photo on a paper-colored mount with a caption set like a plate label,
   when the concept is printed matter.
3. **Band.** A wide crop (around 21:9) across the full viewport width between sections: a pause
   with atmosphere, no text, or one short line.
4. **In the grid.** The image spans whole columns, its edges on the page's axes. Beside text, its
   top aligns with the top of the text block (the heading's cap height) and its bottom with the
   block's bottom, cropped to fit.
5. **Rows and pairs.** Images side by side share their top and bottom edges: one height, widths in
   proportion to their crops, the gutter the grid's gutter. Or make the size difference deliberate
   and large (8 columns against 4), never slight; slight differences look like mistakes.
6. **Overlap.** A text panel or a second image overlapping the lead by a grid unit, or an image
   reaching across a section boundary: once per page, as a signature move.

Rules for every pattern:

- **Bleed, or align, never float.** Every image either touches a viewport edge or sits exactly on
  the grid's axes. An image surrounded by uneven dead space is the clearest sign of an amateur
  layout.
- **No near-bleed.** An image wider than about three quarters of the viewport goes all the way to
  the edges (or to one edge, as a half-bleed). One that stops at the page margins with thin strips
  of background beside it looks like a bleed that didn't make it, especially as the opener: a hero
  photo either fills the first view edge to edge or is clearly a framed, narrower image beside the
  headline.
- **A small set of ratios** (for example 3:2, 4:5, 16:9, 21:9), each chosen for its slot, and
  `object-position` set to each photo's focal point (the boat, the face, the product).
- **Scale has one leader per view**: one large image, the others clearly smaller.
- **Sequence them like a picture editor**: wide, then medium, then close; never two neighbouring
  images at the same size and ratio, except inside a strip or a modular field where sameness is the
  point.
- **No zigzag**: a photo swapping sides in every section is a template rhythm; at most two or three
  alternating rows, then change the pattern (`composition.md`, the page as a sequence).
- **On phones**, images go edge to edge (no side margins) while text keeps its margins; give a
  wide image a taller crop there when the wide one loses the subject (`<picture>` with `media`,
  or another `object-position`).
- **Captions only where they add information**, all in one style, aligned to the image's left
  edge. Credits go somewhere consistent and quiet: a small label in a corner of the image, or a
  credits list in the footer, not a caption under every photo.

```css
/* a page grid with a content column and full-bleed escapes */
.page {
  display: grid;
  grid-template-columns: [full-start] minmax(var(--margin), 1fr)
    [content-start] min(100% - 2 * var(--margin), var(--max-width)) [content-end]
    minmax(var(--margin), 1fr) [full-end];
}
.page > * { grid-column: content; }
.page > .bleed { grid-column: full; }

/* full-bleed hero with text on a scrim */
.hero { position: relative; display: grid; align-items: end; min-height: min(100svh, 60rem); }
.hero > img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
              object-position: 50% 60%; }
.hero::after { content: ""; position: absolute; inset: 0;
               background: linear-gradient(to top, var(--scrim) 0%, transparent 60%); }
.hero > .text { position: relative; z-index: 1; }

/* a row of photos with one shared height: each grows by its aspect ratio */
.photo-row { display: flex; gap: var(--gutter); }
.photo-row > figure { flex: var(--ratio) 1 0; margin: 0; }  /* --ratio: width / height */
.photo-row img { width: 100%; height: auto; aspect-ratio: var(--ratio); object-fit: cover; }
```

## Treat them as one set

- Frame them from the concept, the same way everywhere: one radius or none, a border, a shape.
- Photos from different sources differ in color and light. A shared, subtle grade (a palette tint
  layer with a blend mode at low opacity, or a duotone for secondary images) turns them into a set.
  Leave colors that matter alone: food, skin, the product.
- Credit the author where the license asks for it (CC BY and similar).

## Build them right

- `width` and `height` attributes, or `aspect-ratio`, on every image, so nothing jumps while loading.
- `loading="lazy"` and `decoding="async"` below the fold; the hero image loads eagerly with
  `fetchpriority="high"`.
- `srcset` and `sizes` when several resolutions exist. Never show an image larger than its pixels,
  and don't send a 4000px file into a 600px slot.
- `alt` text that says what the image shows in this context; `alt=""` for purely decorative ones.
- Never stretch an image and never ship a broken `src`.

## No images

- Don't invent stock URLs or hotlink random photos: they break, and their license is unknown.
- Don't fill the gap with a generic illustration, an icon in a box or a plain shape standing in for
  the object. Make the objects properly or show something else, as `objects.md` describes; let type,
  the graphic device and color carry the page (`decoration.md`); or place clearly marked placeholders
  of the right size and ratio when the user will supply photos, and say which images would help most.

`scripts/page-checks.js` reports broken, blurry, stretched and unreserved images, images side by
side whose edges almost but don't quite line up, and images that neither bleed nor sit on the
content edges.

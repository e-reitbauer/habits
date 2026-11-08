# Depth: shadows, blur and layers

Depth tells people what sits on top of what. Generated pages either put the same soft grey shadow
on every card or skip depth entirely; then a sticky header slides over content with nothing
separating them, and text over a photo or a 3D scene turns unreadable.

## Decide what floats

- Elevation means "above the page": menus, popovers, dialogs, sticky bars, toasts, a card while it
  is dragged. Static content mostly lies flat and is separated by space, tone (a surface one step
  lighter or darker) or a hairline.
- One separator per surface: a border, a shadow or a tone step. A 1px border plus a large soft
  shadow on the same card is a generated tell.
- Three to five elevation levels as tokens (`--shadow-1` … `--shadow-4`), each with a role: raised
  control, hovered or dragged card, sticky bar, popover, dialog.

## Shadows that look real

- **One light source** for the page, usually above and slightly left: every shadow falls the same
  way, with the vertical offset larger than the horizontal one.
- **Higher means** larger offset, larger blur and lower opacity.
- **Layer** two to five shadows with doubling offset and blur instead of one big blur: a tight,
  darker contact shadow plus wide, faint ambient ones.

  ```css
  --shadow-color: 250deg 30% 30%; /* the surface's hue, dark and muted */
  --shadow-2: 0 1px 1px hsl(var(--shadow-color) / .10), 0 2px 4px hsl(var(--shadow-color) / .10),
              0 6px 12px hsl(var(--shadow-color) / .10);
  ```

- **Tint** shadows with the hue of the surface they fall on, darker and less saturated, instead of
  black at 20%: black over a colored background looks grey and dirty.
- `filter: drop-shadow()` for shapes that aren't rectangles: cut-out product photos, icons, a
  tooltip with its tip.
- Inset shadows only for things pressed in: wells, pressed toggles.
- Glows only where the concept has a light (neon, a screen, a lamp, fire), in that light's color.
- **Dark mode**: shadows barely show. Lift surfaces by making them lighter (`color.md`), add a faint
  top highlight (`inset 0 1px 0 oklch(100% 0 0 / .06)`), and keep strong shadows for overlays.
- Don't animate `box-shadow` on many elements: fade the opacity of a pseudo-element that carries
  the larger shadow, or move the element with `transform`.

## Backing for anything over moving content

Sticky headers, bottom bars, toolbars and labels over images or a 3D scene need a backing that
keeps their text readable over everything that can pass beneath:

- Opaque, or translucent with `backdrop-filter: blur(12px to 20px) saturate(140% to 180%)` and a
  background alpha of at least about 0.75, plus a hairline or soft shadow along the edge that meets
  the content.
- A header may be transparent over the hero only while nothing scrolls under it; switch to the
  backed state once content passes beneath (IntersectionObserver or a scroll-driven animation).
- Always a fallback: `@supports not (backdrop-filter: blur(1px)) { … opaque surface … }`.
- Check contrast against the worst case beneath: the brightest photo, the busiest frame of the
  scene, a dark section under a light header.
- Blur is expensive, especially over video, canvas and WebGL: keep it to few, small surfaces, never
  stack blurred layers, never animate the blur radius.
- Frosted-glass cards over gradient blobs, as decoration, are a tell. Blur is for legibility.

## Text over images, video and 3D

- Place text where the image is calm (sky, water, a wall), and pick or crop images that leave room.
- A **scrim**: a gradient from transparent to the surface color, only under the text, with several
  eased stops, reaching about 50 to 70% opacity behind the words. Not a near-opaque wash over the
  whole image.
- Or a backed panel from the system, solid or blurred.
- Small labels over imagery: a soft halo in the background color (`text-shadow: 0 1px 2px …,
  0 0 12px …` at low alpha).
- Over a WebGL scene, the backing has to hold in every frame: check the brightest and busiest moment.
- Measure contrast against the lightest pixels under the text, not the average.

`scripts/page-checks.js` reports fixed or sticky bars without a backing, the number of distinct
shadows, and boxes with both a border and a soft shadow.

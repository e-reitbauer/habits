# Icons

Two generated tells: icons everywhere (one per heading, bullet and card, usually Lucide), and icons
the model drew itself. SVG paths written by hand come out lopsided: uneven strokes, curves off the
grid, odd proportions. Both make a page look unfinished.

## When an icon earns its place

- Actions, navigation, status, and repeated items people scan (amenities, file types, contact
  methods). An icon belongs where people recognize it faster than they read the word.
- Pair it with a text label, except the few everyone knows (search, close, menu, play, back).
  An icon-only button needs an `aria-label`; decorative icons get `aria-hidden="true"`.
- Not beside every heading, not in a rounded tile above each card, not before every bullet. A page
  with ten well-placed icons beats one with sixty. When in doubt, leave it out.
- Emoji are not icons.

## Never draw them

- Don't write icon paths yourself and don't approximate one from circles and lines; use a set.
- If the set lacks the exact thing, use the nearest common metaphor from the same set, or text.
- The same goes for logos, mascots and illustrations: use the user's assets, real images or type.
  Exact geometric decoration (lines, circles, patterns from `pattern.py`) is fine.

## Pick the set that matches

One set per product, in one style, matched to the type and the concept:

- **Stroke weight follows the text**: at the size it appears, the icon's stroke should look as heavy
  as the strokes of the text beside it. Light or thin type: 1.5px sets (Iconoir) or Phosphor light
  or thin. Regular text: 2px sets (Tabler) or Phosphor regular. Bold, condensed or poster type:
  Phosphor bold or fill, Material Symbols.
- **Corners follow the letterforms**: rounded or humanist type with rounded sets (Phosphor, Tabler,
  MingCute, Fluent); sharp, technical or grotesque type with square-cornered sets (Carbon,
  Material Symbols sharp).
- **Outline or filled**: outline for most interface icons; the filled form of the same icon for the
  selected or active state; filled as the whole style only for bold, playful brands.
- **Character**: Pixelarticons for pixel and retro concepts, Game-icons for adventurous or crafty
  ones, Pepicons Pencil for hand-made ones.
- Lucide is shadcn's default and the set of most generated pages; use it when the project already
  does.
- In an existing project, use the icon package it already has (grep for the import); never add a
  second set.
- `python3 scripts/icons.py sets` lists the sets with their style and license; sets under CC BY
  need a credit.

## Get them into the page

- With a package manager: the set's own package (`@phosphor-icons/react`, `@tabler/icons-react`,
  `@iconify/react` …), added the project's way (see the `dependencies` skill). Native apps: SF
  Symbols on iOS, Material Symbols on Android.
- Plain HTML or no package: `python3 scripts/icons.py search book --set ph` finds names, and
  `python3 scripts/icons.py get ph:book-open ph:clock` prints inline SVG colored by `currentColor`;
  `--sprite` prints one hidden `<svg>` of symbols to paste once and use with
  `<svg class="icon"><use href="#ph-book-open"/></svg>`. A name that doesn't exist fails loudly.
- No network and no package: ask the user for icons, or leave them out.

## Size, align, color

- Size in `em` relative to the text they sit with (1em to 1.25em), or on a fixed scale (16, 20,
  24px) for interface chrome.
- Beside text, center the icon on the text's cap height, not on the line box or the baseline (see
  "Alignment" in `composition.md`). Use one gap token for every icon and label pair.
- Optical corrections: a play triangle sits slightly right of center; a round icon can be a touch
  larger than a square one to look the same size.
- Color with `currentColor`, so icons follow the text and its states; the accent only where the
  icon is the active thing.

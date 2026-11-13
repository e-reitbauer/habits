# Typography

Generated pages share their fonts: Inter or Geist for the interface, Space Grotesk when they want
to look designed, Instrument Serif, Fraunces or Playfair for "editorial", JetBrains Mono for small
labels. Models pick fonts the way they pick colors, the most typical answer every time. Picking
well means choosing from a wider set, on purpose, and judging the fonts rendered.

## 1. Find the voice

- Describe the voice in three or four words from the concept, not from the industry. Look at the
  subject's own lettering: signage, packaging, manuals, timetables, stamps, enamel signs, rubber
  stamps, the labels on its tools. That vernacular is where a fitting typeface comes from.
## 2. Choose by eye

- Pick faces whose letterforms carry that voice, from everything you know, the way a designer
  flips through specimens: a face with character for the display, a calm one for text, or one
  family with enough range for both.
- When only the usual fonts come to mind, draw some: `python3 scripts/fonts.py --voice "<tags>"
  --role display` (and `--role text`) returns a random set of fitting open fonts, leaving out the
  defaults, each with a working stylesheet link (`--tags` lists the voice and structure tags).
  Take one only if it suits the voice better than what you had.
- When you can render pages, write a specimen (`--specimen <file> --text "<the real headline>"`),
  look at it, and delete it afterwards. Judge with real words at real sizes.
- In the plan's direction, name the fonts and why they fit the voice.
- A font from outside the Google Fonts and Fontshare catalogs: check that the exact name exists at
  its source before using it.

## 3. Pair

- One family with range (widths, weights, optical sizes) can carry a whole page; two is usual; a
  third only for a real job (mono for code or data, a script for one signature).
- Pair by contrast with one shared trait: a sturdy grotesque with a warm oldstyle serif, a
  condensed display with a calm humanist text face. Similar x-heights and proportions keep them
  related. Two faces of the same kind (two geometric sans) look like a mistake.
- Display faces stay display: poster, script, pixel, blackletter and very condensed faces carry a
  few large words, never paragraphs.
- The text face, at 16px and up: open shapes, a generous x-height, real italics, tabular figures
  where there are numbers.

## 4. Set it

- Scale: a modular ratio chosen by mood (about 1.2 for calm product UI, 1.25 to 1.333 editorial,
  1.5 and up for posters), fluid with `clamp()`, as tokens.
- Measure 45 to 75 characters (`max-width: 65ch`). Line height about 1.45 to 1.65 for body text,
  1.0 to 1.2 for headings, tighter as size grows.
- Tracking: tighten large display type slightly (-0.01 to -0.03em), open all caps and small caps
  (+0.04 to +0.1em), never track lowercase body text.
- Use what the font has: `font-optical-sizing: auto` for fonts with an `opsz` axis,
  `font-variant-numeric: tabular-nums` in tables and prices, real small caps and italics. Load
  every weight and style you use and set `font-synthesis: none`, so nothing is faked.
- `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs: no single word stranded on
  a heading's last line.
- Hierarchy from size, weight and space; not from color alone, and not from more fonts.

## 5. Type as an image

Expressive type is often the cheapest signature move: a headline set huge and cropped by the
viewport edge, a variable font's weight or width answering scroll or hover, numbers as large
graphic forms, a word set along a path, a vertical label running up an edge. One such move,
carried by the concept, is enough.

## 6. Load it well

- Only the weights and styles you use (two to four files), or a variable font when you use several.
- `<link rel="preconnect">` to the font host, `display=swap`, and a fallback stack of similar
  proportions; when the swap shifts the layout, tune a local fallback with `size-adjust`.
- In real projects prefer self-hosting (Fontsource or the foundry's files): it is faster and avoids
  sending visitors' IP addresses to a third party, which matters under GDPR.
- More open fonts for real projects: Fontsource, Velvetyne, Collletttivo, Use & Modify, The League
  of Moveable Type, and the directory uncut.wtf.

## Avoid

- Inter, Roboto, Open Sans, Poppins and Montserrat as a reflex; Space Grotesk, Geist, DM Sans,
  Manrope, Instrument Serif, Fraunces and Playfair Display as the "designed" reflex.
  `fonts.py --check <font …>` names them. Each is fine when the user or the design system chose it.
- The italic serif headline as a shortcut to "editorial"; one italic or accent-colored word in a
  headline.
- Monospace for labels by reflex; all-caps paragraphs; letter-spaced lowercase; faux bold and
  italics; more than two families without a reason.

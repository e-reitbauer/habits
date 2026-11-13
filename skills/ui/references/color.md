# Color

Generated palettes look "fine" because their hex values are picked from memory: shades that step
unevenly, dead greys, every hue at the same intensity, accents too loud at large sizes, dark mode as
an inverted light theme. Designers build color as a system in a perceptual space, from the subject,
and use it in deliberate proportions.

## 1. Start from the subject

Take the raw colors from the concept (see `creativity.md`): the subject's materials, light, places
and objects, such as chlorine-blue water, wet concrete, a lane rope's red floats, a stamp's red,
an evening sky over the city. When there are photos, sample from them. Pick a **dominant** hue, a **secondary** one, and one **accent** that is rare and sharp. Then
rebuild them as a system; never use the sampled values raw.

## 2. Build scales in OKLCH

OKLCH (lightness, chroma, hue) is perceptual: equal steps in L look like equal steps, and the same L
looks equally light across hues. HSL is not (yellow and blue at "50%" look nothing alike).

- Generate the scales with `scripts/palette.py` instead of guessing hex values. It holds hue, steps
  lightness evenly, lowers chroma toward the ends so colors stay in gamut, and shifts hue slightly
  across the scale.
- A scale has 12 steps, each with a job:

| Steps | Job |
|---|---|
| 1–2 | app background, subtle background |
| 3–5 | component backgrounds: rest, hover, pressed or selected |
| 6–8 | borders: subtle, default, strong and focus |
| 9–10 | solid fills (buttons, badges), and their hover |
| 11–12 | low-contrast and high-contrast text |

- **Neutrals are tinted**: a grey scale carries a little of the dominant hue (chroma about
  0.005–0.02), warm or cool to fit the concept. Pure greys look dead next to colored elements.
- **Hue shifting**: lighter steps drift a few degrees toward warmer, brighter hues, darker steps
  toward cooler ones with slightly more chroma, the way light and shadow behave. `palette.py
  --shift` does this; keep it small (5–15° across the scale).
- Fix the shades up front and name them as tokens. Never derive colors on the fly with lighten,
  darken or opacity tricks in feature code.

## 3. Proportion and contrast

**Pick a color strategy before picking colors**, the one the concept needs:

| Strategy | How the surface is spent |
|---|---|
| **Restrained** | tinted neutrals carry the page, one accent under about 10% marks action, focus and the current item |
| **Committed** | one saturated color from the subject covers 30 to 60% of the surface: whole sections, the header, a band, a full-color hero |
| **Full palette** | three or four colors from the subject, each with a role and a share: one per kind of content, area or time of day |
| **Drenched** | the whole page lives inside one color family, from its palest to its deepest step |

- Restrained is one strategy among four, not the safe default. A page of off-white with dark text and
  one accent is what generated pages fall back to; use it when the subject is quiet, and then tint
  the neutrals from the subject so the ground itself says something.
- **Light or dark is never a default.** Write one sentence of physical scene (who uses this, where,
  under what light: a phone at the pool's edge in summer sun, a laptop in a dim studio at night) and
  let it decide the ground.
- **Color fields** are a layout tool: a section on a full-strength color, a band, a colored image
  mount. They separate and pace the page better than rules do.
- Within any strategy the accent works because it is rare; spread it everywhere and it stops working.
  Commit to a clear temperature and a clear contrast level.
- Colors change with their surroundings (simultaneous contrast): judge the accent on the surfaces
  it will actually sit on, not on white.
- Large areas want lower chroma; small elements can take high chroma. A saturated color that looks
  right on a button is too loud as a section background.
- Check every text and UI pair with `scripts/contrast.py` (4.5:1 text, 3:1 large text and UI parts).

## 4. Harmony: what people actually find pleasing

Color theory is partly measurable. What the research says, and what to do with it:

- **Pairs harmonize** when they are similar in hue and chroma, differ moderately in lightness (not
  too little, not too much), and are fairly light overall (Ou & Luo's two-color model). The area each
  color covers changes the result, so judge combinations at their real proportions.
- **People like saturated colors more than muted ones, blue most, and dark yellow and dark orange
  least**: "dark orange (brown) and dark yellow (olive)" were the least preferred in the Berkeley
  Color Project, explained by what those colors resemble (rot, mud) rather than by the hue itself
  (Palmer & Schloss). Dark reds and dark greens did fine.
- **Brown is made by context**: an orange surrounded by brighter colors is seen as brown, the same
  orange on black looks orange. A warm color that is fine on its own can turn muddy on a light page.
- **Itten's contrasts** are the levers designers use on purpose: hue, light-dark, cold-warm,
  complementary, simultaneous, saturation, and extension (how much area each color gets). Pick
  one or two as the page's main contrast; using all of them at once is noise.
- **Temperature**: commit to one dominant temperature. A warm beige surface, a cool blue and a hot
  magenta of equal weight fight each other; one of them should dominate and the others stay small.

### Avoid accidental brown and olive

- In OKLCH, yellows and oranges (hue about 45–115) below lightness 0.6 with low chroma read as
  olive or brown. They are the colors people like least, so never get there by accident.
- Don't use the dark end of a warm scale for text, borders or icons. Use the neutral scale's text
  steps on warm surfaces instead; `palette.py` flags warm steps that read as brown.
- When a warm color must be dark, keep its chroma high and turn it toward red (amber to rust, not
  to mud); `palette.py` does this for warm seeds.
- Use beige, sand and wood tones as light surfaces only, with a clean neutral ink on them.
- Brown is right when the subject is brown (coffee, leather, walnut, soil) and the concept says so.
  Then make it rich: higher chroma, a red-leaning hue, and enough lightness contrast around it.
- Audit a palette with `python3 scripts/palette.py --audit <colors…>`.

## 5. Dark mode is its own palette

- Not pure black: a dark, tinted base, around L 0.13–0.20 in OKLCH.
- Elevation goes lighter, not shadowed: each raised surface a few percent lighter.
- Accents get slightly lighter and less saturated than in light mode, or they vibrate.
- Text is off-white from the neutral scale, not `#fff`.
- Generate it (`palette.py --dark`) rather than inverting the light scale, and check contrast on
  the real surfaces.

## 6. Gradients

A gradient is a choice like any other: good when it comes from the concept (light, atmosphere, a
material, heat, depth), generic when it is the purple-to-blue wash on everything.

**Linear and radial gradients**
- Always state the interpolation space: `linear-gradient(in oklab, …)`. Hex and `rgb()` colors
  otherwise mix in sRGB, which runs through a grey dead zone between distant hues. Use `in oklch`
  (with `shorter hue` or `longer hue`) only for deliberate sweeps around the hue wheel.
- Neighboring hues (20–60° apart) blend cleanly; complementary hues turn muddy in the middle.
  Keep complements for small accents.
- Smooth falloff needs eased stops, not just two: add intermediate stops along an ease curve, or the
  ends look banded and the middle looks flat.

**The blurred mesh (three colors and blur)**
1. A base from the palette: a deep tinted dark or a light tinted neutral.
2. Two or three blobs: radial gradients from a color to transparent, in **analogous hues** at
   similar lightness, one slightly brighter as the light source. Place them asymmetrically and
   partly off the edge.
3. Blur the **whole layer once** (`filter: blur(60–120px)` on the container), scaled up about 1.2
   so the blurred edges don't show. Blurring each blob separately shows fuzzy circles.
4. Blur washes colors out: use higher-chroma stops than you want to end up with, or `saturate()`.
5. Add grain: an SVG `feTurbulence` overlay at about 5–8% opacity with an overlay or soft-light
   blend. It hides banding and gives the surface material.
6. Text on top needs a calm area or its own surface; check contrast at the lightest point it covers.
7. Motion: none, or a slow drift of the blobs (20–40 s), moving them with transforms and never
   animating the blur. Static under reduced motion.

`scripts/gradient.py` writes this CSS from palette colors, with the interpolation space, the blur
container and the grain overlay.

## Plan it

In the direction, list the palette as roles with OKLCH values and where each comes from in the
subject, the proportion, the dark-mode approach, and any gradient with its job. Give the
proportion as shares of the page's surface; `scripts/page-checks.js` measures them on the build as
`surface`, and a committed plan that renders 15% color was not built.

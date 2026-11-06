# Anti-patterns: the generated look

These are defaults, not choices. Each one is legitimate for some brief, and the project's own
decisions and the user's explicit wishes always win. Where the brief leaves a choice open, don't
spend it on one of these.

## The test

Banning a style only moves the default to the next one. So for every visual choice in the plan, ask:
**would I have produced this for any similar brief?** If yes, either tie it to a fact about this
subject or replace it, and say what changed.

## The looks generated pages converge on

1. A warm cream background (around `#F4F1EA`) with a high-contrast serif display and a terracotta or
   clay accent (around `#D97757`).
2. A near-black background (`#0B0B0B`, `#111`) with one acid-green or vermilion accent.
3. A broadsheet layout: hairline rules, zero radius, dense newspaper columns.
4. The SaaS card kit: content chopped into identical rounded cards, one radius on everything, the
   same soft grey shadow under each, gradient washes as decoration.
5. The template chrome below, whatever the subject.

## Template chrome

| Default | Instead |
|---|---|
| ALL-CAPS tracked eyebrow label above every heading | Headings that stand alone |
| One word of the headline in italic, bold or the accent color | Let the whole headline carry the meaning |
| Badge or pill above the H1 | Put the information in the text, or leave it out |
| Meta strings joined with middle dots (`A · B · C`) | The project's separators, or a short sentence |
| Labels written as `WORD — fragment` | Plain labels |
| `→` appended to every link and button | Arrows only where something moves forward |
| Decorative `01 / 02 / 03` numbering, `03 / 10` counters | Numbers only for real sequences: steps, timelines |
| Monospace for small data labels by reflex | The body face, tabular figures for numbers |
| Em dashes in UI copy | Period, comma, colon |
| Emoji as icons | The project's icon set, or text |

## Color, type and surface

| Default | Instead |
|---|---|
| Inter, Geist, Space Grotesk, Roboto, Instrument Serif, picked by reflex | Typefaces chosen from the subject; one or two families, clearly distinct |
| Purple-to-blue or any gradient on backgrounds, text or buttons | Flat color, unless the brief calls for atmosphere |
| Colored glows and box-shadows; `shadow-lg` and `rounded-2xl` on everything | Radius and elevation that follow hierarchy |
| Glassmorphism | Solid surfaces |
| Always-dark theme with grey body text | The system preference (or the project's choice), contrast-checked |
| Accent color sprinkled everywhere | Accent only on what is active: focus, current item, selection, primary action |
| Colored top or left border on cards | Structure from layout, spacing and type |

## Layout and content

| Default | Instead |
|---|---|
| Centered hero with a big number, small label and gradient accent | Open with the most characteristic thing of the subject: its product, image, data or action |
| Identical three-column icon-card grid | A layout that fits each section's content |
| Every section the same height and rhythm | Rhythm that follows importance |
| Stats without a source | Every number with its source and date, or none |
| Lorem ipsum, perfect demo data | Real content, including the worst case |
| Text where an image belongs | Real screenshots and photos |
| Filler copy: "Seamless", "Powerful", "Unlock", "Elevate", "Supercharge" | Say what it does, in the user's words |

## Motion

The anti-pattern is generic motion, not motion. A page with no feedback at all is a default too.
Plan motion with `motion.md`.

| Default | Instead |
|---|---|
| Fade-and-slide-up on every section as it scrolls in | Motion with a job: feedback, state change, continuity; one orchestrated moment where it earns it |
| Hover-scale and shadow-lift on every card; bounce, blur-in, glow | Feedback that fits the element and the concept |
| The same 300 ms `ease` on everything, or `transition: all` | Motion tokens: durations by size and frequency, curves by direction |
| No hover, press or focus feedback at all | Every interactive element answers |
| Animation that ignores `prefers-reduced-motion` | Reduced motion: keep fades, drop movement |

## Restraint

Restraint means fewer bold moves, not smaller ones. Let one or two signature moves carry the
design (see `creativity.md`) and keep everything around them quiet. Before finishing, remove one
accessory that doesn't serve the concept.

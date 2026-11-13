# Anti-patterns: the generated look

These are defaults, not choices: each is evidence that nobody decided, never proof that a page is
bad. Each one is legitimate for some brief, and the project's own decisions and the user's explicit
wishes always win. Where the brief leaves a choice open, don't spend it on one of these.

This list is for checking a plan, not for making one. A direction built by avoiding these items
lands on the next default (number 6 below is exactly that). Make the direction from the subject,
a reference and a committed concept (`creativity.md`), then check it here.

## The test

Banning a style only moves the default to the next one. So for every visual choice in the plan, ask:
**would I have produced this for any similar brief?** If yes, either tie it to a fact about this
subject or replace it, and say what changed. A choice that is common but chosen for a stated reason
from this subject (a classic serif because the client's shop sign is set in it) is a decision, not a
default.

## The looks generated pages converge on

1. A warm cream background (around `#F4F1EA`) with a high-contrast serif display and a terracotta or
   clay accent (around `#D97757`).
2. A near-black background (`#0B0B0B`, `#111`) with one acid-green or vermilion accent.
3. A broadsheet layout: hairline rules, zero radius, dense newspaper columns.
4. The SaaS card kit: content chopped into identical rounded cards, one radius on everything, the
   same soft grey shadow under each, gradient washes as decoration.
5. The template chrome below, whatever the subject.
6. **The anti-slop look**, what pages converge on once 1 to 5 are avoided: a pale, cool off-white
   page with near-black text and one saturated accent; every section split into a heading column on
   the left and content on the right; hairline rules between all sections; big numbers as the only
   graphic idea; no decoration, no color fields, objects drawn as plain shapes. It looks careful and
   is as anonymous as the cream page.
7. The predictable opposite of the category: the dark "premium" page for a business whose peers are
   bright, the minimal page for one whose peers are busy. Avoiding the category default is still
   steering by it.

## Template chrome

| Default | Instead |
|---|---|
| Any small label, kicker, tagline or status line above a heading, in caps or not, with or without a rule ("Under construction in …", "Our story", "New") | Headings that stand alone; the information goes into the heading, the first sentence or a caption (see `composition.md`) |
| A floating box with dead space beside it; header edges that line up with nothing | One grid and shared alignment axes; empty space with a job (see `composition.md`) |
| Stock buttons, nav bars and inputs that ignore the concept | Frame elements styled from the page's material |
| One word of the headline in italic, bold or the accent color | Let the whole headline carry the meaning |
| Badge or pill above the H1 | Put the information in the text, or leave it out |
| Meta strings joined with middle dots (`A · B · C`) | The project's separators, or a short sentence |
| Labels written as `WORD — fragment` | Plain labels |
| `→` appended to every link and button | Arrows only where something moves forward |
| Decorative `01 / 02 / 03` numbering, `03 / 10` counters | Numbers only for real sequences: steps, timelines |
| Monospace for small data labels by reflex | The body face, tabular figures for numbers |
| Em dashes in UI copy | Period, comma, colon |
| Emoji as icons; an icon beside every heading or in a tile above every card; icons drawn by hand as SVG | A few icons, from one library set that matches the type (`icons.md`), or text |
| Icons and dots nudged into place by eye (`translateY(1px)`), sitting on the baseline | Marks centered on the cap height (`composition.md`, alignment) |

## Color, type and surface

| Default | Instead |
|---|---|
| Inter, Geist, Space Grotesk, Roboto, Instrument Serif, Fraunces, Playfair Display, picked by reflex | Faces chosen for the concept's voice, or a draw from `fonts.py`; one or two families, clearly distinct (`typography.md`) |
| The purple-to-blue wash, gradient text, gradient buttons, a gradient on every surface | Gradients with a job from the concept, built as in `color.md`: palette hues, `in oklab`, grain |
| Hex values picked by feel; pure greys; one saturation for everything | OKLCH scales from `palette.py`, tinted neutrals, chroma by area size |
| Colored glows and box-shadows; `shadow-lg` and `rounded-2xl` on everything; a border plus a soft shadow on one card | Radius and elevation that follow hierarchy: layered, tinted shadows only on what floats (`depth.md`) |
| Glassmorphism as decoration; a sticky header with no backing over scrolling content | Solid surfaces; blur only to back bars and labels over moving content (`depth.md`) |
| Always-dark theme with grey body text | The system preference (or the project's choice), contrast-checked |
| Accent color sprinkled everywhere | Accent only on what is active: focus, current item, selection, primary action |
| Colored top or left border on cards | Structure from layout, spacing and type |

## Layout and content

| Default | Instead |
|---|---|
| Centered hero with a big number, small label and gradient accent | Open with the most characteristic thing of the subject: its product, image, data or action |
| Identical three-column icon-card grid | A layout that fits each section's content |
| Every section the same height and rhythm | Rhythm that follows importance |
| Every section a heading column beside a content column; photo and text swapping sides down the page | A sequence of different layout patterns, one per section (`composition.md`) |
| A hairline rule between every section | Sections separated by color fields, scale changes, a device from the subject, or space |
| Objects drawn as plain circles, rectangles or a single low-poly shape | Made objects with a recognisable silhouette, light and detail, or no object (`objects.md`) |
| Stats without a source | Every number with its source and date, or none |
| Lorem ipsum, perfect demo data | Real content, including the worst case |
| Text where an image belongs | Real screenshots and photos |
| Photos as boxes floating inside the margins, side by side with ragged edges, a caption under each; identical rounded cards; a dark wash over the whole image | Images as architecture: a full-bleed hero, split bleeds, bands, rows with shared edges, each on the grid or at a viewport edge (`imagery.md`) |
| Only type and boxes, nothing from the subject; or generic decoration (dot grid, blobs, sparkles) | One motif from the concept, repeated with variation (`decoration.md`) |
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

## After the list

A page with none of these can still be forgettable. Removing a tell never adds anything: whatever
this pass takes out, the concept has to put something of its own in the same place. If the page
is clean of every item here and the memory test in `creativity.md` still gets a mood for an answer,
the page is too timid, and the fix is a bolder move, not another removal.

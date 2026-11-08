---
name: ui
description: >
  Designs user interfaces the way a product designer does: learn the design system, research the
  subject, plan the flow, states, components and layout, get the user's approval, then build from the
  system, look at the result and validate it. Use for any UI work on the web or in native apps
  (Compose, SwiftUI): building or redesigning a page, screen, component, layout or theme, adding a UI
  feature, picking colors, fonts, spacing or motion, fixing what a screenshot shows ("this is
  misaligned", "looks off", "[image #1]"), and reviewing UI or UX. Triggers include "ui", "ux",
  "design", "screen", "page", "layout", "style", "restyle", "css", "make it look better", pasted
  screenshots of an app or site, or /ui.
---

# UI

Design before code. A designer settles who the screen is for, what it must do, which states it has
and which existing parts it is made of before anything visual exists. Claude's habit is the opposite:
going straight to markup and filling every open choice with the most common default. This skill
makes the design explicit, gets it approved, then builds it from the project's own system.

**The user decides.** Everything here fills in what the user left open; none of it outranks what
they actually asked for. If they want a purple gradient, Inter, a centered hero, no plan or a
quick hack, build that well. When a request clashes with this skill, you may say so once, in a
sentence, with the alternative, and then do what they chose. Equally, don't read a wish into
silence: when the user said nothing about a choice, the guidance here applies.

**Avoiding a default is not a direction.** This skill lists the looks generated pages converge on,
but a design made by steering away from them lands on the next default (a cool grey page because
cream is "AI", every section split in two because centered heroes are). Directions come from the
subject, a real reference and a committed concept (`references/creativity.md`); the lists only
check the result.

## 1. Pick the mode and the surface

| Mode | When | Steps |
|---|---|---|
| **Fix** | something visible is wrong: alignment, overflow, color, a state | 2, then "Fixing" in step 6, 8, 9 |
| **Extend** | a new screen, section or component inside an existing design system | 2, 3 if the domain is unfamiliar, 4, 5, 6, 7, 8, 9 |
| **Create** | a new product, a redesign, or no design system yet | every step |

When unsure between two modes, pick the larger one.

The surface decides where creativity goes:

- **Expressive** (marketing site, portfolio, editorial page, event, shop front): identity is the
  job. The whole of `references/creativity.md` applies, including decoration and signature moves.
- **Product** (app screens, dashboards, settings, tools, data-dense views): convention in the middle,
  identity at the edges. Follow `references/product.md`; run the direction only for the edges
  (onboarding, empty states, the accent, the type, motion personality).
- **Native** (Jetpack Compose, Compose Multiplatform, SwiftUI, UIKit): platform rules first. Follow
  `references/native.md` together with the expressive or product guidance, and translate every CSS
  technique in the other references into the platform's own (tokens become the theme, CSS custom
  properties become theme values, Playwright checks become screenshot tests).

## 2. Learn the system

- Find the source of truth: OpenSpec specs (especially a design-system spec), `DESIGN.md`, theme and
  token files, CSS custom properties, Tailwind config, Compose `MaterialTheme` or custom theme
  objects, SwiftUI asset catalogs and environment values, the component folders or design-system
  module, a Storybook, Figma files the user links (read them with the Figma tools when available),
  the project's CLAUDE.md and memory.
- **Inventory** the components, tokens, icon package and image assets before designing anything. Search by role and by synonym,
  not only by name: button / action / cta / link-button, card / panel / tile / surface, dialog / modal /
  sheet / drawer, banner / alert / notice / toast, badge / chip / tag / pill. Grep for visible text too.
- A deliberate choice in the project wins over everything below. Don't restyle what nobody asked
  about; point it out instead.

## 3. Research the subject

In Create mode, and in Extend mode when the domain or the kind of screen is new to you, load the
`research` skill before planning. Find out who uses this and for what job, how comparable products
solve the same problem, the platform's conventions, and the subject's own world: its objects,
materials, printed matter, signage, places, tools and rituals. Distinctive design comes from the
subject; without this step the plan falls back to defaults. Look at real work too: the best sites,
apps and printed pieces in the category, and one outside it.

## 4. Plan

**Read before planning.** Open these with the Read tool before you write the plan; the guidance that
makes the result professional lives in them, and a plan written from memory falls back to defaults:

- every mode that plans: `references/process.md`, `references/composition.md`,
  `references/anti-patterns.md`, `references/ux.md`;
- Create mode, or when the system leaves the identity open: also `references/creativity.md`,
  `references/color.md`, `references/typography.md`, `references/decoration.md`;
- when the page has photos: `references/imagery.md`; when it shows objects without photos:
  `references/objects.md`; product surfaces: `references/product.md`; native: `references/native.md`.

**The plan gate.** In Create and Extend mode, the plan is written out as text in your reply, before
you write or edit any UI file. Your thinking is not visible to the user and doesn't count; the plan
is a message they can read. "Your plan is approved", "go ahead" or "build it" skips the approval
question in step 5, never the written plan; only an explicit "no plan" skips it. Writing the page
first and describing it afterwards is not a plan.

**Rules the build is held to** (the references explain each; these are the ones generated pages
break most):
- The direction comes from the subject's world, one real reference and a dealt card
  (`scripts/direction.py`), never from avoiding a look.
- Sections form a sequence of different layout patterns; no two neighbours share one, the photo
  never swaps sides section after section, and at least one moment breaks the content width.
- Every section is framed by numbers in the plan: the grid spans of text and media, the lead
  element and its size, every empty area and its job, the height (`references/composition.md`).
  The build follows the numbers, so the composition holds even if you never see a render. No side of
  a section is left empty without a named job; somewhere on an expressive page the largest type is
  5× the body size or more.
- Photos bleed to a viewport edge or sit exactly on grid lines, in sizes that differ on purpose;
  never a box inside the margins with dead space beside it, and never a near-bleed (almost full
  width but stopping at the margins), least of all the opener.
- Decoration stays inside its section and never crosses the navigation or a control.
- One graphic device from a real artifact, in at least three places at different scales; bare is
  a default too.
- No small label, kicker or tag above a heading, no decorative 01/02/03 numbering, no meta strings
  joined with middle dots, no identical card grids; the information goes into the heading, the
  text or a caption.
- Objects without photos are crafted or replaced (`references/objects.md`), never plain shapes.
- You render and review the result yourself (step 7).

1. **Brief**: user, job, success signal, constraints, real content.
2. **Flow**: one per user goal, from entry through the main path, branches and error recovery to exit.
3. **States**: ideal, empty, loading, error, partial and extreme content, each with its next step.
4. **Component map**: each region mapped to an existing component, a new variant, or a new component
   with the reason (step 6).
5. **Direction** (Create, or when the system leaves it open): follow `references/creativity.md`:
   the subject's world, the category default and its predictable opposite, one primary reference,
   the constraints dealt by `scripts/direction.py`, five concepts and the pick. Then set:
   - the color strategy and palette, as in `references/color.md`;
   - the typefaces, as in `references/typography.md`: draw candidates with `scripts/fonts.py`
     for the concept's voice instead of reaching for your usual fonts;
   - the graphic device and how much of it, as in `references/decoration.md`;
   - the images: each one's role, ratio and placement (`references/imagery.md`);
   - the objects the page shows without photos, and how they are made (`references/objects.md`);
   - the icon set that matches the type (`references/icons.md`), or no icons;
   - elevation and backing: what floats, the shadow levels, how bars over content stay readable
     (`references/depth.md`);
   - the signature moves.
   If the concept would clearly gain from a cinematic layer (3D, a scroll-driven story), mention
   the `cinematic` skill to the user in a sentence; use it when they ask for that kind of site.
6. **Layout**: the grid, then the page as a sequence of sections in this table, every cell filled
   (`references/composition.md` explains each column):

   ```
   | # | Section | Layout pattern | Spans (text / media, which edge bleeds) | Lead and its size | Empty areas and their jobs | Height |
   ```

   "Empty areas" names every area wider than about a quarter of the screen that has no content, and
   what it does there (holds the object, frames the headline, rests the eye before the order form).
   An area without a job is a mistake to fix in the plan, not in the build. Then an ASCII wireframe
   per screen (or per breakpoint when they differ) with the alignment axes marked.
7. **Motion**: the motion tokens, what gives feedback, how states are entered, and the signature
   moment, following `references/motion.md`. In Extend mode, use the system's motion if it has one.
8. **Plan check**: the memory test and ambition check in `references/creativity.md`, the defaults in
   `references/anti-patterns.md` ("would I have produced this for any similar brief?"), the
   composition check, and the UX checklist in `references/ux.md`. Revise and say what you changed.

Scale it to the work: a new section in an existing system may need a five-line brief, a state table
and a component map; a new product needs all eight.

## 5. Get approval before building

- **OpenSpec projects**: the plan becomes the change. Why and what go in `proposal.md`, flows and
  states become requirements and scenarios in the spec deltas, design-system additions become a
  delta to the design-system spec, and the component map, layout sketch, direction and the
  alternatives you rejected go in `design.md`. The user approves the proposal before `/opsx:apply`.
  Other spec or ADR systems: follow theirs the same way.
- **Everywhere else**: show the plan, then ask with **AskUserQuestion**: *Approve*, *Change
  something*, and in Create mode *Show another direction*.
- Write no UI code before approval. If the user said up front to go ahead or that the plan is
  approved, skip the question, not the plan (step 4's gate). If nobody can answer (headless runs)
  and nothing was approved in advance, stop after the plan and list the open decisions.
- If building shows the plan was wrong, stop and revise it with the user instead of improvising.

## 6. Build from the system

**Components: the reuse ladder.** Take the first rung that fits:

1. use an existing component as it is;
2. use it with its existing props, slots or modifier classes;
3. add a **variant** to it;
4. **compose** existing components into a new one;
5. write a **new component**, only with a one-line reason why 1 to 4 don't fit, placed where the
   design system keeps its components and built on its tokens.

Never copy a component and adjust the copy: two near-copies mean a variant or a component is missing.
Don't wrap a system component just to restyle it; change it at the source or add a variant.

**Start a new web page's layout from this structure** (Create mode, when the project has no layout
system of its own). It holds structure only; color, type and spacing come from the direction. It
makes the common composition mistakes impossible instead of something to catch later: a section
can't leak a decoration into its neighbours or over the header, and an image can't end up almost
full width but short of the edges.

```css
/* every top-level section is a band: one grid with the page margins, 12 named content columns
   (`col 1` … `col 12`), its own stacking context and a clip */
.band {
  display: grid;
  column-gap: var(--gutter);
  grid-template-columns:
    [full-start] minmax(calc(var(--margin) - var(--gutter)), 1fr)
    [content-start] repeat(12, [col] minmax(0, calc((var(--content-width) - 11 * var(--gutter)) / 12)))
    [content-end] minmax(calc(var(--margin) - var(--gutter)), 1fr) [full-end];
  position: relative;
  isolation: isolate;          /* decorations' z-index stays inside the band */
  overflow: clip;              /* nothing the band draws escapes it */
}
.band > * { grid-column: content; }
.band--reach { overflow: visible; }   /* the one element the plan lets cross a boundary; still below the header */

/* the header sits above every band; give it a backing when content scrolls under it (references/depth.md) */
.site-header { position: sticky; top: 0; z-index: 10; }

/* text and media take spans of the 12 columns, or bleed from a column line to an edge */
.span        { grid-column: col var(--from, 1) / span var(--n, 6); }  /* text 1–5: --from: 1; --n: 5 */
.bleed       { grid-column: full; }                                   /* edge to edge */
.bleed-start { grid-column: full-start / col var(--to, 7); }          /* left edge up to (not into) column --to */
.bleed-end   { grid-column: col var(--from, 7) / full-end; }          /* from column --from to the right edge */
.layer       { grid-row: 1; }      /* stack in one cell: a bleed photo with its text on top (text after it in the source) */
:is(.bleed, .bleed-start, .bleed-end) > :is(img, video, picture) { display: block; width: 100%; height: 100%; object-fit: cover; }
@media (max-width: 700px) {        /* phones: media edge to edge, text in the margins, stacked in source order */
  .bleed-start, .bleed-end { grid-column: full; }
  .span { grid-column: content; }
}
```

The plan's spans map straight onto these: "text 1–5, photo bleeding right from 7" is a `.span`
(`--from: 1; --n: 5`) followed by a `.bleed-end` (`--from: 7`) in the same band, and they sit side
by side without overlapping. Columns of text and media never share cells, except a `.layer` pair on
purpose (an opener with its headline on the photo, on a scrim). Never place blocks side by side by
forcing them into one row (`grid-row`) and pushing one over with margins, `calc()` offsets or
`position: absolute`: that overlaps the moment a value is off. Side by side means each block has
its own `.span` or bleed. An opener photo is `.bleed`, or a
half-bleed beside the headline, never a full-width image inside `content`. Decorations are children
of their band and positioned within it.

**Tokens only.** No literal color, font, size, spacing or radius in feature code. When a needed token
doesn't exist, don't invent a name and don't hardcode the value: propose adding it to the token
source (in OpenSpec, as part of the design-system delta) or ask.

**Build what the plan says**: every state in the state table, realistic and worst-case content, the
UX rules in `references/ux.md`, the motion plan with feedback on every interactive element
(`references/motion.md`), the signature moves and the graphic device at full strength, every
section in the layout pattern the plan gave it, every element on the grid and styled from the
concept (`references/composition.md`), objects made as `references/objects.md` says, and icons
fetched from the chosen set, never drawn by hand.

**Fixing** (Fix mode): name the element and exactly what is wrong (position, color, size, overflow,
state), find the component (grep for visible text, classes, nearby labels), find the root cause
(cascade and specificity, inherited color, flex or grid alignment, fixed sizes, stacking context,
overflow, a missing token, an unstyled state), fix the cause with the smallest change, never by
stacking overrides, `!important` or `overflow: hidden` on the page, then check everything else that
uses the component, every breakpoint and theme.

## 7. Design review: look at it and push it

A designer never ships a layout they haven't looked at. This step is yours, not the user's: do it
even when they said they will check the result themselves, and regardless of the validation choice.

- Render it: Playwright (`browser_navigate`, `browser_take_screenshot` with `fullPage`), or
  `npx playwright screenshot --full-page URL FILE`, or headless Chrome
  (`chrome --headless --screenshot=FILE --window-size=1440,900 URL`). Native: a preview screenshot
  test, `adb exec-out screencap -p`, or `xcrun simctl io booted screenshot`. Serve local files over
  HTTP when `file://` is blocked (`python3 -m http.server`). Put the screenshots in the scratch or
  temp directory, not the project.
- Look at the whole page at desktop and phone width, then answer in writing, as in "Design review"
  in `references/validation.md`: would you know the subject with the name covered? What does one
  viewport leave you with? Which section looks like a template? Is the device visible in at least
  three places? Does every image sit on the grid or a viewport edge? Does any object look like a
  placeholder?
- Fix the weakest two things, render again, and repeat once more. Most of the quality comes from
  these two rounds.
- If nothing can render (a sandbox without a browser), say so plainly, review the code against the
  same questions, and list what the user should look at first.

## 8. Validate

Unless the user already gave a standing choice (check memory), ask with **AskUserQuestion** how to
validate this change:

- **Automatic**: Claude renders it and runs the checks in `references/validation.md`.
- **Manual**: Claude gives an exact checklist: where to look, which states and widths, what right
  looks like.
- **Both**: automatic checks, then a short manual list for what automation can't judge.

When the user says to always use one ("always validate automatically", "I always check myself"), save
it to memory, as a project memory when they said it about this project, and from then on use it
without asking, saying so in one line. Without a way to ask (headless) and no saved choice, validate
manually and say so. "I'll check it myself" chooses manual validation; it doesn't skip step 7.

Never call something correct because a screenshot looks fine. Vision models miss most layout bugs;
the deterministic checks come first, and screenshots answer specific questions.

## 9. Report

- What changed and where (`file:line`).
- Every touched component: **reused**, **extended** (which variant) or **new** (why).
- Tokens added, if any.
- What the design review changed.
- The validation result, or the manual checklist.
- Anything you noticed but didn't change.

## Tools

The scripts live in this skill's `scripts/` folder (the base directory is shown when the skill loads):

- `python3 scripts/direction.py [--seed N] [--cards 2]`: deals structural constraints for a
  direction (color strategy, layout spine, grid, graphic device, scale, density, type structure),
  so the plan starts away from your usual answer. See `references/creativity.md`.
- `python3 scripts/contrast.py FG BG [FG BG ...] [--fix] [--min 4.5]`: WCAG ratio and APCA Lc for each
  pair; `--fix` suggests the closest passing color of the same hue; `--palette C1 C2 ...` checks every
  pair of a palette. Use it on every new or changed color pair.
- `python3 scripts/palette.py SEED [--name N] [--neutral] [--shift DEG] [--dark] [--css]`: a 12-step
  OKLCH scale from a seed color (see `references/color.md` for the job of each step), with a
  contrast report; `--neutral` makes a tinted grey from the seed, `--dark` the dark-mode scale.
- `python3 scripts/gradient.py C1 C2 [C3] [--base COLOR] [--grain 0.06]`: CSS for a blurred mesh
  background from palette colors, interpolated in OKLab, with the blur container and grain. Its
  output holds color literals: put it in the token or theme file, or swap the values for tokens.
- `python3 scripts/fonts.py --voice "TAGS" [--role display|text|mono] [--specimen FILE]`: a random draw
  of fitting open fonts with working stylesheet links, leaving out the defaults; `--check FONT …`
  flags overused ones. See `references/typography.md`.
- `python3 scripts/icons.py sets | search QUERY [--set ph] | get SET:NAME … [--sprite]`: real icons from
  open sets as inline SVG (needs network). See `references/icons.md`.
- `python3 scripts/pattern.py KIND [--size] [--stroke] [--color] [--opacity] [--fade]`: exact background
  patterns (dots, grid, waves, contour lines …) as a token-colored mask layer. See
  `references/decoration.md`.
- `python3 scripts/scan.py [PATH] [--tokens GLOB ...] [--summary]`: lists hardcoded colors, font families
  and Tailwind arbitrary values outside the token files. Run it on the files you touched.
- `scripts/page-checks.js`: pass the file's contents as the function of Playwright's `browser_evaluate`;
  it reports overflow, clipped text, small or overlapping targets, low contrast, unnamed controls,
  heading order, icons and dots off the text's cap height, icon sets in use, shadows, bars without
  a backing, broken or blurry images, neighbouring sections with the same layout, sections with
  content on one side and nothing on the other, the scale contrast, and the fonts and colors in use.
  See `references/validation.md`.
- 3D objects and stills: the recipes in the `cinematic` skill's `references/modelling.md`, used as
  `references/objects.md` describes.

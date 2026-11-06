---
name: ui
description: >
  Designs user interfaces the way a product designer does: learn the design system, research the
  subject, plan the flow, states, components and layout, get the user's approval, then build from the
  system and validate the result. Use for any UI work: building or redesigning a page, screen,
  component, layout or theme, adding a UI feature, picking colors, fonts, spacing or motion, fixing
  what a screenshot shows ("this is misaligned", "looks off", "[image #1]"), and reviewing UI or UX.
  Triggers include "ui", "ux", "design", "screen", "page", "layout", "style", "restyle", "css",
  "make it look better", pasted screenshots of an app or site, or /ui.
---

# UI

Design before code. A designer settles who the screen is for, what it must do, which states it has
and which existing parts it is made of before anything visual exists. Claude's habit is the opposite:
going straight to markup and filling every open choice with the most common default. This skill
makes the design explicit, gets it approved, then builds it from the project's own system.

## 1. Pick the mode

| Mode | When | Steps |
|---|---|---|
| **Fix** | something visible is wrong: alignment, overflow, color, a state | 2, then "Fixing" in step 6, 7, 8 |
| **Extend** | a new screen, section or component inside an existing design system | 2, 3 if the domain is unfamiliar, 4, 5, 6, 7, 8 |
| **Create** | a new product, a redesign, or no design system yet | every step |

When unsure between two modes, pick the larger one.

## 2. Learn the system

- Find the source of truth: OpenSpec specs (especially a design-system spec), `DESIGN.md`, theme and
  token files, CSS custom properties, Tailwind config, the component folders or design-system module,
  a Storybook, the project's CLAUDE.md and memory.
- **Inventory** the components and tokens before designing anything. Search by role and by synonym,
  not only by name: button / action / cta / link-button, card / panel / tile / surface, dialog / modal /
  sheet / drawer, banner / alert / notice / toast, badge / chip / tag / pill. Grep for visible text too.
- A deliberate choice in the project wins over everything below. Don't restyle what nobody asked
  about; point it out instead.

## 3. Research the subject

In Create mode, and in Extend mode when the domain or the kind of screen is new to you, load the
`research` skill before planning. Find out who uses this and for what job, how comparable products
solve the same problem, the platform's conventions, and the subject's own vocabulary, materials and
imagery. Distinctive design comes from the subject; without this step the plan falls back to defaults.
In Create mode, use its brainstorming step to produce two or three genuinely different directions.

## 4. Plan

Write the plan with the templates in `references/process.md`:

1. **Brief**: user, job, success signal, constraints, real content.
2. **Flow**: one per user goal, from entry through the main path, branches and error recovery to exit.
3. **States**: ideal, empty, loading, error, partial and extreme content, each with its next step.
4. **Component map**: each region mapped to an existing component, a new variant, or a new component
   with the reason (step 6).
5. **Layout sketch**: an ASCII wireframe per screen (or per breakpoint when they differ), with one line
   on why the hierarchy is the way it is.
6. **Direction** (Create, or when the system leaves it open): follow `references/creativity.md`.
   Write a concept from the subject, generate five spanning the obvious to the unusual, and pick the
   least typical one that fits. Then set 4 to 6 named colors, typefaces and their roles, layout and
   alignment, and the signature moves.
7. **Motion**: the motion tokens, what gives feedback, how states are entered, and the signature
   moment, following `references/motion.md`. In Extend mode, use the system's motion if it has one.
8. **Plan check**: test it against `references/anti-patterns.md` ("would I have produced this for any
   similar brief?"), the ambition check in `references/creativity.md`, and the UX checklist in
   `references/ux.md`. Revise and say what you changed.

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
- Write no UI code before approval. If the user said up front to go ahead without approval, state the
  plan briefly and build. If nobody can answer (headless runs), stop after the plan and list the open
  decisions.
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

**Tokens only.** No literal color, font, size, spacing or radius in feature code. When a needed token
doesn't exist, don't invent a name and don't hardcode the value: propose adding it to the token
source (in OpenSpec, as part of the design-system delta) or ask.

**Build what the plan says**: every state in the state table, realistic and worst-case content, the
UX rules in `references/ux.md`, the motion plan with feedback on every interactive element
(`references/motion.md`), the signature moves at full strength, and none of the patterns in
`references/anti-patterns.md`.

**Fixing** (Fix mode): name the element and exactly what is wrong (position, color, size, overflow,
state), find the component (grep for visible text, classes, nearby labels), find the root cause
(cascade and specificity, inherited color, flex or grid alignment, fixed sizes, stacking context,
overflow, a missing token, an unstyled state), fix the cause with the smallest change, never by
stacking overrides, `!important` or `overflow: hidden` on the page, then check everything else that
uses the component, every breakpoint and theme.

## 7. Validate

Unless the user already gave a standing choice (check memory), ask with **AskUserQuestion** how to
validate this change:

- **Automatic**: Claude renders it and runs the checks in `references/validation.md`.
- **Manual**: Claude gives an exact checklist: where to look, which states and widths, what right
  looks like.
- **Both**: automatic checks, then a short manual list for what automation can't judge.

When the user says to always use one ("always validate automatically", "I always check myself"), save
it to memory, as a project memory when they said it about this project, and from then on use it
without asking, saying so in one line. Without a way to ask (headless) and no saved choice, validate
manually and say so.

Never call something correct because a screenshot looks fine. Vision models miss most layout bugs;
the deterministic checks come first, and screenshots answer specific questions.

## 8. Report

- What changed and where (`file:line`).
- Every touched component: **reused**, **extended** (which variant) or **new** (why).
- Tokens added, if any.
- The validation result, or the manual checklist.
- Anything you noticed but didn't change.

## Tools

The scripts live in this skill's `scripts/` folder (the base directory is shown when the skill loads):

- `python3 scripts/contrast.py FG BG [FG BG ...] [--fix] [--min 4.5]`: WCAG ratio and APCA Lc for each
  pair; `--fix` suggests the closest passing color of the same hue; `--palette C1 C2 ...` checks every
  pair of a palette. Use it on every new or changed color pair.
- `python3 scripts/scan.py [PATH] [--tokens GLOB ...] [--summary]`: lists hardcoded colors, font families
  and Tailwind arbitrary values outside the token files. Run it on the files you touched.
- `scripts/page-checks.js`: pass the file's contents as the function of Playwright's `browser_evaluate`;
  it reports overflow, clipped text, small or overlapping targets, low contrast, unnamed controls,
  heading order and the fonts and colors in use. See `references/validation.md`.

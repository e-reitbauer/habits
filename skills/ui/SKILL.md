---
name: ui
description: >
  Designs, builds, restyles and fixes user interfaces while avoiding the generic "AI-made" look.
  Use for any UI work: fixing what a screenshot shows ("this is misaligned", "why is this text
  white?", "[image #1] looks off"), building or redesigning a page, component, layout or theme,
  picking colors, fonts, spacing or animation, and reviewing UI for polish. Triggers include
  pasted screenshots of an app or site, "ui", "style", "restyle", "design", "layout", "looks
  off", "align", "css", "make it look better", or /ui.
---

# UI Skill

Build UI that looks deliberately designed for this project, not generated. Typical AI design
is the anti-pattern: when a choice is just the common default, pick something that fits the
project instead.

## 1. Learn the project's design first

Before touching anything:
- Find the design source of truth: design docs (e.g. `docs/*SCHEMA*.md`, `DESIGN.md`), theme
  files, CSS variables / tokens, Tailwind config, component library, and the project's
  CLAUDE.md and memory.
- Note the fonts, color tokens, spacing scale, radius, icon set and motion rules in use.
- Reuse existing tokens and components. Never hardcode a color, font or spacing value that a
  token already covers, and don't invent new tokens unless the change needs one.

A deliberate choice in the project wins over the rules below. If the project already chose
Inter, keep Inter. Don't restyle things nobody asked about; point them out instead.

## 2. Fixing what a screenshot shows

1. Name the exact element and what is wrong with it (position, color, size, overflow, state).
2. Find the component: grep for visible text, class names or nearby labels.
3. Find the root cause before editing: cascade/specificity, inherited color, flex/grid
   alignment, fixed sizes, z-index/stacking context, overflow, a missing theme token, or a
   state (hover, focus, active, disabled) that isn't styled.
4. Fix the cause with the smallest change. Don't stack overrides or `!important` on top of a
   rule that is wrong.
5. Check what else the fix touches: other places using the component, other breakpoints,
   light and dark themes, hover/focus states, long text and empty states.

## 3. Anti-AI-look rules

Default rules for new UI and restyles (from research into what makes a site read as AI-generated):

| Don't | Do |
|---|---|
| Inter, Geist, Space Grotesk, Instrument Serif, an italic serif "accent word" | Fonts chosen for the project's character |
| Gradients on backgrounds, text or buttons; colored glows / box-shadows | Flat color, 1px lines |
| Always-dark theme with grey body text | Light + dark following the system, readable text, contrast checked (WCAG AA) |
| Centered hero, badge/pill above the H1, eyebrow labels over headings | Left-aligned hero, headings that stand alone |
| Colored top/left border on cards | Ruled lines, tables, rows |
| Identical icon-card grids | A layout that fits each section's content |
| Decorative "01 / 02 / 03" numbering, "03 / 10" counters | Let order and content speak |
| Stats without a source | Every number links to its source, with a date |
| Text where an image belongs | Real screenshots, real images |
| Em dashes in UI copy | Period, comma, colon |
| Emoji as icons | Plain text or the project's icon set |
| Bounce, blur-in, glow animations | Short, purposeful motion; nothing under `prefers-reduced-motion` |
| Accent color sprinkled everywhere | Accent only on active things: focus, current item, selection, matches |

Also watch for the general template look: everything `rounded-2xl` + `shadow-lg`, glassmorphism
everywhere, purple-to-blue palettes, hover-scale on every card, three-column feature grids,
and filler copy ("Seamless", "Powerful", "Unlock", "Elevate").

## 4. Verify

- Run what the project has: typecheck, lint, build (e.g. `nuxt typecheck`, `npm run build`,
  `tsc --noEmit`).
- Check contrast for any new or changed color pair against its background (WCAG AA: 4.5:1 for
  body text, 3:1 for large text and UI parts).
- Check both themes and `prefers-reduced-motion` when the change touches color or motion.
- Browser screenshots: don't drive Playwright or browser tools unless the project allows it.
  Some projects record in memory that the user checks visuals themselves; follow that. When nothing is
  recorded, ask once before using the browser.

## 5. Report

Say what changed, where (`file:line`), and what to look at in the browser to confirm it,
including any state or breakpoint that needs a manual check. Mention anything you noticed
but didn't change.

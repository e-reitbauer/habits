# Changelog

All notable changes to habits. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- `ui` works like a designer: it learns the design system, researches the subject (through `research`), plans the brief, flows, states, component map and layout, gets approval (as an OpenSpec change where there is one), builds only from existing tokens and components, and asks whether to validate automatically, manually or both. References cover the process, UX rules, the generated-look anti-patterns, motion and micro-interactions, creativity (a concept picked from five, signature moves), color (OKLCH scales, tinted neutrals, harmony, proportion, dark mode, gradients), composition and alignment, typography, icons, decoration, imagery, and depth (shadows, blur, readable bars and text over images). What the user explicitly asks for wins over the skill's guidance.
- `ui` directions start from the subject instead of from what to avoid: the subject's world, a concept in one sentence and its signature moves, then the memory, name and rerun tests. Color starts from a strategy (restrained, committed, full palette, drenched); the page is planned as a sequence of different layout patterns; decoration is one graphic device from a real artifact with a minimum as well as a maximum; photos get roles, ratios and placements (half-bleed, hero and detail, sequence strip); the pale, undecorated "anti-slop" look is listed as a default of its own; examples no longer use the eval subjects.
- `ui` starts new web pages from a structural base: every section is a clipped band with its own stacking context and twelve named content columns, the header sits above all bands, text takes column spans and media bleed from a column line to an edge, so decorations can't leak over the navigation, images can't stop just short of the edges, and blocks sit side by side without overlap hacks.
- `ui` prints the plan before the first file write even when the plan is approved in advance, and always renders and reviews its own work in two rounds, separate from the user's validation choice.
- `cinematic` prints the storyboard before code, builds objects from the subject with modelling recipes, starts from a pinned three.js skeleton (one framed shot per scene with the object kept out of the type area, a light change per scene, resize, pause, render on demand, reduced motion, context loss), keeps the chrome minimal and captions on the scene's calm ground, loads without a percentage counter, and labels its budgets against Google's thresholds.
- `ui` asks less before the model designs: only `process.md` and `creativity.md` are read before planning, the rest when their choice comes up; a real reference, a dealt card (`direction.py`) and rival concepts are optional pushes for when the first idea is the category's default; fonts are chosen by eye for the voice, with `fonts.py` as a fallback; the floors (layout variety, scale, color share, device, motion, made objects) moved from the plan into the design review; the section table keeps spans and the lead. `cinematic` no longer forces six `ui` references and a dealt card before the storyboard. The eval graders that required `direction.py` and `fonts.py` are gone.
- `commit` remembers a standing approval choice when the user says to always approve one way.
- `ui` holds a build to floors as firmly as to bans, so a page can't pass by being tidy and timid: the list of generated looks stays closed until the plan is written and checks template chrome last; `page-checks.js` reports `surface` (the share of the page that is color, gradient, media or neutral) and `motion` (keyframes, scroll-driven and view transitions, running animations, motion libraries), read before any detail in the design review; a subject made of physical things shows at least one made object instead of type alone; the "restraint" advice and the timetable as the only worked concept are gone.
- `cinematic` storyboards give every scene a ground and a light as values, with at least two moods and a peak that looks different from the opening; the skeleton blends `MOODS` (ground, key light, environment, ink) between shots, and `scene-checks.js` reports `groundAndLight` and scrolls instantly, so a page's `scroll-behavior: smooth` no longer keeps it from travelling the story.
- `cinematic` scenes move and look alive: the skeleton's camera flies curves through the shots, slows at each one without stopping and chases the scroll with damping; a visible scene keeps breathing (slow orbit, pointer parallax, float) and renders on demand only for reduced motion; light starts from a warm key, cool fill and accent rim with the environment at about half; each shot sets an arbitrary object pose, and the story has as many scenes as turns instead of five. `modelling.md` adds printed detail (legends, labels, engraving as canvas textures), sound may be a signature moment behind a toggle, `direction.py --surface cinematic` no longer deals restrained color or stepped scale, and `scene-checks.js` waits for the camera to settle before it samples framing and moods.
- `cinematic` grounds are places, not swatches: the skeleton draws a backdrop that darkens overhead with a pool of each mood's light behind the object, storyboards name the ground's form (light pool, patterned floor, gradient), and `modelling.md` covers shadows that sit right (one shadow story, a high shadow light, a fitted shadow camera, the ground's own color, a contact shadow that follows the object) and a floor with a pattern from the subject. The chrome uses real icons from `ui`'s `icons.py`. `scene-checks.js` reports `oneColorGround` and each shadow light's elevation, frustum size and filter.
- `cinematic` loads `ui` first on every run, and both cinematic evals check that it does. Detail shots aim at the detail along its surface normal with a raking light, objects stay inside the frame outside close-ups, a full-screen ground is a deep or muted step of a color rather than the accent at full strength, contact shadows follow the object's bounding box, and markings are checked in the shot that shows them. `scene-checks.js` reports `loudGround` and `objectCropped`.
- `cinematic` shots can `hold`: a detail shot stays still for part of its scroll instead of turning away at once; floors are materials (grain, fibres, wear, roughness) before patterns, and a printed surface stays fine and low in contrast.
- `cinematic` handles places as well as objects: text stays clear of the set, the camera never passes through scenery, sets are compiled before the first scroll, journeys run on smooth curves with a cap on how fast the world passes, `modelling.md` has a craft bar for sets (buildings, trees, water, haze) and `three.md` a triangle budget. Sound only when the user asks or the subject is sound, and a form over a scene gets its own surface. `scene-checks.js` reads the pixels behind text (`textLegibility`), reports the camera inside or against scenery (`cameraClearance`), and measures framing per mesh in front of the camera, so a long subject no longer covers the whole screen. `ui` lists headings with an italic half as a generated tell, `page-checks.js` reports them (`italicInHeadings`), and forms pick from known dates instead of a bare date field.

### Added

- `habits statusline`: how many units the current session has loaded, for a Claude Code status line script.
- `javascript` unit: modules, style, async, pitfalls and verify commands for `.js`, `.mjs`, `.cjs` and `.jsx` files.
- `ui` references for native apps (`native.md`: Compose and SwiftUI rules, theming, screenshot and accessibility testing), product UI (`product.md`: identity at the edges, convention in the middle) and objects without photos (`objects.md`: a ladder from real photos to rendered 3D stills and crafted SVG, with a craft bar); `direction.py` deals structural direction constraints; `page-checks.js` reports neighbouring sections with the same layout, sections with content on one side and nothing on the other (`deadSides`), the page's scale contrast, wide images that stop short of the edges (`nearBleed`), decorations that cover a control or reach out of their section (`controlsCovered`, `decorationEscapes`), and text that overlaps other text or a photo (`contentOverlaps`). Each section in a plan is framed by numbers (grid spans, the lead and its size, empty space and its job, height), so the composition holds even when the page can't be rendered.
- `cinematic` references `modelling.md` (procedural objects, finish, CC0 sources) and `skeleton.md` (shots framed by numbers: `fill` sets how much of the screen the object covers, `shift` where it sits), and `scene-checks.js` (renderer and software-rendering detection, frame times, long tasks, canvas accessibility, and text that sits inside the object's screen area).
- `ui` evals check for what a page has, not only what it avoids (section variety, a graphic device, image placement, crafted objects, a design review), and a new no-photos case, `greenfield-honey-objects`.
- `research` skill: research and brainstorm before large or hard-to-reverse work.
- `cinematic` skill: storyboarded, scroll-driven and 3D experiences with performance budgets, accessible fallbacks and a list of cinematic clichés.
- `ui` tools: `palette.py` (12-step OKLCH scales, tinted neutrals, dark mode), `gradient.py` (blurred mesh backgrounds in OKLab with grain), `contrast.py` (WCAG and APCA contrast, nearest passing color), `scan.py` (hardcoded colors, fonts and arbitrary values), `fonts.py` (a random draw from a catalog of open fonts matched to a voice, leaving out the overused ones), `icons.py` (real icons from open sets, never drawn by hand), `pattern.py` (exact background patterns colored by tokens) and `page-checks.js` (measured checks on a rendered page, including icons off the cap height, bars without a backing and broken or blurry images).
- An eval suite for `ui` in `evals/ui`, with a plain-HTML fixture, openly licensed photos for a greenfield case, and a script that compares the current skill, v0.2.0 and Anthropic's frontend-design.

### Fixed

- The context size read right after a compaction no longer uses the usage from before it, which triggered a false context rot check.

## [0.2.0] - 2026-11-06

### Added

- Secret guard: a hook that blocks `git commit` and `git push` when the changes would record API keys, tokens, private keys or `.env` files. Lines marked `habits:allow-secret` are skipped.
- Context health: units that were loaded long ago are injected again when they next apply, and Claude is asked to run a context rot check as the context grows (`refreshTokens`, `rotCheckEvery`).
- Skills: `versioning` (SemVer, CalVer, build numbers), `branching` (trunk-based, GitHub Flow, Git Flow, release branches), `patterns` (design and architecture), `context` (context rot check), and `new-unit`.
- Units: `typescript`, `python`, `rust`, `swift`, `vue`, `nuxt`, `spring-boot`, `compose-multiplatform`, `docker-compose`, `xcode`, `github-actions`, `postgres`.
- Automatic session names through `habits title`, set with Claude Code's `sessionTitle` hook field.
- `habits install-cli`, help text, and a `status` that says when each unit loads.
- Visible notices when units load or refresh (`notify`).
- Test suite and CI.

### Changed

- Existing units expanded into style guides with conventions, pitfalls and verify commands.
- `ship` now defers to the `versioning` and `branching` skills.

### Fixed

- Resuming a session no longer injects units that are already in its context.
- List values in unit frontmatter keep commas inside `{a,b}` globs.
- An invalid glob in one unit no longer stops every unit from matching.

## [0.1.0] - 2026-11-06

### Added

- First release: daily skills (`commit`, `pr`, `ship`, `ui`, `hygiene`, `secrets`, `dependencies`, `errors`, `units`), units for Kotlin, Gradle, Maven, Android, unit testing, Playwright and OpenSpec, triggered by files, markers, commands or by hand, and the `habits` CLI.

[0.2.0]: https://github.com/e-reitbauer/habits/compare/c566b7b...v0.2.0
[0.1.0]: https://github.com/e-reitbauer/habits/commit/c566b7b

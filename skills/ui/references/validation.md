# Validation

Vision models miss most layout bugs in screenshots and tend to see the layout they intended. So the
order is fixed: things that are measured first, screenshots second and only for specific questions,
self-critique last.

## Design review (step 7 of the skill, always)

This is the designer looking at their own work, before any validation choice. Models believe their
HTML, CSS and SVG came out as intended far more often than it did, so look at the rendered page,
not at the code.

1. Render the whole page at 1440 and 390px (full-page screenshots) and the first viewport at both.
   Native: the preview screenshots or device screenshots. Open them with the Read tool.
2. Write short answers, honestly, as if critiquing someone else's work:
   - **Memory**: what would someone describe an hour after seeing the first viewport? A mood is
     not an answer.
   - **Name**: with the business name covered, which details could only belong to this subject?
   - **Template**: which section looks like it came from a template? Does any layout pattern repeat
     in neighbouring sections? Is there a hairline between every pair of sections?
   - **Device**: where does the graphic device appear, at which scales? Fewer than three places?
   - **Images**: does each one bleed or sit on the grid? Do neighbours differ in size and ratio? Is
     any photo a small box with dead space beside it?
   - **Objects**: does any made object look like a placeholder (`objects.md`, the craft bar)?
   - **Atoms**: do the nav, buttons, inputs and footer belong to this page, or to a component kit?
   - **Plan**: which planned signature move is weaker in the build than in the plan? Does each
     section match its numbers (spans, the lead's size, the empty space and its job)?
   - **Measured**: run `scripts/page-checks.js` and read `deadSides` (content on one side, nothing
     on the other), `sectionRepeats` (neighbours built the same way), `scaleContrast` (5× or more
     somewhere on an expressive page), `nearBleed` (a wide image that stops at the margins),
     `controlsCovered` and `decorationEscapes` (a decoration over the nav or a button, or reaching out
     of its section). Each finding is one of the weakest points.
3. Fix the two weakest points, render again, answer again. Then a second round.

When nothing can render, review against the plan's numbers instead: for every section, read the CSS
and confirm the grid lines, sizes and heights it sets are the ones the plan gave it.
4. Report what the review changed.

Tips for rendering: lazy images may be blank in full-page screenshots; set them to eager or scroll
through first. Delete the screenshots and any `.playwright-mcp/` folder from the project afterwards.

## Automatic

1. **Build and static checks**: the project's typecheck, lint and build. Then
   `python3 scripts/scan.py <touched files>` for hardcoded colors, fonts and arbitrary values, and
   `python3 scripts/contrast.py` for every new or changed color pair. Use the project's token linters
   too when it has them (stylelint `declaration-strict-value`, eslint-plugin-tailwindcss
   `no-arbitrary-value`, detekt compose rules).
2. **Measured checks on the rendered page** (web): open the page with the Playwright tools, then for
   each width (375, 768 and 1440 px, plus any breakpoint the change targets), resize and run
   `browser_evaluate` with the contents of `scripts/page-checks.js`. Every non-empty list is a
   finding: page overflow, clipped text, small or overlapping targets, low contrast, unnamed
   controls, unlabeled fields, missing alt text, heading order, labels above headings, marks off
   the cap height (`marksOffCenter`), bars without a backing, broken, blurry or stretched images,
   boxes with a border plus a soft shadow, images side by side whose edges almost line up,
   images that float off the grid, sections with a dead side (`deadSides`) and neighbouring
   sections with the same structure (`sectionRepeats`). `scaleContrast` should reach the plan's
   lead sizes. `icons` should show one set in one style, and
   `shadows` no more distinct values than the plan's elevation levels. Compare
   `leftEdges` and `rightEdges` with the plan's grid: a few heavily used edges are the axes, and
   every one-off edge is an element to align or justify. Compare `fontsDeclared` and `colorsUsed`
   with the tokens, and run `python3 scripts/fonts.py --check <fonts>` on the fonts in use. Read
   `browser_console_messages`: any error means the page isn't done.
   When the page is served over HTTP and the script is reachable from it, fetching and evaluating
   it inside `browser_evaluate` saves pasting the whole file.
3. **Each state**: trigger empty, loading, error and long-content states (seed data, block a request,
   paste long text) and repeat step 2 where the layout changes. Both themes if the project has two.
4. **Screenshots with questions**: take before-and-after screenshots of the changed area. Answer
   concrete questions, not "does it look good":
   - Is the primary action the most prominent element? Is there exactly one?
   - Does the new part align with the grid and edges of its neighbors?
   - Compared with before: what changed besides the target? Anything that shouldn't have?
   - Does every state from the plan look the way the state table says?
   - Is every icon and dot level with the middle of the capitals beside it? (zoom in on the
     screenshot of that element)
   - Scroll so the busiest content passes under every sticky bar: is its text still readable?
   - Does every image either reach a viewport edge or sit exactly on the grid? Do images side by
     side share their top and bottom edges?
   When you need to point at a spot, describe it by its element, not by pixel guesses.
5. **Critique against the plan**: does the result match the brief, the flow and the state table? Run
   the checklist in `ux.md`. Fix what you find, then repeat the checks the fix touches.

Clean up after the browser tools: they may write logs or snapshots (for example `.playwright-mcp/`)
into the project. Delete them or make sure they are ignored.

**Other platforms**
- Android: `adb exec-out screencap -p > shot.png` (to the scratch or temp directory); layout bounds via
  `adb shell uiautomator dump`.
- iOS simulator: `xcrun simctl io booted screenshot shot.png`.
- Compose: the project's screenshot tests (Roborazzi, Paparazzi, Compose Preview Screenshot Testing)
  or rendered previews; run the token scan over the touched files.
- When a unit for the platform is loaded, follow its verify steps.

## Manual

Give the user a checklist they can follow without guessing:

```
Open:   <URL or screen, and how to get there>
Widths: 375, 768, 1440 (or the devices that matter)
Check:
- <state>: <how to trigger it> → <what you should see>
- <state>: ...
- Keyboard: Tab through <area>; focus is visible on each control and reaches <control>
- <anything automation can't judge: motion, feel, copy tone>
```

Each line states what right looks like, so a mismatch is obvious.

## Reporting

List what was checked, at which widths and states, and every finding with what was done about it.
Say plainly what wasn't checked and why.

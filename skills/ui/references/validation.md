# Validation

Vision models miss most layout bugs in screenshots and tend to see the layout they intended. So the
order is fixed: things that are measured first, screenshots second and only for specific questions,
self-critique last.

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
   controls, unlabeled fields, missing alt text, heading order. Compare `fontsDeclared` and
   `colorsUsed` with the tokens. Read `browser_console_messages` for errors.
3. **Each state**: trigger empty, loading, error and long-content states (seed data, block a request,
   paste long text) and repeat step 2 where the layout changes. Both themes if the project has two.
4. **Screenshots with questions**: take before-and-after screenshots of the changed area. Answer
   concrete questions, not "does it look good":
   - Is the primary action the most prominent element? Is there exactly one?
   - Does the new part align with the grid and edges of its neighbors?
   - Compared with before: what changed besides the target? Anything that shouldn't have?
   - Does every state from the plan look the way the state table says?
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

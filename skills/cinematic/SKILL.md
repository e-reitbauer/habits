---
name: cinematic
description: >
  Designs and builds award-level, cinematic web experiences: scroll-driven 3D scenes, WebGL and
  three.js, shaders, choreographed scroll stories, page transitions and signature interactions,
  with real performance and accessibility. Use when the user asks for an immersive, cinematic,
  award-worthy, "Awwwards", 3D, three.js, WebGL, react-three-fiber, GSAP or scroll-driven site,
  scrollytelling, or "make it an experience". Also consider it when a design concept from the ui
  skill would clearly gain from a cinematic layer, and suggest it before building.
---

# Cinematic

Award-winning sites aren't defined by effects. Judges weight design 40%, usability 30%, creativity
20% and content 10%, and most entries fail on usability and speed rather than imagination. What
wins is one strong idea told like a film: a story in scenes, one signature moment, real content,
and motion with timing and purpose, while it still loads fast and works on a mid-range phone.

Two things decide whether it feels cinematic or generated:
- **Spectacle is the point.** Restraint applies to the interface chrome, not to the scene. The
  peak should be big: a dramatic camera move, an object coming apart, a change of light, scale
  that fills the screen. The budgets in step 5 are what make that affordable, not a reason to play
  it safe.
- **The interface lives in the scene.** Type, navigation, buttons and captions are composed with
  the 3D, the way titles are composed in a film: anchored to the same grid, styled from the
  concept, timed with the camera. A stock landing page laid over a canvas, with labels above its
  headings and a default button, undoes the scene behind it. Each frame is composed so the type has
  its own calm area; captions boxed in dark plates mean the frame wasn't. The chrome stays minimal:
  a wordmark, one action and a quiet chapter indicator, not a website's tab bar of sections.
  Minimal is not bare: controls and facts carry real icons from `ui`'s `scripts/icons.py` (an
  arrow or the subject's own symbol on the action, an icon beside each spec, a chevron on the
  chapter indicator), from one set whose stroke matches the type. A hollow square or
  a dot standing in for an icon is the bare version.

**Load `ui` first, every time.** Before anything else, before reading any reference or writing a
plan, call the Skill tool with `habits:ui`. It is mandatory, not a suggestion: a request that names
only this skill, says "go straight to building" or comes pre-approved doesn't skip it. `ui` holds
the process this skill builds on (system, research, concept, color, motion, approval, design
review), the generated tells the build is checked against, and the tools this skill uses (icons,
palettes, fonts, patterns, contrast). A run without it ships labels above headings and middle-dot
meta lines. Then follow its process and add what's here. Before the storyboard, read
this skill's `references/scroll.md`, `references/three.md`, `references/modelling.md` and
`references/skeleton.md` with the Read tool, and `ui`'s `creativity.md`; open `ui`'s other
references (`color.md`, `typography.md`, `objects.md`, `icons.md`, `decoration.md`) when you make
those choices, and `anti-patterns.md` only afterwards, to check the storyboard and the build, as in
`ui`. The storyboard replaces the `ui` section sequence: a fixed-canvas story is planned in scenes
and shots, not in page sections; if you deal a card, use
`python3 <ui skill>/scripts/direction.py --surface cinematic`. Read `ui`'s `composition.md` and
`imagery.md` only for parts of the page that scroll as ordinary HTML.

**The user decides.** Their wishes and references come first; this skill fills in what they left
open. If they want a particular library, effect or look, build it well, even when it is one of the
clichés below; say so once if you see a better option, then follow their call. When the cinematic
layer is your idea rather than theirs, suggest it in a sentence (what it adds, what it costs in
time and weight) and build it only if they want it.

## 1. Storyboard before code

**The storyboard gate.** The storyboard appears in your reply, together with the `ui` plan, before you
write any page, script or style file. "The plan is approved" or "build it" skips the approval
question, never the storyboard. Writing the scene first and describing it afterwards is not a
storyboard.

Write the experience as scenes, the way a director would:

```
| Scene | Scroll / trigger | What the user sees | Type area | Shot: fill and shift | What moves (camera, objects, type) | Ground and light | Content and message | Interaction |
```

The ground and light column holds values, like the shot: the ground's color and its form, the key
light's color and strength, and the ink the scene's type takes on that ground (the `MOODS` of
`references/skeleton.md`). The form is what makes the ground a place rather than a swatch: a pool
of light behind the object and a darker sky (the skeleton's backdrop), a floor with a pattern from
the subject (a cutting mat, a workbench, a drawing of the object), or a gradient that turns with
the story. One flat color behind the object in every frame is the generated default. A story told on one ground under one light is a product viewer, however
good the object. At least the peak looks different from the opening: the ground drops to dark and
one raking light picks out the object, or the ground takes on the subject's color, or day turns
to evening. Two moods are the minimum, and each change falls on a turn in the story. A ground that
fills the screen stays calmer than what sits on it: a deep shade or a muted tint of the color, not
the accent at full strength. A saturated mid-tone red, orange or magenta over the whole screen
shouts over the object and the type; full chroma belongs to the action and small marks.

The shot column is the `SHOTS` table of `references/skeleton.md`: `fill` is how much of the screen's
width the object covers, `shift` where it sits, on the side away from the type area. A shot with a
fill above about 0.7 is a close-up and carries at most one short line of type, in a band the object
doesn't reach. Frame by these numbers: you may never see a frame before shipping.

- An **establishing** scene that sets the world in the first viewport, quickly.
- **Development** scenes, each with one idea, each revealing something new about the subject.
- One **peak**: the signature moment, the thing people will screenshot or send to a friend.
- A **resolution** that lands on the main action (contact, buy, explore), never on a dead end.

Give the story as many scenes as it has turns: five in every story is a template of its own, and
seven or nine are as normal. In each shot the object takes whatever state that turn needs (a part
opens, layers lift by different amounts, it turns over to show its printed underside), not one
effect switched on and off.

Then name the **camera language** (static, dolly, orbit, crane, push-in, cut)
and how scenes **transition** (continuous camera, match cut, wipe, morph). The camera keeps
travelling: it slows at a shot and rounds it, and stops only when the scroll does. Get the
storyboard approved with the rest of the plan.

## 2. Pick the lightest medium per scene

Use the cheapest tool that achieves the scene, and mix them:

| Medium | Good for |
|---|---|
| CSS, scroll-driven animations, View Transitions | type, layout and image choreography, page transitions |
| SVG | line, diagram and drawing effects, masks |
| Canvas 2D | generative patterns, particles in the thousands, pixel art |
| WebGL / three.js (or react-three-fiber) | real 3D objects and spaces, shaders, light |
| Video or image sequences | photoreal motion that would be too heavy to render live |

A full 3D scene for something CSS could do is a cost with no benefit.

## 3. Art direction for 3D

- **Make the object from the subject**: geometry that belongs to it (a product, a tool, a place, an
  instrument), built with the recipes in `references/modelling.md` (displaced, lathed, extruded,
  bevelled, cut, instanced) or loaded from a CC0 or user-supplied glTF. Default primitives (spheres,
  boxes, torus knots, icosahedra) read as placeholders, and so does a single undeformed primitive
  standing in for the real thing. Check every object against the craft bar in `modelling.md`.
- **Light is the mood**: three points as the start (a warm key with a soft shadow, a cool fill, and
  a rim in the palette's accent that draws the silhouette), an environment (`RoomEnvironment`
  through `PMREMGenerator`, or an HDRI) turned down to about half so it fills in rather than
  flattens, or baked lighting; a contact shadow so objects stand on something, and one shadow story
  (the shadow from a high light, in the ground's own darkened color, following the object when it
  lifts; "Shadows and the floor" in `modelling.md`); tone mapping chosen on purpose.
- **Materials with intent**: one or two hero materials (rough, wet, translucent, printed), not
  shiny glass on everything. Print on the object what the real one carries (legends, labels,
  scales, engraving; `modelling.md`): a blank object reads as a model.
- **Alive while it's on screen**: a slow orbit, the pointer's parallax, parts drifting on their own
  phases, so the scene doesn't freeze between scroll gestures (`references/skeleton.md`).
- **Color from the palette** (`ui/references/color.md`); post-processing (bloom, grain,
  aberration, depth of field) only where it serves the scene, and subtle.
- **Composition**: frame each scene like a still. In the storyboard, name for every scene the area
  of the screen its type occupies (left third, lower band, right column) and keep the object out of
  that area at the scene's key frame and at the transitions into and out of it, at desktop and
  phone sizes; the last scene, with the main action, is where objects drift over text most often.
  Close-ups are the other: when the object fills the frame there is no calm area left, so a close-up
  shot crops the object to one side of the screen and keeps the other side for the type, or carries
  no more than one short line in a band the object doesn't reach.
  Keep the subject readable at phone size. Outside close-ups the whole object stays inside the
  frame with a margin; a crop is a decision the storyboard names, not an accident of `fill`.
  A shot that shows a detail (an engraving, a label, a port, a switch) aims at it: `look` is the
  detail's point, `dir` its surface normal tilted 15 to 30 degrees, `fill` sized so the detail
  itself spans a third of the width or more, and a raking light across it. Engraving reads by the
  shadows in its grooves: seen edge-on by a grazing camera, or face-on under flat light, it vanishes.
  A detail also needs time: it holds still for part of its scroll (`hold` in the skeleton) and
  gets a longer section, or it turns away before anyone has read it.
- **Places, not only objects**: when the scene is a set the camera travels through (a landscape, a
  street, a route), keep the text clear of it in every shot. The camera never passes through or
  grazes the scenery (a tree, a roof, a wall), at a shot or between two; nothing stands between it
  and its look point. Build the set to the bar in `modelling.md` ("Sets").

## 4. Scroll as the timeline

See `references/scroll.md`. In short:
- Scroll drives **progress** through a scene, not only triggers. Scrub with a little smoothing,
  and let the camera chase that progress on a curve with damping rather than sit on it.
- Pin sparingly, and only when the user can tell how long it lasts (progress, chapters).
- Never take scroll away: keyboard, anchors, Back, find-in-page and screen readers keep working.
  Smooth-scroll libraries are optional and must not break them.
- Mobile gets its own choreography, designed for touch and a small, tall screen, not the desktop
  version shrunk.

## 5. Performance is part of the design

See `references/three.md`, and start from the skeleton in `references/skeleton.md` (pinned
versions, resize, a damped camera path, idle life, pause offscreen, reduced motion, context loss,
disposal). Budgets to
design against, stricter than Google's "good" thresholds (LCP 2.5 s, INP 200 ms) on purpose,
because a scene adds load:
- **Load**: LCP under about 2 s, first meaningful content without waiting for WebGL, page weight
  under about 3 MB before optional assets.
- **Frame rate**: a steady 60 fps on a mid-range phone, and no long main-thread tasks while
  scrolling (INP under about 100 ms).
- **No stutter while scrolling**: build every set before the first scroll, show each once and
  compile it (`renderer.compileAsync`, textures through `renderer.initTexture`), so nothing compiles
  or uploads on first view. Things that travel (a train, a car, the camera) move along smooth
  curves, never a polyline or a straight blend between shots, and the world passes the camera no
  faster than the eye can follow: a long jump between two places is a cut or a fade, not scenery
  streaming by at scroll speed.
- Show the HTML content first, then initialize the scene. Pause rendering when it's offscreen or the
  tab is hidden; while it's visible it keeps rendering, because it keeps moving. Render on demand
  only for the reduced-motion still.
- **Loading without a countdown**: the HTML and a poster still of the first scene show at once; the
  scene fades in over the poster when its first frame is ready; heavy assets stream in after the
  first scene is visible. No percentage counter.

## 6. Content and access first

- All text, navigation and actions live in the HTML, readable and usable before and without the
  canvas. The canvas is decoration (`aria-hidden`) or has a text equivalent.
- **Reduced motion**: a composed still or a calm version of each scene, with no camera moves,
  parallax or scrubbing. Still beautiful, not a broken page.
- **No WebGL or a weak device**: a designed fallback (poster image, video or 2D version), chosen
  by capability and measured frame rate, not by user agent.
- Text over moving scenes keeps its contrast at every frame; give it a calm area or its own surface.
  A fixed header over the scene needs a backing once anything scrolls beneath it (a translucent
  surface with `backdrop-filter` blur, or a scrim), checked at the brightest, busiest frame; see the
  ui skill's `references/depth.md`.
- A form over a scene (a booking, a sign-up) sits on its own solid surface, never bare over the
  set, with fields styled from the page's system and labels at 4.5:1 or more; on a phone it gets
  its own place in the flow, not a layer over the scene. Follow `ui`'s `references/ux.md` (Forms).
- No sound unless the user asks for it or the subject is sound (an instrument, a venue, a record).
  Then it sits behind a visible toggle, off until pressed, never autoplays, and is synthesised with
  Web Audio so it adds no weight (`references/skeleton.md`).

## 7. Clichés

These are the generated or template versions of cinematic. Avoid them unless the user asks:
- the particle sphere, orbiting rings, glowing network nodes, starfield or warp tunnel;
- a floating glass blob, torus knot or chrome object with no relation to the subject;
- bloom, chromatic aberration and film grain on everything at once;
- a preloader that counts from 0 to 100%;
- every heading split into letters that slide up; horizontal scroll sections with no reason;
- magnetic buttons, custom blob cursors and image-distortion hovers everywhere;
- scroll hijacking that makes the page feel slower than native.

A loader, cursor or horizontal section is fine when it is part of the story; the cliché is using it
because sites like this usually have one.

## 8. Validate

First the `ui` design review (always): render each scene's key frame at desktop and phone width,
compare it with the storyboard, and push the weakest two scenes, twice. Scroll programmatically to
each scene's progress point before the screenshot.

Then use the validation choice from `ui` (ask, or follow the saved preference). In addition to its
checks:
- run `scripts/scene-checks.js` in Playwright's `browser_evaluate` while scrolling through every scene,
  also with the CPU throttled (CDP `Emulation.setCPUThrottlingRate`, rate 4) and at a phone-sized
  viewport. It first reports which renderer the browser uses: headless browsers usually render WebGL
  in software (SwiftShader), and then frame rates mean nothing; report draw calls, triangles, long
  tasks and the structure checks instead, and say the fps needs a real device. Open the page with
  `?debug` so it also reports `textOverObject`: every point in the scroll where a heading, caption or
  button sits inside the object's screen area. Fix each one by changing that shot's fill or shift;
  a dark plate behind the text is not the fix. `textLegibility` reads the rendered pixels behind
  every piece of text that has no surface of its own and lists where the contrast falls under
  WCAG (4.5:1, 3:1 for large text) or the ground behind it is busy; fix the shot, not the
  text's color alone. `cameraClearance` lists where the camera sits inside or against scenery, or
  something stands between it and the subject. It also reports `groundAndLight`: the ground's color
  and the lights at every tenth of the scroll, and how far they move over the whole story. `flat`
  means the ground never changes and the light moves too little to read as another scene: the
  storyboard's moods are not in the build. `oneColorGround` means each frame's ground is a single
  flat color (no light pool, gradient, pattern or floor). `loudGround` lists the points where a
  saturated mid-tone fills the ground. `objectCropped` lists where the object runs out of the
  frame: right for a close-up, a framing error anywhere else. `shadows` lists each shadow light's lowest
  elevation, how large its shadow camera is against the object, and the filter, with the problem
  each one causes;
- Lighthouse for load metrics;
- the reduced-motion (`browser_emulate_media`) and no-WebGL versions, scene by scene;
- a screenshot of each scene's key frame, checked against the storyboard.

Report the measured numbers, not impressions.

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

This skill sits on top of `ui`: load the `ui` skill too and follow its process (system, research,
concept, color, motion, approval, design review), then add what's here. Before the storyboard, read
this skill's `references/scroll.md`, `references/three.md`, `references/modelling.md` and
`references/skeleton.md` with the Read tool, and from `ui`: `creativity.md`, `color.md`,
`typography.md`, `anti-patterns.md` and `objects.md`. The storyboard replaces the `ui` section
sequence: a fixed-canvas story is planned in scenes and shots, not in page sections, so deal its
constraints with `python3 <ui skill>/scripts/direction.py --surface cinematic`. Read `ui`'s
`composition.md` and `imagery.md` only for parts of the page that scroll as ordinary HTML.

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
| Scene | Scroll / trigger | What the user sees | Type area | Shot: fill and shift | What moves (camera, objects, type) | Light | Content and message | Interaction |
```

The shot column is the `SHOTS` table of `references/skeleton.md`: `fill` is how much of the screen's
width the object covers, `shift` where it sits, on the side away from the type area. A shot with a
fill above about 0.7 is a close-up and carries at most one short line of type, in a band the object
doesn't reach. Frame by these numbers: you may never see a frame before shipping.

- An **establishing** scene that sets the world in the first viewport, quickly.
- **Development** scenes, each with one idea, each revealing something new about the subject.
- One **peak**: the signature moment, the thing people will screenshot or send to a friend.
- A **resolution** that lands on the main action (contact, buy, explore), never on a dead end.

Then name the **camera language** (static, dolly, orbit, crane, push-in, cut), the **lighting mood**
and where it changes,
and how scenes **transition** (continuous camera, match cut, wipe, morph). Get the storyboard
approved with the rest of the plan.

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
- **Light is the mood**: an environment (`RoomEnvironment` through `PMREMGenerator`, or an HDRI)
  plus a deliberate key light with a soft shadow, fill and rim, or baked lighting; a contact shadow
  so objects stand on something; tone mapping chosen on purpose (`modelling.md`).
- **Materials with intent**: one or two hero materials (rough, wet, translucent, printed), not
  shiny glass on everything.
- **Color from the palette** (`ui/references/color.md`); post-processing (bloom, grain,
  aberration, depth of field) only where it serves the scene, and subtle.
- **Composition**: frame each scene like a still. In the storyboard, name for every scene the area
  of the screen its type occupies (left third, lower band, right column) and keep the object out of
  that area at the scene's key frame and at the transitions into and out of it, at desktop and
  phone sizes; the last scene, with the main action, is where objects drift over text most often.
  Close-ups are the other: when the object fills the frame there is no calm area left, so a close-up
  shot crops the object to one side of the screen and keeps the other side for the type, or carries
  no more than one short line in a band the object doesn't reach.
  Keep the subject readable at phone size.

## 4. Scroll as the timeline

See `references/scroll.md`. In short:
- Scroll drives **progress** through a scene, not only triggers. Scrub with a little smoothing.
- Pin sparingly, and only when the user can tell how long it lasts (progress, chapters).
- Never take scroll away: keyboard, anchors, Back, find-in-page and screen readers keep working.
  Smooth-scroll libraries are optional and must not break them.
- Mobile gets its own choreography, designed for touch and a small, tall screen, not the desktop
  version shrunk.

## 5. Performance is part of the design

See `references/three.md`, and start from the skeleton in `references/skeleton.md` (pinned
versions, resize, pause, render on demand, reduced motion, context loss, disposal). Budgets to
design against, stricter than Google's "good" thresholds (LCP 2.5 s, INP 200 ms) on purpose,
because a scene adds load:
- **Load**: LCP under about 2 s, first meaningful content without waiting for WebGL, page weight
  under about 3 MB before optional assets.
- **Frame rate**: a steady 60 fps on a mid-range phone, and no long main-thread tasks while
  scrolling (INP under about 100 ms).
- Show the HTML content first, then initialize the scene. Pause rendering when it's offscreen or the
  tab is hidden, and render on demand when nothing moves.
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
- Sound only on request, with a visible toggle, never autoplay.

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
  a dark plate behind the text is not the fix;
- Lighthouse for load metrics;
- the reduced-motion (`browser_emulate_media`) and no-WebGL versions, scene by scene;
- a screenshot of each scene's key frame, checked against the storyboard.

Report the measured numbers, not impressions.

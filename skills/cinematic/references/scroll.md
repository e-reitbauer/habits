# Scroll-driven stories

## Mapping scroll to scenes

- Give each scene a scroll range and drive everything in it from one progress value (0 to 1).
  Camera, objects and type all read that value, so the scene stays in sync and can be scrubbed in
  both directions.
- Smooth the scrub slightly (GSAP ScrollTrigger `scrub: 0.5`–`1`, or a damped value in the render
  loop) so trackpads and wheels feel continuous; never so much that the page lags behind the hand.
- Ease within the scene: hold on the important frame, move quickly between them. Linear progress
  feels mechanical.
- Snap to scene boundaries only when scenes are discrete chapters, and keep the snap soft.

## Pinning

- Pin when the scene needs the viewport to itself, and show how long it lasts: a chapter marker, a
  progress line, or content that obviously advances.
- Keep pinned stretches short (one to two viewports of scroll per idea). Long pins feel like a
  stuck page.
- Test resize and orientation changes: pinned layouts are where layout shift and jumps appear.

## Native scroll stays native

- Keyboard (Space, Page Down, arrows), anchor links, Back and Forward, find-in-page and screen
  readers must all keep working. Test each.
- A smooth-scroll library (Lenis) is optional. If used, drive it and the scroll animations from one
  loop (`gsap.ticker`), turn it off under reduced motion, and keep `position: sticky` working.
- Never change the scroll distance per wheel tick so much that the page feels slower than a normal
  page.

## Choosing the technology

- **CSS scroll-driven animations** (`animation-timeline: scroll()` / `view()`) for layout and type
  choreography: no JavaScript, off the main thread. Put them behind `@supports
  (animation-timeline: scroll())` and make the page complete without them.
- **View Transitions** for page and state changes (same-document, and cross-document where
  supported); name the elements that should morph.
- **GSAP + ScrollTrigger** for complex timelines, pinning and syncing with WebGL.
- **three.js / react-three-fiber**: read the scroll progress in the render loop and set the camera
  and uniforms from it; use a camera path (a curve) rather than many hand-written tweens.

## Mobile

- Design the phone version as its own storyboard: tall frames, thumb-reachable actions, fewer and
  lighter scenes, larger type.
- Account for the browser chrome collapsing (`svh`/`dvh` units) and for momentum scroll.
- Replace hover-driven moments with tap or scroll-driven ones on purpose.

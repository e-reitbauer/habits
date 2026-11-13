# Motion and micro-interactions

Motion is part of the design, not decoration added at the end. A static interface with no feedback
is as much a default as one where everything fades in. Designers plan motion as a small system: what
moves, why, how fast, and with which curve, and they give the product one or two moments people
remember.

## What motion is for

Every animation has one of these jobs. If it has none, cut it.

| Job | Examples |
|---|---|
| **Feedback**: the system heard you | press and hover states, a toggle that slides, a button that confirms, a count that ticks up |
| **State change**: something is now different | a mode switch, loading to loaded, an item added to a list, an error appearing |
| **Continuity**: where things came from and went | a card expanding into its detail, a panel sliding from the edge it belongs to, a list item moving to its new place |
| **Relationship and hierarchy**: what belongs together, what comes first | children following their parent, a short stagger that sets reading order |
| **Signifier**: how to interact | a sheet that peeks to show it can be dragged, a handle that nudges |
| **Delight**: the memorable moment | completing the main task, the first open, a success state that is worth a second of attention |

## The motion system

Define it as tokens next to the other design tokens, then use only those.

**Durations** (scale them to distance and size; small things move faster):
- Micro feedback (press, hover, focus, toggles): 100–150 ms
- Small state changes (menus, tooltips, chips, inline validation): 150–250 ms
- Panels, dialogs, sheets, expanding cards: 250–400 ms
- Page or view transitions: 300–500 ms
- The signature moment: up to about 1 s, once

**Easing**:
- Entering and responding: ease-out (fast start, soft landing). Default for almost everything.
- Leaving: ease-in, and shorter than the entrance.
- Moving across the screen: ease-in-out.
- Linear only for progress, loops and things tied to the pointer or scroll.
- Prefer a custom curve over the keyword (for example `cubic-bezier(0.2, 0, 0, 1)` for standard,
  a stronger deceleration for entrances). Springs for anything the user drags or flings.

**Frequency rule**: the more often an interaction happens, the shorter and quieter its motion. An
action done a hundred times a day gets 100 ms of feedback or nothing. Keyboard-driven actions and
typing get no animation. Rare, meaningful moments can afford more.

## Micro-interactions

Design each one deliberately with Saffer's four parts:

1. **Trigger**: what starts it (a tap, a hover, a system event like "upload finished").
2. **Rules**: what happens and what can't happen.
3. **Feedback**: what the user sees, hears or feels so they understand the rules. Every interactive
   element has feedback for hover (where there is a pointer), press, focus and disabled.
4. **Loops and modes**: what changes on repeat, over time, or the second time ("first like plays
   the full animation, later ones a short pulse").

Then give the product **one or two signature micro-interactions** that come from the concept (see
`creativity.md`): the way its main action confirms, the way its key object moves. That is where a
product becomes recognizable. A booking app might drop the chosen slot into a ticket; a library site
might stamp the due date onto a borrowed book.

## Choreography

- When several things move, they move as a group with a lead: the parent first, children follow with
  a short offset (30–80 ms between items, at most about 5 steps before the rest appear together).
- One direction per transition. Things enter from where they live and leave the way they came.
- Don't animate more than one thing that competes for attention at a time.
- Page load: on an expressive page one orchestrated sequence that reveals the hierarchy; on a
  product screen nothing. Never the same fade-and-slide on every section.
- Scroll-linked motion is tied to the content: progress, a reveal, the device or the object
  answering the scroll, parallax with a reason. Never on body text.

## Craft

- Animate `transform` and `opacity`. Avoid animating layout properties (width, height, top, margin).
- Never `transition: all`; list the properties.
- Animations are interruptible: a new input takes over from the current state, it doesn't wait.
- Don't enter from `scale(0)`; start around 0.9–0.95 with opacity.
- Content is complete and readable without any animation (late-loading scripts, disabled motion,
  unsupported features). Progressive features such as View Transitions or scroll-driven animations
  go behind `@supports` or a feature check.
- `prefers-reduced-motion: reduce` means less motion, not none: keep fades and color changes that
  carry meaning, remove movement, parallax, zoom and autoplay.
- Nothing blinks or flashes more than 3 times a second. Long-running motion next to content has a pause.

## Plan it

In the plan's direction, write a motion line: the motion tokens (durations and curves), what gets
feedback, the transitions between states, and the signature moment. In the state table, say how
each state is entered.

## The floor

An expressive page that ships with hover transitions and nothing else has no motion design, however
complete its motion plan was. The build has at least the opening sequence or one scroll-linked
sequence, and the signature moment. `scripts/page-checks.js` reports what it finds as `motion`;
when everything except `controlsWithTransition` is zero, the plan didn't reach the page. Product
screens need feedback and state transitions only.

## Avoid

- Down-time animation that only fills a wait the system could skip.
- Motion that fights for attention, creates urgency or blocks the user.
- Animating everything the same way, which is no better than animating nothing.
- Removing all motion to look restrained: feedback and continuity are usability, not decoration.

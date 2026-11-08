# Design plan: templates and a worked example

Fill in only what the mode needs (see the skill's step 1). Keep every part short: the plan is for
deciding, not for documenting.

## Templates

**Brief**
```
User:        who, in what situation (device, time pressure, expertise)
Job:         what they are trying to get done, in their words
Success:     how they and we know it worked
Constraints: platform, design system, accessibility, performance, legal, scope
Content:     the real content and its extremes (longest name, biggest number, empty)
```

**Flow** (one per user goal)
```
Goal: ...
Entry:    where the user comes from
Main:     step → step → step
Branches: what can differ (no data yet, partial permission, second visit)
Errors:   what can fail and how the user recovers
Exit:     where they end up, and what they see that confirms success
```

**State table**
```
| State      | What the screen shows | Next step for the user |
| ideal      |                       |                        |
| empty      | first use / no results / filtered to nothing (each differs) |  |
| loading    | under 1 s: nothing; 1-10 s: indicator; over 10 s: progress |  |
| error      | what failed, what still works |                  |
| partial    | some data, slow parts, offline |                  |
| extreme    | very long text, 1 item, 1000 items, missing images |    |
```

**Component map**
```
| Region          | Component            | Rung (reuse / props / variant / compose / new + reason) |
```

**Layout sketch**: ASCII per screen, with the reading order and the one primary action marked.
```
+--------------------------------------+
| Logo        Nav ............ Account |
+--------------------------------------+
| H1 (what this is)                    |
| one-line context                     |
| [Primary action]   secondary link    |
+--------------------------------------+
```
Then one line: why this hierarchy (what the user must see first, and why).

**Direction** (Create mode; see `creativity.md`)
```
World:      seven artifacts, systems, places or rituals of the subject, each with its visual trait
Ruts:       the category default, and its predictable opposite
Reference:  the one primary real-world reference and the three traits taken from it;
            secondary references and the one detail each contributes
Card:       the direction.py seed and the card kept (values rejected, with the brief's reason)
Concepts:   five one-liners from obvious to unusual, each with how typical it is; the pick and why
Concept:    the chosen one, in one sentence
Scene:      one sentence of physical scene (who, where, under what light) and the light or dark ground it implies
Colors:     the color strategy; 4-6 named values with roles (ink, surface, field, accent, ...) and
            where each covers the page, contrast-checked
Type:       voice tags; the fonts.py candidates considered; families and roles, scale, weights
Device:     the artifact it comes from, its kind, its large instance and its echoes (at least three places)
Objects:    each object the page shows without a photo, and the rung of objects.md that makes it
Images:     the photo plan: role, ratio, pattern, focal point, section (imagery.md)
Icons:      the set and weight matched to the type, where icons appear; or none
Depth:      what floats, shadow levels, how bars over content stay readable
Signature:  the structural move and the signature interaction that express the concept
From:       which fact about the subject each choice comes from
```

**Sections** (the page as a sequence, each framed by numbers; see `composition.md`)
```
| # | Section | Layout pattern | Spans (text / media, bleed) | Lead and its size | Space and its job | Height | What changes from the previous one |
```

**Motion** (see `motion.md`)
```
Tokens:     durations (micro / small / panel / page) and curves (enter / exit / move)
Feedback:   what answers hover, press, focus, and how
States:     how each state in the state table is entered and left
Signature:  the one moment worth more than 400 ms, if any
Reduced:    what remains under prefers-reduced-motion
```

**Plan check**
- For each choice in the direction and layout: would I have made it for any similar brief? If yes,
  either justify it from the subject or replace it, and say what changed.
- The memory, name and rerun tests in `creativity.md`. Could someone guess this direction from the
  category alone, or from the category plus "avoid the AI look"? Then rework it.
- Does the plan match the anti-slop look (`anti-patterns.md`, number 6): pale neutral page, one
  accent, every section split in two, hairlines, no device? Then change the color strategy, the
  section sequence or the device.
- Run the UX checklist in `ux.md` over the flow and the state table.
- Count the primary actions per screen: exactly one.

## Worked example

Request: "add online booking to our physiotherapy practice's site" (Extend: the site has a design
system with buttons, cards called `tile`, a form field component and a notice component).

```
Brief
User:        existing and new patients, mostly on phones, often in pain, some older
Job:         book a first or follow-up appointment with the right therapist without calling
Success:     a confirmed slot and a confirmation email; fewer phone bookings
Constraints: existing design system; WCAG AA; no account needed; the practice software's API gives
             free slots per therapist per day
Content:     6 therapists, 3 treatment types of 30/45/60 min, slots up to 4 weeks ahead,
             names up to ~30 characters

Flow: book an appointment
Entry:    "Book online" from any page header, or a therapist's profile (pre-selects them)
Main:     treatment → therapist (or "anyone") → day → time → contact details → confirm
Branches: coming from a profile skips the therapist step; "anyone" shows the earliest slots first
Errors:   slot taken meanwhile → say so, keep details, show the next 3 free slots; API down →
          phone number and opening hours
Exit:     confirmation screen with date, time, address, cancel link; email with the same

States
| ideal   | days with free slots marked; times as large buttons | pick a time |
| empty   | no slot in the next 4 weeks for this therapist | offer "anyone" or the waiting list |
| loading | slots load per day: inline indicator in the time list only | none needed |
| error   | API down: booking replaced by phone and hours | call |
| extreme | 30-character names wrap; 40 slots in a day group by morning and afternoon | |

Component map
| Step header          | existing heading styles          | reuse    |
| Treatment choice     | tile                             | props (selectable) |
| Time buttons         | button                           | variant: "slot" (fixed width, 44 px tall) |
| Day picker           | none fits                        | new: DayStrip, a horizontal list of 14 days; a full calendar is too dense on a phone |
| Contact fields       | form field                       | reuse    |
| Slot-taken message   | notice                           | reuse (warning) |

Layout (phone)
+---------------------------+
| ← Back   Step 3 of 5      |
| Choose a day              |
| [Mo 3][Tu 4][We 5] → ...  |
| Morning                   |
| [08:00] [08:45] [09:30]   |
| Afternoon                 |
| [14:00] [15:30]           |
+---------------------------+
Why: one decision per step for people in pain on a phone; progress shown because the flow is 5 steps.
```

Plan check: the stepper and the slot grid are what every booking tool does, and they are kept on
purpose here (Jakob's law: patients know them). No direction step: the site's system already sets it.

## A weak plan, for contrast

```
Make a modern booking page with a hero, a calendar and a form. Use cards for the therapists and a
gradient button. Add nice animations.
```

It names no user, job or states. "Modern", "nice" and "gradient" are defaults, not decisions. It
invents components (cards, gradient button) instead of mapping regions to the existing system.

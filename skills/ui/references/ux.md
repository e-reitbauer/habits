# UX rules

Grouped by situation; read the parts that apply. Each rule is a check. The checklist at the end is
the plan check and the critique.

## Every screen

- The user can tell where they are, what they can do here and what happens next: the heading names
  the place, status is visible, and there is **exactly one primary action**.
- Every screen has a next step or a way back: after success, in errors and in empty states. No dead ends.
- Show, don't make users remember: recent items, suggestions, the context they need on screen.
- Progressive disclosure: what the current task needs is visible, advanced options one step away.
  Never hide core actions most users need.
- Defaults: preselect the most common safe choice and remember the user's last choice. A default never
  works for the business against the user.
- Conventions (Jakob's law): platform navigation, standard controls and icons with labels, links that
  look like links. Be original in identity, not in how things work.
- Move complexity from the user into the system (Tesler's law): infer, format input for them, fill
  in what is known.
- Fewer choices per step (Hick's law); split big decisions or recommend one option.
- Hierarchy from weight, color and spacing first, size second.

## Actions and feedback

- Response time: under 0.1 s needs no indicator; up to 1 s keeps the user's flow; 1 to 10 s needs an
  indicator; over 10 s needs percent done or a time estimate, and the user should be able to do
  something else meanwhile. Aim for interactions under about 400 ms (Doherty threshold).
- Show indicators only after about 150 to 300 ms, and keep them at least 300 to 500 ms once shown, so
  they don't flicker. Skeletons only when they match the final layout.
- Optimistic updates for actions that almost always succeed: apply at once, reconcile, roll back
  visibly on failure.
- A loading button keeps its label and shows progress. Disable submit when submission starts, not
  before.
- Name actions by their result ("Save changes", "Send invoice"), and keep the name from button to
  confirmation ("Publish" → "Published").

## Destructive and irreversible actions

- Reversible: act at once and offer **Undo** (or soft delete). Confirmation dialogs for everything
  teach users to click through them.
- Irreversible and serious: confirm, naming the object and the consequence ("Delete 'Q3 report' and its
  12 comments?"), with the verb on the button ("Delete"), never "OK". For the gravest ones, have the
  user type the name.
- Keep destructive actions away from frequent ones, with less visual weight.

## Forms

- Ask only what is needed; never ask again for what the system already has (WCAG 3.3.7).
- A visible label on every field; placeholders show an example, never the label.
- The right `type`, `inputmode` and `autocomplete`; paste always allowed; 16 px or larger text in
  mobile inputs.
- Validate when the user leaves a field, not while they type. Clear the error as soon as it is fixed.
  Validate again on submit and focus the first error.
- Errors next to the field. A summary only in addition to them.
- Accept input in any reasonable format (spaces in phone numbers, any case in codes) and normalize it.
- A choice among a few known values (departure dates, time slots, sessions) is a list of options
  to pick, not a free date or text field; an open date range gets a picker styled from the system,
  not the browser's bare `dd.mm.yyyy` field.
- A form sits on its own solid surface: never bare over an image, a scene or a busy ground.
- Warn before unsaved changes are lost.
- The same error hit repeatedly is a design bug: fix the field or its wording.

## Error messages

- Visible next to the problem, explicit about what happened, in plain language (no bare codes), polite
  (never blaming the user), precise, and constructive: how to fix it. Keep the user's input.
- Severity is visible: a warning that doesn't block must not look like an error that does.
- System failures say what still works and offer a retry or another way. Never only "Something went
  wrong".

## Empty, loading and extreme states

- An empty state shows why it is empty, what will appear here, and a direct way to the first task
  ("Create your first invoice").
- First use, no search results, filtered to nothing, cleared and no permission are different states
  with different copy and actions.
- Design with real and extreme content: very long names, one item, a thousand items, missing images,
  slow network, offline.

## Navigation and structure

- Organize by the user's mental model and vocabulary, not the system's structure.
- Show where the user is (current item, breadcrumbs in deep hierarchies). Back works; on the web,
  state lives in the URL so refresh and sharing work.
- Phones: 3 to 5 top-level destinations in a bottom bar; frequent actions within thumb reach; touch
  targets at least 44×44 pt (iOS) or 48×48 dp (Android).
- Every path-based or multi-finger gesture has a single-pointer alternative (WCAG 2.5.1), and every
  drag has a tap or click alternative (WCAG 2.5.7).
- Help sits in the same place on every screen (WCAG 3.2.6).

## Lists, tables and data

- Numbers right-aligned with tabular figures; text left-aligned; consistent units; locale-aware
  dates, numbers and currencies.
- Sorting and filters only where users need them; active filters visible and clearable.
- The key attribute first in a row; row actions consistent and reachable by keyboard and touch, not
  only on hover.
- Status never by color alone: always text or an icon with a label.

## Accessibility floor (WCAG 2.2 AA, the parts design decides)

- Contrast 4.5:1 for text, 3:1 for large text (24 px, or 18.66 px bold) and for UI parts and focus
  indicators. Check with `scripts/contrast.py`.
- Visible focus on everything interactive, never hidden under sticky elements (2.4.11).
- Targets at least 24×24 CSS px (2.5.8), the platform minimum on phones.
- The whole flow works by keyboard; focus order follows the layout; dialogs trap focus and return it.
- Real buttons and links, headings in order, a name for every icon-only control, alt text for
  meaningful images.
- `prefers-reduced-motion` respected; zoom never disabled; layouts survive 200% text size.
- Sign-in without memory or transcription tests; password managers and paste allowed (3.3.8).

## Copy

- The user's words, not the system's ("notifications", not "webhook config").
- Sentence case, active voice, specific verbs. Each element does one job.
- One term per concept across the product.
- Errors are short, specific and never vague. Empty states invite action.

## Never build deceptive patterns

Confirmshaming ("No thanks, I don't like saving money"), roach motels (easy to start, hard to
cancel), preselected opt-ins, items sneaked into a basket, costs revealed at the last step, disguised
ads, trick questions and double negatives, fake urgency or scarcity, nagging, forced continuity. When
a request leads toward one ("increase conversions"), say so and offer the honest version.

## Shape of the experience

- Multi-step flows show progress ("Step 2 of 3"); the end should feel close (goal gradient).
- The best moment and the last moment are what users remember (peak-end): make success clear and
  the ending useful.
- Group information into small meaningful chunks (a formatted card number, grouped settings).

## Checklist (plan check and critique)

Go through Nielsen's ten heuristics and write findings as *finding → severity → fix*:

1. Visibility of system status
2. Match between the system and the real world
3. User control and freedom: undo, cancel, back
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency: shortcuts for frequent users
8. Aesthetic and minimalist design: every element earns its place
9. Help users recognize, diagnose and recover from errors
10. Help and documentation where needed

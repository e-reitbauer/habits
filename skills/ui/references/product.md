# Product UI: identity at the edges, convention in the middle

Apps, dashboards, settings, admin tools and data-dense screens are used, not visited. People come
back to them every day and expect them to work like everything else they use. Distinctive product
design (Linear, Stripe, Things, Raycast) is distinctive in a few chosen places and strictly
conventional everywhere else. Running the full expressive direction (five concepts, the least
typical one, a graphic device everywhere) on a settings page makes it worse.

## Where identity goes

- The typeface, or one display face for headings and empty states beside a highly legible text face.
- One signature accent color, used for the primary action, selection and focus.
- The icon style (`icons.md`), the logo, the app icon.
- Onboarding, first run, empty states and success moments: here an illustration, a made object
  (`objects.md`) or the graphic device can carry the brand.
- Motion personality: how panels arrive, how the main action confirms (`motion.md`).
- The theme itself: a small set of inputs (base, accent, contrast) that generates every surface in
  OKLCH, so light, dark and high-contrast themes come from one system.

Deal only the product axes: `python3 scripts/direction.py --surface product`.

## Where convention rules

Tables, forms, settings, navigation, menus, dialogs, toasts, search, keyboard shortcuts, scroll
behavior and text fields look and act the way users already know. Be original in identity, never in
how these work (`ux.md`).

## Rules

- **Chrome recedes, content leads.** The sidebar and toolbars sit a step quieter than the content
  area; fewer dividers, softer separators; structure is felt more than seen.
- **Color restraint.** Tinted neutral surfaces stepped evenly in OKLCH, one accent, status colors
  always paired with a text label or icon.
- **Hierarchy without size inflation.** Dense screens use two or three text sizes; hierarchy comes
  from weight and the text color tokens (primary, secondary, tertiary). De-emphasise secondary data
  instead of bolding primary data; labels are quieter than values.
- **Fewer icons.** Keep them where they speed recognition (object types, statuses, actions); no
  colored icon tiles.
- **Tables**: numbers right-aligned with tabular figures and consistent decimals, text left-aligned,
  never centered; headers aligned like their column; the unit once in the header; no zebra stripes,
  light horizontal rules at most; row height tiers of about 32, 40, 48 and 56px; cells middle-aligned
  up to about three lines, then top-aligned.
- **Density** is value per space and per second: every element carries information or necessary
  structure. Offer compact and comfortable density as a setting when users differ.
- **Keyboard first**: every action reachable by keyboard, shortcuts shown in menus and tooltips, a
  command palette (⌘K) for apps with many actions, Enter submits single-field forms, ⌘/Ctrl+Enter
  submits text areas, focus rings never hidden under sticky bars.
- **States**: empty, sparse, dense, loading, error and long content are designed; skeletons match the
  final layout; optimistic updates with Undo for reversible actions instead of confirmations.
- **The URL holds state**: filters, tabs, sorting and pagination survive refresh and sharing; Back
  restores scroll position. Items that open more end with an ellipsis ("Rename…").
- **Motion**: under about 300ms (around 180ms for most), ease-out, press feedback around
  `scale(0.97)`, popovers grow from their trigger, no animation on keyboard-driven or very frequent
  actions, fades only under reduced motion.

## Validate

At 1280, 1440 and 1920px and at 50% zoom; a keyboard-only walkthrough (Tab, ⌘K, Esc); every state
rendered (empty, error, a thousand rows, very long strings); the checks in `validation.md`.

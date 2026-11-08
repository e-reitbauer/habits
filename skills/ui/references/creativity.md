# Creativity: from correct to memorable

Language models collapse toward the most typical answer, and different models collapse toward the
same one. Avoiding the generated look only removes the most typical result; the next most typical
one is "tasteful and safe": correct, restrained, forgettable. Worse, steering away from a known look
produces a new shared look: when every run avoids cream and serif, every run lands on the same cool
grey page with a sans and one red accent. A good designer gets past all of these the same way:
starting from the subject, borrowing from one real reference, letting an outside constraint push
the first idea somewhere else, and then committing.

Use this in Create mode, and in Extend mode when the system leaves the identity open. On product
surfaces it applies to the edges only (`product.md`). Creativity goes into identity, content and
signature moments. Usability stays conventional (see `ux.md`): people should be surprised by how it
looks and feels, never by how it works.

## 1. Mine the subject's world

Before colors and fonts, list **seven things from the subject's world that its audience knows by
heart**: objects, materials, printed matter, signage, places, tools, rituals, measurements,
vocabulary, what insiders notice that outsiders don't. Concrete things with visual properties, not
moods.

- A municipal swimming pool: lane ropes and their colored floats, the tiled pool floor with its
  black lane lines, the depth numbers painted on the edge, the changing-room locker tags on rubber
  bands, the timetable of lane hours, chlorine-blue water against wet concrete, the clock with the
  sweeping second hand.
- A bookbinder: marbled endpapers, head bands, linen thread, the bone folder, gold tooling on a
  spine, the press, signatures folded and stacked.

Then write two lines:
- **The category default**: the page every business of this kind already ships (for a pool: a photo
  slider of happy swimmers, blue and white, opening hours in a table).
- **Its predictable opposite**: what you get by avoiding that default (for a pool: a dark,
  minimal "premium spa" page). Both are ruts. If someone could guess your direction from the
  category alone, or from the category plus "avoid the AI look", rework it.

## 2. Pick one primary reference

Choose **one real artifact** as the primary reference, ideally from outside the web: a poster series,
a timetable, a field guide, a ticket, a manual, a map, a packaging range, a shop sign, a printed
program. Name it and the three traits you take from it (its grid, its type, its color, its way of
labelling). Secondary references may each contribute **one bounded detail**. Mixing several
references equally averages them into the safest middle; synthesis means choosing and adapting.

## 3. Deal a constraint from outside

Run `python3 scripts/direction.py`. It deals two cards of structural constraints: how color is spent,
what leads the layout, the grid, the kind of graphic device, the scale contrast, the density and how
the type is organised. Keep the card that fits the brief better and fill every value from the
subject. A value may be rejected only with a reason from the brief ("drenched color would hide the
clinic's warnings"), and then that axis is dealt again with another seed. The card is how the plan
escapes your first idea; the subject is what makes it specific. Name the seed and the card in the
plan.

## 4. Write the concept, diverge, then choose

Write the **concept**: one sentence that says what this design is, built from something true about
the subject, the reference and the card. Every later decision should express it.

- Weak: "a modern, clean site for a public pool."
- Strong: "the pool's lane timetable as the page: each section is a lane with its hours, the
  colored float ropes divide the sections, and the depth numbers set the scale of the headings."

Your first concept is the most probable one, so don't stop there:

- Write **five concepts** that span the whole range, from the obvious to the unusual, each with a
  one-line rationale and your honest estimate of how typical it is (how likely any designer, or any
  model, would land on it).
- Include at least one built on a **far analogy**: borrowed from outside the web, such as signage,
  packaging, a printed program, a map, a tool, an instrument panel, a game. Analogies that are far
  but still related raise novelty; ones that are too far stop helping, so keep a real link.
- Drop concepts that fight the brief or the users' job. From the rest, pick the **least typical one
  that still clearly fits**, or present two or three to the user (step 5 of the skill).
- Don't take inspiration from the tools the audience operates (a terminal for developers, a
  spreadsheet for accountants): it comes back as a costume. Take it from their world around the work.
- A subject association is not a reason by itself: "books want a serif", "tech wants mono", "spa
  wants beige" are the associations to question.

## 5. Commit with signature moves

A concept only shows when it changes something visible. Choose a few **signature moves** and make
them decisively; timid versions of good ideas read as defaults.

- **One structural move**: a layout, typographic system or navigation idea that comes from the
  concept (sections as lanes, an index styled like a bookbinder's sample card, the schedule as the
  hero).
- **One graphic device** from the subject, repeated at several scales (`decoration.md`).
- **One signature interaction**: the micro-interaction people remember (see `motion.md`).
- **Material**: real imagery, made objects, texture or data from the subject rather than stock and
  icons (`imagery.md`, `objects.md`). Where there are no assets, design with type, color, shape and
  made objects so the absence doesn't show.
- **Contrast**: commit to clear extremes in scale, weight, color and density somewhere. Pages that
  keep every value in the middle feel generic even when every value is correct.
- **Commit every atom**: navigation, buttons, inputs, links, captions and the footer are built in
  the concept's vocabulary. A stock component inside a committed page is a lapse.

Everything else stays quiet so the signature moves carry. Restraint means fewer bold moves, not
smaller ones, and not fewer of them than one per view.

## 6. Check for ambition, not only correctness

After the plan check against the anti-patterns, ask:

- **The memory test**: if someone left after one viewport, what would they describe an hour later?
  If the honest answer is a mood ("clean", "calm", "modern"), the concept hasn't committed yet.
- **The name test**: cover the business name. Could the page belong to any other pool, shop or app
  in its category? Then the concept isn't visible yet.
- **The rerun test**: if you got a similar brief tomorrow, would you arrive at much the same page?
  Change the parts you would repeat.
- What would someone screenshot or tell a friend about? If nothing, add or sharpen a signature move.
- Would a studio known for distinctive work show this in its portfolio? What would it change?
- Is anything bold only in the plan but timid in the build?

Then build, look at the result in the design review (step 7 of the skill), and push the one or two
places that fell flat.

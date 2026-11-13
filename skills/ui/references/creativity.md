# Creativity: from correct to memorable

Language models collapse toward the most typical answer, and different models collapse toward the
same one. Avoiding the generated look only removes the most typical result; the next most typical
one is "tasteful and safe": correct, restrained, forgettable. Worse, steering away from a known look
produces a new shared look: when every run avoids cream and serif, every run lands on the same cool
grey page with a sans and one red accent. A good designer gets past all of these the same way:
starting from the subject, finding the idea in it, and then committing hard. Process doesn't make
a page distinctive; a specific idea carried all the way through does.

Use this in Create mode, and in Extend mode when the system leaves the identity open. On product
surfaces it applies to the edges only (`product.md`). Creativity goes into identity, content and
signature moments. Usability stays conventional (see `ux.md`): people should be surprised by how it
looks and feels, never by how it works.

## 1. Mine the subject's world

Before colors and fonts, note **the things from the subject's world that its audience knows by
heart**: objects, materials, printed matter, signage, places, tools, rituals, measurements,
vocabulary, what insiders notice that outsiders don't. Concrete things with visual properties, not
moods. A handful is enough when one of them already holds the idea.

- A municipal swimming pool: lane ropes and their colored floats, the tiled pool floor with its
  black lane lines, the depth numbers painted on the edge, the changing-room locker tags on rubber
  bands, the timetable of lane hours, chlorine-blue water against wet concrete, the clock with the
  sweeping second hand.
- A bookbinder: marbled endpapers, head bands, linen thread, the bone folder, gold tooling on a
  spine, the press, signatures folded and stacked.

## 2. Write the concept

Write the **concept**: one sentence that says what this design is, built from something true about
the subject. Every later decision should express it.

- Weak: "a modern, clean site for a public pool."
- Strong, led by a color and a pattern: "the pool floor as the page: chlorine-blue tile fills the
  opener, the black lane lines run down the whole page as its column rules, and the depth numbers
  painted on the edge set the scale of the headings."
- Strong, led by an object: "the book taken apart: a made book block opens section by section down
  the page, marbled endpaper fills the bands between them, and the index is a sample card of spines."

The examples in these references show the method, not a repertoire. A concept that reuses one of
them for another subject (lanes, a timetable, a ticket, a sample card) is a default like any other;
so is the same kind of device two briefs in a row.

A concept that comes straight out of the subject and excites you is a good one; go with it. Don't
take inspiration from the tools the audience operates (a terminal for developers, a spreadsheet for
accountants): it comes back as a costume. Take it from their world around the work.

## 3. When the first idea is the category's

If someone could guess the direction from the category alone (for a pool: a photo slider of happy
swimmers, blue and white), or from the category plus "avoid the AI look" (a dark, minimal "premium
spa" page), push it. Any of these helps; none is required:

- **A real reference** from outside the web (a poster series, a timetable, a field guide, a ticket,
  a packaging range, a shop sign), and the two or three traits you take from it. One reference,
  adapted, beats several averaged into the safest middle.
- **A dealt card**: `python3 scripts/direction.py` deals structural constraints (how color is
  spent, what leads the layout, the grid, the device, scale, density, type structure). Take what
  sparks something, drop what fights the brief.
- **Rival concepts**: sketch three or four, one of them from a far analogy (signage, an instrument
  panel, a game), and pick the one that fits best and that you'd most like to see built, or show
  two to the user (step 5 of the skill).

## 4. Commit with signature moves

A concept only shows when it changes something visible. Choose a few **signature moves** and make
them decisively; timid versions of good ideas read as defaults.

- **One structural move**: a layout, typographic system or navigation idea that comes from the
  concept (sections as lanes, an index styled like a bookbinder's sample card, the product taken
  apart down the page).
- **One graphic device** from the subject, repeated at several scales (`decoration.md`).
- **One signature interaction**: the micro-interaction people remember (see `motion.md`).
- **Material**: real imagery, made objects, texture or data from the subject rather than stock and
  icons (`imagery.md`, `objects.md`). Where there are no assets, design with type, color, shape and
  made objects so the absence doesn't show.
- **Contrast**: commit to clear extremes in scale, weight, color and density somewhere. Pages that
  keep every value in the middle feel generic even when every value is correct.
- **Commit every atom**: navigation, buttons, inputs, links, captions and the footer are built in
  the concept's vocabulary. A stock component inside a committed page is a lapse.

Every view has at least one of these moves at full strength. What surrounds it speaks the same
vocabulary more plainly; plain is not stock, and it is not empty.

## 5. Check for ambition, not only correctness

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

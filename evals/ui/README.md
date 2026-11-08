# ui skill evals

Cases that check whether the `ui` skill designs like a designer: it reuses the design system,
keeps colors in tokens, fixes causes instead of symptoms, designs every state, plans before code, and
asks for approval and for how to validate.

Cases that extend an app copy `fixture/` first: Ledgerly, a small plain-HTML invoicing site with tokens,
components and a `DESIGN.md`. The fixture has deliberate traps:

- an `action-button` that a request for a "call to action" should find;
- a `panel` that a request for cards should reuse;
- no warning color token;
- a nav that overflows at 375 px because of a fixed `min-width`;
- footer links smaller than 24 px.

Four greenfield cases build a site from nothing: `greenfield-subject-direction` (Cragline, a
bouldering gym), `greenfield-bakery` (Krume, a sourdough bakery), `greenfield-honey-objects`
(Imkerei Hollerer, a beekeeper with no photos, so the products have to be made or carried by type)
and `greenfield-sailing-photos` (Böe, a sailing school), which copies the openly licensed photos in
`photos/` into the run (credits in `photos/CREDITS.md`) and checks fonts, icons, decoration, depth,
alignment and how the photos are used. Besides the generated look, they check what a page has: a
varied section sequence, a graphic device in several places, photo placement, crafted objects and a
design review.

The LLM graders that read the trace (plan before code) are unreliable on long traces; read the plan
in the kept trace (`--keep-temp`) before trusting a FAIL. The eval sandbox blocks headless browsers
and CDNs, so runs can't render their own pages here.

Most graders are deterministic (regex over the files, file existence, tool use); the rest are narrow
LLM checks. Each case runs three times per configuration.

## Running

These are real, billed Claude runs. One case once, to check the setup:

```
claude plugin eval . --eval-dir evals/ui --scaffold --allow-tools Write,Edit,Bash --runs 1 --case fix-header-overflow
```

The whole suite against the current skill, habits v0.2.0 and Anthropic's frontend-design plugin
(10 cases × 3 runs × 4 configurations = 120 runs):

```
evals/ui/compare.sh --max-cost-usd 20
```

Look at the generated pages in the reports too: the greenfield case is where taste shows, and that
needs a human.

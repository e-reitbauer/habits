# ui skill evals

Seven cases that check whether the `ui` skill designs like a designer: it reuses the design system,
keeps colors in tokens, fixes causes instead of symptoms, designs every state, plans before code, and
asks for approval and for how to validate.

Cases that extend an app copy `fixture/` first: Ledgerly, a small plain-HTML invoicing site with tokens,
components and a `DESIGN.md`. The fixture has deliberate traps:

- an `action-button` that a request for a "call to action" should find;
- a `panel` that a request for cards should reuse;
- no warning color token;
- a nav that overflows at 375 px because of a fixed `min-width`;
- footer links smaller than 24 px.

Most graders are deterministic (regex over the files, file existence, tool use); the rest are narrow
LLM checks. Each case runs three times per configuration.

## Running

These are real, billed Claude runs. One case once, to check the setup:

```
claude plugin eval . --eval-dir evals/ui --scaffold --allow-tools Write,Edit,Bash --runs 1 --case fix-header-overflow
```

The whole suite against the current skill, habits v0.2.0 and Anthropic's frontend-design plugin
(7 cases × 3 runs × 4 configurations = 84 runs):

```
evals/ui/compare.sh --max-cost-usd 20
```

Look at the generated pages in the reports too: the greenfield case is where taste shows, and that
needs a human.

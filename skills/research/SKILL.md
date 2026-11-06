---
name: research
description: >
  Use before large, ambiguous or hard-to-reverse work: a new feature or module, a cross-cutting change, picking a
  library, schema or architecture, working in unfamiliar code or APIs, or when the user asks to research,
  brainstorm, explore options or "think this through first". Not for changes you can describe in one sentence.
---

# Research and brainstorming

Mistakes made before the first line of code compound through everything built on them. This skill finds the facts, the options and the user's intent before large work starts, and stays out of the way when the work is small.

## 1. Is it worth it?

Do it when at least one holds:

- The solution is ambiguous: you can't describe the diff in one sentence.
- A decision is hard to reverse: schema, public API, data migration, new dependency, architecture, file formats others read.
- The request leaves open something that would change what gets built, and neither the request nor the code answers it.
- The code, library or API is unfamiliar, or version-sensitive enough that memory isn't trustworthy.
- The change touches many files or every reader of a shared shape.

Skip it, and just do the work, when:

- The task is small and clear: a bug with a repro, a rename, a one-line fix, a fix within existing spec requirements, a choice that is cheap to undo.
- The user already gave a spec or made the decisions, or the project's specs already settle them. Echo it back briefly; don't reopen what's settled.
- The user says to just do it. State any significant choice in one line and go.
- Nobody can answer (headless runs, loops, scheduled tasks). Write your assumptions down instead of asking.
- A quick throwaway build would answer the question faster than discussion would.

Size the effort to the work: a few lookups for one fact, a real investigation only for a real decision.

## 2. Start from the project's source of truth

- If the project keeps specs or decision records (OpenSpec's `openspec/specs/`, ADRs, design docs), read the ones for the area first. They hold intent, requirements and past decisions; code only shows what got built. Treat their requirements as settled constraints.
- Read code only for what the specs don't answer: how something is implemented today, what a change would touch, whether code and spec still agree. Don't read code to re-derive what a spec already states.
- Without specs, read the relevant code until you can explain how it works today and what the change would touch, and follow how the codebase already solves this kind of problem.
- Never ask what the specs or the code already answer.

## 3. Sort the unknowns

- **Facts** (how an API behaves, what a version supports, whether a package exists): look them up.
- **Preferences** (what the user wants, what matters most, what's out of scope): ask.
- **Feasibility** (will this approach work, is it fast enough): spike it, with a timebox, as throwaway code.

## 4. Research facts properly

- Start broad, then narrow.
- Primary sources first: the source code, official docs, changelogs, the package registry. Treat blogs, forum answers and your own memory as leads to verify, not answers.
- Check that every package, version, flag and API you plan to use actually exists in the version the project uses.
- Stop when another search wouldn't change the decision. Say what you checked and what you couldn't confirm.
- Delegate to subagents only for independent, parallel lines of inquiry, each with a clear question and a short report back.

## 5. Brainstorm before converging

Your first idea is likely the most generic one. Before picking:

- Generate several real alternatives, including the smallest change that would work and the way the codebase already does it.
- Drop the weak ones: those that work against why the user wants this, or that the existing code rules out.
- Present two or three, concretely, with what each trades off. Recommend one and say why. If there is genuinely one sensible way, say so and why the others don't fit.

## 6. Ask well

- Ask only when the answer changes what gets built.
- Make each question specific to this project and what you found, about behavior and outcomes rather than internals the user may not know.
- Until you know why they want it, ask open questions; options steer. Once you know why, name the choices with your pick.
- One question at a time, or a short batch with `AskUserQuestion` when they're independent.
- Say your defaults out loud. A default the user never heard is one they couldn't reject.

## 7. Write it down, sized to the work

Record the decisions, the alternatives and why they lost, the non-goals and the open assumptions. A few lines in the conversation for medium work; a file for large work, where the project keeps such docs or where the user wants it. Write decisions and tradeoffs, not an implementation manual.

In an OpenSpec project the change is the write-up; don't create a separate doc. Brainstorm in `/opsx:explore` (it writes nothing), then `/opsx:propose`: the why and what go in `proposal.md`, the alternatives and decisions in `design.md`. If the direction you land on contradicts a spec, that is what the proposal is for; never diverge silently.

For hard-to-reverse decisions, get the user's approval before building. If building later shows an assumption was wrong, stop and revisit the decision instead of patching around it.

## Red flags

| Thought | Reality |
|---|---|
| "I'll read the code to see how this feature should work" | If there's a spec, it says how it should work. Code says how it works now. |
| "Let me ask a few questions first" | Did the code already answer them? Does each answer change what gets built? |
| "Any constraints I should know about?" | Generic questions get generic answers. Ask about the specific case you found. |
| "The first approach looks fine" | Generate the alternatives before you defend one. |
| "One more search to be sure" | If it can't change the decision, stop. |
| "I remember this API" | Check the version the project uses. |
| "I'll spin up several agents for this" | Only for independent questions. Delegation adds parallelism, not insight. |
| "They said sounds good" | Approval covers what they saw. Show the actual design. |
| "The spike works, I'll build on it" | Spikes are throwaway. Keeping one is a decision for the user. |
| "This needs a full design doc" | Only if the solution is ambiguous. A doc that only lists steps is a sign to start coding. |

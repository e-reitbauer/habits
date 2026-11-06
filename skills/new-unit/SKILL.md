---
name: new-unit
description: >
  Use when creating or improving a habits unit: the user asks for guidance on a language, tool, framework, platform,
  testing practice or workflow that has no unit yet, habits suggested creating one, or an existing unit needs work.
  Covers choosing triggers, what to write, and registering and validating the unit.
---

# Creating a habits unit

A unit is one small file of professional guidance for one technology, which habits injects only when a project uses that technology. Getting the triggers and the content right is what makes it useful.

## 1. Find where units live

Units are the `units/<category>/<id>.md` files in the habits plugin. The plugin root was given at session start, and `habits` on the PATH runs the CLI.

- Check the root is a git working copy (`git -C <root> rev-parse --show-toplevel`). If it's an installed copy under `~/.claude/plugins/cache/`, an update would overwrite your edit. Tell the user to clone the habits repo and install from that folder (`claude plugin marketplace add <folder>`), then work there.
- Run `habits units` to see what exists. Improve an existing unit rather than adding a near-duplicate.

## 2. Scope it

- One technology per unit, named in one or two lowercase words joined by a hyphen: `swift`, `gradle`, `spring-boot`, `docker-compose`. Never a combination like `kotlin-gradle`; those are two units that load together.
- Categories: `languages`, `tools` (build tools, CLIs, package managers), `frameworks`, `platforms`, `testing`, `workflows` (processes like OpenSpec). Add a category folder only when none fits.
- The file name is the id.

## 3. Choose the triggers

A unit should load in every session that needs it, and in no other. Use as many triggers as fit:

- `paths`: globs of the technology's own files: its source extension (`**/*.swift`) and its config files (`**/Package.swift`, `**/docker-compose.y{a,}ml`). Avoid globs another unit already owns: check `habits units`.
- `commands`: the CLI names someone runs when using it (`docker compose`, `xcodebuild`). Command prefixes match word by word, after stripping `cd …&&`, env assignments and `sudo`.
- `markers`: only for project-level workflows that should load at session start (`openspec/specs`). Relative globs without `{}`; add `*/…` variants for monorepos.
- `lsp`: the language server plugin id, if an official one exists (`<name>-lsp@claude-plugins-official`).
- `script`: only when the guidance must be computed from the project, like the OpenSpec spec index. A Python script next to the unit; it gets `{"cwd", "root"}` as JSON on stdin and prints text.

## 4. Write the content

Write for a strong developer who already knows the language but not the conventions. Every line is read in every session that loads the unit, so each must earn its place.

Include:
- The official style guide or conventions, linked in the first line, and the points from it that are most often gotten wrong.
- Idioms that separate professional code from merely working code.
- Concrete pitfalls, with the correct alternative.
- How to build, test and verify narrowly (exact commands), and what to gitignore.

Leave out:
- General programming advice, and anything already covered by the `hygiene`, `secrets`, `dependencies` or `errors` skills.
- Facts about a single project; those belong in that project's CLAUDE.md or OpenSpec config.
- Tutorials and explanations of basics.

Format: a first line naming the technology and its style guide, then short sections (`Style`, `Idioms`, `Pitfalls`, `Verify`, or whatever fits) of terse imperative bullets. Aim for 20 to 45 lines.

```markdown
---
id: swift
title: Swift
paths: ["**/*.swift"]
lsp: swift-lsp@claude-plugins-official
---
Swift. Follow the Swift API Design Guidelines (swift.org/documentation/api-design-guidelines).

Style
- …
```

## 5. Register and check it

There is no registry to edit: the file's location registers it. Then:

1. `habits validate`: fix every error and warning.
2. `habits units`: confirm the triggers read as intended.
3. `habits status <a project that uses the technology>`: the unit should be listed with matching files, and nothing unrelated should match.
4. `habits load <id>`: read it the way Claude will receive it.

Commit with the commit skill (`feat(units): add <id> unit`). Don't push unless the user asks.

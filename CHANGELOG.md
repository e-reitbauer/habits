# Changelog

All notable changes to habits. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- `ui` works like a designer: it learns the design system, researches the subject (through `research`), plans the brief, flows, states, component map and layout, gets approval (as an OpenSpec change where there is one), builds only from existing tokens and components, and asks whether to validate automatically, manually or both. References cover the process, UX rules and the generated-look anti-patterns.
- `commit` remembers a standing approval choice when the user says to always approve one way.

### Added

- `ui` tools: `contrast.py` (WCAG and APCA contrast, nearest passing color), `scan.py` (hardcoded colors, fonts and arbitrary values) and `page-checks.js` (measured checks on a rendered page).
- An eval suite for `ui` in `evals/ui`, with a plain-HTML fixture and a script that compares the current skill, v0.2.0 and Anthropic's frontend-design.

### Fixed

- The context size read right after a compaction no longer uses the usage from before it, which triggered a false context rot check.

## [0.2.0] - 2026-11-06

### Added

- Secret guard: a hook that blocks `git commit` and `git push` when the changes would record API keys, tokens, private keys or `.env` files. Lines marked `habits:allow-secret` are skipped.
- Context health: units that were loaded long ago are injected again when they next apply, and Claude is asked to run a context rot check as the context grows (`refreshTokens`, `rotCheckEvery`).
- Skills: `versioning` (SemVer, CalVer, build numbers), `branching` (trunk-based, GitHub Flow, Git Flow, release branches), `patterns` (design and architecture), `context` (context rot check), and `new-unit`.
- Units: `typescript`, `python`, `rust`, `swift`, `vue`, `nuxt`, `spring-boot`, `compose-multiplatform`, `docker-compose`, `xcode`, `github-actions`, `postgres`.
- Automatic session names through `habits title`, set with Claude Code's `sessionTitle` hook field.
- `habits install-cli`, help text, and a `status` that says when each unit loads.
- Visible notices when units load or refresh (`notify`).
- Test suite and CI.

### Changed

- Existing units expanded into style guides with conventions, pitfalls and verify commands.
- `ship` now defers to the `versioning` and `branching` skills.

### Fixed

- Resuming a session no longer injects units that are already in its context.
- List values in unit frontmatter keep commas inside `{a,b}` globs.
- An invalid glob in one unit no longer stops every unit from matching.

## [0.1.0] - 2026-11-06

### Added

- First release: daily skills (`commit`, `pr`, `ship`, `ui`, `hygiene`, `secrets`, `dependencies`, `errors`, `units`), units for Kotlin, Gradle, Maven, Android, unit testing, Playwright and OpenSpec, triggered by files, markers, commands or by hand, and the `habits` CLI.

[0.2.0]: https://github.com/e-reitbauer/habits/compare/c566b7b...v0.2.0
[0.1.0]: https://github.com/e-reitbauer/habits/commit/c566b7b

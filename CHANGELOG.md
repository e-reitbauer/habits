# Changelog

All notable changes to habits. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

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

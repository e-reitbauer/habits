---
name: versioning
description: >
  Use when deciding a version number: bumping a version, cutting a release, tagging, writing a changelog entry,
  setting up versioning for a project, or when asked which versioning scheme to use (SemVer, CalVer, build numbers).
  Detects the project's scheme and picks the next version correctly.
---

# Versioning

## 1. Detect the scheme in use

Follow what the project already does; never switch schemes as a side effect.

- Tags: `git tag --sort=-creatordate | head`. Note the format (`v1.2.3`, `1.2.3`, `2026.11.0`, `app-v1.2.3` per package).
- Version sources: `package.json`, `gradle.properties` / `build.gradle(.kts)`, `pom.xml`, `Cargo.toml`, `pyproject.toml`, `.claude-plugin/plugin.json`, Xcode `MARKETING_VERSION` / `CURRENT_PROJECT_VERSION`, Android `versionName` / `versionCode`.
- Release tooling owns the number when present: release-please, semantic-release, changesets. Then you don't edit versions by hand; you write the commits or changesets that drive them.
- `CHANGELOG.md`: keep its existing format (Keep a Changelog or the tool's generated style).

## 2. The schemes, and when each fits

| Scheme | Shape | Fits |
|---|---|---|
| SemVer | `MAJOR.MINOR.PATCH` | libraries, CLIs, plugins, APIs: anything others depend on |
| CalVer | `YYYY.MM.MICRO` or `YY.MM` | apps and services released on a schedule, where "how new" matters more than compatibility |
| Build numbers | an always-increasing integer | store builds: Android `versionCode`, iOS `CURRENT_PROJECT_VERSION`, next to a user-facing SemVer or CalVer |
| Unversioned | commit SHA | continuously deployed sites and services with no consumers of a version |

When setting up a new project, recommend SemVer for anything with consumers and CalVer for scheduled apps, and say why.

## 3. Picking the next SemVer version

From the Conventional Commits since the last tag (`git log <last-tag>..HEAD --oneline`):
- any `!` or `BREAKING CHANGE` footer: MAJOR (before 1.0.0, bump MINOR instead)
- any `feat`: MINOR
- otherwise any `fix` or `perf`: PATCH
- only `docs`, `chore`, `ci`, `test`, `style`, `refactor`: no release needed

Breaking means a consumer has to change something: removed or renamed public API, changed behaviour they rely on, raised minimum runtime or platform. Internal refactors are never breaking.

Pre-releases: `1.3.0-rc.1`, `1.3.0-beta.2`, ordered and incremented within their label; the final release drops the suffix. `0.x` signals an unstable API; move to `1.0.0` when the API is something you commit to.

## 4. Rules

- One version, one meaning: never re-tag or move a published tag, and never reuse a version number. A broken release gets a new patch.
- Bump every place that holds the version in the same commit (manifest, lockfile entries, plugin.json, app version files), conventionally `chore(release): x.y.z`.
- Mobile: increase the build number for every store upload, even when the user-facing version stays the same.
- Monorepos: either one version for everything (fixed) or per-package versions (independent, with per-package tags like `pkg@1.2.3`). Follow the project's choice; changesets and release-please both support either.
- Tag after the release commit is on the release branch, and push tags explicitly (`git push origin <tag>`) only with the user's go-ahead.
- Changelog entries describe what changed for users, grouped by Added / Changed / Fixed / Removed, newest first.

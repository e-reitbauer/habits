---
name: dependencies
description: >
  Use before adding, upgrading or removing a library, package, plugin or SDK in any project (npm, Gradle, Maven,
  Cargo, pip, Swift packages). Decides whether a dependency is warranted and adds it the project's way.
---

# Dependencies

- First check whether the standard library, the platform or an existing dependency covers it. For small things, a few lines of code beat a new package.
- Prefer maintained, widely used packages, added through the project's mechanism (version catalog, lockfile, package manager). Never hand-edit lockfiles.
- Pin versions the way the project already does; no ranges or `latest`.
- No unrelated upgrades or removals as a side effect. Version bumps are their own change.
- Name each new dependency and why in your summary.

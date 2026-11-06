---
id: gradle
title: Gradle
paths: ["**/*.gradle.kts", "**/*.gradle", "**/gradle/libs.versions.toml", "**/gradle.properties", "**/gradle/wrapper/**"]
commands: ["gradlew", "gradle"]
---
Gradle:
- Always use the wrapper (`./gradlew`), never a global `gradle`. Don't change the wrapper version unless asked.
- Run the narrowest task that proves a change (`./gradlew :module:test --tests 'SomeTest'`, `:module:compileKotlin…`), and the full build only before finishing. Add `--continue` to collect every failure in one run.
- Long builds: run them in the background, write output to a log, and read the first error, not the last.
- If the project has a version catalog (`gradle/libs.versions.toml`), every dependency and plugin version goes there and build scripts use `libs.…`. Never hard-code versions in build scripts.
- Shared build logic belongs in the project's convention plugins (`build-logic/` or `buildSrc/`), not copied between modules.
- Keep builds configuration-cache friendly: no work at configuration time, no `project` access inside task actions.

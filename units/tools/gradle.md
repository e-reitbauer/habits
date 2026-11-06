---
id: gradle
title: Gradle
paths: ["**/*.gradle.kts", "**/*.gradle", "**/gradle/libs.versions.toml", "**/gradle.properties", "**/gradle/wrapper/**"]
commands: ["gradlew", "gradle"]
---
Gradle. Use the Kotlin DSL (`*.gradle.kts`) for new build logic.

Running builds
- Always the wrapper (`./gradlew`), never a global `gradle`. Don't change `gradle/wrapper/gradle-wrapper.properties` unless asked.
- Narrowest task first: `:module:compileKotlin…`, `:module:test --tests 'pkg.SomeTest'`; the full `build` only before finishing. `--continue` shows every failure in one run; `--offline` when dependencies are cached.
- Long builds run in the background with output to a log. Read the first error (`grep -n "e: \|error:\|FAILED" build.log`), not the tail.
- Don't `clean` by habit: it throws away the build cache. Use it only for suspected stale output.

Dependencies
- The version catalog (`gradle/libs.versions.toml`) is the single source of versions: `[versions]`, `[libraries]`, `[plugins]`, `[bundles]`. Build scripts use `libs.foo` and `alias(libs.plugins.foo)`.
- No versions in build scripts, and no dynamic versions (`+`, `latest.release`).
- `implementation` over `api` unless the dependency's types are part of the module's public API; `testImplementation` for test-only libraries.
- Investigate conflicts with `./gradlew :module:dependencyInsight --dependency <name> --configuration <conf>`.

Build logic
- Shared configuration goes in convention plugins (a `build-logic/` included build, or `buildSrc`) applied by id. No copy-paste between modules, and no new `allprojects` / `subprojects` blocks.
- Apply plugins in the `plugins {}` block, not with `apply plugin:`.
- Lazy APIs only: `tasks.register`, `Provider` and `Property`. Never `tasks.create` or eager `getByName` in new code.
- Stay configuration-cache compatible: no work at configuration time, no `project` access inside task actions.

Settings and properties
- Modules are declared in `settings.gradle.kts`, with repositories centralized in `dependencyResolutionManagement`.
- `gradle.properties` holds build flags (`org.gradle.caching=true`, `org.gradle.configuration-cache=true`, JVM args), never secrets.

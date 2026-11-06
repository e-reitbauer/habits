---
id: maven
title: Maven
paths: ["**/pom.xml", "**/.mvn/**"]
commands: ["mvn", "mvnw"]
---
Maven.

Running builds
- Use the wrapper (`./mvnw`) when the project has one.
- Build only the changed module and what it needs: `-pl <module> -am`. Run one test with `-Dtest=Class#method`, adding `-Dsurefire.failIfNoSpecifiedTests=false` in multi-module builds.
- `-q` to cut noise, `-o` offline when dependencies are cached. Don't `clean` by habit.
- `verify` runs integration tests too; `install` only when another local project needs the artifact.

POM structure
- The parent POM owns `<dependencyManagement>`, `<pluginManagement>` and `<properties>` (versions, `maven.compiler.release`, `project.build.sourceEncoding`). Child modules declare dependencies without versions.
- Import BOMs (`<type>pom</type><scope>import</scope>`, e.g. Spring Boot or JUnit) instead of pinning every artifact.
- Pin every plugin version (compiler, surefire, failsafe, jar, enforcer); never rely on the super-POM's defaults.
- Use the right scope: `test` for test libraries, `provided` for container-supplied APIs, `runtime` for drivers.
- On a growing project, add `maven-enforcer-plugin` with `requireMavenVersion` and `dependencyConvergence`.

Dependencies
- Before adding one, check `./mvnw dependency:tree -Dincludes=<group>:<artifact>`. Resolve conflicts in `dependencyManagement`, not with scattered `<exclusions>`.
- `./mvnw versions:display-dependency-updates` lists updates; bump them in a separate change.

Tests
- Unit tests (`*Test`) run under surefire; integration tests (`*IT`) under failsafe, bound to `integration-test` and `verify`. Don't mix them.

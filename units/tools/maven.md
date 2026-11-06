---
id: maven
title: Maven
paths: ["**/pom.xml", "**/.mvn/**"]
commands: ["mvn", "mvnw"]
---
Maven:
- Use the wrapper (`./mvnw`) when the project has one.
- Build only what changed: `-pl <module> -am`. Run a single test with `-Dtest=Class#method`. Use `-q` to cut noise and `-o` offline when dependencies are cached.
- Versions live in the parent's `<dependencyManagement>` / `<pluginManagement>` or a BOM; child modules omit them. Shared versions go in `<properties>`.
- Pin plugin versions explicitly (compiler, surefire, failsafe); don't rely on Maven's defaults.
- Unit tests run under surefire (`*Test`), integration tests under failsafe (`*IT`). Don't mix them.
- Check `./mvnw dependency:tree` before adding a dependency, to spot version conflicts.

---
id: unit-testing
title: Unit testing
paths: ["**/test/**", "**/tests/**", "**/__tests__/**", "**/*Test.kt", "**/*Tests.kt", "**/*Test.java", "**/*Tests.swift", "**/*.test.*", "**/src/*Test/**"]
---
Unit testing.

What to test
- Every bug fix gets a regression test that fails without the fix.
- Test behaviour through the public API: inputs, outputs and observable effects. Not private methods, not call order.
- Cover the edge cases the change touches: empty, absent, boundaries and error paths.

Structure
- Arrange, act, assert. One behaviour per test, and a name that states it (`returns empty list when no tags match`; backtick names in Kotlin).
- Small focused fixtures. Builders or factory functions instead of copy-pasted setup. No logic (loops, conditionals) inside tests.
- Mirror the production package layout, and use the project's framework and assertion style (JUnit 5, kotlin.test, Kotest, Swift Testing or XCTest, Vitest or Jest). Don't introduce another.

Isolation and determinism
- Control time (an injected clock), randomness (seeds), and IO and network (fakes, in-memory implementations, MockWebServer, Testcontainers for integration tests).
- Kotlin coroutines: `runTest` with a test dispatcher and virtual time. Anywhere async: wait on conditions, never sleep.
- Every test passes alone and in any order. No shared mutable state between tests.
- Prefer fakes over mocks, and mock only boundaries you don't own. Don't verify mock interactions that the output already proves.

Discipline
- Never weaken, skip or delete a failing test to get green. If a test is wrong, explain why and fix it on purpose.
- A flaky test gets its cause fixed (timing, ordering, shared state), not a retry.
- Run the narrowest relevant tests while iterating and the full suite before finishing, then report exactly what ran and the result.

---
id: unit-testing
title: Unit testing
paths: ["**/test/**", "**/tests/**", "**/__tests__/**", "**/*Test.kt", "**/*Tests.kt", "**/*Test.java", "**/*.test.*", "**/src/*Test/**"]
---
Unit testing:
- Every bug fix gets a test that fails without the fix. Write it first when practical.
- Never weaken, skip or delete a test to make it pass. If a test is wrong, explain why and fix it on purpose.
- Test behaviour through the public API, not implementation details. One reason to fail per test, with a name that states the expected behaviour.
- Keep tests deterministic: control time, randomness, network and shared state (injected clocks, seeds, fakes). No sleeps; wait on conditions.
- Prefer fakes over deep mocking, and mock only at system boundaries.
- Iterate on the narrowest relevant tests, run the full suite before finishing, and report what ran and what passed or failed.
- Use the project's existing test framework, naming and layout; don't introduce another.

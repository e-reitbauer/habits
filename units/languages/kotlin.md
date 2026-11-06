---
id: kotlin
title: Kotlin
paths: ["**/*.kt"]
lsp: kotlin-lsp@claude-plugins-official
---
Kotlin:
- Prefer `val` and read-only collections; model data with data classes. Avoid `!!`: use `?.`, `?:`, early returns, or `requireNotNull(x) { "why" }`.
- State preconditions with `require`, invariants with `check`, and unreachable states with `error("why")`, not generic exceptions.
- Model states and results with sealed types and an exhaustive `when`; no `else` branch on a sealed type, so new cases fail to compile.
- Coroutines use structured concurrency: launch in the owning component's scope, never `GlobalScope`; `runBlocking` only in `main` and tests. Move blocking work off the caller with `withContext(Dispatchers.IO)`.
- Kotlin Multiplatform: shared logic lives in `commonMain`; use `expect`/`actual` only for real platform APIs, and keep platform code thin.
- Follow the project's ktlint/detekt setup if it has one.

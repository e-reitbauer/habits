---
id: kotlin
title: Kotlin
paths: ["**/*.kt"]
lsp: kotlin-lsp@claude-plugins-official
---
Kotlin. Follow the official Kotlin coding conventions (kotlinlang.org/docs/coding-conventions.html) unless the project's ktlint, detekt or .editorconfig says otherwise.

Style
- 4-space indent. Trailing commas in multiline parameter and argument lists.
- Naming: PascalCase types, camelCase functions and properties, SCREAMING_SNAKE_CASE for `const val` and top-level immutable constants. A private mutable backing property is `_state` behind a public read-only `state`.
- One public top-level class per file, named after it. A file of top-level functions is named for what it holds (`StringExtensions.kt`).
- Class layout: properties and `init` blocks, secondary constructors, functions, then the companion object last.
- Expression bodies for single-expression functions. Named arguments for booleans and for several parameters of the same type. Default parameters over overloads.
- Explicit return types on public API; omit types elsewhere when the right side makes them obvious.

Idioms
- `val` over `var`; read-only types (`List`, `Map`) in signatures, mutable ones only locally.
- No `!!`. Use `?.`, `?:`, early return, or `requireNotNull(x) { "why" }`.
- `require` for arguments, `check` for state, `error("why")` for the unreachable.
- Sealed interfaces with an exhaustive `when` (no `else`) for states and results; `data class` for values; `@JvmInline value class` for typed ids.
- Scope functions with intent and never nested: `apply` to configure, `also` for side effects, `let` to map a nullable.
- String templates over concatenation; `buildString` / `buildList` for builders.

Coroutines
- Structured concurrency: launch from the owning component's scope. Never `GlobalScope`; `runBlocking` only in `main` and tests.
- Suspend functions are main-safe: move blocking work with `withContext(Dispatchers.IO)`, and inject dispatchers so tests can replace them.
- Never swallow `CancellationException`; rethrow it when catching `Exception`.
- Expose `StateFlow` / `Flow` read-only and keep the `MutableStateFlow` private.

Multiplatform
- Shared code lives in `commonMain`. Use `expect`/`actual` only for real platform APIs; prefer an interface plus platform implementations.
- No `java.*` or Android APIs in common code.

Verify
- Compile and test only the touched module first (`:module:compileKotlin…`, `:module:test`), and fix every new warning you introduced.

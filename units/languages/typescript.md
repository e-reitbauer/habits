---
id: typescript
title: TypeScript
paths: ["**/*.ts", "**/*.tsx", "**/*.mts", "**/*.cts", "**/tsconfig*.json"]
commands: ["tsc"]
lsp: typescript-lsp@claude-plugins-official
---
TypeScript. Follow the project's ESLint and Prettier config; otherwise the TypeScript handbook's do's and don'ts and typescript-eslint's recommended rules.

Types
- `strict: true` is the baseline. Never weaken compiler options to make an error go away.
- No `any`. Use `unknown` and narrow it, generics, or a precise type. A cast (`as`) needs a reason; a non-null assertion (`!`) is a bug waiting to happen.
- Model alternatives as discriminated unions (`{ kind: "ok", value } | { kind: "error", error }`) with exhaustive `switch` checks via `never`.
- `type` for unions and computed types, `interface` for object shapes meant to be extended; follow the codebase where it has chosen.
- Derive types instead of repeating them: `typeof`, `keyof`, `ReturnType`, `Pick`, `Omit`, `satisfies` for checked literals.
- Validate untrusted data (API responses, env, user input) at the boundary with a schema (zod, valibot) instead of casting.

Style
- camelCase values and functions, PascalCase types and components, UPPER_SNAKE only for true constants. No `I` prefix on interfaces.
- `const` by default, `let` when reassigned, never `var`. Strict equality (`===`).
- ES modules with named exports; avoid default exports unless the framework requires them (pages, config files).
- `async`/`await` over raw promise chains; never leave a promise floating: await it, return it, or `void` it on purpose.
- Prefer `readonly` and immutable updates; `Array.prototype` methods over index loops when they read clearer.

Pitfalls
- `enum` emits runtime code and has odd semantics; prefer a `const` object with `as const` or a union of string literals.
- Optional chaining hides missing data: decide whether absence is valid before writing `?.`.
- `JSON.parse` and `fetch().json()` return `any`: type them through validation.

Verify
- `npx tsc --noEmit` (or the project's `typecheck` script), then lint and tests. Fix type errors properly; no `@ts-ignore` (use `@ts-expect-error` with a comment if truly unavoidable).

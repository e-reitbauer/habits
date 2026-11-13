---
id: javascript
title: JavaScript
paths: ["**/*.js", "**/*.mjs", "**/*.cjs", "**/*.jsx"]
commands: ["node"]
lsp: typescript-lsp@claude-plugins-official
---
JavaScript. Follow the project's ESLint and Prettier (or Biome) config; otherwise ESLint's recommended rules and MDN's JavaScript guide (developer.mozilla.org/docs/Web/JavaScript/Guide).

Modules
- ES modules in new code. Check `"type"` in `package.json` and the extension (`.mjs`, `.cjs`) before writing an import, and never mix `require` and `import` in one file.
- Named exports. Relative imports carry the extension in Node ESM and in the browser (`./util.js`).
- A module meant to be imported has no side effects at the top level; work starts in a function the caller invokes.

Style
- `const` by default, `let` when reassigned, never `var`. `===` and `!==`; `== null` only where the codebase uses it for null-or-undefined.
- camelCase values and functions, PascalCase classes and components, UPPER_SNAKE for true constants, `#private` fields for class internals.
- `??` for defaults, not `||`, so `0`, `''` and `false` survive. Optional chaining only where absence is valid.
- `for…of` and array methods over index loops; never `for…in` on arrays. Template literals, destructuring and spread over manual assembly.
- JSDoc types on exported functions (`@param`, `@returns`, `@typedef`); keep `// @ts-check` or `checkJs` passing where the project has it.

Async
- `async`/`await`. Every promise is awaited, returned or handled; a floating promise loses its error.
- `Promise.all` for independent work instead of awaiting in a loop; `Promise.allSettled` when one failure must not cancel the rest.
- Cancel with `AbortController` (`fetch`, and listeners through `{ signal }`). Timers, listeners and observers are removed when their owner goes away.
- `fetch` resolves on HTTP errors: check `response.ok` before reading the body.

Pitfalls
- A method passed as a callback loses `this`: pass an arrow function or bind it.
- `sort()` compares as strings and sorts in place: pass a comparator, and use `toSorted()` for a copy. `reverse()` and `splice()` mutate too.
- Spread and `Object.assign` copy one level; `structuredClone` for a deep copy.
- `Number.isNaN`, not `isNaN` or `=== NaN`; `Number(x)` or `parseInt(x, 10)`; money as integer cents, never floats.
- `Date` months start at 0 and non-ISO strings parse differently per engine: store ISO 8601, format with `Intl.DateTimeFormat`.
- In the DOM, `textContent`, never `innerHTML` with anything a user or a server supplied. No `eval` or `new Function` on input.

Verify
- `node --check file.js` for syntax, then the project's lint and test scripts (`npm run lint`, `npm test`, or `node --test path`), the touched test first.
- Keep `node_modules/`, build output (`dist/`, `build/`) and coverage out of version control; commit the lockfile.

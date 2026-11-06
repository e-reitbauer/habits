---
id: nuxt
title: Nuxt
paths: ["**/nuxt.config.*", "**/app.config.*", "**/server/api/**", "**/server/routes/**", "**/app/pages/**", "**/pages/**/*.vue"]
commands: ["nuxi", "nuxt"]
---
Nuxt 3/4. Follow the official docs' conventions (nuxt.com/docs); the vue unit applies to components too.

Structure
- Use the conventional directories and their auto-imports: `pages/` (file routing), `components/`, `composables/`, `layouts/`, `middleware/`, `plugins/`, `server/` (Nitro). Don't import what Nuxt auto-imports.
- Nuxt 4 layout keeps app code under `app/`; follow whichever layout the project uses.
- Server routes in `server/api/*.ts` with `defineEventHandler`; validate input with `getValidatedQuery` / `readValidatedBody` and a schema.

Data fetching
- `useFetch` / `useAsyncData` for data needed during render, so it's fetched once on the server and hydrated; give `useAsyncData` a stable key.
- `$fetch` only in event handlers and server code, not at component setup (it would fetch twice).
- Handle `pending` and `error` states explicitly.

State and config
- `useState` for SSR-safe shared state (never module-level `ref`s, which leak between requests); Pinia for larger stores.
- Runtime config through `runtimeConfig` in `nuxt.config` and `useRuntimeConfig()`; secrets only in the private (non-`public`) part, set via `NUXT_*` env vars.

SSR pitfalls
- Browser-only APIs (`window`, `localStorage`) only in `onMounted`, `<ClientOnly>`, or `.client` plugins.
- Avoid hydration mismatches: no `Date.now()`, random values or locale-dependent formatting during render without matching server output.

Rendering and SEO
- Per-route rendering via `routeRules` (prerender, SWR, SPA); `useSeoMeta` / `useHead` for metadata.
- Static hosting: `nuxt generate`, and make sure dynamic routes are prerendered or crawled.

Verify
- `nuxi typecheck`, the build (`nuxi build` or `nuxi generate`), and a dev-server check of the touched pages.

---
id: vue
title: Vue
paths: ["**/*.vue"]
---
Vue 3. Follow the official style guide (vuejs.org/style-guide), priority A and B rules at least.

Components
- `<script setup lang="ts">` with the Composition API for new code; follow the codebase if it uses the Options API.
- Multi-word component names in PascalCase (`TagList.vue`, not `List.vue`); base components prefixed (`BaseButton`), single-instance ones prefixed `The` (`TheHeader`).
- Typed props and emits: `defineProps<{ … }>()`, `defineEmits<{ … }>()`, `withDefaults` for defaults, `defineModel` for v-model.
- Props down, events up. Never mutate a prop; emit or use `defineModel`.
- Keep components focused: extract logic into composables (`useTags()`) that return refs and functions.

Reactivity
- `ref` for values, `reactive` only for objects you never replace; don't destructure reactive objects (use `toRefs` / `storeToRefs`).
- `computed` for derived state, never a watcher that copies state into another ref.
- `watch` with explicit sources for side effects; clean up in `onWatcherCleanup` or `onUnmounted`.

Templates
- `v-for` always with a stable `:key` (an id, not the index); never `v-if` on the same element as `v-for`.
- Keep expressions simple; move logic into computed properties or functions.
- No `v-html` with untrusted content.

State
- Pinia for shared state, with setup-style stores; server data through the project's fetching layer rather than copied into stores.

Verify
- `vue-tsc --noEmit` (or the project's typecheck script), lint, and component tests with the project's runner (Vitest + Vue Test Utils).

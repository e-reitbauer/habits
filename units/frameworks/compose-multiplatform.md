---
id: compose-multiplatform
title: Compose Multiplatform
paths: ["**/src/commonMain/**/*.kt", "**/composeResources/**"]
---
Compose Multiplatform. Follow JetBrains' Compose Multiplatform docs and the Jetpack Compose API guidelines (github.com/androidx/androidx/blob/androidx-main/compose/docs/compose-api-guidelines.md).

Sharing
- UI and state in `commonMain`; platform code only for what has no common API, behind an interface or `expect`/`actual`.
- Resources through `composeResources/` and the generated `Res` class (`stringResource(Res.string.x)`, `painterResource(Res.drawable.x)`); no platform-specific resource lookups in common code.
- Only use libraries with multiplatform support in common code (Ktor, kotlinx.serialization, kotlinx-datetime, multiplatform ViewModel and navigation).

Composables
- PascalCase noun names for UI-emitting composables; lowerCamelCase for ones that return values (`rememberX`).
- `modifier: Modifier = Modifier` as the first optional parameter, applied to the root.
- Stateless composables with hoisted state; `remember`/`rememberSaveable` for local UI state; collect flows with `collectAsStateWithLifecycle()` (or `collectAsState()` where lifecycle isn't available).
- Stable, immutable parameters to keep recomposition cheap; keys in lazy lists.
- Side effects only in effect handlers (`LaunchedEffect`, `DisposableEffect`) with correct keys.

Platform integration
- iOS: hosted in a `ComposeUIViewController`; keep Swift-facing APIs simple (no generics or sealed hierarchies across the boundary without care).
- Test shared UI with the multiplatform `runComposeUiTest`.

Verify
- Build the shared module for each target the change affects (`:module:compileKotlinIosSimulatorArm64`, `:module:compileDebugKotlinAndroid`, wasm if used), not just one platform.

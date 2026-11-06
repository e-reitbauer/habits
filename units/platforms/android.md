---
id: android
title: Android
paths: ["**/AndroidManifest.xml", "**/src/androidMain/**", "**/src/main/res/**"]
commands: ["adb", "emulator"]
---
Android. Follow the official guide to app architecture (developer.android.com/topic/architecture).

Architecture
- UI layer (Compose or Views plus a ViewModel that exposes immutable UI state as a `StateFlow`), data layer (repositories as the single source of truth), and a domain layer only when logic is shared.
- Unidirectional data flow: events go up, state comes down. A screen's state is one immutable data class or sealed interface.
- ViewModels hold no `Context`, `View` or `Activity` references. State that must survive process death goes in `SavedStateHandle`.

Jetpack Compose (when used)
- Stateless composables with state hoisted to the caller; `remember` / `rememberSaveable` for local UI state.
- Collect flows with `collectAsStateWithLifecycle()`.
- Pass stable parameters (immutable data, `@Immutable` / `@Stable` where needed) to avoid needless recomposition, and give lazy list items a `key`.
- `modifier: Modifier = Modifier` is the first optional parameter and is passed to the root element. Add previews for the meaningful states.

Threading and lifecycle
- No disk, network or database work on the main thread. Use `viewModelScope` / `lifecycleScope`, and collect UI flows inside `repeatOnLifecycle(Lifecycle.State.STARTED)`.
- Deferrable background work that must survive process death goes through WorkManager.

Resources and manifest
- User-facing text lives in `strings.xml`, with `<plurals>` for counts. Colors, typography and dimensions come from the theme (Material 3 tokens).
- Request only the permissions you need, at runtime with a rationale, and handle both denial and permanent denial.
- Check API levels against `minSdk`; guard with `Build.VERSION.SDK_INT` or use AndroidX compat APIs.
- Every component with an intent filter declares `android:exported` explicitly.

Verify
- `./gradlew :app:assembleDebug` or `:app:installDebug`. On a device: `adb install -r <apk>`, `adb shell am start -n <package>/<activity>`, and `adb logcat --pid=$(adb shell pidof -s <package>)`.
- Never commit `local.properties`, keystores, or real API keys in `google-services.json` or manifest placeholders.

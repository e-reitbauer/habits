---
id: android
title: Android
paths: ["**/AndroidManifest.xml", "**/src/androidMain/**", "**/src/main/res/**"]
commands: ["adb", "emulator"]
---
Android:
- Declare only the permissions the app needs. Request dangerous ones at runtime with a clear reason, and handle denial and "don't ask again".
- Never block the main thread with disk, network or database work. Use lifecycle-aware scopes (`viewModelScope`, `lifecycleScope` with `repeatOnLifecycle`).
- UI state must survive configuration changes and process death: keep it in ViewModels and `SavedStateHandle`, not in Activities.
- User-visible text goes in `strings.xml`; colors and dimensions come from resources or the theme.
- Check an API's level against `minSdk` before using it.
- When behaviour depends on the platform, verify on an emulator or device with adb (`adb install -r`, `adb shell am start`, `adb logcat` filtered to the app's package).
- Never commit `local.properties`, keystores, or config files holding real credentials, unless the project deliberately tracks them.

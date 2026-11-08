# Native apps: Compose and SwiftUI

The other references are written in web terms. On native platforms the same design decisions apply,
expressed through the platform: tokens become the theme, CSS techniques become modifiers, and the
platform's own rules for navigation, insets, text size and back come first. Load the project's
units (`compose-multiplatform`, `swift`, `xcode`) for code conventions.

## Platform rules that are not optional

**Android (Compose)**
- Edge-to-edge is enforced for apps targeting SDK 35+ on Android 15+, with no opt-out from SDK 36.
  Never assume opaque system bars: content uses `WindowInsets.safeDrawing`, anything that swipes
  uses `safeGestures`; pass `Scaffold`'s `innerPadding` down; lists get
  `contentPadding = WindowInsets.safeDrawing.asPaddingValues()` so items scroll behind the bars;
  `consumeWindowInsets` keeps nested layouts from padding twice.
- Predictive back is on by default at SDK 36: handle back with `BackHandler` /
  `PredictiveBackHandler` or the navigation library, never by intercepting the key.
- Large screens (sw ≥ 600dp) ignore orientation and resizability locks from SDK 36: every screen
  works in landscape and wide windows. Navigation follows the window size: bottom `NavigationBar`
  (compact, five destinations at most), `NavigationRail` (medium), drawer (expanded).
- Touch targets at least 48×48dp (`Modifier.sizeIn(minWidth = 48.dp, minHeight = 48.dp)` on custom
  clickables). Text in `sp` only, never in fixed-height boxes; test at font scale 2.0.
- Contrast 4.5:1 for text under 18sp (14sp bold), 3:1 above; `onX` colors only on `X`.

**iOS (SwiftUI)**
- Touch targets at least 44×44pt; pad small controls' hit area with `.contentShape` or padding.
- Dynamic Type: semantic text styles (`.body`, `.headline`), custom fonts through
  `.font(.custom("Name", size: 17, relativeTo: .body))`, spacing with `@ScaledMetric`; at
  accessibility sizes, reflow (HStack to VStack) instead of truncating.
- iOS 26 Liquid Glass: standard bars, tab bars, toolbars and sheets adopt it automatically; remove
  custom backgrounds on them. Glass belongs only to the navigation layer floating over content
  (`.glassEffect`, `GlassEffectContainer`, `.buttonStyle(.glass)`), never on lists, cards or rows,
  never glass on glass. Tint only the primary action. Respect Reduce Transparency.
- Haptics only for commits, toggles, detents and errors: `.sensoryFeedback(.success, trigger:)`;
  Compose `LocalHapticFeedback.current.performHapticFeedback(...)`.

## Expressing the brand

- **Compose**: the default is Material 3 configured with your own `ColorScheme`, `Typography` (set
  `fontFamily` on each style you use; use a reduced set of the 15 roles) and `Shapes`. Generate the
  color roles from the brand seed with Material Theme Builder or `scripts/palette.py` instead of
  picking 30 values by hand. Extra tokens (brand colors, spacing, motion) go in an `@Immutable` data
  class provided through `staticCompositionLocalOf` and read through an `AppTheme` object. A fully
  custom design system only when Material lacks the concepts; then every component wraps its own
  styling and you handle text selection colors and ripple.
- Material 3 Expressive (`MaterialExpressiveTheme`, `MotionScheme.expressive()`, `ButtonGroup`,
  `FloatingToolbar`) is stable only from material3 1.5; check the project's version first, and keep
  `LoadingIndicator` and `MaterialShapes` behind their experimental opt-in. Read motion from
  `MaterialTheme.motionScheme` (springs for movement and size, easing for color and opacity).
- Dynamic color (wallpaper-based) weakens a strong brand: turn it off, or use it only for neutral
  surfaces.
- **SwiftUI**: an app-wide `.tint`, custom fonts with `relativeTo:`, tokens as `EnvironmentValues`
  (`@Entry`) or `ShapeStyle` extensions, colors in the asset catalog with light, dark and
  high-contrast variants.
- The brand lives in the typeface, the color roles, the shape scale, the motion personality, the
  icon set, the app icon, the launch screen, onboarding and empty states. Navigation, back
  behavior, sheets, system bars, text fields and list scrolling stay the platform's.
- Elevation on Android is tonal first (`tonalElevation`), shadow second; radii nest concentrically.

## Design review and validation

- Previews and screenshots: Compose Preview Screenshot Testing (`@PreviewTest` previews in
  `src/screenshotTest`, `./gradlew updateDebugScreenshotTest` then `validateDebugScreenshotTest`),
  Roborazzi (`recordRoborazziDebug`, `verifyRoborazziDebug`; Compose Multiplatform desktop and iOS),
  Paparazzi; swift-snapshot-testing on iOS. Render every state, both themes and the largest font scale.
- Accessibility: Compose `composeTestRule.enableAccessibilityChecks()` with
  `onRoot().tryPerformAccessibilityChecks()` (`ui-test-junit4-accessibility`); XCUITest
  `try app.performAccessibilityAudit()` on each screen; Xcode Accessibility Inspector.
- On a device or emulator: `adb exec-out screencap -p > shot.png`,
  `adb shell uiautomator dump` (bounds for 48dp and content descriptions),
  `adb shell settings put system font_scale 2.0`, `adb shell cmd uimode night yes`;
  `xcrun simctl io booted screenshot shot.png`, `xcrun simctl ui booted appearance dark`,
  `xcrun simctl ui booted content_size accessibility-extra-extra-extra-large`.
- Run `scripts/scan.py` on the touched Kotlin or Swift files for literal colors.

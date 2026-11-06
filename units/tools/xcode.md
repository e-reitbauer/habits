---
id: xcode
title: Xcode
paths: ["**/*.pbxproj", "**/*.xcconfig", "**/*.xcscheme", "**/*.xcworkspacedata", "**/Info.plist", "**/*.entitlements", "**/*.xcassets/**"]
commands: ["xcodebuild", "xcrun", "xcode-select"]
---
Xcode projects.

Project files
- Never hand-edit `project.pbxproj` for anything Xcode or a generator can do. If the project uses XcodeGen or Tuist (`project.yml`, `Project.swift`), edit that and regenerate.
- When a pbxproj edit is unavoidable (adding a file, a build phase), keep IDs unique and every reference consistent, then verify the project still opens and builds.
- Build settings belong in `.xcconfig` files where the project uses them, not scattered across targets in the pbxproj.
- Never commit `xcuserdata/`, `DerivedData/` or `*.xcuserstate`.

Versions and signing
- `MARKETING_VERSION` is the user-facing version; `CURRENT_PROJECT_VERSION` (build number) increases with every upload.
- Don't change signing settings, team IDs, bundle identifiers or provisioning without the user asking; never commit certificates or provisioning profiles.
- Capabilities go through the `.entitlements` file and matching `Info.plist` usage descriptions (`NSLocationWhenInUseUsageDescription` etc.); a missing usage description crashes at runtime.

Building from the command line
- List schemes and destinations: `xcodebuild -list`, `xcrun simctl list devices available`.
- Build: `xcodebuild -scheme <Scheme> -destination 'platform=iOS Simulator,name=<Device>' build`; add `-quiet` to cut noise and read the first `error:`.
- Test: the same with `test`, or `-only-testing:<Target>/<Class>/<test>` for one test.
- Simulator: `xcrun simctl boot`, `install`, `launch`, and `xcrun simctl spawn <id> log stream --predicate 'process == "<App>"'` for logs.
- Kotlin Multiplatform projects build the shared framework from Gradle as part of the Xcode build phase; when it fails, read the Gradle output in the build log first.

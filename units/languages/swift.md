---
id: swift
title: Swift
paths: ["**/*.swift"]
lsp: swift-lsp@claude-plugins-official
---
Swift. Follow the Swift API Design Guidelines (swift.org/documentation/api-design-guidelines), and the project's SwiftLint or swift-format config if it has one.

Naming and API design
- Clarity at the point of use beats brevity: calls read as English phrases (`list.insert(item, at: 0)`).
- UpperCamelCase for types and protocols, lowerCamelCase for everything else. Acronyms are cased uniformly (`urlString`, `HTTPClient`).
- Protocols that describe what something is are nouns (`Collection`); capabilities end in -able, -ible or -ing (`Equatable`, `ProgressReporting`).
- Mutating and non-mutating pairs follow the verb/participle pattern: `sort()` / `sorted()`.
- Booleans read as assertions: `isEmpty`, `hasChanges`, `canSubmit`.
- Omit an argument label only when the argument's role is obvious (`max(a, b)`).

Style
- 4-space indent. `let` by default. Access control as tight as possible (`private` first); classes `final` unless designed for subclassing.
- Prefer structs and enums; use classes for identity or shared mutable state.
- `guard` for early exits. No force unwrap (`!`) or `try!` outside tests and truly impossible cases; use the `if let value` shorthand.
- One extension per protocol conformance (`extension Tag: Codable {}`), grouped with `// MARK: -`.
- Trailing closure syntax, except when a call takes several closures.

Concurrency
- async/await and structured concurrency (`async let`, task groups) over completion handlers and GCD.
- UI state and UI-facing types are `@MainActor`.
- Shared mutable state lives in an `actor`. Make types `Sendable`, and fix strict-concurrency warnings instead of silencing them with `@unchecked Sendable`.
- Long-running work checks for cancellation (`try Task.checkCancellation()`).

SwiftUI (when used)
- Views are small value types. `@State` is private and owned by the view, `@Binding` for shared, `@Observable` models on iOS 17+ (`ObservableObject` on older targets).
- No heavy work in `body`; derive values instead of storing duplicate state.

Errors
- Throw typed errors (an `enum` conforming to `Error`) when the caller needs the reason. Don't hide failures with a bare `try?`.

Verify
- Build the scheme that uses the code: `xcodebuild -scheme <Scheme> -destination 'platform=iOS Simulator,name=<Device>' build`, or `swift build` / `swift test` for packages.

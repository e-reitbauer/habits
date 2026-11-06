---
id: rust
title: Rust
paths: ["**/*.rs", "**/Cargo.toml"]
commands: ["cargo", "rustc"]
lsp: rust-analyzer-lsp@claude-plugins-official
---
Rust. Follow the Rust API Guidelines (rust-lang.github.io/api-guidelines) and `rustfmt` defaults; treat `clippy` warnings as work to do.

Style
- snake_case functions, variables and modules; UpperCamelCase types and traits; SCREAMING_SNAKE_CASE constants and statics.
- Conversions named by cost: `as_` (free, borrowed), `to_` (expensive), `into_` (consuming). Getters without a `get_` prefix.
- Small modules; `pub` only what is part of the API, `pub(crate)` for internal sharing.
- Derive common traits where they make sense (`Debug`, `Clone`, `PartialEq`, `Eq`, `Hash`, `Default`).

Errors
- Return `Result` and propagate with `?`. No `unwrap()` / `expect()` in library or request-handling code; `expect("why this can't fail")` only for real invariants.
- Libraries define error enums (`thiserror`); applications may use `anyhow` with `.context(...)` for messages.
- `panic!` is for bugs, never for expected failure.

Ownership and idioms
- Borrow (`&str`, `&[T]`, `impl AsRef<…>`) in parameters; take ownership only when you store the value.
- Don't `clone()` to quiet the borrow checker; restructure first and clone deliberately.
- Iterators and combinators over index loops; `match` and `if let` over chains of `is_some()` / `unwrap()`.
- Newtypes for domain values (`struct UserId(u64)`), enums for states.
- `unsafe` only with a `// SAFETY:` comment stating the invariants that make it sound.

Async (when used)
- Don't block inside async code (`std::fs`, `thread::sleep`, heavy CPU): use the runtime's async APIs or `spawn_blocking`.
- Don't hold a `std::sync::Mutex` guard across `.await`.

Verify
- `cargo check`, `cargo clippy --all-targets -- -D warnings`, `cargo test -p <crate>` for the touched crate, `cargo fmt --check`.

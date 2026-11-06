---
name: errors
description: >
  Use when writing or reviewing error handling, validation, exceptions, try/catch, Result types or user-facing error
  messages, in any language. Keeps failures loud, narrow and honest instead of swallowed or hidden.
---

# Error handling

- Never swallow errors: no empty catch, no catch-log-continue where the caller needs to know. Handle meaningfully or propagate.
- Catch the narrowest type, at the level that can act on it.
- Validate at system boundaries (handlers, CLI args, file and network input); trust internal calls. No handling for cases that cannot happen.
- Fail early with a message naming what went wrong and the value involved. No silent fallbacks that mask bugs.
- User-facing errors say what to do next and never leak internals.
- Release resources on every path (`use`, try-with-resources, `finally`, `defer`).

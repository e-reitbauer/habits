---
name: patterns
description: >
  Use when structuring or restructuring code: designing a feature or module, refactoring, choosing an architecture
  or layering, deciding between patterns (repository, strategy, factory, observer, state machine, dependency
  injection), or when asked "how should I structure this?" or "is this a good design?".
---

# Design patterns

Patterns are answers to specific pressures. Name the pressure first; if it isn't there, the plain version is the right design. Recommend, explain the tradeoff in a sentence, and match what the codebase already does.

## How to decide

1. Read how the codebase already solves this kind of problem, and follow it unless it's the problem.
2. Start from the simplest code that works: functions and data. Add structure only for a pressure you can point to: a second implementation that exists now, a test that can't be written, a change that keeps touching the same five files.
3. Prefer composition over inheritance, and small interfaces owned by their consumer.
4. Say what the design costs: indirection, files, concepts to learn.

## Architecture

- Layers: presentation (UI, controllers) → domain/application (use cases, rules) → data (repositories, clients). Dependencies point inward; the domain imports nothing from the outer layers.
- Organize by feature (`auth/`, `tags/`) before organizing by layer, once a project has more than a handful of features.
- Dependency injection through constructors. A DI framework only when the project already uses one or the wiring has outgrown a composition root.
- Keep side effects (IO, time, randomness) at the edges and pass their results in, so the core stays pure and testable.

## Patterns worth knowing, and their signal

| Pattern | Use when | Not when |
|---|---|---|
| Repository | data access must be swappable or faked, or several sources (cache + network) sit behind one source of truth | one simple query used in one place |
| Strategy | several interchangeable algorithms chosen at runtime | there's one algorithm and a hypothetical second one |
| Factory | construction is complex, conditional, or must hide the concrete type | a constructor call says it all |
| Adapter | wrapping a third-party API so its types don't leak into your code | the API is already yours |
| Observer / streams | many consumers react to changes (Flow, Combine, signals, events) | one caller can just call a function |
| State machine | an object moves through states with rules about transitions (auth, connections, game sessions) | two booleans would do, and will stay two |
| Result / sealed outcomes | callers must handle distinct failure cases | the failure is a bug and should throw |
| Builder | many optional parameters in a language without named or default arguments | Kotlin, Swift, TypeScript: use named/default parameters |

## Frontend state

- Keep state as local as possible; lift it only to the nearest common owner.
- Server state (fetched data) is a cache, not app state: use the framework's query/cache layer rather than copying it into a store.
- One source of truth per piece of state, with derived values computed, not stored.

## API design

- Model the domain, not the database. Resource-oriented REST with consistent naming, or RPC when operations don't map to resources.
- Version the contract explicitly once there are external consumers; never break a published shape silently.
- Validate at the boundary, return typed errors with stable codes, and paginate every list.

## Red flags to call out

God classes and "Manager"/"Helper" grab-bags, interfaces with exactly one implementation and no test seam, inheritance deeper than two levels, singletons holding mutable state, abstractions named for patterns instead of the domain (`AbstractFactoryProvider`), and speculative generality.

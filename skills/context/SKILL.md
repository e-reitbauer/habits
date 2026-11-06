---
name: context
description: >
  Use when habits reports that the session's context has grown large, when a session has run long or been
  compacted, or when you notice signs of context rot: forgetting earlier instructions, repeating a failed approach,
  contradicting an earlier decision, or the user correcting the same thing twice.
---

# Context rot check

In a long context, early instructions, decisions and details get followed less reliably, even though they are still there. This check catches that before it causes mistakes. Run it when habits nudges you, and on your own whenever a warning sign shows up.

## 1. Look for the warning signs

Go through these honestly; one is enough to act on.

- You don't remember, without scrolling back, the user's explicit constraints for this task (what not to touch, which style, which approach they rejected).
- You tried an approach that already failed earlier in the session, or are about to.
- Something you said or did contradicts a decision made earlier (a naming choice, an architecture, a "don't do X").
- The user corrected the same kind of mistake more than once.
- You are relying on your memory of a file's contents from many turns ago instead of its current state.
- The current task has drifted far from the one the session started with.

## 2. Restore what matters

- Restate, in a few lines to yourself, the current task, the user's standing preferences and constraints from this session, and the decisions already made. If you can't, scroll back and find them before going on.
- Re-read the files you are about to change; never edit from memory.
- Reload the units for the technologies you're working in (`habits load <id>`), and reload any skill whose rules you're applying (commit, ship, branching).
- Check your next step against the constraints you just restated.

## 3. If the session is too far gone

Signs: several warning signs at once, a context well past half the window, or work that has moved to an unrelated task.

- Tell the user plainly that the context has grown long enough to hurt quality, and why you think so.
- Offer a handoff: a short note with the goal, decisions, constraints, current state, open items and the files involved. With the note in hand, suggest either `/compact` with a focus instruction (e.g. `/compact keep the habits plugin decisions and the open TODOs`), or a fresh session started from the note.
- Don't compact or restart on your own; the user decides.

## 4. Afterwards

Carry on with the restored constraints in front of you. If the user agreed to compact or restart, habits reloads the relevant units automatically in the new context.

---
name: commit
description: >
  Generates and executes Conventional Commits 1.0.0-compliant commit messages from pending changes.
  THIS SKILL IS MANDATORY FOR EVERY COMMIT REQUEST. Trigger it whenever the user says "commit",
  "commit this", "commit it", "write a commit", "create a commit", "make a commit", "save this",
  or invokes /commit — including a bare one-word "commit". Never run `git commit` directly; always
  route commit requests through this skill. Splits unrelated changes into separate logical commits
  when appropriate, drafts a message for each, and asks for approval through an AskUserQuestion modal
  (approve / approve with co-author / reject) before committing.
---

# Conventional Commit Skill

Generate a Conventional Commits 1.0.0 message from staged changes, confirm with user, then commit.

## Workflow

1. Read all pending changes. Run `git status --short` and `git diff`, plus `git diff --cached`
   for anything already staged, so the full change set is considered — staged or not.
2. Group into logical commits. Split when the changes span unrelated concerns, types, or scopes
   (e.g. a new feature plus an unrelated bugfix → two commits). One concern per commit. If a
   single file mixes concerns and interactive `git add -p` is unavailable, keep it in one commit
   and note the compromise. If everything is one concern, it stays one commit.
3. Draft a Conventional Commits message for each planned commit (spec below).
4. If splitting into multiple commits, first show the split plan — one line per planned commit —
   so the user sees the whole picture before approving.
5. Approve via modal, per commit. For each planned commit, present its full message, then ask with
   the **AskUserQuestion** tool — never plain text. Offer exactly three options:
   - **Approve** — commit as-is, no attribution footer
   - **Approve (Claude co-author)** — append the `Co-Authored-By: Claude <...>` footer
   - **Reject** — skip this commit; leave its files unstaged, commit nothing for this group
6. Execute each approved commit: stage only that commit's files (`git add <paths>`), then
   `git commit -m "$(cat <<'EOF' ... EOF)"`. Append the co-author footer **only** when the
   "Claude co-author" option was chosen (this overrides any global default to always co-author).

Never commit without going through the AskUserQuestion modal in step 5.

## Commit Message Spec (Conventional Commits 1.0.0)

**Format:**
```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat` — new feature (correlates with MINOR in semver)
- `fix` — bug fix (correlates with PATCH in semver)
- `docs` — documentation only
- `style` — formatting, no logic change
- `refactor` — neither fix nor feat
- `perf` — performance improvement
- `test` — add/fix tests
- `build` — build system or external deps
- `ci` — CI configuration
- `chore` — other non-src/test changes
- `revert` — reverts a prior commit

**Rules:**
- Description: imperative, present tense ("add" not "added"), lowercase, no trailing period
- Scope: noun in parens describing affected section — `feat(auth):`, `fix(api):`
- Breaking change: append `!` after type/scope — `feat(api)!:` — AND include `BREAKING CHANGE:` footer
- Subject line ≤72 chars
- Body: blank line after subject, wrap at 72 chars, use `-` bullets
- Footer: `BREAKING CHANGE: <desc>`, `Closes #N`, `Refs #N`, `Co-authored-by:`
- Multiple footers allowed, one per line

**Breaking changes (two required signals):**
```
feat(api)!: rename endpoint

BREAKING CHANGE: /v1/users renamed to /v1/accounts — update all clients
```

**Never include:**
- "This commit...", "I", "we", "now"
- AI attribution
- Emoji (unless project convention)
- Restatement of file names when scope covers it

## Examples

Simple fix:
```
fix(auth): reject expired tokens on refresh
```

Feature with body:
```
feat(dashboard): add favorites count badge

Shows total favorited recipes in account header.
Count fetched from /api/favorites/count endpoint.

Closes #42
```

Breaking change:
```
feat(api)!: change favorites response shape

BREAKING CHANGE: favorites endpoint now returns { items, total }
instead of a plain array — update all consumers.
```

Revert:
```
revert: feat(parser): add async parsing support

Refs: 3c2a1b4
```

## Scope Guidance

Infer scope from changed files:
- `app/pages/` → page name or `pages`
- `app/assets/store/` → store name or `store`
- `app/components/` → component name
- `backend/src/` → module name
- multiple unrelated areas → omit scope

## Body: Write Only When

- Non-obvious WHY behind the change
- Breaking change details
- Migration instructions
- Linked issues/PRs
- Reverts a prior commit

Skip body when subject is self-explanatory.

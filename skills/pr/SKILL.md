---
name: pr
description: >
  Generates a pull request title and body from the current branch's commits and diff vs main.
  Conventional-commit-aware: groups changes by type, surfaces breaking changes prominently.
  Use when user says "create a PR", "write PR description", "open PR", "make a pull request", or invokes /pr.
  Shows draft for approval, then runs `gh pr create` only on confirmation.
---

# PR Skill

Generate a PR title + body from branch diff, confirm, then optionally create via `gh pr create`.

## Workflow

1. Run these in parallel:
   - `git log main..HEAD --oneline` — list commits on branch
   - `git diff main..HEAD --stat` — files changed
   - `git diff main..HEAD` — full diff (for context)
2. Draft PR title and body (spec below)
3. Show draft in code block, ask: approve / edit / cancel
4. On approval: run `gh pr create --title "..." --body "$(cat <<'EOF' ... EOF)"` targeting `main`

## PR Title

- Max 70 chars
- Format mirrors conventional commit subject: `<type>(<scope>): <summary>`
- If branch has one dominant type, use it. Mixed changes → use most impactful type
- Imperative mood, no trailing period
- Breaking change → append `!`: `feat(api)!: rename endpoint`

## PR Body Template

```markdown
## Summary
- <bullet: what changed and why — focus on intent, not file names>
- <bullet>
- <bullet if needed>

## Changes
<grouped by type, only types that appear>
**feat:** <brief description>
**fix:** <brief description>
**refactor:** <brief description>

## Breaking Changes
> BREAKING CHANGE: <description> — only include if present, else omit section entirely

## Test plan
- [ ] <thing to verify manually>
- [ ] <edge case to check>```

## Rules

**Summary bullets:**
- 1–4 bullets, each one sentence
- WHY over WHAT — "allows users to see total favorites" not "added count field to response"
- Skip if covered by Changes section

**Changes section:**
- Group by conventional commit type
- Skip types with no commits
- One line per type, not per commit

**Breaking Changes:**
- Only include if any commit has `!` or `BREAKING CHANGE:` footer
- Quote the breaking change description verbatim from the commit

**Test plan:**
- 2–5 items, concrete and checkable
- Based on what actually changed — not generic boilerplate
- Include: happy path, edge cases that the diff touches, regression risk areas

**Never include:**
- File paths as the main description ("changed favorites-store.ts")
- Commit hashes
- "This PR...", "I", "we"
- Redundant sections (omit Breaking Changes if none, omit Changes if only one commit)
- AI attribution, including "Generated with Claude Code" footers

## Scope inference from files

- `app/pages/` → page name
- `app/assets/store/` → store name  
- `app/components/` → component name
- `backend/src/` → backend module
- mixed frontend+backend → omit scope, note in summary

## Examples

Single-focus branch:
```
fix(favorites): correct count endpoint and store sync

## Summary
- Favorites count was returning wrong total due to missing aggregation in repository layer
- Frontend store now reads from dedicated `/favorites/count` endpoint

## Changes
**fix:** add total count field to favorites repository response
**feat:** expose GET /favorites/count route

## Test plan
- [ ] Favorite a recipe, verify count badge updates in account header
- [ ] Unfavorite, verify count decrements
- [ ] Hard refresh — count should persist from server```

Mixed changes:
```
feat(dashboard)!: redesign account page with favorites count

## Summary
- Account page now shows total favorited recipes in header badge
- Favorites store updated to track count separately from list

## Changes
**feat:** favorites count badge in account header
**fix:** store no longer refetches full list on count-only updates
**refactor:** extract favorites API calls into composable

## Breaking Changes
> BREAKING CHANGE: FavoritesStore.items no longer auto-fetches on mount — call fetchFavorites() explicitly

## Test plan
- [ ] Badge shows correct count on page load
- [ ] Count updates immediately on favorite/unfavorite without full reload
- [ ] Old code calling store directly still works or migration path is clear```

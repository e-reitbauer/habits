---
name: ship
description: >
  Ships finished work end to end: checks, commits (via the commit skill), versioning, push,
  pull request (via the pr skill), CI pipeline watching, release and publish verification.
  Use when the user says "ship it", "ship this", "push and watch CI", "release", "cut a release",
  "publish", "bump the version", "anything uncommitted/unpushed?", "did the release run?", or
  invokes /ship.
---

# Ship Skill

Take finished work from the working tree to a verified release, using the project's own
release setup. Each step builds on the one before; stop and report when a step fails.

## Ground rules

- Commits go through the **commit** skill, PRs through the **pr** skill. Never run
  `git commit` or `gh pr create` directly.
- Invoking this skill approves the commit + push for the current work. Merges, tags,
  publishing, and deploys to production still need the user's explicit OK, asked with
  **AskUserQuestion**.
- Never force-push, skip hooks (`--no-verify`), or edit CI secrets.
- Don't bump a version that release tooling bumps itself.

## 1. Preflight

Run in parallel:
- `git status --short`, `git branch --show-current`, `git log @{u}..HEAD --oneline`
  (unpushed), `git fetch` then `git log HEAD..@{u} --oneline` (behind)
- `git remote get-url origin` and `gh auth status`
- `git log $(git describe --tags --abbrev=0 2>/dev/null)..HEAD --oneline` (since last tag)

Check:
- **GitHub account:** remotes may use SSH host aliases (for example `github.com-work`). Make sure `gh` is logged in as the account that owns the repo; if
  not, tell the user to run `gh auth switch`.
- **Behind the remote:** pull/rebase first if the branch is behind.
- **Secrets:** scan the diff for tokens, keys, `.env` files, and credentials before
  anything is committed. Stop and report if found.

## 2. Detect the release setup

| Found | Release mechanism | Version bump |
|---|---|---|
| `release-please-config.json` / release-please action | Release PR from Conventional Commits; merging it tags, releases, publishes | Never manual |
| `.changeset/` | Changesets | Add a changeset (`npx changeset`), don't edit versions |
| semantic-release config | Fully automatic on push | Never manual |
| Workflow on `tags:` | Pushing a tag triggers the release (Docker images, binaries) | Bump manifest if it holds the version, then tag `vX.Y.Z` |
| `package.json` + `npm publish` without tooling | Manual | `npm version <x> --no-git-tag-version` |
| `Cargo.toml` / `pyproject.toml` / `gradle.properties` / `build.gradle(.kts)` | Manual or tag-driven | Edit the version field |
| Xcode project | App Store / TestFlight | `MARKETING_VERSION` (+ `CURRENT_PROJECT_VERSION` build number) |
| Pages / deploy on push only | No versions | Nothing to bump |

Read `.github/workflows/*` to learn what runs on push, PR, tag and merge, and which
commands CI runs (tests, lint, build).

No release setup and no version file: skip versioning unless the user asks for it.

## 3. Pick the version (only when bumping manually)

Use SemVer from the Conventional Commits since the last tag:
- any `!` / `BREAKING CHANGE` → major (before 1.0.0: minor)
- any `feat` → minor
- otherwise `fix` / `perf` → patch
- only `docs` / `chore` / `ci` / `test` / `style` / `refactor` → no release needed

Follow the project's existing tag format (`v1.2.3` vs `1.2.3`) and changelog style. Include
the proposed version in the plan for approval.

## 4. Plan, then local checks

Show one short plan: commits to make, version (if any), push target, PR or not, what CI and
release will do. Then run the same checks CI runs (tests, lint, typecheck, build) locally. Fix
failures before committing; report anything you can't fix.

## 5. Commit and push

1. Commit with the **commit** skill.
2. Pick the target:
   - Repo merges through PRs (protected default branch, or recent history shows merged PRs:
     `gh pr list --state merged --limit 5`): work on a feature branch, push, then open the PR
     with the **pr** skill.
   - Repo pushes to the default branch directly: push it.
   - On the default branch with PR-only history: create a branch first.
3. Push with `git push -u origin <branch>`. If a tag triggers the release, push the tag only
   after the user confirms.

## 6. Watch the pipelines

- Find the runs: `gh run list --branch <branch> --limit 5` (and `gh pr checks <pr>` for PRs).
- Watch them with `gh run watch <id> --exit-status` as a background command; don't poll in a
  loop.
- On failure: `gh run view <id> --log-failed`, find the cause, fix it, commit with the commit
  skill, push, and watch again. Report flaky or unrelated failures instead of retrying blindly.

## 7. Release and verify

- **release-please:** after the push to the default branch, find the release PR
  (`gh pr list --label "autorelease: pending"`), show its version and changelog, and ask the user
  before merging. After the merge, watch the release workflow.
- **Tag-driven:** after the user confirms, push the tag, then watch the tag workflow.
- **Verify the artifact actually exists:**
  - npm: `npm view <pkg>@<version> version`
  - GitHub release: `gh release view <tag>`
  - Docker: the image tag in the registry (workflow output or `docker manifest inspect`)
  - Pages / deploy: the deploy run succeeded and the URL returns 200 (`curl -sI`)
- If a release workflow didn't run or didn't publish, find out why (missing trigger, failed
  job, skipped step, version already published) before suggesting a re-run.

## 8. Loose ends

- Open Dependabot PRs: list them with their check status (`gh pr list --author app/dependabot`).
  Merge only when the user says so.
- Leftover uncommitted or unpushed work: list it.

## 9. Report

End with what shipped: commits, version, PR link, workflow run results, release / package /
deploy links, and anything still pending (release PR waiting, review pending, failed checks).

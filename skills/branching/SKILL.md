---
name: branching
description: >
  Use when creating, naming, syncing, merging or cleaning up git branches, when deciding whether work goes on a
  branch or straight to main, when choosing merge vs rebase vs squash, or when asked which branching strategy a
  project should use (trunk-based, GitHub Flow, Git Flow, release branches).
---

# Branching

## 1. Detect the strategy in use

Follow the project's strategy; don't introduce a new one as a side effect.

- Branches: `git branch -a`. A long-lived `develop` (plus `release/*`, `hotfix/*`) means Git Flow; `release/x.y` branches mean release branches; only `main` plus short feature branches means GitHub Flow or trunk-based.
- How changes land: `gh pr list --state merged --limit 10 --json baseRefName,headRefName,mergeCommit` and `git log --merges --oneline -10`. PR merges into `main` mean a branch-and-PR flow; direct commits on `main` mean trunk-based or a solo project.
- Merge style: merge commits, squash (one commit per PR on main) or rebase (linear history). Check the repo settings (`gh repo view --json squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed`) and match it.
- Protection: if `main` is protected or every change arrives by PR, never commit to it directly.
- Branch names: look at recent ones and copy the pattern (`feat/140-live-player-map`, `fix/login-redirect`, `user/topic`).

## 2. The strategies, and when each fits

| Strategy | Shape | Fits |
|---|---|---|
| Trunk-based | everyone integrates into `main` daily; branches live hours, not days; features hidden behind flags | strong CI, continuous deployment, small experienced teams |
| GitHub Flow | short-lived feature branch, PR, review, merge to `main`, deploy from `main` | most teams and web projects; the default to recommend |
| Git Flow | `develop` for integration, `release/*` to stabilize, `hotfix/*` from `main`, `main` = released | scheduled releases of versioned software that maintains past versions |
| Release branches | `main` moves on; `release/x.y` branches get only backported fixes | supporting several released versions at once (libraries, mobile apps in review) |

When asked to set one up, recommend GitHub Flow unless the release cadence or support needs call for another, and say why.

## 3. Working on branches

- Name it type/scope: `feat/<issue>-<short-topic>`, `fix/<topic>`, `chore/<topic>`, lowercase with hyphens, matching the commit types. Put the issue number in when there is one.
- Branch from the up-to-date base (`git fetch` first): `main`, or `develop` under Git Flow, or the release branch for a backport.
- Keep branches short-lived and focused on one change. Split unrelated work into its own branch.
- Stay current with the base: rebase a private branch onto it, or merge the base in once the branch is shared. Never rewrite history others have pulled.
- Never force-push a shared branch. On your own branch after a rebase, use `git push --force-with-lease`, never plain `--force`.
- Resolve conflicts by understanding both sides; never take "ours" or "theirs" wholesale without reading.
- After the merge, delete the branch locally and on the remote, and switch back to the base.

## 4. Before opening the PR

The branch builds and passes tests, the diff contains only this change, and it is pushed with an upstream (`git push -u origin <branch>`). Then open the PR with the **pr** skill.

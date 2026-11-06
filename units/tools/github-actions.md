---
id: github-actions
title: GitHub Actions
paths: ["**/.github/workflows/*.yml", "**/.github/workflows/*.yaml", "**/action.yml", "**/action.yaml", "**/.github/dependabot.yml"]
commands: ["gh run", "gh workflow"]
---
GitHub Actions. Follow GitHub's security hardening guide (docs.github.com/actions/security-for-github-actions).

Security
- Set `permissions:` explicitly at workflow or job level, as narrow as possible (`contents: read` by default); never rely on the broad default token.
- Pin third-party actions to a full commit SHA with the version in a comment (`uses: owner/action@<sha> # v4.2.0`); first-party `actions/*` at least to a major tag.
- Never interpolate untrusted input (`github.event.*.title`, `body`, branch names) directly into `run:`; pass it through `env:` and quote it.
- Secrets through `secrets.*` and environments with protection rules for production; never echo them. `pull_request_target` with a checkout of PR code is a known hole; avoid it.

Structure
- Trigger narrowly (`paths:`, branch filters); `concurrency:` with `cancel-in-progress: true` for PR builds, `false` for releases.
- Cache dependencies through the setup actions (`setup-node` with `cache:`, `setup-java` with `cache: gradle`) or `actions/cache` with a lockfile hash key.
- Reuse with reusable workflows (`workflow_call`) or composite actions instead of copy-paste; `needs:` for ordering, a matrix for platform or version spreads.
- Set `timeout-minutes` on jobs.

Working with runs
- `gh run list --workflow <file> --limit 5`, `gh run watch <id> --exit-status`, `gh run view <id> --log-failed`.
- Lint workflow changes before pushing when `actionlint` is available; a YAML error only shows up after the push otherwise.
- Keep Dependabot updating actions (`package-ecosystem: github-actions`) alongside the project's dependencies.

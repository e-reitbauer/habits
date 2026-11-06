---
name: secrets
description: >
  Use whenever API keys, tokens, passwords, .env files, config with credentials, or CI/deploy secrets are involved,
  and before staging changes that touch configuration. Keeps credentials out of tracked files, logs and output, and
  makes sure secrets land in the right environment.
---

# Secrets

- Never write a secret into tracked files, fixtures, docs, logs or commit messages. Read it from env vars or a secret store and refer to it by name.
- `.env`-style files stay ignored; commit a `.env.example` with placeholders.
- Scan the diff for credentials before staging. If one was committed or pushed, say so plainly: it has to be rotated, not just deleted.
- Confirm the environment (dev, staging, production) before setting a CI or deploy secret.
- Never print a secret's value; name it instead.
- Don't read credential stores (`~/.ssh`, `~/.aws`, keychains) unless the task needs it.

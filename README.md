# habits

Professional development habits for [Claude Code](https://claude.com/claude-code).

habits gives Claude the habits of a careful developer: clean commits, no stray files, no leaked secrets, dependencies added on purpose. It also brings the specific know-how for each language, tool and workflow a project uses, and only when the project uses it. A Kotlin project gets Kotlin guidance. Your Vue project never sees it.

## Install

```
/plugin install habits --marketplace e-reitbauer/habits
```

Then, optionally, put the `habits` command on your PATH. After one Claude Code session has started with habits installed, run:

```
python3 "$(cat ~/.local/share/habits/root)/habits" install-cli
```

habits needs Python 3 on your PATH and uses only its standard library.

## What's inside

**Skills** cover the things needed every day. Claude loads each one when its situation comes up, and gets a one-line index of all of them at the start of every session.

| Skill | Used when |
|---|---|
| `commit` | committing: Conventional Commits, split by concern, approved before it runs |
| `pr` | opening a pull request: title and body from the branch |
| `ship` | shipping end to end: checks, commit, version, push, CI, release |
| `ui` | designing and building UI like a designer: research, plan, approval, build from the design system, validate |
| `cinematic` | award-level, cinematic sites: storyboarded scroll-driven scenes, three.js and WebGL, fast and accessible |
| `hygiene` | creating files, adding build output, committing: keeps the repo clean |
| `secrets` | touching keys, tokens, `.env` files or CI secrets |
| `dependencies` | adding, upgrading or removing a dependency |
| `errors` | writing error handling and validation |
| `versioning` | picking a version: SemVer, CalVer, build numbers, pre-releases, tags |
| `branching` | branches, merges and branching strategies: trunk-based, GitHub Flow, Git Flow, release branches |
| `patterns` | structuring code: architecture, layering and when a design pattern earns its place |
| `research` | before large, ambiguous or hard-to-reverse work: research facts, brainstorm options, ask only what matters |
| `context` | checking a long session for context rot and recovering from it |
| `units` | listing or loading units by hand |
| `new-unit` | writing a new unit or improving one: triggers, content, validation |

The `ui` skill plans before it builds: a brief, the flows, every state, a map of which existing components each part reuses, a layout sketch, a concept chosen from several, a color system and a motion plan. It gets the plan approved (in an OpenSpec project, as the change proposal), builds only from the project's tokens and components, and then validates the result automatically, by hand or both, as you choose. Whatever you ask for explicitly wins over its guidance. It bundles eight tools: an OKLCH palette generator, a blurred-mesh gradient writer, a contrast checker that also suggests the nearest passing color, a font picker that draws fitting open fonts at random instead of the usual few, an icon fetcher for real icon sets, a background pattern writer, a scanner for hardcoded colors and fonts, and measured checks for a rendered page (overflow, clipped text, small targets, contrast, labels, icon alignment, unreadable sticky bars, broken images). Its evals live in `evals/ui`. The `cinematic` skill builds on it for immersive sites.

Where a skill asks you to choose (how to validate a UI change, how to approve a commit), saying "always" makes Claude remember the answer.

**Units** cover everything extra: one small file per language, framework, tool, platform, database, testing practice or workflow.

| Category | Units |
|---|---|
| languages | `kotlin`, `swift`, `typescript`, `python`, `rust` |
| frameworks | `vue`, `nuxt`, `spring-boot`, `compose-multiplatform` |
| tools | `gradle`, `maven`, `docker-compose`, `xcode`, `github-actions` |
| platforms | `android` |
| databases | `postgres` |
| testing | `unit-testing`, `playwright` |
| workflows | `openspec` |

## How units load

Each unit says when it applies, and loads once per session when the first of its triggers fires:

| Trigger | Fires when | Example |
|---|---|---|
| `paths` | Claude reads or edits a matching file | `["**/*.kt"]` |
| `markers` | the project contains a match, checked at session start | `["*/openspec/specs"]` |
| `commands` | Claude runs a matching shell command | `["adb", "npx playwright"]` |
| manual | you ask for it, or run `habits load <unit>` | |

Loading is lazy on purpose: a session spent on git or docs doesn't carry Android guidance it never uses. When a unit loads, Claude Code shows a line such as `habits: loaded gradle`.

A unit can also run a `script` whose output becomes part of it. The `openspec` unit uses one to list the project's specs and active changes, so a project that uses OpenSpec needs no CLAUDE.md.

When Claude touches a code file type that no unit covers, it offers to write one. When a unit names a language server plugin that isn't installed, it suggests installing it. Both can be switched off.

## Secret guard

Before Claude runs a `git commit` or `git push`, habits scans the added lines it would record for API keys, tokens, private keys and files like `.env`. If it finds one, the command is blocked and Claude is told where (never the value) and what to do. A deliberate fake, such as a key in a test fixture, is allowed by marking its line with `habits:allow-secret`. Switch it off with `habits config set secretGuard off`.

## Long sessions

Long contexts lose earlier instructions: they're still there, but followed less reliably. habits watches the context size from the session transcript:

- A unit loaded long ago is injected again the next time it applies, once the context has grown by `refreshTokens` (150k by default) since it loaded.
- Every `rotCheckEvery` tokens (150k by default), Claude is asked to run the `context` skill's check for context rot, and to suggest a compaction or a fresh session with a handoff note when it finds it.
- After a compaction, everything reloads as it's needed.

Set either threshold to `0` to switch it off.

## Session names

Once the task is clear, Claude names the session with two to four words, such as `fix-login-redirect`, and renames it when the work moves on. The name shows up with your next message. It's set through Claude Code's official hook field, and survives compaction. Switch it off with `habits config set autoTitle off`.

## The CLI

```
habits status [DIR]          what applies to this project and when it loads
habits units                 every unit with its triggers
habits load <unit>           print a unit, exactly as Claude receives it
habits validate              check every unit for errors
habits config                show settings
habits config set <key> <v>  autoLsp off|suggest, autoCreate off|suggest, notify on|off, autoTitle on|off,
                             secretGuard on|off, refreshTokens <n>, rotCheckEvery <n>
habits title <name>          name the current session (Claude runs this)
habits config disable <unit> stop a unit from loading (enable to undo)
habits install-cli [DIR]     put the habits command in DIR (default ~/.local/bin)
habits statusline            how many units this session has loaded, for your status line
```

To show it in Claude Code's status line, pipe the status line's JSON into `habits statusline` from your status line script. It prints `habits 3`:

```sh
input=$(cat)
habits_text=$(printf '%s' "$input" | habits statusline 2>/dev/null)
```

Settings live in `~/.config/habits/config.json`, and per-session state in `~/.cache/habits/`.

## Writing a unit

A unit is a markdown file at `units/<category>/<id>.md`:

```markdown
---
id: gradle
title: Gradle
paths: ["**/*.gradle.kts", "**/gradle/libs.versions.toml"]
commands: ["gradlew", "gradle"]
---
Gradle:
- Always use the wrapper (`./gradlew`), never a global `gradle`.
- Run the narrowest task that proves a change.
```

- `id` matches the file name.
- Write only what Claude wouldn't do right by default, in a few short bullets. Every line costs context in every session that loads the unit.
- Keep globs tight. `paths` globs support `**`, `*`, `?` and `{a,b}`, relative to the project root.
- Optional fields: `markers`, `commands`, `script` (a file next to the unit; it gets `{"cwd", "root"}` as JSON on stdin) and `lsp` (a plugin id such as `kotlin-lsp@claude-plugins-official`).

Run `habits validate` before committing a new unit.

## License

[MIT](LICENSE)

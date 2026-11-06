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
| `ui` | building or fixing UI, avoiding the generic AI-made look |
| `hygiene` | creating files, adding build output, committing: keeps the repo clean |
| `secrets` | touching keys, tokens, `.env` files or CI secrets |
| `dependencies` | adding, upgrading or removing a dependency |
| `errors` | writing error handling and validation |
| `units` | listing or loading units by hand |
| `new-unit` | writing a new unit or improving one: triggers, content, validation |

**Units** cover everything extra: one small file per language, tool, platform, testing practice or workflow.

| Category | Units |
|---|---|
| languages | `kotlin`, `swift` |
| tools | `gradle`, `maven` |
| platforms | `android` |
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

## The CLI

```
habits status [DIR]          what applies to this project and when it loads
habits units                 every unit with its triggers
habits load <unit>           print a unit, exactly as Claude receives it
habits validate              check every unit for errors
habits config                show settings
habits config set <key> <v>  autoLsp off|suggest, autoCreate off|suggest, notify on|off
habits config disable <unit> stop a unit from loading (enable to undo)
habits install-cli [DIR]     put the habits command in DIR (default ~/.local/bin)
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

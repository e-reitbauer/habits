---
name: units
description: >
  Use when the user asks to load, list, show or check habits units, asks which guidance applies to the current
  project, or names a technology unit to pull in by hand. Examples: "load the maven unit", "what habits apply here?".
---

# Habits units

Units are the granular guidance files for languages, tools, platforms, testing and workflows. Most load on their own when a matching file is touched, a matching command runs, or a marker exists in the project. This skill covers loading them by hand and reporting on them.

Use the habits CLI whose path was given at session start (`python3 "<plugin root>/habits" <command>`):

- `units`: every unit with its triggers. Use it to find the right id.
- `load <id>`: prints the unit. Follow its contents as project instructions for the rest of the session.
- `status`: which units apply to this project and why, file types with no unit, missing LSPs, config.
- `config`, `config set autoLsp|autoCreate off|suggest`, `config set notify|autoTitle on|off`, `config disable|enable <id>`: only when the user asks to change behaviour.

When the user asks for a unit that doesn't exist, say so and list the closest ids.

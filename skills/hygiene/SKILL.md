---
name: hygiene
description: >
  Use before creating files or folders in a project, when a tool or build step produces output, and before committing.
  Keeps the repository clean: no stray folders or scratch files, correct .gitignore entries, no build output or IDE files
  in version control. Use it even when the task is about something else and only touches files on the side.
---

# Repository hygiene

- Leave the tree as you found it, plus the intended change. Temporary files go in the session scratchpad or `$TMPDIR`; remove what you created when done.
- Build output, caches, IDE folders, OS files (`.DS_Store`) and local env files never go into version control.
- When something you add produces output, gitignore its folder in the same change, with the narrowest anchored pattern (`/build/`, not `build`).
- Leave other tools' folders (`.idea/`, `.vscode/`, `.claude/`) alone unless asked.
- Don't reformat or reorder files you aren't otherwise changing.
- Before committing, check `git status` for anything unintended, and stage by path.

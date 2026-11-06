"""Hook handlers. Each reads the hook payload and returns (text to inject, ids of units it loaded)."""

import os
import re
from pathlib import Path

import config
from units import ROOT, load_units, project_root

# Extensions that never call for a unit of their own
NON_CODE = {
    "", "md", "txt", "json", "jsonc", "yaml", "yml", "toml", "lock", "csv", "tsv", "log",
    "png", "jpg", "jpeg", "gif", "svg", "webp", "ico", "pdf", "env", "gitignore", "properties",
    "xml", "html", "css", "sql", "sh", "zsh", "bash", "bat", "ttf", "otf", "woff", "woff2",
    "resolved", "jar", "zip", "keystore", "jks",
}
FILE_TOOLS = {"Read", "Edit", "Write", "MultiEdit", "NotebookEdit"}


def _block(unit, cwd, root):
    return f"<habits-unit id=\"{unit.id}\">\n{unit.content(cwd, root)}\n</habits-unit>"


def skill_index():
    """One line per bundled skill: its name and the first sentence of its description."""
    lines = []
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        words, inside = [], False
        for line in skill.read_text(encoding="utf-8").splitlines()[1:]:
            if line.startswith("description:"):
                inside = True
                words.append(line[len("description:"):].strip().lstrip(">|").strip())
            elif inside and line[:1].isspace():
                words.append(line.strip())
            elif inside or line == "---":
                break
        text = " ".join(w for w in words if w)
        lines.append(f"- {skill.parent.name}: {re.split(r'(?<=[.!?]) ', text)[0]}")
    return "\n".join(lines)


def session_start(payload):
    session = payload.get("session_id", "default")
    cwd = Path(payload.get("cwd") or os.getcwd())
    root = project_root(cwd)
    # A fresh, cleared or compacted context has none of the units loaded before
    config.reset_state(session)
    config.register_root(ROOT)

    cfg = config.load_config()
    units, _ = load_units()
    marked = [u for u in units if u.markers and u.id not in cfg["disabled"] and u.matches_markers(root)]
    if marked:
        config.save_state(session, {"loaded": [u.id for u in marked], "suggested": []})

    parts = [
        "habits is active. Load these skills with the Skill tool whenever the situation applies, "
        "even mid-task:\n" + skill_index(),
        "Extra guidance arrives as <habits-unit> blocks when you touch matching files or run matching "
        "commands; follow them like project instructions. The habits CLI is "
        f"`python3 \"{ROOT}/habits\"` (`units`, `load <id>`, `status`).",
        *(_block(u, cwd, root) for u in marked),
    ]
    return "\n\n".join(parts), [u.id for u in marked]


def _relpath(file_path, cwd):
    path = Path(file_path)
    try:
        return path.resolve().relative_to(cwd.resolve()).as_posix()
    except ValueError:
        return path.as_posix().lstrip("/")


def post_tool_use(payload):
    tool = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}
    session = payload.get("session_id", "default")
    cwd = Path(payload.get("cwd") or os.getcwd())

    if tool in FILE_TOOLS:
        target = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not target:
            return "", []
        rel = _relpath(target, cwd)
        match = lambda u: u.paths and u.matches_path(rel)
    elif tool == "Bash" and tool_input.get("command"):
        rel = None
        command = tool_input["command"]
        match = lambda u: u.commands and u.matches_command(command)
    else:
        return "", []

    cfg = config.load_config()
    state = config.load_state(session)
    units, _ = load_units()
    matched = [u for u in units if u.id not in cfg["disabled"] and match(u)]
    fresh = [u for u in matched if u.id not in state["loaded"]]
    root = project_root(cwd) if fresh else cwd

    parts = [_block(u, cwd, root) for u in fresh]
    state["loaded"] += [u.id for u in fresh]

    if cfg["autoLsp"] == "suggest":
        installed = config.installed_plugins()
        for u in fresh:
            key = f"lsp:{u.lsp}"
            if u.lsp and u.lsp not in installed and key not in state["suggested"]:
                parts.append(f"habits: the {u.title} unit recommends the LSP plugin `{u.lsp}`, which is "
                             f"not installed. Mention once that the user can run `/plugin install {u.lsp}` "
                             "for code intelligence.")
                state["suggested"].append(key)

    if rel is not None and cfg["autoCreate"] == "suggest" and not matched:
        ext = Path(rel).suffix.lstrip(".").lower()
        key = f"ext:{ext}"
        if ext not in NON_CODE and key not in state["suggested"]:
            parts.append(f"habits: no unit covers .{ext} files. If this project actively uses that "
                         "technology, offer once to create a habits unit for it (new-unit skill).")
            state["suggested"].append(key)

    if parts:
        config.save_state(session, state)
    return "\n\n".join(parts), [u.id for u in fresh]

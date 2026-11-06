"""Hook handlers. Each reads the hook payload and returns a dict with any of:
context (text to inject), loaded (ids of units it loaded), title (session title to set),
deny (reason to refuse the tool call).
"""

import json
import os
import re
from pathlib import Path

import config
import guard
from units import ROOT, command_words, load_units, project_root

# Extensions that never call for a unit of their own
NON_CODE = {
    "", "md", "txt", "json", "jsonc", "yaml", "yml", "toml", "lock", "csv", "tsv", "log",
    "png", "jpg", "jpeg", "gif", "svg", "webp", "ico", "pdf", "env", "gitignore", "properties",
    "xml", "html", "css", "sql", "sh", "zsh", "bash", "bat", "ttf", "otf", "woff", "woff2",
    "resolved", "jar", "zip", "keystore", "jks",
}
FILE_TOOLS = {"Read", "Edit", "Write", "MultiEdit", "NotebookEdit"}
TITLE_LIMIT = 60

NAMING = ("Name this session: as soon as the task is clear, run `habits title \"<name>\"` with two to four "
          "lowercase words joined by hyphens that name the task or project (e.g. `fix-login-redirect`). "
          "Run it again when the work moves to a clearly different task. The title appears with the "
          "user's next message.")


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


def requested_title(command):
    """The title from a `habits title <name>` call inside a shell command, if any."""
    for words in command_words(command):
        if words[0] == "habits" and words[1:2] == ["title"]:
            name = " ".join(words[2:])
        elif words[0].startswith("python") and len(words) > 2 and words[1].endswith("/habits") and words[2] == "title":
            name = " ".join(words[3:])
        else:
            continue
        name = name.strip()
        if name and len(name) <= TITLE_LIMIT and "\n" not in name:
            return name
    return None


def session_start(payload):
    session = payload.get("session_id", "default")
    cwd = Path(payload.get("cwd") or os.getcwd())
    root = project_root(cwd)
    # A fresh, cleared or compacted context has lost the units loaded before; a resumed one still has them
    if payload.get("source") != "resume":
        title = config.load_state(session).get("title")
        config.reset_state(session)
        if title:
            config.save_state(session, {"loaded": {}, "suggested": [], "title": title})
    config.register_root(ROOT)

    cfg = config.load_config()
    state = config.load_state(session)
    units, _ = load_units()
    marked = [u for u in units if u.markers and u.id not in cfg["disabled"]
              and u.id not in state["loaded"] and u.matches_markers(root)]
    if marked:
        state["loaded"].update({u.id: 0 for u in marked})
        config.save_state(session, state)

    parts = [
        "habits is active. Load these skills with the Skill tool whenever the situation applies, "
        "even mid-task:\n" + skill_index(),
        "Extra guidance arrives as <habits-unit> blocks when you touch matching files or run matching "
        "commands; follow them like project instructions. The habits CLI is `habits` "
        f"(or `python3 \"{ROOT}/habits\"`): `units`, `load <id>`, `status`.",
    ]
    if cfg["autoTitle"] == "on" and payload.get("source") != "resume" and not state.get("title"):
        parts.append(NAMING)
    parts += [_block(u, cwd, root) for u in marked]
    return {"context": "\n\n".join(parts), "loaded": [u.id for u in marked]}


def pre_tool_use(payload):
    command = (payload.get("tool_input") or {}).get("command")
    if payload.get("tool_name") != "Bash" or not command or "git" not in command:
        return {}
    if config.load_config()["secretGuard"] != "on":
        return {}
    reason = guard.check_command(command, payload.get("cwd") or os.getcwd())
    return {"deny": reason} if reason else {}


def context_tokens(transcript_path):
    """Current context size in tokens, from the usage of the transcript's latest assistant message."""
    if not transcript_path:
        return None
    try:
        with open(transcript_path, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            fh.seek(max(0, fh.tell() - 2_000_000))
            lines = fh.read().decode("utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        if '"compact_boundary"' in line:  # compacted after the last reply: its usage is stale
            try:
                return int(json.loads(line)["compactMetadata"]["postTokens"])
            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                return None
        if '"usage"' not in line or '"assistant"' not in line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        usage = (entry.get("message") or {}).get("usage")
        if entry.get("type") == "assistant" and usage:
            return sum(usage.get(k) or 0 for k in
                       ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
    return None


ROT_CHECK = ("habits: this session's context is now about {k}k tokens. Long contexts lose earlier "
             "instructions and details. Before answering, load the `context` skill and run its check.")


def prompt_submit(payload):
    session = payload.get("session_id", "default")
    cfg = config.load_config()
    state = config.load_state(session)
    result, changed = {}, False

    title = state.get("pendingTitle")
    if title and title != state.get("title") and cfg["autoTitle"] == "on":
        state["title"] = result["title"] = title
        changed = True

    every = cfg["rotCheckEvery"]
    tokens = context_tokens(payload.get("transcript_path")) if every else None
    if tokens is not None:
        last = state.get("rotCheckAt", 0)
        if tokens < last:  # the context shrank (compaction): start counting again
            state["rotCheckAt"] = tokens
            changed = True
        elif tokens - last >= every:
            state["rotCheckAt"] = tokens
            result["context"] = ROT_CHECK.format(k=tokens // 1000)
            changed = True

    if changed:
        config.save_state(session, state)
    return result


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
    title = None

    if tool in FILE_TOOLS:
        target = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not target:
            return {}
        rel = _relpath(target, cwd)
        match = lambda u: u.paths and u.matches_path(rel)
    elif tool == "Bash" and tool_input.get("command"):
        rel = None
        command = tool_input["command"]
        title = requested_title(command)
        match = lambda u: u.commands and u.matches_command(command)
    else:
        return {}

    cfg = config.load_config()
    state = config.load_state(session)
    units, _ = load_units()
    matched = [u for u in units if u.id not in cfg["disabled"] and match(u)]
    fresh = [u for u in matched if u.id not in state["loaded"]]
    tokens = context_tokens(payload.get("transcript_path")) if matched else None

    # A unit loaded long ago sits far back in a long context and gets followed less: inject it again
    stale = []
    if tokens is not None and cfg["refreshTokens"]:
        for u in matched:
            if u.id not in state["loaded"]:
                continue
            at = state["loaded"][u.id]
            if at is None or tokens < at:  # unknown position, or the context shrank: restart the count
                state["loaded"][u.id] = tokens
            elif tokens - at >= cfg["refreshTokens"]:
                stale.append(u)

    root = project_root(cwd) if fresh or stale else cwd
    parts = [_block(u, cwd, root) for u in fresh]
    parts += [f"habits: refreshing the {u.title} unit, loaded about {(tokens - state['loaded'][u.id]) // 1000}k "
              f"tokens ago.\n{_block(u, cwd, root)}" for u in stale]
    for u in fresh + stale:
        state["loaded"][u.id] = tokens or 0

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

    if title:
        state["pendingTitle"] = title
    if parts or title or stale:
        config.save_state(session, state)
    return {"context": "\n\n".join(parts), "loaded": [u.id for u in fresh],
            "refreshed": [u.id for u in stale]}

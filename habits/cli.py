"""habits CLI: hook entry point plus status, units, load, config and validate."""

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

import config
import hooks
from units import ROOT, glob_regex, load_units, project_root

HOOKS = {"session-start": ("SessionStart", hooks.session_start),
         "post-tool-use": ("PostToolUse", hooks.post_tool_use)}
SKIP_DIRS = {".git", "node_modules", "build", "dist", "target", ".gradle", ".idea", ".venv", "__pycache__"}


def cmd_hook(args):
    event, handler = HOOKS[args[0]]
    try:
        text, loaded = handler(json.load(sys.stdin))
    except Exception as e:  # a broken hook must never break the session
        print(f"habits {args[0]}: {e}", file=sys.stderr)
        return 0
    output = {}
    if text:
        output["hookSpecificOutput"] = {"hookEventName": event, "additionalContext": text}
    if loaded and config.load_config()["notify"] == "on":
        output["systemMessage"] = "habits: loaded " + ", ".join(loaded)
    if output:
        print(json.dumps(output))
    return 0


def _project_files(root):
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-co", "--exclude-standard"],
                             capture_output=True, text=True, timeout=10)
        if out.returncode == 0:
            return out.stdout.splitlines()
    except (OSError, subprocess.TimeoutExpired):
        pass
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        files += [Path(dirpath, f).relative_to(root).as_posix() for f in filenames]
        if len(files) > 50000:
            break
    return files


def cmd_status(args):
    root = project_root(Path(args[0] if args else os.getcwd()).resolve())
    cfg = config.load_config()
    units, errors = load_units()
    files = _project_files(root)
    installed = config.installed_plugins()

    print(f"habits status for {root}  ({len(files)} files)\n")
    print("Skills (available in every session, each loads when its situation comes up):")
    print("  " + ", ".join(sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))))

    at_start, on_use, covered, listed = [], [], set(), set()
    for u in units:
        if u.id in cfg["disabled"]:
            continue
        if u.markers and u.matches_markers(root):
            at_start.append(u)
            listed.add(u.id)
            continue
        hits = [f for f in files if u.paths and u.matches_path(f)]
        covered.update(hits)
        if hits:
            note = f"{len(hits)} matching files"
            if u.commands:
                note += f", or on running {' / '.join(u.commands)}"
            if u.lsp:
                note += f"; LSP {'installed' if u.lsp in installed else 'not installed: ' + u.lsp}"
            on_use.append((u, note))
            listed.add(u.id)

    print("\nUnits that load at session start (their marker is in this project):")
    print("  " + (", ".join(u.id for u in at_start) or "none"))
    print("\nUnits that load the first time a matching file is touched in this project:")
    for u, note in on_use or []:
        print(f"  {u.id:<14} {note}")
    if not on_use:
        print("  none")
    others = [u for u in units if u.id not in listed and u.id not in cfg["disabled"]]
    by_command = [u for u in others if u.commands]
    if by_command:
        print("\nOther units that load when you run one of their commands:")
        for u in by_command:
            print(f"  {u.id:<14} {' / '.join(u.commands)}")
    manual = [u.id for u in others if u.triggers == ["manual"]]
    if manual:
        print(f"\nUnits that load only on request: {', '.join(manual)}")
    if cfg["disabled"]:
        print(f"\nDisabled units: {', '.join(cfg['disabled'])}")

    gaps = Counter(Path(f).suffix.lstrip(".").lower() for f in files if f not in covered)
    gaps = [(e, n) for e, n in gaps.most_common() if e not in hooks.NON_CODE][:10]
    if gaps:
        print("\nFile types with no unit:")
        width = max(len(e) for e, _ in gaps) + 2
        for ext, n in gaps:
            print(f"  .{ext:<{width}} {n} file{'' if n == 1 else 's'}")
    print(f"\nConfig ({config.CONFIG_FILE}): autoLsp={cfg['autoLsp']} autoCreate={cfg['autoCreate']} "
          f"notify={cfg['notify']}")
    if errors:
        print(f"\n{len(errors)} unit error(s); run `habits validate`.")
    return 0


def cmd_units(args):
    units, _ = load_units()
    for u in units:
        triggers = []
        if u.paths:
            triggers.append("files " + ", ".join(u.paths))
        if u.markers:
            triggers.append("markers " + ", ".join(u.markers))
        if u.commands:
            triggers.append("commands " + ", ".join(u.commands))
        print(f"{u.category + '/' + u.id:<24} {' | '.join(triggers) or 'manual'}")
    return 0


def cmd_load(args):
    if len(args) != 1:
        print("usage: habits load <unit>", file=sys.stderr)
        return 1
    unit = next((u for u in load_units()[0] if u.id == args[0]), None)
    if not unit:
        print(f"no unit {args[0]!r}; see `habits units`", file=sys.stderr)
        return 1
    cwd = Path(os.getcwd())
    print(hooks._block(unit, cwd, project_root(cwd)))
    return 0


def cmd_config(args):
    cfg = config.load_config()
    if not args:
        print(json.dumps(cfg, indent=2))
        return 0
    action, rest = args[0], args[1:]
    if action == "get" and len(rest) == 1:
        print(json.dumps(cfg.get(rest[0])))
        return 0
    if action == "set" and len(rest) == 2:
        key, value = rest
        if key not in config.CHOICES:
            print(f"unknown key {key!r}; settable: {', '.join(config.CHOICES)}", file=sys.stderr)
            return 1
        if value not in config.CHOICES[key]:
            print(f"{key} must be one of: {', '.join(config.CHOICES[key])}", file=sys.stderr)
            return 1
        cfg[key] = value
    elif action in ("enable", "disable") and len(rest) == 1:
        if rest[0] not in {u.id for u in load_units()[0]}:
            print(f"no unit {rest[0]!r}; see `habits units`", file=sys.stderr)
            return 1
        disabled = set(cfg["disabled"])
        (disabled.add if action == "disable" else disabled.discard)(rest[0])
        cfg["disabled"] = sorted(disabled)
    else:
        print("usage: habits config [get KEY | set KEY VALUE | enable UNIT | disable UNIT]", file=sys.stderr)
        return 1
    config.save_config(cfg)
    print(json.dumps(cfg, indent=2))
    return 0


def cmd_validate(args):
    units, errors = load_units()
    warnings, seen, globs = [], {}, {}
    for u in units:
        rel = u.file.relative_to(ROOT)
        if u.id in seen:
            errors.append(f"{rel}: id {u.id!r} already used by {seen[u.id]}")
        seen[u.id] = rel
        if u.id != u.file.stem:
            errors.append(f"{rel}: id {u.id!r} must match the file name")
        if not u.body:
            errors.append(f"{rel}: empty body")
        if u.lsp and "@" not in u.lsp:
            errors.append(f"{rel}: lsp must be a plugin id like name@marketplace")
        if u.script and not (u.file.parent / u.script).is_file():
            errors.append(f"{rel}: script {u.script!r} not found next to the unit")
        for m in u.markers:
            if "{" in m or m.startswith("/"):
                errors.append(f"{rel}: marker {m!r} must be a relative glob without {{}}")
        for c in u.commands:
            if not c.split():
                errors.append(f"{rel}: empty command prefix")
        for g in u.paths:
            try:
                glob_regex(g)
            except ValueError as e:
                errors.append(f"{rel}: {e}")
            if g in globs:
                warnings.append(f"{rel}: glob {g!r} also in {globs[g]}")
            globs[g] = rel
        lines = len(u.body.splitlines())
        if lines > 40:
            warnings.append(f"{rel}: {lines} lines; units should stay short")
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(units)} units, {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


LAUNCHER = """#!/bin/sh
# habits CLI launcher, written by `habits install-cli`. Finds the plugin wherever Claude Code keeps it.
root=$(cat "${XDG_DATA_HOME:-$HOME/.local/share}/habits/root" 2>/dev/null)
if [ -z "$root" ] || [ ! -d "$root/habits" ]; then
  echo "habits: plugin not found. Start a Claude Code session once so it can register itself." >&2
  exit 1
fi
exec python3 "$root/habits" "$@"
"""


def cmd_install_cli(args):
    target_dir = Path(args[0]).expanduser() if args else Path.home() / ".local" / "bin"
    target = target_dir / "habits"
    if target.exists() and "habits install-cli" not in target.read_text(errors="replace"):
        print(f"{target} exists and was not written by habits; not touching it.", file=sys.stderr)
        return 1
    target_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(LAUNCHER)
    target.chmod(0o755)
    config.register_root(ROOT)
    print(f"Installed {target}")
    if str(target_dir) not in os.environ.get("PATH", "").split(os.pathsep):
        print(f"{target_dir} is not on your PATH. Add this to your shell profile:\n"
              f"  export PATH=\"{target_dir}:$PATH\"")
    return 0


HELP = """habits: professional development habits for Claude Code

Usage: habits <command> [args]

  status [DIR]          what applies to this project: skills, units and when they load,
                        file types no unit covers, LSP status
  units                 every unit with its triggers
  load <unit>           print a unit (what Claude gets when it loads)
  validate              check all units for errors
  config                show settings
  config set <key> <v>  autoLsp off|suggest, autoCreate off|suggest, notify on|off
  config disable <unit> stop a unit from loading (enable to undo)
  install-cli [DIR]     put a `habits` command in DIR (default ~/.local/bin)
  help                  show this help
"""


def cmd_help(args):
    print(HELP, end="")
    return 0


COMMANDS = {"hook": cmd_hook, "status": cmd_status, "units": cmd_units, "load": cmd_load,
            "config": cmd_config, "validate": cmd_validate, "install-cli": cmd_install_cli,
            "help": cmd_help, "--help": cmd_help, "-h": cmd_help}


def main(argv):
    if not argv:
        return cmd_help([])
    if argv[0] not in COMMANDS or (argv[0] == "hook" and (len(argv) < 2 or argv[1] not in HOOKS)):
        print(f"habits: unknown command {' '.join(argv)!r}\n", file=sys.stderr)
        print(HELP, end="", file=sys.stderr)
        return 2
    return COMMANDS[argv[0]](argv[1:])

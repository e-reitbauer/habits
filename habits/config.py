"""User config (~/.config/habits/config.json) and per-session state (~/.cache/habits)."""

import json
import os
import time
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "habits"
CACHE_DIR = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "habits"
DATA_DIR = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share") / "habits"
CONFIG_FILE = CONFIG_DIR / "config.json"
ROOT_FILE = DATA_DIR / "root"

DEFAULTS = {"autoLsp": "suggest", "autoCreate": "suggest", "notify": "on", "disabled": []}
CHOICES = {"autoLsp": ("off", "suggest"), "autoCreate": ("off", "suggest"), "notify": ("on", "off")}


def load_config():
    config = dict(DEFAULTS)
    try:
        config.update(json.loads(CONFIG_FILE.read_text()))
    except FileNotFoundError:
        pass
    return config


def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2) + "\n")


def register_root(root):
    """Record where the plugin lives, so the `habits` launcher finds it after updates move it."""
    if ROOT_FILE.is_file() and ROOT_FILE.read_text().strip() == str(root):
        return
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ROOT_FILE.write_text(str(root) + "\n")


def _state_file(session_id):
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_") or "default"
    return CACHE_DIR / "sessions" / f"{safe}.json"


def load_state(session_id):
    try:
        return json.loads(_state_file(session_id).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {"loaded": [], "suggested": []}


def save_state(session_id, state):
    path = _state_file(session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state))


def reset_state(session_id):
    _state_file(session_id).unlink(missing_ok=True)
    sessions = CACHE_DIR / "sessions"
    if sessions.is_dir():
        cutoff = time.time() - 7 * 86400
        for old in sessions.glob("*.json"):
            if old.stat().st_mtime < cutoff:
                old.unlink(missing_ok=True)


def installed_plugins():
    path = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    try:
        return set(json.loads(path.read_text()).get("plugins", {}))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

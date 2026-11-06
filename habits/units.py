"""Units: small markdown files of extra guidance, loaded when one of their triggers fires.

Triggers (any combination; a unit with none loads only on request):
  paths:    globs of files Claude reads or edits         e.g. ["**/*.kt"]
  markers:  globs that exist in the project at start    e.g. ["openspec/specs", "*/openspec/specs"]
  commands: shell command prefixes Claude runs          e.g. ["docker compose", "adb"]
A unit may also name a `script` (next to the unit file) whose output is appended to its body.

Frontmatter is a YAML subset: `key: value`, `key: [a, "b"]`, or a key followed by `- item` lines.
"""

import json
import os
import re
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UNITS_DIR = ROOT / "units"
FIELDS = {"id", "title", "paths", "markers", "commands", "script", "lsp"}
WRAPPERS = {"sudo", "time", "nohup", "env", "exec"}


@dataclass
class Unit:
    id: str
    title: str
    body: str
    file: Path
    paths: list = field(default_factory=list)
    markers: list = field(default_factory=list)
    commands: list = field(default_factory=list)
    script: str = ""
    lsp: str = ""

    @property
    def category(self):
        return self.file.parent.name

    @property
    def triggers(self):
        return [t for t in ("paths", "markers", "commands") if getattr(self, t)] or ["manual"]

    def matches_path(self, relpath):
        return any(glob_regex(g).fullmatch(relpath) for g in self.paths)

    def matches_markers(self, root):
        return any(next(root.glob(m), None) is not None for m in self.markers)

    def matches_command(self, command):
        for words in command_words(command):
            for prefix in self.commands:
                p = prefix.split()
                if words[:len(p)] == p:
                    return True
        return False

    def content(self, cwd, root):
        """The body plus the script's output, if the unit has a script."""
        if not self.script:
            return self.body
        script = self.file.parent / self.script
        cmd = ["python3", str(script)] if script.suffix == ".py" else [str(script)]
        try:
            out = subprocess.run(cmd, input=json.dumps({"cwd": str(cwd), "root": str(root)}),
                                 capture_output=True, text=True, timeout=5).stdout.strip()
        except (OSError, subprocess.TimeoutExpired) as e:
            out = f"(script {self.script} failed: {e})"
        return f"{out}\n\n{self.body}" if out else self.body


def command_words(command):
    """Yield the words of each simple command in a shell line, wrappers and env assignments removed."""
    for segment in re.split(r"&&|\|\||[;|\n]", command):
        try:
            words = shlex.split(segment)
        except ValueError:
            words = segment.split()
        while words and (words[0] in WRAPPERS or re.match(r"^[A-Za-z_]\w*=", words[0])):
            words = words[1:]
        if words:
            yield [os.path.basename(words[0]), *words[1:]]


def _scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text):
    """Return (meta, body, errors)."""
    if not text.startswith("---\n"):
        return {}, text, ["missing frontmatter (file must start with ---)"]
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text, ["frontmatter is not closed with ---"]
    meta, errors, key = {}, [], None
    for n, line in enumerate(text[4:end].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key and isinstance(meta.get(key), list):
            meta[key].append(_scalar(item.group(1)))
            continue
        kv = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if not kv:
            errors.append(f"line {n}: cannot parse {line!r}")
            continue
        key, value = kv.group(1), kv.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            meta[key] = [_scalar(v) for v in value[1:-1].split(",") if v.strip()]
        elif value == "":
            meta[key] = []
        else:
            meta[key] = _scalar(value)
    return meta, text[end + 4:].lstrip("\n"), errors


_glob_cache = {}


def glob_regex(glob):
    """Compile a glob with **, *, ? and {a,b} into a regex over posix paths."""
    if glob in _glob_cache:
        return _glob_cache[glob]
    out, i = [], 0
    while i < len(glob):
        c = glob[i]
        if glob.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif glob.startswith("**", i):
            out.append(".*")
            i += 2
        elif c == "*":
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        elif c == "{":
            close = glob.find("}", i)
            if close == -1:
                raise ValueError(f"unclosed {{ in {glob!r}")
            out.append("(?:" + "|".join(re.escape(p) for p in glob[i + 1:close].split(",")) + ")")
            i = close + 1
        else:
            out.append(re.escape(c))
            i += 1
    _glob_cache[glob] = re.compile("".join(out))
    return _glob_cache[glob]


def _as_list(value):
    return [value] if isinstance(value, str) else list(value or [])


def load_units():
    """Return (units, errors) for every units/**/*.md file."""
    units, errors = [], []
    for path in sorted(UNITS_DIR.rglob("*.md")):
        meta, body, errs = parse_frontmatter(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT)
        errors += [f"{rel}: {e}" for e in errs]
        unknown = set(meta) - FIELDS
        if unknown:
            errors.append(f"{rel}: unknown field(s) {', '.join(sorted(unknown))}")
        units.append(Unit(
            id=str(meta.get("id", path.stem)),
            title=str(meta.get("title", path.stem)),
            body=body.strip(),
            file=path,
            paths=_as_list(meta.get("paths")),
            markers=_as_list(meta.get("markers")),
            commands=_as_list(meta.get("commands")),
            script=str(meta.get("script") or ""),
            lsp=str(meta.get("lsp") or ""),
        ))
    return units, errors


def project_root(cwd):
    try:
        top = subprocess.run(["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=3).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        top = ""
    return Path(top) if top else Path(cwd)

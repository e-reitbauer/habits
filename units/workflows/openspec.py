"""Script for the openspec unit: prints the spec index and active changes of every OpenSpec root.

Reads {"cwd": ..., "root": ...} on stdin.
"""

import json
import re
import sys
from pathlib import Path


def find_roots(cwd, root):
    """Nearest openspec/ at or above cwd; otherwise every one up to two levels inside the project."""
    for d in [cwd, *cwd.parents]:
        if (d / "openspec" / "specs").is_dir():
            return [d / "openspec"]
        if d == root:
            break
    found = [*root.glob("*/openspec/specs"), *root.glob("*/*/openspec/specs")]
    return sorted(s.parent for s in found if "node_modules" not in s.parts)


def purpose(spec):
    m = re.search(r"^## Purpose\s*\n+(.+)$", spec.read_text(encoding="utf-8"), re.M)
    return re.sub(r"([.!?]) .*", r"\1", m.group(1).strip())[:220] if m else ""


def describe(root):
    out = [f"OpenSpec root: {root}", f"Specs (read {root}/specs/<id>/spec.md):"]
    out += [f"- {s.parent.name}: {purpose(s)}" for s in sorted(root.glob("specs/*/spec.md"))]
    changes = []
    for change in sorted(p for p in root.glob("changes/*") if p.is_dir()):
        if change.name == "archive" or change.name.startswith("."):
            continue
        tasks = change / "tasks.md"
        text = tasks.read_text(encoding="utf-8") if tasks.is_file() else ""
        done = len(re.findall(r"^\s*- \[[xX]\]", text, re.M))
        total = len(re.findall(r"^\s*- \[[ xX]\]", text, re.M))
        changes.append(f"- {change.name} ({done}/{total} tasks done)")
    if changes:
        out += ["Active changes:", *changes]
    for name in ("config.yaml", "config.yml"):
        cfg = root / name
        if cfg.is_file():
            extra = [l for l in cfg.read_text(encoding="utf-8").splitlines()
                     if l.strip() and not l.lstrip().startswith("#") and not l.startswith("schema:")]
            if extra:
                out += [f"Project context ({cfg}):", *extra]
            break
    return "\n".join(out)


def main():
    ctx = json.load(sys.stdin)
    roots = find_roots(Path(ctx["cwd"]).resolve(), Path(ctx["root"]).resolve())
    print("\n\n".join(describe(r) for r in roots))


if __name__ == "__main__":
    main()

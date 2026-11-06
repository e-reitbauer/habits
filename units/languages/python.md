---
id: python
title: Python
paths: ["**/*.py", "**/pyproject.toml", "**/requirements*.txt"]
commands: ["pytest", "uv", "pip"]
lsp: pyright-lsp@claude-plugins-official
---
Python. Follow PEP 8 and PEP 257, and the project's formatter and linter (ruff, black) when configured.

Style
- snake_case functions and variables, PascalCase classes, UPPER_SNAKE constants, a leading underscore for internals.
- Type hints on every public function (PEP 484/604 syntax: `list[str]`, `str | None`). Keep them honest; check with pyright or mypy when the project uses one.
- Imports at the top, grouped stdlib / third-party / local; no wildcard imports.
- f-strings for formatting; `pathlib.Path` over `os.path`; context managers (`with`) for files, locks and connections.
- Docstrings for public modules, classes and functions: one summary line, then details if needed.

Idioms
- `dataclass` (or `attrs`/pydantic where the project uses them) for data; `enum.Enum` for fixed choices.
- Comprehensions and generators over manual loops that build lists; `any()`, `all()`, `sum()` over flag loops.
- EAFP where it reads clearer (`try` the operation, catch the specific exception), never a bare `except:` or `except Exception: pass`.
- `if __name__ == "__main__":` guard for runnable modules.

Pitfalls
- No mutable default arguments (`def f(x=[])`); use `None` and create inside.
- Don't shadow builtins (`list`, `id`, `type`, `input`).
- Run subprocesses with an argument list, never `shell=True` with interpolated input.

Environment
- Work inside the project's environment (`uv`, poetry, venv); never `pip install` into the system Python. Dependencies go in `pyproject.toml` (or the project's requirements files), pinned the project's way.

Verify
- `pytest` for the touched tests first (`pytest path::test_name`), then the suite; run the configured linter and type checker.

"""Secret guard: finds credentials in what a `git commit` or `git push` is about to record.

Only added lines count. A line containing `habits:allow-secret` is skipped (fake keys in test fixtures).
Findings name the file and the kind of secret, never the value.
"""

import re
import subprocess
from pathlib import Path

from units import command_words

ALLOW = "habits:allow-secret"

PATTERNS = [
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})\b")),
    ("GitLab token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Stripe live key", re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{24,}\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{32,}")),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}")),
    ("npm token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY-----")),
]

SECRET_FILES = re.compile(
    r"(?:^|/)(?:\.env(?:\.(?!example$|sample$|template$|dist$)[\w.-]+)?|id_(?:rsa|dsa|ecdsa|ed25519)"
    r"|[^/]+\.(?:pem|p12|pfx|jks|keystore)|local\.properties)$"
)


def _git(cwd, *args):
    try:
        out = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout if out.returncode == 0 else None


def scan_diff(diff):
    """Return [(file, kind)] for secrets in the added lines of a unified diff."""
    findings, current = [], None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[4:].strip()
            current = path[2:] if path.startswith("b/") else None
            if current and SECRET_FILES.search(current):
                findings.append((current, "file that usually holds secrets"))
        elif line.startswith("+") and current and ALLOW not in line:
            for kind, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append((current, kind))
    return sorted(set(findings))


def _commit_diff(cwd, args):
    commits_all = any(a in ("-a", "--all") or (re.fullmatch(r"-[a-zA-Z]+", a) and "a" in a) for a in args)
    return _git(cwd, "diff", "HEAD" if commits_all else "--cached", "--no-color", "--no-ext-diff")


def _push_diff(cwd):
    if _git(cwd, "rev-parse", "--abbrev-ref", "@{u}"):
        return _git(cwd, "log", "-p", "--format=", "--no-color", "--no-ext-diff", "@{u}..HEAD")
    return _git(cwd, "log", "-p", "--format=", "--no-color", "--no-ext-diff", "HEAD", "--not", "--remotes")


def check_command(command, cwd):
    """If the shell command commits or pushes, return a refusal reason when secrets would be recorded."""
    cwd = Path(cwd)
    for words in command_words(command):
        if words[0] == "cd" and len(words) > 1:
            cwd = (cwd / Path(words[1]).expanduser()).resolve()
            continue
        if words[0] != "git":
            continue
        args, here = words[1:], cwd
        while len(args) >= 2 and args[0] == "-C":
            here = (here / Path(args[1]).expanduser()).resolve()
            args = args[2:]
        if not args or args[0] not in ("commit", "push"):
            continue
        diff = _commit_diff(here, args[1:]) if args[0] == "commit" else _push_diff(here)
        findings = scan_diff(diff or "")
        if findings:
            listed = "; ".join(f"{f}: {k}" for f, k in findings[:10])
            more = f" (and {len(findings) - 10} more)" if len(findings) > 10 else ""
            return (f"habits secret guard: this git {args[0]} would record possible secrets: {listed}{more}. "
                    "Don't print the values. Tell the user what was found and where, remove the secret "
                    "(move it to an env var or secret store, and gitignore the file), and if it was already "
                    "pushed anywhere, tell the user it must be rotated. If it is a deliberate fake (a test "
                    f"fixture), mark that line with `{ALLOW}`. The user can turn the guard off with "
                    "`habits config set secretGuard off`.")
    return None

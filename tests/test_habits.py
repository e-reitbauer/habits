"""Tests for the habits plugin. Run with: python3 -m unittest discover -s tests"""

import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

# Isolate config, cache and data before the modules compute their paths
_HOME = tempfile.mkdtemp(prefix="habits-test-")
os.environ.update(HOME=_HOME, XDG_CONFIG_HOME=f"{_HOME}/config", XDG_CACHE_HOME=f"{_HOME}/cache",
                  XDG_DATA_HOME=f"{_HOME}/data")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "habits"))

import cli  # noqa: E402
import config  # noqa: E402
import guard  # noqa: E402
import hooks  # noqa: E402
from units import Unit, _split_list, command_words, glob_regex, parse_frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FAKE_AWS_KEY ="AKIAIOSFODNN7EXAMPLE"  # habits:allow-secret (AWS's documented example key)


def git(cwd, *args):
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True)


def make_repo():
    repo = Path(tempfile.mkdtemp(prefix="habits-repo-"))
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    (repo / "README.md").write_text("hi\n")
    git(repo, "add", "README.md")
    git(repo, "commit", "-qm", "init")
    return repo


def transcript(tokens):
    """A fake transcript whose latest assistant message reports a context of `tokens`."""
    path = Path(tempfile.mkstemp(prefix="habits-transcript-", suffix=".jsonl")[1])
    entry = {"type": "assistant", "message": {"usage": {"input_tokens": 1, "cache_read_input_tokens": tokens - 1,
                                                        "cache_creation_input_tokens": 0}}}
    path.write_text(json.dumps({"type": "user"}) + "\n" + json.dumps(entry) + "\n")
    return str(path)


class Parsing(unittest.TestCase):
    def test_globs(self):
        g = glob_regex("**/*.kt")
        self.assertTrue(g.fullmatch("A.kt"))
        self.assertTrue(g.fullmatch("src/main/A.kt"))
        self.assertFalse(g.fullmatch("build.gradle.kts"))
        self.assertTrue(glob_regex("**/*Controller.{kt,java}").fullmatch("a/TagController.java"))
        self.assertFalse(glob_regex("**/gradle/*.toml").fullmatch("gradle/sub/x.toml"))
        with self.assertRaises(ValueError):
            glob_regex("**/*.{kt")

    def test_list_splitting_respects_braces_and_quotes(self):
        self.assertEqual(_split_list('"**/*.{yml,yaml}", "a,b", c'), ["**/*.{yml,yaml}", "a,b", "c"])

    def test_frontmatter(self):
        meta, body, errors = parse_frontmatter('---\nid: x\npaths: ["a", "b"]\ncommands:\n  - git\n---\nBody\n')
        self.assertEqual(errors, [])
        self.assertEqual(meta, {"id": "x", "paths": ["a", "b"], "commands": ["git"]})
        self.assertEqual(body, "Body\n")
        self.assertTrue(parse_frontmatter("no frontmatter")[2])

    def test_command_words(self):
        words = list(command_words("cd backend && FOO=1 ./gradlew test | tee log; sudo adb devices"))
        self.assertEqual(words[1][:2], ["gradlew", "test"])
        self.assertIn(["adb", "devices"], words)

    def test_unit_command_prefix(self):
        unit = Unit(id="p", title="P", body="b", file=Path("p.md"), commands=["npx playwright"])
        self.assertTrue(unit.matches_command("npx playwright test -g x"))
        self.assertFalse(unit.matches_command("npx vitest"))

    def test_invalid_glob_disables_only_itself(self):
        unit = Unit(id="u", title="U", body="b", file=Path("u.md"), paths=["**/*.{kt", "**/*.kt"])
        self.assertTrue(unit.matches_path("A.kt"))

    def test_all_units_validate(self):
        with redirect_stdout(io.StringIO()) as out:
            code = cli.cmd_validate([])
        self.assertEqual(code, 0, out.getvalue())

    def test_requested_title(self):
        self.assertEqual(hooks.requested_title('habits title "fix-login"'), "fix-login")
        self.assertEqual(hooks.requested_title('python3 "/x/habits" title new-task'), "new-task")
        self.assertIsNone(hooks.requested_title("habits title " + "x" * 80))
        self.assertIsNone(hooks.requested_title("echo habits title"))


class Guard(unittest.TestCase):
    def test_scan_diff(self):
        diff = f'+++ b/cfg.py\n+KEY = "{FAKE_AWS_KEY}"\n'  # habits:allow-secret
        self.assertEqual(guard.scan_diff(diff), [("cfg.py", "AWS access key")])
        self.assertEqual(guard.scan_diff(diff.replace('"\n', '"  # habits:allow-secret\n')), [])
        self.assertEqual(guard.scan_diff("+++ b/.env\n+X=1\n"), [(".env", "file that usually holds secrets")])
        self.assertEqual(guard.scan_diff("+++ b/.env.example\n+X=\n"), [])

    def test_commit_and_push(self):
        repo = make_repo()
        (repo / "cfg.py").write_text(f'KEY = "{FAKE_AWS_KEY}"\n')
        git(repo, "add", "cfg.py")
        self.assertIn("AWS access key", guard.check_command('git commit -m "x"', repo))
        self.assertIn("AWS access key", guard.check_command(f'cd {repo} && git commit -m "x"', "/"))
        git(repo, "commit", "-qm", "leak")
        self.assertIn("git push", guard.check_command("git push origin main", repo))
        self.assertIsNone(guard.check_command("ls -la", repo))
        self.assertIsNone(guard.check_command("git push", make_repo()))


class Hooks(unittest.TestCase):
    def setUp(self):
        self.session = f"s{self._testMethodName}"
        self.repo = make_repo()
        (self.repo / "openspec" / "specs" / "a").mkdir(parents=True)
        (self.repo / "openspec" / "specs" / "a" / "spec.md").write_text("# a\n\n## Purpose\n\nDoes a.\n")

    def touch(self, rel, tokens=None, tool="Read"):
        return hooks.post_tool_use({"session_id": self.session, "cwd": str(self.repo), "tool_name": tool,
                                    "tool_input": {"file_path": str(self.repo / rel)},
                                    "transcript_path": transcript(tokens) if tokens else None})

    def start(self, source="startup"):
        return hooks.session_start({"session_id": self.session, "cwd": str(self.repo), "source": source})

    def test_session_start_loads_markers_and_index(self):
        result = self.start()
        self.assertEqual(result["loaded"], ["openspec"])
        self.assertIn("- commit:", result["context"])
        self.assertIn("Name this session", result["context"])

    def test_unit_loads_once_then_refreshes_after_growth(self):
        self.start()
        self.assertEqual(self.touch("A.kt", tokens=10_000)["loaded"], ["kotlin"])
        self.assertFalse(self.touch("B.kt", tokens=50_000).get("context"))
        refreshed = self.touch("C.kt", tokens=10_000 + config.DEFAULTS["refreshTokens"])
        self.assertEqual(refreshed["refreshed"], ["kotlin"])
        self.assertIn("refreshing the Kotlin unit", refreshed["context"])

    def test_resume_keeps_loaded_units(self):
        self.start()
        self.touch("A.kt", tokens=10_000)
        self.assertEqual(self.start("resume")["loaded"], [])
        self.assertFalse(self.touch("B.kt", tokens=20_000).get("loaded"))

    def test_compact_reloads(self):
        self.start()
        self.touch("A.kt", tokens=10_000)
        self.assertEqual(self.start("compact")["loaded"], ["openspec"])
        self.assertEqual(self.touch("B.kt", tokens=5_000)["loaded"], ["kotlin"])

    def test_uncovered_extension_suggests_a_unit_once(self):
        self.start()
        self.assertIn("no unit covers .zig", self.touch("main.zig")["context"])
        self.assertFalse(self.touch("other.zig").get("context"))

    def test_title_flow(self):
        self.start()
        hooks.post_tool_use({"session_id": self.session, "cwd": str(self.repo), "tool_name": "Bash",
                             "tool_input": {"command": 'habits title "taggd-work"'}})
        self.assertEqual(hooks.prompt_submit({"session_id": self.session})["title"], "taggd-work")
        self.assertNotIn("title", hooks.prompt_submit({"session_id": self.session}))
        self.assertNotIn("Name this session", self.start("compact")["context"])

    def test_rot_check(self):
        self.start()
        every = config.DEFAULTS["rotCheckEvery"]
        submit = lambda tokens: hooks.prompt_submit({"session_id": self.session, "transcript_path": transcript(tokens)})
        self.assertNotIn("context", submit(every - 1))
        self.assertIn("load the `context` skill", submit(every + 5_000)["context"])
        self.assertNotIn("context", submit(every + 50_000))
        self.assertIn("context", submit(2 * every + 10_000))

    def test_context_size_after_compaction_uses_post_compact_tokens(self):
        path = Path(transcript(650_000))
        boundary = {"type": "system", "subtype": "compact_boundary",
                    "compactMetadata": {"preTokens": 650_000, "postTokens": 36_000}}
        with path.open("a") as fh:
            fh.write(json.dumps(boundary) + "\n")
        self.assertEqual(hooks.context_tokens(str(path)), 36_000)


def ui_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "skills" / "ui" / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UiTools(unittest.TestCase):
    contrast = ui_script("contrast")
    scan = ui_script("scan")

    def test_contrast_matches_known_values(self):
        c = self.contrast
        self.assertAlmostEqual(c.ratio(c.parse("#000"), c.parse("#fff")), 21.0, places=2)
        self.assertAlmostEqual(c.ratio(c.parse("#777777"), c.parse("white")), 4.48, places=2)
        self.assertAlmostEqual(c.apca(c.parse("#000"), c.parse("#fff")), 106.04, places=1)
        self.assertAlmostEqual(c.apca(c.parse("#fff"), c.parse("#000")), -107.88, places=1)

    def test_contrast_parses_every_notation(self):
        c = self.contrast
        for text in ("#b92548", "#B92548FF", "rgb(185, 37, 72)", "rgba(185 37 72 / 1)", "0xFFB92548"):
            self.assertEqual(c.parse(text)[:3], (185, 37, 72), text)
        self.assertEqual(c.composite(c.parse("rgba(0,0,0,.5)"), c.parse("#fff")), (128, 128, 128))
        with self.assertRaises(ValueError):
            c.parse("nope")

    def test_contrast_fix_reaches_the_minimum(self):
        c = self.contrast
        bg = c.parse("#ffffff")
        for fg in ("#777777", "#b9a548", "#3a86ff"):
            fixed = c.fix(c.parse(fg), bg, 4.5)
            self.assertGreaterEqual(c.ratio(c.parse(fixed), bg), 4.5, fg)

    def test_scan_finds_literals_outside_token_files(self):
        root = Path(tempfile.mkdtemp(prefix="habits-scan-"))
        (root / "tokens.css").write_text(":root { --accent: #b92548; }\n")
        (root / "app.css").write_text("#header { color: var(--accent); }\n"
                                      ".card { background: #fff; border: 1px solid rgba(0,0,0,.1); }\n"
                                      ".ok { color: #abc; } /* habits:allow-literal */\n")
        (root / "page.html").write_text('<a href="#abc">x</a><div class="bg-[#123456]">&#123;</div>\n')
        found = {(Path(p).name, kind, value) for p, _, kind, value in self.scan.scan([str(root)],
                                                                                  self.scan.DEFAULT_TOKENS)}
        self.assertEqual(found, {("app.css", "color", "#fff"), ("app.css", "color", "rgba(0,0,0,.1)"),
                                 ("page.html", "arbitrary", "bg-[#123456]")})


if __name__ == "__main__":
    unittest.main()

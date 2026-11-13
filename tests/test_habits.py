"""Tests for the habits plugin. Run with: python3 -m unittest discover -s tests"""

import importlib.util
import io
import json
import os
import random
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


class StatusLine(unittest.TestCase):
    def run_statusline(self, payload, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            stdin, sys.stdin = sys.stdin, io.StringIO(json.dumps(payload))
            try:
                cli.cmd_statusline(list(args))
            finally:
                sys.stdin = stdin
        return out.getvalue().strip()

    def test_counts_loaded_units(self):
        config.save_state("sl", {"loaded": {"kotlin": 1, "gradle": 2, "android": 3, "openspec": 4}})
        self.assertEqual(self.run_statusline({"session_id": "sl"}), "habits 4")

    def test_counts_zero_without_units(self):
        self.assertEqual(self.run_statusline({"session_id": "nothing-loaded"}), "habits 0")


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

    def test_palette_text_steps_reach_contrast_on_subtle_background(self):
        palette = ui_script("palette")
        for seed in ("#b92548", "#e8a33d", "#1f5f8b", "#ffff00", "#101010"):
            for dark in (False, True):
                rgbs = [palette.to_rgb(*s) for s in palette.scale(self.contrast.parse(seed), dark=dark)]
                self.assertGreaterEqual(self.contrast.ratio(rgbs[10], rgbs[1]), 4.5, (seed, dark))
                self.assertGreaterEqual(self.contrast.ratio(rgbs[11], rgbs[1]), 7.0, (seed, dark))

    def test_palette_neutral_is_tinted_but_quiet(self):
        palette = ui_script("palette")
        steps = palette.scale(self.contrast.parse("#1f5f8b"), neutral=True)
        self.assertTrue(all(0.002 < c <= 0.02 for _, c, _ in steps))

    def test_palette_flags_brown_and_olive(self):
        palette = ui_script("palette")
        parse = self.contrast.parse
        self.assertTrue(palette.reads_muddy(*palette.to_oklch(parse("#6e5a3a"))))
        self.assertTrue(palette.reads_muddy(*palette.to_oklch(parse("#271e0e"))))
        self.assertFalse(palette.reads_muddy(*palette.to_oklch(parse("#e0a034"))))
        self.assertFalse(palette.reads_muddy(*palette.to_oklch(parse("#b92548"))))

    def test_palette_dark_warm_steps_turn_toward_red(self):
        palette = ui_script("palette")
        steps = palette.scale(self.contrast.parse("#e8a33d"))
        self.assertLess(steps[10][2], steps[8][2])

    def test_gradient_interpolates_in_oklab_and_warns_on_far_hues(self):
        gradient = ui_script("gradient")
        css = gradient.css(["#e8a33d", "#d9603b"], "#2a1d0b", "mesh", 90, 0.06, False)
        self.assertIn("in oklab", css)
        self.assertIn("feTurbulence", css)
        far = gradient.hue_gap(self.contrast.parse("#1f5f8b"), self.contrast.parse("#e8a33d"))
        self.assertGreater(far, 90)

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

    def test_fonts_draw_matches_the_voice_and_leaves_out_overused_fonts(self):
        fonts = ui_script("fonts")
        catalog = fonts.load()
        picks, _ = fonts.sample(catalog, ["serif", "warm"], "display", 6, random.Random(1), False)
        self.assertTrue(picks)
        for f in picks:
            self.assertIn("d", f["roles"])
            self.assertTrue(f["tags"] & {"serif", "warm"})
            self.assertFalse(fonts.common(f), f["name"])
        again, _ = fonts.sample(catalog, ["serif", "warm"], "display", 6, random.Random(1), False)
        self.assertEqual([f["name"] for f in picks], [f["name"] for f in again])

    def test_fonts_links_and_check(self):
        fonts = ui_script("fonts")
        by_name = {f["name"]: f for f in fonts.load()}
        self.assertEqual(fonts.link(by_name["Literata"]),
                         "https://fonts.googleapis.com/css2?family=Literata:wght@200..900&display=swap")
        self.assertEqual(fonts.link(by_name["Alfa Slab One"]),
                         "https://fonts.googleapis.com/css2?family=Alfa+Slab+One&display=swap")
        self.assertTrue(fonts.link(by_name["Gambetta"]).startswith("https://api.fontshare.com/v2/css?f[]=gambetta@"))
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(fonts.main(["--check", "Inter", "Fraunces", "Literata"]), 1)
        self.assertIn("Literata                   ok", out.getvalue())

    def test_pattern_writes_a_token_colored_mask(self):
        pattern = ui_script("pattern")
        for kind in ("dots", "grid", "diagonal", "cross", "waves", "zigzag", "checker", "rings", "hatch", "contour"):
            css = pattern.css(kind, 24, 1.5, "var(--pattern)", 0.12, "radial", "p", 7)
            self.assertIn("background: var(--pattern)", css, kind)
            self.assertIn('mask: url("data:image/svg+xml,', css, kind)
            self.assertNotIn("#", css.split("data:")[1].split('")')[0], kind)  # '#' would cut the data URI
            self.assertIn("mask-composite: intersect", css, kind)
        self.assertEqual(pattern.css("contour", 24, 1, "red", 0.1, None, "p", 3),
                         pattern.css("contour", 24, 1, "red", 0.1, None, "p", 3))

    def test_icons_refuses_names_without_a_set(self):
        icons = ui_script("icons")
        with self.assertRaises(SystemExit):
            icons.svg("sailboat")

    def test_direction_deals_every_axis_repeatably_from_a_seed(self):
        direction = ui_script("direction")
        card = direction.deal(random.Random(5), "expressive")
        self.assertEqual(set(card), set(direction.AXES))
        self.assertEqual(card, direction.deal(random.Random(5), "expressive"))
        for axis, (value, meaning, risk) in card.items():
            self.assertIn((value, meaning, risk), direction.AXES[axis])

    def test_direction_product_cards_stay_restrained_or_committed(self):
        direction = ui_script("direction")
        for seed in range(30):
            card = direction.deal(random.Random(seed), "product")
            self.assertEqual(set(card), set(direction.PRODUCT_AXES))
            self.assertIn(card["color strategy"][0], {"restrained", "committed"})

    def test_direction_cinematic_cards_leave_layout_to_the_storyboard(self):
        direction = ui_script("direction")
        card = direction.deal(random.Random(3), "cinematic")
        self.assertEqual(set(card), set(direction.CINEMATIC_AXES))
        self.assertNotIn("layout spine", card)

    def test_direction_cinematic_cards_never_deal_restrained_color_or_stepped_scale(self):
        direction = ui_script("direction")
        for seed in range(30):
            card = direction.deal(random.Random(seed), "cinematic")
            self.assertNotEqual(card["color strategy"][0], "restrained")
            self.assertEqual(card["scale"][0], "extreme contrast")

    def test_direction_cards_name_no_fonts_or_hex_colors(self):
        direction = ui_script("direction")
        fonts = {f["name"] for f in ui_script("fonts").load()}
        text = repr(direction.AXES)
        self.assertNotRegex(text, r"#[0-9a-fA-F]{3,6}\b")
        self.assertFalse([f for f in fonts if f"'{f}'" in text or f" {f} " in text])


if __name__ == "__main__":
    unittest.main()

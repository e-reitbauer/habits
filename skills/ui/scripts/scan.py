#!/usr/bin/env python3
"""Find hardcoded design values outside the design system: colors, font families, Tailwind arbitrary values.

  scan.py [PATH ...] [--tokens GLOB ...] [--summary]

PATH defaults to the current directory. Files that define tokens are skipped; by default any path
containing token, theme, color, colour, palette or variables, plus tailwind.config.*. Pass --tokens to
name them exactly. Image and icon folders (drawable, mipmap, assets, icons, fonts) are skipped
too. Exits 1 when something is found, so it can gate a check.
"""

import argparse
import fnmatch
import os
import re
import sys
from collections import Counter

EXTENSIONS = {".css", ".scss", ".sass", ".less", ".html", ".htm", ".vue", ".svelte", ".astro", ".js",
              ".jsx", ".ts", ".tsx", ".mjs", ".kt", ".kts", ".swift", ".dart", ".xml"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".output", ".nuxt", ".next", "coverage", ".gradle",
             "Pods", "DerivedData", "vendor", "target", ".venv", "__pycache__"}
DEFAULT_TOKENS = ["*token*", "*theme*", "*color*", "*colour*", "*palette*", "*variables*",
                  "tailwind.config.*"]

HEX = re.compile(r"(?<![\w&/#-])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![\w-])")
FUNC = re.compile(r"\b(?:rgba?|hsla?|oklch|oklab|lab|lch|hwb)\(\s*[\d.][^)]*\)")
COMPOSE = re.compile(r"\bColor\(\s*0x[0-9a-fA-F]{6,8}|\bColor\(\s*red\s*:")
FONT = re.compile(r"font-family\s*:\s*(?!\s*var\()(?!\s*inherit)([^;}\n]+)")
ARBITRARY = re.compile(r"\b[a-z][\w-]*-\[(?:#|\d|rgb|hsl)[^\]\s]*\]")
SELECTOR = re.compile(r"^\s*[^:{]*#[\w-]+[^:]*\{")
ASSET_DIRS = re.compile(r"(^|/)(drawable[\w-]*|mipmap[\w-]*|assets|icons|fonts)/")


def is_token_file(path, patterns):
    name = path.replace(os.sep, "/").lower()
    return any(fnmatch.fnmatch(name, p.lower()) or fnmatch.fnmatch(os.path.basename(name), p.lower())
               for p in patterns)


def files(paths):
    for root in paths:
        if os.path.isfile(root):
            yield root
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for f in filenames:
                if os.path.splitext(f)[1] in EXTENSIONS and not f.endswith(".min.js"):
                    yield os.path.join(dirpath, f)


def scan_line(line):
    found = []
    for m in HEX.finditer(line):
        before = line[:m.start()]
        if "href=" in before[-8:] or "url(" in before[-6:] or SELECTOR.match(line[:m.end()] + "{"):
            continue
        found.append(("color", m.group()))
    found += [("color", m.group()) for m in FUNC.finditer(line)]
    found += [("color", m.group()) for m in COMPOSE.finditer(line)]
    found += [("font", m.group(1).strip()) for m in FONT.finditer(line)]
    found += [("arbitrary", m.group()) for m in ARBITRARY.finditer(line)]
    return found


def scan(paths, token_patterns):
    results = []
    for path in files(paths):
        if is_token_file(path, token_patterns) or ASSET_DIRS.search(path.replace(os.sep, "/")):
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for n, line in enumerate(fh, 1):
                    if "habits:allow-literal" in line:
                        continue
                    results += [(path, n, kind, value) for kind, value in scan_line(line)]
        except OSError:
            continue
    return results


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("paths", nargs="*", default=["."])
    p.add_argument("--tokens", nargs="+", metavar="GLOB", help="globs of files that define tokens")
    p.add_argument("--summary", action="store_true", help="count distinct values instead of listing lines")
    args = p.parse_args(argv)
    results = scan(args.paths, args.tokens or DEFAULT_TOKENS)
    if not results:
        print("scan: no hardcoded colors, fonts or arbitrary values outside the token files")
        return 0
    if args.summary:
        for (kind, value), n in Counter((k, v) for _, _, k, v in results).most_common():
            print(f"{n:4}  {kind:<9} {value}")
    else:
        for path, n, kind, value in results:
            print(f"{path}:{n}: {kind}: {value}")
    print(f"scan: {len(results)} hardcoded value(s); use a token, or mark a deliberate one with "
          f"habits:allow-literal", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

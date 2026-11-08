#!/usr/bin/env python3
"""Find and fetch real icons from open icon sets, so no icon is ever drawn by hand.

  icons.py sets                          the sets, with their style, to pick one that fits the design
  icons.py search bread [--set ph] [-n 20]
  icons.py get ph:bread ph:clock-bold [--class icon]   inline SVG, colored by currentColor
  icons.py get ph:bread ph:clock --sprite              one hidden <svg> of <symbol>s, used via <use>

Uses the public Iconify API (api.iconify.design), which serves 200,000+ icons from open sets. In a
project with an icon package installed, use the package instead and keep to its set.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.iconify.design"

# prefix, name, license, style: pick the set by the design's stroke, corners and weight
SETS = [
    ("ph", "Phosphor", "MIT", "six weights per icon (-thin, -light, regular, -bold, -fill, -duotone); "
     "rounded; the easiest set to match to a type weight"),
    ("tabler", "Tabler", "MIT", "2px stroke, round joins, 24px; neutral, technical; -filled for some"),
    ("iconoir", "Iconoir", "MIT", "1.5px stroke, rounded; light and calm"),
    ("ri", "Remix Icon", "Apache-2.0", "-line and -fill pairs; neutral, slightly geometric"),
    ("material-symbols", "Material Symbols", "Apache-2.0", "filled by default, -outline, -rounded, "
     "-outline-rounded; Google's look, very complete"),
    ("carbon", "Carbon", "Apache-2.0", "IBM; square-cornered, technical, 32px grid; data and engineering tools"),
    ("fluent", "Fluent UI", "MIT", "Microsoft; soft and rounded, -24-regular and -24-filled; productivity"),
    ("mingcute", "MingCute", "Apache-2.0", "soft, rounded, friendly; -line and -fill"),
    ("solar", "Solar", "CC-BY-4.0, credit the author", "expressive styles: -linear, -bold, -bold-duotone, "
     "-line-duotone, -broken, -outline"),
    ("hugeicons", "Hugeicons", "MIT", "rounded stroke, numbered variants (home-01 ...)"),
    ("akar-icons", "Akar", "MIT", "2px rounded, simple and small set"),
    ("radix-icons", "Radix Icons", "MIT", "15px, crisp, for dense interfaces"),
    ("teenyicons", "Teenyicons", "MIT", "tiny 15px, -outline and -solid; minimal"),
    ("system-uicons", "System UIcons", "Unlicense", "thin and minimal"),
    ("bi", "Bootstrap Icons", "MIT", "16px, outline and -fill"),
    ("heroicons", "Heroicons", "MIT", "Tailwind's set (outline 1.5px, -solid, -20-solid); very common"),
    ("pixelarticons", "Pixelarticons", "MIT", "pixel grid; retro, games, terminals"),
    ("game-icons", "Game-icons", "CC-BY-3.0, credit the author", "illustrative silhouettes; adventure, "
     "fantasy, crafts, tools"),
    ("pepicons-pencil", "Pepicons Pencil", "CC-BY-4.0, credit the author", "hand-drawn look; casual, crafty"),
    ("lucide", "Lucide", "ISC", "2px rounded; the default of shadcn and of most generated pages: use it "
     "when the project already does, otherwise pick a set that fits the design"),
]


def fetch(path):
    url = f"{API}{path}"
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "habits-ui-icons"})
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.read().decode()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise SystemExit(f"icons: {url} answered {e.code}")
    except (urllib.error.URLError, TimeoutError) as e:
        raise SystemExit(f"icons: can't reach the Iconify API ({e}); use the project's icon package, "
                         "or ask the user for the icons")


def search(query, prefix, limit):
    params = {"query": query, "limit": max(limit, 32)}
    if prefix:
        params["prefix"] = prefix
    data = json.loads(fetch(f"/search?{urllib.parse.urlencode(params)}"))
    return data["icons"][:limit]


def svg(icon):
    prefix, _, name = icon.partition(":")
    if not prefix or not name:
        raise SystemExit(f"icons: write icons as set:name, e.g. ph:bread (got {icon!r})")
    body = fetch(f"/{prefix}/{name}.svg")
    if body is None:
        raise SystemExit(f"icons: {icon} doesn't exist; search for it: icons.py search {name} --set {prefix}")
    return body


def inline(icon, cls):
    body = svg(icon)
    return body.replace("<svg ", f'<svg class="{cls}" aria-hidden="true" focusable="false" ', 1)


def symbol(icon):
    body = svg(icon)
    view_box = re.search(r'viewBox="([^"]+)"', body).group(1)
    inner = re.search(r"<svg[^>]*>(.*)</svg>", body, re.S).group(1)
    return f'  <symbol id="{icon.replace(":", "-")}" viewBox="{view_box}">{inner}</symbol>'


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("sets", help="list the icon sets and their style")
    s = sub.add_parser("search", help="find icon names")
    s.add_argument("query")
    s.add_argument("--set", dest="prefix", help="limit to one set, e.g. ph")
    s.add_argument("-n", type=int, default=20)
    g = sub.add_parser("get", help="print icons as inline SVG")
    g.add_argument("icons", nargs="+", metavar="SET:NAME")
    g.add_argument("--class", dest="cls", default="icon", help="class on each <svg> (default: icon)")
    g.add_argument("--sprite", action="store_true", help="one hidden sprite of <symbol>s instead")
    args = p.parse_args(argv)

    if args.command == "sets":
        for prefix, name, license_, style in SETS:
            print(f"{prefix:<17} {name:<17} {license_}\n{'':<17} {style}")
        return 0
    if args.command == "search":
        found = search(args.query, args.prefix, args.n)
        print("\n".join(found) if found else f"no icons for {args.query!r}; try a broader word or another set")
        return 0 if found else 1
    if args.sprite:
        print('<svg xmlns="http://www.w3.org/2000/svg" hidden>')
        print("\n".join(symbol(i) for i in args.icons))
        print("</svg>")
        ids = ", ".join(f'<svg class="{args.cls}" aria-hidden="true"><use href="#{i.replace(":", "-")}"/></svg>'
                        for i in args.icons[:2])
        print(f"<!-- use: {ids} -->")
        return 0
    for icon in args.icons:
        print(inline(icon, args.cls))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

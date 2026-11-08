#!/usr/bin/env python3
"""Write the CSS for a blurred mesh background (two or three colors, one blur, grain).

  gradient.py C1 C2 [C3] [--base COLOR] [--blur 90] [--grain 0.06] [--drift] [--name mesh]

Use colors from the palette. Neighboring hues blend cleanly; the script warns when two colors are
far apart on the hue wheel, because complementary colors turn muddy when blurred together. Put the
element behind the content: <div class="mesh" aria-hidden="true"></div> inside a positioned parent.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contrast import hexof, parse  # noqa: E402
from palette import to_oklch  # noqa: E402

SPOTS = [("18% 24%", "55%"), ("84% 16%", "50%"), ("62% 88%", "60%")]
GRAIN = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E"
         "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' "
         "stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E"
         "%3C/svg%3E")


def hue_gap(a, b):
    return abs((to_oklch(a)[2] - to_oklch(b)[2] + 180) % 360 - 180)


def css(colors, base, name, blur, grain, drift):
    blobs = ",\n    ".join(f"radial-gradient(in oklab circle at {at}, {c} 0%, transparent {size})"
                           for c, (at, size) in zip(colors, SPOTS))
    out = f"""/* Blurred mesh: the blobs are blurred once as a layer, grain hides banding. */
.{name} {{
  position: absolute;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  isolation: isolate;
  background: {base};
  pointer-events: none;
}}
.{name}::before {{
  content: "";
  position: absolute;
  inset: 0;
  background:
    {blobs};
  filter: blur({blur}px) saturate(1.15);
  transform: scale(1.25);
}}
.{name}::after {{
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("{GRAIN}");
  opacity: {grain};
  mix-blend-mode: overlay;
}}"""
    if drift:
        out += f"""
@media (prefers-reduced-motion: no-preference) {{
  .{name}::before {{ animation: {name}-drift 32s ease-in-out infinite alternate; }}
}}
@keyframes {name}-drift {{
  from {{ transform: scale(1.25) translate(0, 0) rotate(0deg); }}
  to {{ transform: scale(1.3) translate(-3%, 2%) rotate(6deg); }}
}}"""
    return out


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("colors", nargs="+", metavar="COLOR", help="two or three palette colors")
    p.add_argument("--base", default=None, help="background under the blobs (default: darkened first color)")
    p.add_argument("--blur", type=int, default=90, help="blur radius in px (60-120 works for most sizes)")
    p.add_argument("--grain", type=float, default=0.06, help="grain opacity (0 to switch it off)")
    p.add_argument("--drift", action="store_true", help="add a slow drift, off under reduced motion")
    p.add_argument("--name", default="mesh", help="class name")
    args = p.parse_args(argv)
    if not 2 <= len(args.colors) <= 3:
        p.error("give two or three colors")
    try:
        rgbs = [parse(c) for c in args.colors]
        base = args.base or hexof(tuple(c * 0.18 for c in rgbs[0][:3]))
        parse(base)
    except ValueError as e:
        print(f"gradient: {e}", file=sys.stderr)
        return 2
    for i in range(len(rgbs)):
        for j in range(i + 1, len(rgbs)):
            gap = hue_gap(rgbs[i], rgbs[j])
            if gap > 90:
                print(f"gradient: {args.colors[i]} and {args.colors[j]} are {gap:.0f}° apart; blurred together "
                      f"they turn muddy. Neighbors 20-60° apart blend cleanly.", file=sys.stderr)
    print(css([hexof(c) for c in rgbs], base, args.name, args.blur, args.grain, args.drift))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

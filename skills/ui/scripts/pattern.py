#!/usr/bin/env python3
"""Write CSS for a background pattern with exact geometry, colored by a design token.

  pattern.py dots|grid|diagonal|cross|waves|zigzag|checker|rings|hatch|contour
             [--size 24] [--stroke 1.5] [--color "var(--pattern)"] [--opacity 0.12]
             [--fade radial|top|bottom|left|right] [--class pattern] [--seed 7]

The pattern is an SVG mask on a ::before layer, so its color comes from a token (dark mode works)
and it never sits on top of content. Hand-drawn SVG comes out uneven; this draws it exactly. Pick
the motif from the concept (see references/decoration.md), not from this list.
"""

import argparse
import math
import random
import sys
import urllib.parse


def tile(kind, s, w, rng):
    """SVG markup and tile size for one repeat of the pattern (black = visible)."""
    h = s / 2
    if kind == "dots":
        return f'<circle cx="{h}" cy="{h}" r="{w}"/>', s, s
    if kind == "grid":
        return f'<path d="M{s} 0V{s}M0 {s}H{s}" fill="none" stroke="#000" stroke-width="{w * 2}"/>', s, s
    if kind == "diagonal":
        return (f'<path d="M-{h} {h}L{h} -{h}M0 {s}L{s} 0M{h} {s + h}L{s + h} {h}" fill="none" '
                f'stroke="#000" stroke-width="{w}"/>'), s, s
    if kind == "cross":
        a = s / 6
        return (f'<path d="M{h - a} {h}H{h + a}M{h} {h - a}V{h + a}" stroke="#000" stroke-width="{w}" '
                f'stroke-linecap="round"/>'), s, s
    if kind == "waves":
        a = s / 4
        return (f'<path d="M0 {h}Q{s / 4} {h - a} {h} {h}T{s} {h}" fill="none" stroke="#000" '
                f'stroke-width="{w}"/>'), s, s
    if kind == "zigzag":
        a = s / 4
        return (f'<path d="M0 {h + a / 2}L{h} {h - a / 2}L{s} {h + a / 2}" fill="none" stroke="#000" '
                f'stroke-width="{w}" stroke-linejoin="miter"/>'), s, s
    if kind == "checker":
        return f'<path d="M0 0H{h}V{h}H0ZM{h} {h}H{s}V{s}H{h}Z"/>', s, s
    if kind == "rings":
        rings = "".join(f'<circle cx="{h}" cy="{h}" r="{r:.2f}"/>' for r in (s * 0.12, s * 0.27, s * 0.42))
        return f'<g fill="none" stroke="#000" stroke-width="{w}">{rings}</g>', s, s
    if kind == "hatch":
        return (f'<path d="M0 0L{s} {s}M{s} 0L0 {s}" fill="none" stroke="#000" stroke-width="{w}"/>'), s, s
    if kind == "contour":
        # topographic lines: rings around a few peaks, each bent by low-frequency waves
        size = s * 24
        paths = []
        for _ in range(3):
            cx, cy = rng.uniform(0.15, 0.85) * size, rng.uniform(0.15, 0.85) * size
            waves = [(rng.randint(2, 5), rng.uniform(0.04, 0.12), rng.uniform(0, math.tau)) for _ in range(3)]
            for k in range(1, 9):
                r0 = k * s * 1.4
                points = []
                for i in range(73):
                    t = i / 72 * math.tau
                    r = r0 * (1 + sum(a * math.sin(f * t + p) for f, a, p in waves))
                    points.append(f"{cx + r * math.cos(t):.1f} {cy + r * math.sin(t):.1f}")
                paths.append("M" + "L".join(points) + "Z")
        return (f'<path d="{"".join(paths)}" fill="none" stroke="#000" stroke-width="{w}" '
                f'stroke-linejoin="round"/>'), size, size
    raise ValueError(kind)


FADES = {
    "radial": "radial-gradient(closest-side, #000 30%, transparent)",
    "top": "linear-gradient(to bottom, #000, transparent)",
    "bottom": "linear-gradient(to top, #000, transparent)",
    "left": "linear-gradient(to right, #000, transparent)",
    "right": "linear-gradient(to left, #000, transparent)",
}


def css(kind, size, stroke, color, opacity, fade, cls, seed):
    body, w, h = tile(kind, size, stroke, random.Random(seed))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}">{body}</svg>'
    uri = "data:image/svg+xml," + urllib.parse.quote(svg.replace('"', "'"), safe=" =:/',.-()")
    repeat = "no-repeat" if kind == "contour" else "repeat"
    position = "50% 50% / cover" if kind == "contour" else f"0 0 / {w:g}px {h:g}px"
    layers = f'url("{uri}") {position} {repeat}'
    composite = ""
    if fade:
        layers += f", {FADES[fade]}"
        composite = "  -webkit-mask-composite: source-in;\n  mask-composite: intersect;\n"
    return f"""/* {kind} pattern from pattern.py: --size {size:g} --stroke {stroke:g}{f' --fade {fade}' if fade else ''} */
.{cls} {{
  position: relative;
  isolation: isolate;
}}
.{cls}::before {{
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background: {color};
  opacity: {opacity:g};
  -webkit-mask: {layers};
  mask: {layers};
{composite}}}"""


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("kind", choices=["dots", "grid", "diagonal", "cross", "waves", "zigzag", "checker", "rings",
                                    "hatch", "contour"])
    p.add_argument("--size", type=float, default=24, help="tile size in px (default 24)")
    p.add_argument("--stroke", type=float, default=1.5, help="line width, or dot radius for dots (default 1.5)")
    p.add_argument("--color", default="var(--pattern, currentColor)", help="any CSS color, ideally a token")
    p.add_argument("--opacity", type=float, default=0.12, help="layer opacity (default 0.12: quiet)")
    p.add_argument("--fade", choices=sorted(FADES), help="fade the pattern out toward an edge or the rim")
    p.add_argument("--class", dest="cls", default="pattern", help="class name (default: pattern)")
    p.add_argument("--seed", type=int, default=7, help="variation for contour")
    args = p.parse_args(argv)
    print(css(args.kind, args.size, args.stroke, args.color, args.opacity, args.fade, args.cls, args.seed))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Generate a 12-step OKLCH color scale from a seed color, with a contrast report.

  palette.py SEED [--name accent] [--neutral] [--shift 10] [--dark] [--css]
  palette.py --audit C1 C2 ...      flag colors that read as brown or olive

Step 9 keeps the seed's hue and chroma at a usable lightness (it is the solid fill); 1-8 are light
backgrounds and borders, 11-12 text that reaches 4.5:1 and 7:1 on step 2. --neutral turns the seed
into a tinted grey, --shift moves hue across the scale (light steps toward warm, dark toward cool),
--dark builds the dark-mode scale. See references/color.md for the job of each step.
"""

import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contrast import hexof, parse, ratio  # noqa: E402

JOBS = ["app background", "subtle background", "component", "component hover", "component active",
        "subtle border", "border", "strong border, focus", "solid fill", "solid hover",
        "low-contrast text", "high-contrast text"]
LIGHT_L = [0.993, 0.982, 0.958, 0.932, 0.904, 0.870, 0.820, 0.745, None, None, 0.52, 0.27]
DARK_L = [0.155, 0.185, 0.225, 0.255, 0.285, 0.325, 0.385, 0.470, None, None, 0.80, 0.94]
# share of the seed's chroma per step (ends are low so they stay in gamut and calm)
LIGHT_C = [0.06, 0.12, 0.22, 0.30, 0.38, 0.46, 0.56, 0.72, 1.0, 1.0, 0.92, 0.55]
DARK_C = [0.18, 0.22, 0.32, 0.40, 0.48, 0.55, 0.65, 0.80, 1.0, 1.0, 0.75, 0.35]
WARM, COOL = 95.0, 265.0  # hues that read lighter (yellow) and darker (blue) in OKLCH


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_oklch(rgb):
    r, g, b = (_lin(c) for c in rgb[:3])
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def _linear_rgb(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
            -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
            -0.0041960863 * l_ - 0.7034186168 * m_ + 1.7076147010 * s_)


def in_gamut(L, C, H):
    return all(-1e-4 <= c <= 1 + 1e-4 for c in _linear_rgb(L, C, H))


def to_rgb(L, C, H):
    def enc(c):
        c = max(0.0, min(1.0, c))
        return 255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)
    return tuple(round(enc(c)) for c in _linear_rgb(L, C, H))


def fit(L, C, H):
    """Largest chroma up to C that is inside sRGB at this lightness and hue."""
    if in_gamut(L, C, H):
        return C
    lo, hi = 0.0, C
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if in_gamut(L, mid, H) else (lo, mid)
    return lo


def toward(h, target, degrees):
    diff = (target - h + 180) % 360 - 180
    return (h + max(-degrees, min(degrees, diff))) % 360


def scale(seed, neutral=False, shift=0.0, dark=False):
    L0, C0, H0 = to_oklch(seed)
    if neutral:
        C0 = min(max(C0 * 0.12, 0.006), 0.02)
    lights, chromas = (DARK_L, DARK_C) if dark else (LIGHT_L, LIGHT_C)
    steps = []
    # the solid fill: the seed itself unless it is too light or dark to carry text
    solid_l = min(max(L0, 0.45 if not dark else 0.55), 0.75 if not dark else 0.82)
    for i, (L, share) in enumerate(zip(lights, chromas)):
        if i == 8:
            L = solid_l
        elif i == 9:
            L = solid_l + (0.05 if dark else -0.045)
        t = (L - 0.5) * 2  # -1 dark .. +1 light
        H = toward(H0, WARM if t > 0 else COOL, abs(t) * shift / 2) if shift else H0
        if not neutral and is_warm(H0) and L < DARK_WARM_L:
            # dark, dull yellows and oranges read as olive and brown: turn toward red and keep color
            H = toward(H, 40.0, (DARK_WARM_L - L) / (DARK_WARM_L - 0.2) * 25)
            share = max(share, 0.85)
        C = fit(L, C0 * share if not neutral else C0 * (0.6 + 0.4 * (1 - abs(t))), H)
        steps.append([L, C, H])
    # text steps must read on the subtle background (step 2)
    bg = to_rgb(*steps[1])
    for i, minimum in ((10, 4.5), (11, 7.0)):
        L, C, H = steps[i]
        while ratio(to_rgb(L, fit(L, C, H), H), bg) < minimum and 0.02 < L < 0.99:
            L += 0.01 if dark else -0.01
        steps[i] = [L, fit(L, C, H), H]
    return steps


DARK_WARM_L = 0.62  # below this, yellows and oranges start to read as olive and brown


def is_warm(h):
    return 45 <= h <= 115


def reads_muddy(L, C, H):
    """Dark, low-chroma yellow or orange: perceived as olive or brown, the least liked colors."""
    return is_warm(H) and L < DARK_WARM_L and C < 0.10


def oklch_css(L, C, H):
    return f"oklch({L * 100:.1f}% {C:.3f} {H:.1f})"


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("seed")
    p.add_argument("--name", default="color", help="token prefix for --css (default: color)")
    p.add_argument("--neutral", action="store_true", help="a tinted grey scale from the seed's hue")
    p.add_argument("--shift", type=float, default=0.0, help="hue shift across the scale in degrees")
    p.add_argument("--dark", action="store_true", help="the dark-mode scale")
    p.add_argument("--css", action="store_true", help="print CSS custom properties")
    p.add_argument("more", nargs="*", help=argparse.SUPPRESS)
    p.add_argument("--audit", action="store_true",
                   help="check the given colors for muddy (olive or brown) tones instead of building a scale")
    args = p.parse_args(argv)
    try:
        if args.audit:
            return audit([args.seed, *args.more])
        seed = parse(args.seed)
    except ValueError as e:
        print(f"palette: {e}", file=sys.stderr)
        return 2
    steps = scale(seed, args.neutral, args.shift, args.dark)
    rgbs = [to_rgb(*s) for s in steps]
    if args.css:
        for i, (s, rgb) in enumerate(zip(steps, rgbs), 1):
            print(f"  --{args.name}-{i}: {oklch_css(*s)}; /* {hexof(rgb)} {JOBS[i - 1]} */")
        return 0
    white, black = (255, 255, 255), (0, 0, 0)
    for i, (s, rgb) in enumerate(zip(steps, rgbs), 1):
        note = ""
        if i in (11, 12):
            note = f"{ratio(rgb, rgbs[1]):.1f}:1 on step 2"
        elif i == 9:
            on = "white" if ratio(white, rgb) >= ratio(black, rgb) else "black"
            note = f"{on} text {max(ratio(white, rgb), ratio(black, rgb)):.1f}:1"
        if reads_muddy(*s):
            note += "  reads as brown/olive: use the neutral text steps unless brown is meant"
        print(f"{i:>2}  {hexof(rgb)}  {oklch_css(*s):<26} {JOBS[i - 1]:<22} {note}")
    return 0


def audit(colors):
    """Flag colors that read as olive or brown; exit 1 when any does."""
    muddy = 0
    for text in colors:
        L, C, H = to_oklch(parse(text))
        bad = reads_muddy(L, C, H)
        muddy += bad
        print(f"{text:<22} {oklch_css(L, C, H):<26} {'reads as brown or olive' if bad else 'ok'}")
    return 1 if muddy else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

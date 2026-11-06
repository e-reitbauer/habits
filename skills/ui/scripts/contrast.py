#!/usr/bin/env python3
"""Check color contrast (WCAG 2.2 ratio plus APCA Lc) and suggest the nearest color that passes.

  contrast.py FG BG [FG BG ...]          check pairs
  contrast.py FG BG --fix [--min 4.5]    also suggest the closest FG that reaches --min
  contrast.py --palette C1 C2 C3 ...     every pair in a palette, best first

Colors: #rgb, #rgba, #rrggbb, #rrggbbaa, rgb()/rgba(), hsl()/hsla(), 0xAARRGGBB (Compose),
black, white. A translucent foreground is composited over its background.
"""

import argparse
import colorsys
import re
import sys
from itertools import permutations

NAMED = {"black": "#000000", "white": "#ffffff"}


def parse(text):
    """Return (r, g, b, a) with r, g, b in 0..255 and a in 0..1."""
    s = NAMED.get(text.strip().lower(), text.strip().lower())
    m = re.fullmatch(r"#([0-9a-f]{3,8})", s)
    if m and len(m[1]) in (3, 4, 6, 8):
        h = m[1]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        return r, g, b, int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    m = re.fullmatch(r"0x([0-9a-f]{8})", s)
    if m:
        h = m[1]
        return int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16), int(h[0:2], 16) / 255
    m = re.fullmatch(r"(rgba?|hsla?)\((.*)\)", s)
    if m:
        parts = [p for p in re.split(r"[\s,/]+", m[2].strip()) if p]
        if len(parts) not in (3, 4):
            raise ValueError(f"can't read color {text!r}")

        def num(p, scale):
            return float(p[:-1]) / 100 * scale if p.endswith("%") else float(p.rstrip("deg"))

        a = num(parts[3], 1) if len(parts) == 4 else 1.0
        if m[1].startswith("rgb"):
            r, g, b = (round(num(p, 255)) for p in parts[:3])
            return r, g, b, a
        h, sat, lig = num(parts[0], 360) / 360, num(parts[1], 1), num(parts[2], 1)
        r, g, b = colorsys.hls_to_rgb(h % 1, lig, sat)
        return round(r * 255), round(g * 255), round(b * 255), a
    raise ValueError(f"can't read color {text!r}")


def composite(fg, bg):
    a = fg[3]
    return tuple(round(f * a + b * (1 - a)) for f, b in zip(fg[:3], bg[:3]))


def hexof(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c))):02x}" for c in rgb[:3])


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (_lin(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def apca(txt, bg):
    """APCA-W3 0.1.9 lightness contrast Lc. Positive: dark text on light; negative: light on dark."""
    def y(rgb):
        r, g, b = ((c / 255) ** 2.4 for c in rgb[:3])
        v = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
        return v + (0.022 - v) ** 1.414 if v < 0.022 else v

    yt, yb = y(txt), y(bg)
    if abs(yb - yt) < 0.0005:
        return 0.0
    if yb > yt:
        sapc = (yb ** 0.56 - yt ** 0.57) * 1.14
        out = 0.0 if sapc < 0.1 else sapc - 0.027
    else:
        sapc = (yb ** 0.65 - yt ** 0.62) * 1.14
        out = 0.0 if sapc > -0.1 else sapc + 0.027
    return out * 100


# OKLab, for changing lightness while keeping hue and chroma
def _to_oklab(rgb):
    r, g, b = (_lin(c) for c in rgb[:3])
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def _from_oklab(lab):
    L, a, b = lab
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    lin = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
           -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
           -0.0041960863 * l_ - 0.7034186168 * m_ + 1.7076147010 * s_)

    def enc(c):
        c = max(0.0, min(1.0, c))
        return 255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)

    return tuple(round(enc(c)) for c in lin)


def fix(fg, bg, minimum):
    """Closest color to fg (same hue and chroma, new lightness) reaching the minimum ratio, or None."""
    L, a, b = _to_oklab(fg)
    best = None
    for target in (0.0, 1.0):  # try darker and lighter
        if ratio(_from_oklab((target, a, b)), bg) < minimum:
            continue
        lo, hi = L, target  # lo fails (or is the start), hi passes
        for _ in range(40):
            mid = (lo + hi) / 2
            if ratio(_from_oklab((mid, a, b)), bg) >= minimum:
                hi = mid
            else:
                lo = mid
        cand = _from_oklab((hi, a, b))
        if ratio(cand, bg) >= minimum and (best is None or abs(hi - L) < best[0]):
            best = (abs(hi - L), cand)
    return hexof(best[1]) if best else None


def verdict(r):
    if r >= 7:
        return "AAA"
    if r >= 4.5:
        return "AA"
    if r >= 3:
        return "AA large/UI only"
    return "FAIL"


def check(fg_text, bg_text, want_fix=False, minimum=4.5):
    bg = parse(bg_text)
    if bg[3] < 1:
        raise ValueError(f"background {bg_text!r} is translucent; give the color it ends up as")
    fg = composite(parse(fg_text), bg)
    r = ratio(fg, bg)
    line = (f"{fg_text} on {bg_text}: {r:.2f}:1  {verdict(r):<16} APCA Lc {apca(fg, bg):+.1f}")
    if want_fix and r < minimum:
        suggestion = fix(fg, bg, minimum)
        line += (f"\n  closest passing foreground for {minimum}:1: {suggestion}" if suggestion
                 else f"\n  no foreground of this hue reaches {minimum}:1 on this background")
    return r, line


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("colors", nargs="+", metavar="COLOR")
    p.add_argument("--fix", action="store_true", help="suggest the closest passing foreground")
    p.add_argument("--min", type=float, default=4.5,
                   help="ratio to reach with --fix and to pass the exit code (default 4.5)")
    p.add_argument("--palette", action="store_true", help="check every ordered pair of the colors")
    args = p.parse_args(argv)
    try:
        if args.palette:
            pairs = sorted(((ratio(composite(parse(f), parse(b)), parse(b)), f, b)
                            for f, b in permutations(args.colors, 2) if parse(b)[3] == 1),
                           reverse=True)
            for r, f, b in pairs:
                print(f"{r:5.2f}:1  {verdict(r):<16} {f} on {b}")
            return 0
        if len(args.colors) % 2:
            p.error("give colors in FG BG pairs")
        failed = False
        for i in range(0, len(args.colors), 2):
            r, line = check(args.colors[i], args.colors[i + 1], args.fix, args.min)
            failed |= r < args.min
            print(line)
        return 1 if failed else 0
    except ValueError as e:
        print(f"contrast: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

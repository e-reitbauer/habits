#!/usr/bin/env python3
"""Deal structural constraints for a design direction, so the plan starts away from your usual answer.

  direction.py [--seed N] [--cards 2] [--surface expressive|product]

A model asked for "a distinctive direction" lands on the same few every time, and steering away
from a banned look lands on the next one. A random constraint from outside the model breaks that.
The cards hold structure only (how color is spent, what leads the layout, the grid, the kind of
graphic device, scale, density, how the type is organised), never fonts, palettes or styles: the
subject fills them in. Deal, read both cards against the brief, keep the one that fits better, and
reject a value only with a reason from the brief, then deal that axis again with a new seed.
"""

import argparse
import random
import sys

# axis -> list of (value, what it means, how it goes wrong)
AXES = {
    "color strategy": [
        ("restrained", "tinted neutrals carry the page; one accent under 10% marks action and state",
         "reads as a template when the neutrals are the usual off-white; tint them from the subject"),
        ("committed", "one saturated color from the subject covers 30 to 60% of the surface: whole sections, the header, a band",
         "every section the same color; vary it with its own lighter and darker steps"),
        ("full palette", "three or four colors from the subject, each with a role and a share of the page",
         "colors with no roles become a rainbow; give each one a job and a place"),
        ("drenched", "the whole page lives inside one color family, from its palest to its deepest step",
         "low contrast between text and ground; check every pair"),
    ],
    "layout spine": [
        ("image-led", "the photos or objects carry the story; text sits around them",
         "images shrunk into boxes; let them fill fields, bands and edges"),
        ("type-led", "headlines and words at large scale carry the page",
         "every heading the same huge size; vary scale with importance"),
        ("object-led", "one or a few made objects from the subject are shown large and return through the page",
         "a primitive stand-in for the object; see objects.md"),
        ("diagram-led", "a map, plan, chart, timetable or route from the subject structures the page",
         "a fake chart as wallpaper; use real data or a real place"),
        ("collection-led", "the page is an index, menu, catalog or set of items the visitor browses",
         "identical cards; give items different scales or a list form"),
        ("sequence-led", "the page follows a process or a day in order, each section a step",
         "decorative 01/02/03; number only what really happens in order"),
    ],
    "grid": [
        ("asymmetric columns", "a wide and a narrow column that swap or shift between sections", "a fixed 50/50 split repeated"),
        ("modular fields", "a grid of equal fields; content and images span 1, 2 or 4 of them", "every item in one field"),
        ("one column with breakouts", "a narrow reading column; images and devices break out to wider lines or the edges", "nothing ever breaks out"),
        ("layered", "elements overlap on purpose: type over images, images across section edges", "accidental overlaps that hide content"),
        ("manuscript", "a classic page: one strong text block, margins that hold notes, captions and small images", "a plain blog post"),
    ],
    "graphic device": [
        ("pattern from an artifact", "a repeat built from one real object of the subject (a tile, a weave, a ruled sheet, a chart)", "generic dots or grids"),
        ("glyph system", "one rule makes a small family of marks, one per section or category", "random shapes with no visible rule"),
        ("frames and labels", "tickets, tags, stamps, mounts, folios, crop marks from the subject's printed matter", "sticker-bombing; one frame kind, used where it means something"),
        ("real-data graphic", "a map, timetable, route, measurement or schedule drawn exactly", "invented numbers"),
        ("type as ornament", "oversized numerals or words, cropped by edges, as structure", "outlined giant words with no meaning"),
        ("print treatment", "one print process applied to one class of images or panels (halftone, duotone, overprint)", "on every image and on body text"),
        ("cut and shape", "images and sections cut to a shape from the subject; edges between sections take that shape", "random blobs and waves"),
    ],
    "scale": [
        ("extreme contrast", "one element per view is far larger than the rest (5x and more)", "several huge things competing"),
        ("stepped", "a clear ladder of three or four sizes, no giant", "everything mid-size, nothing leads"),
    ],
    "density": [
        ("airy", "few elements per view, generous space with a job", "dead space beside a small box"),
        ("dense", "much information per view, tight but ordered, like an almanac or a parts catalog", "clutter without a grid"),
    ],
    "type structure": [
        ("one family with range", "a single family carries everything through widths, weights or optical sizes", "no contrast; use the range hard"),
        ("contrast pair", "a display face and a text face that differ clearly and share one trait", "two faces of the same kind"),
        ("display plus plain", "a characterful display face for few words, a quiet text face for the rest", "the display face in paragraphs"),
    ],
}

PRODUCT_AXES = ("color strategy", "type structure", "density")
# a fixed-canvas scroll story is planned in scenes and shots, so the page-layout axes don't apply
CINEMATIC_AXES = ("color strategy", "type structure", "scale")
# a scene is spectacle: quiet neutrals and a size ladder with no giant give a product viewer
CINEMATIC_NEVER = ("restrained", "stepped")


def deal(rng, surface):
    axes = {"product": PRODUCT_AXES, "cinematic": CINEMATIC_AXES}.get(surface, AXES)
    card = {}
    for axis in axes:
        values = AXES[axis]
        if surface == "product" and axis == "color strategy":
            values = values[:2]  # product UI: restrained or committed, never drenched
        elif surface == "cinematic":
            values = [v for v in values if v[0] not in CINEMATIC_NEVER]
        card[axis] = rng.choice(values)
    return card


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--seed", type=int, help="repeat a deal")
    p.add_argument("--cards", type=int, default=2, help="how many cards to deal (default 2)")
    p.add_argument("--surface", choices=["expressive", "product", "cinematic"], default="expressive",
                   help="product deals color strategy, type structure and density; cinematic deals "
                        "color strategy, type structure and scale (the storyboard plans the rest)")
    args = p.parse_args(argv)
    seed = args.seed if args.seed is not None else random.randrange(1_000_000)
    rng = random.Random(seed)
    print(f"seed {seed}\n")
    for n in range(1, args.cards + 1):
        print(f"Card {n}")
        for axis, (value, meaning, risk) in deal(rng, args.surface).items():
            print(f"  {axis + ':':<16} {value}: {meaning}")
            print(f"  {'':<16} goes wrong when: {risk}")
        print()
    print("Keep the card that fits the brief better. Fill every value from the subject. Reject a value only\n"
          "with a reason from the brief, and deal that axis again with another seed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

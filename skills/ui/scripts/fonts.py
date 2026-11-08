#!/usr/bin/env python3
"""Pick fonts from a catalog of open fonts at random, so the choice doesn't collapse onto the usual few.

  fonts.py --voice "warm editorial" [--role display|text|mono] [-n 6] [--seed N] [--common]
  fonts.py --voice "..." --specimen specimen.html --text "Your headline"   compare them rendered
  fonts.py --check "Inter" "Fraunces"   flag defaults and fonts generated pages keep reusing
  fonts.py --tags                       list the voice and structure tags

Every font here exists on Google Fonts or Fontshare (checked against their catalogs), so the
import lines work. The sample is random on purpose: a model asked for "a fitting font" picks the
same handful every time. Take the sample, judge it against the concept, pick one or draw again.
"""

import argparse
import html
import random
import sys

# The fonts generated pages reach for first. Not banned: use one when the user or the project's
# design system asks for it, or when the concept truly calls for it and you can say why.
DEFAULTS = {"Inter", "Roboto", "Open Sans", "Lato", "Arial", "Helvetica", "Helvetica Neue", "Poppins",
            "Montserrat", "Raleway", "Nunito", "Nunito Sans", "Source Sans 3", "Noto Sans", "Ubuntu",
            "Segoe UI", "system-ui", "Oswald", "Bebas Neue", "Merriweather", "Lora", "Roboto Slab",
            "Roboto Mono", "Pacifico", "Lobster", "Dancing Script", "Great Vibes", "Press Start 2P", "Orbitron",
            "Cinzel", "Comic Sans MS", "Quicksand", "Work Sans", "PT Sans", "Mulish", "Titillium Web"}
AI_FAVORITES = {"Space Grotesk", "Geist", "Geist Mono", "DM Sans", "DM Serif Display", "Manrope",
                "Plus Jakarta Sans", "Outfit", "Sora", "Urbanist", "Figtree", "Syne", "Inter Tight",
                "Instrument Serif", "Instrument Sans", "Fraunces", "Playfair Display", "Cormorant",
                "Cormorant Garamond", "EB Garamond", "Bricolage Grotesque", "Archivo", "JetBrains Mono",
                "Space Mono", "IBM Plex Mono", "Satoshi", "General Sans", "Clash Display", "Cabinet Grotesk",
                "Unbounded"}
COMMON_RANK = 100  # Google Fonts popularity rank at or below which a font counts as common

# name | roles (d display, t text, m mono) | tags | source (g<popularity rank> or fs:<slug>) | weights
CATALOG = """
Public Sans | dt | neo-grotesque utilitarian calm | g84 | 100..900 ital
Schibsted Grotesk | dt | grotesque editorial sturdy | g98 | 400..900 ital
Hanken Grotesk | dt | grotesque calm friendly | g142 | 100..900 ital
Familjen Grotesk | dt | grotesque quirky editorial | g437 | 400..700 ital
Host Grotesk | dt | grotesque utilitarian calm | g401 | 300..800 ital
Funnel Display | d | grotesque quirky bold | g452 | 300..800
Funnel Sans | t | grotesque calm utilitarian | g441 | 300..800 ital
Darker Grotesque | d | grotesque quirky editorial | g499 | 300..900
Onest | dt | neo-grotesque friendly calm | g165 | 100..900
Golos Text | t | neo-grotesque utilitarian | g248 | 400..900
Rethink Sans | dt | grotesque friendly | g231 | 400..800 ital
Albert Sans | dt | geometric calm | g172 | 100..900 ital
Red Hat Display | d | geometric sturdy friendly | g120 | 300..900 ital
Red Hat Text | t | geometric friendly | g239 | 300..700 ital
Libre Franklin | dt | grotesque classic sturdy | g81 | 100..900 ital
Geologica | dt | geometric technical | g169 | 100..900
Unbounded | d | wide geometric bold futuristic | g175 | 200..900
Anybody | d | wide condensed quirky poster | g679 | 100..900 ital wdth
Big Shoulders | d | condensed industrial poster | g488 | 100..900 opsz
Barlow | dt | grotesque industrial utilitarian | g46 | 100,200,300,400,500,600,700,800,900 ital
Barlow Condensed | d | condensed industrial sporty | g71 | 100,200,300,400,500,600,700,800,900 ital
Saira | dt | techno sporty | g56 | 100..900 ital wdth
Saira Condensed | d | condensed techno sporty | g182 | 100,200,300,400,500,600,700,800,900
Antonio | d | condensed poster bold | g314 | 100..700
League Gothic | d | condensed vintage poster | g266 | 400 wdth
Fjalla One | d | condensed sturdy | g97 | 400
Pathway Gothic One | d | condensed calm | g415 | 400
Sofia Sans | dt | humanist friendly | g211 | 1..1000 ital
Sofia Sans Condensed | d | condensed humanist | g354 | 1..1000 ital
Sofia Sans Extra Condensed | d | condensed poster | g431 | 1..1000 ital
Encode Sans | t | grotesque utilitarian | g254 | 100..900 wdth
Encode Sans Expanded | d | wide technical | g806 | 100,200,300,400,500,600,700,800,900
Chivo | dt | grotesque sturdy editorial | g257 | 100..900 ital
Kanit | d | techno sporty bold | g33 | 100,200,300,400,500,600,700,800,900 ital
Epilogue | dt | grotesque editorial quirky | g130 | 100..900 ital
Lexend | t | geometric calm friendly | g100 | 100..900
Karla | dt | grotesque quirky | g66 | 200..800 ital
Rubik | dt | rounded friendly | g32 | 300..900 ital
IBM Plex Sans | dt | grotesque technical industrial | g49 | 100..700 ital wdth
IBM Plex Sans Condensed | d | condensed technical | g244 | 100,200,300,400,500,600,700 ital
Overpass | dt | grotesque utilitarian | g136 | 100..900 ital
Commissioner | dt | humanist editorial | g310 | 100..900
Gantari | dt | geometric friendly | g498 | 100..900 ital
Radio Canada Big | dt | grotesque quirky friendly | g422 | 400..700 ital
Wix Madefor Display | d | grotesque calm | g502 | 400..800
Atkinson Hyperlegible Next | t | grotesque utilitarian calm | g411 | 200..800 ital
Tenor Sans | d | humanist elegant | g263 | 400
Josefin Sans | d | geometric vintage elegant | g92 | 100..700 ital
Jost | dt | geometric classic | g52 | 100..900 ital
Questrial | t | geometric calm | g160 | 400
Fira Sans | dt | humanist technical | g62 | 100,200,300,400,500,600,700,800,900 ital
Fira Sans Condensed | d | condensed humanist | g225 | 100,200,300,400,500,600,700,800,900 ital
Cabin | dt | humanist friendly | g110 | 400..700 ital wdth
Asap Condensed | d | condensed utilitarian | g311 | 200,300,400,500,600,700,800,900 ital
Signika | t | humanist utilitarian | g262 | 300..700
Alumni Sans | d | condensed elegant | g450 | 100..900 ital
Tomorrow | dt | techno futuristic | g490 | 100,200,300,400,500,600,700,800,900 ital
Michroma | d | wide techno futuristic | g419 | 400
Oxanium | d | techno futuristic | g291 | 200..800
Chakra Petch | d | techno quirky | g156 | 300,400,500,600,700 ital
Rajdhani | d | techno condensed | g123 | 300,400,500,600,700
Teko | d | condensed sporty | g150 | 300..700
Bai Jamjuree | dt | techno calm | g364 | 200,300,400,500,600,700 ital
Krona One | d | wide bold | g569 | 400
Syncopate | d | wide futuristic | g464 | 400,700
Gruppo | d | wide delicate retro | g334 | 400
Poiret One | d | geometric delicate vintage | g383 | 400
Federo | d | vintage elegant | g1114 | 400
Marcellus | d | glyphic classic elegant | g173 | 400
Forum | d | glyphic classic | g353 | 400
Belleza | d | humanist elegant | g427 | 400
Mona Sans | dt | grotesque sturdy | g412 | 200..900 ital wdth
Spline Sans | dt | grotesque quirky | g617 | 300..700
Inclusive Sans | t | grotesque friendly | g748 | 300..700 ital
Reddit Sans | dt | grotesque friendly | g454 | 200..900 ital
Hedvig Letters Sans | t | humanist editorial | g1072 | 400
Afacad | dt | humanist calm | g457 | 400..700 ital
Gabarito | d | geometric bold friendly | g331 | 400..900
Kumbh Sans | dt | geometric calm | g290 | 100..900
Tilt Warp | d | bold playful retro | g690 | 400
Climate Crisis | d | bold poster loud | g1283 | 400
Bowlby One | d | bold poster loud | g511 | 400
Dela Gothic One | d | bold poster loud | g328 | 400
Rubik Mono One | d | wide bold loud | g325 | 400
Staatliches | d | condensed poster vintage | g377 | 400
Squada One | d | condensed techno sporty | g516 | 400
Russo One | d | techno sporty bold | g273 | 400
Passion One | d | bold poster | g303 | 400,700,900
Paytone One | d | bold friendly rounded | g307 | 400
Lilita One | d | bold playful rounded | g168 | 400
Titan One | d | bold playful rounded | g197 | 400
Bangers | d | playful loud comic | g281 | 400
Bungee | d | signage loud poster | g157 | 400
Fredoka | dt | rounded playful friendly | g114 | 300..700 wdth
Baloo 2 | dt | rounded playful friendly | g179 | 400..800
Varela Round | t | rounded friendly | g190 | 400
M PLUS Rounded 1c | dt | rounded calm friendly | g125 | 100,300,400,500,700,800,900
DynaPuff | d | rounded playful | g678 | 400..700 wdth
Gluten | d | playful rounded | g1002 | 100..900
Parkinsans | dt | quirky geometric | g548 | 300..800
Playpen Sans | dt | handwritten friendly playful | g623 | 100..800
Literata | t | serif literary calm | g222 | 200..900 ital opsz
Source Serif 4 | dt | serif transitional editorial | g109 | 200..900 ital opsz
Libre Caslon Text | t | serif oldstyle classic | g253 | 400,700 ital
Libre Caslon Display | d | serif oldstyle elegant | g566 | 400
Libre Baskerville | t | serif transitional classic | g68 | 400..700 ital
Crimson Pro | t | serif oldstyle literary | g213 | 200..900 ital
Spectral | dt | serif editorial delicate | g178 | 200,300,400,500,600,700,800 ital
Newsreader | dt | serif editorial | g121 | 200..800 ital opsz
Vollkorn | dt | serif oldstyle sturdy rustic | g216 | 400..900 ital
Alegreya | t | serif oldstyle literary warm | g269 | 400..900 ital
Gelasio | t | serif transitional | g386 | 400..700 ital
Petrona | dt | serif quirky | g438 | 100..900 ital
Piazzolla | t | serif sturdy editorial | g735 | 100..900 ital opsz
Brygada 1918 | t | serif oldstyle vintage | g657 | 400..700 ital
Besley | d | serif bold vintage | g425 | 400..900 ital
Hahmlet | d | serif quirky | g760 | 100..900
Young Serif | d | serif vintage warm | g517 | 400
Gloock | d | didone bold | g408 | 400
Bodoni Moda | d | didone elegant luxurious | g144 | 400..900 ital opsz
Libre Bodoni | dt | didone classic | g389 | 400..700 ital
Abril Fatface | d | didone bold poster | g188 | 400
Rozha One | d | didone bold | g605 | 400
Prata | d | didone elegant | g255 | 400
Yeseva One | d | didone bold warm | g385 | 400
Gilda Display | d | didone elegant delicate | g340 | 400
Italiana | d | didone delicate elegant | g446 | 400
Bellefair | d | serif delicate elegant | g635 | 400
Cardo | t | serif oldstyle classic | g247 | 400,700 ital
Gentium Book Plus | t | serif oldstyle literary | g1083 | 400,700 ital
Old Standard TT | t | didone vintage | g264 | 400,700 ital
IM Fell English | d | serif oldstyle vintage rustic | g535 | 400 ital
Sorts Mill Goudy | dt | serif oldstyle classic | g398 | 400 ital
Linden Hill | d | serif oldstyle delicate | g1473 | 400 ital
Castoro | t | serif oldstyle | g639 | 400..700 ital
Castoro Titling | d | glyphic classic | g1394 | 400
Ibarra Real Nova | t | serif transitional classic | g759 | 400..700 ital
Imbue | d | didone condensed elegant | g1166 | 100..900 opsz
Radley | t | serif warm | g726 | 400 ital
Rosarivo | t | serif delicate | g1064 | 400 ital
Lustria | t | serif calm | g703 | 400
Ovo | d | serif delicate | g568 | 400
Della Respira | d | serif delicate classic | g882 | 400
STIX Two Text | t | serif transitional classic | g312 | 400..700 ital
Faustina | t | serif sturdy | g180 | 300..800 ital
Domine | t | serif sturdy | g151 | 400..700
Hedvig Letters Serif | t | serif editorial | g741 | 400 opsz
Noto Serif Display | d | didone elegant | g416 | 100..900 ital wdth
Texturina | d | blackletter serif vintage | g1501 | 100..900 ital opsz
Grenze | dt | serif blackletter quirky | g954 | 100..900 ital
Bitter | t | slab sturdy | g106 | 100..900 ital
Zilla Slab | dt | slab editorial quirky | g171 | 300,400,500,600,700 ital
Arvo | dt | slab geometric | g145 | 400,700 ital
Rokkitt | d | slab vintage | g368 | 100..900 ital
Aleo | t | slab warm | g272 | 100..900 ital
Josefin Slab | d | slab vintage delicate | g349 | 100..700 ital
Kreon | t | slab calm | g576 | 300..700
Podkova | d | slab sturdy | g745 | 400..800
Alfa Slab One | d | slab bold poster | g104 | 400
Ultra | d | slab bold poster vintage | g508 | 400
Coustard | d | slab warm | g933 | 400,900
Bevan | d | slab bold vintage | g553 | 400 ital
Holtwood One SC | d | slab wide vintage poster | g1190 | 400
Rye | d | western vintage ornamental | g481 | 400
Sancreek | d | western ornamental | g995 | 400
Graduate | d | slab sporty vintage | g644 | 400
DM Mono | m | mono calm | g146 | 300,400,500 ital
Fragment Mono | m | mono technical utilitarian | g626 | 400 ital
Martian Mono | m | mono wide technical | g604 | 100..800 wdth
Red Hat Mono | m | mono friendly | g650 | 300..700 ital
Azeret Mono | m | mono technical | g496 | 100..900 ital
Xanh Mono | m | mono quirky serif | g951 | 400 ital
Courier Prime | m | mono vintage typewriter | g210 | 400,700 ital
Cutive Mono | m | mono typewriter vintage delicate | g376 | 400
Spline Sans Mono | m | mono quirky | g633 | 300..700 ital
Sometype Mono | m | mono calm | g719 | 400..700 ital
Victor Mono | m | mono quirky | g1286 | 100..700 ital
Chivo Mono | m | mono sturdy | g586 | 100..900 ital
Reddit Mono | m | mono friendly | g1054 | 200..900
Major Mono Display | d | mono quirky futuristic | g866 | 400
Syne Mono | m | mono quirky | g863 | 400
Special Elite | d | typewriter vintage rustic | g259 | 400
Caveat | d | handwritten casual | g99 | 400..700
Kalam | d | handwritten casual | g209 | 300,400,700
Gochi Hand | d | handwritten playful | g492 | 400
Permanent Marker | d | handwritten loud | g195 | 400
Rock Salt | d | handwritten rough rustic | g440 | 400
Homemade Apple | d | script handwritten | g366 | 400
Reenie Beanie | d | handwritten casual | g391 | 400
Covered By Your Grace | d | handwritten casual | g542 | 400
Nanum Pen Script | d | handwritten delicate | g399 | 400
Patrick Hand | d | handwritten friendly | g283 | 400
Pangolin | d | handwritten friendly | g532 | 400
Mali | d | handwritten friendly rounded | g587 | 200,300,400,500,600,700 ital
Yellowtail | d | script retro | g192 | 400
Damion | d | script retro | g381 | 400
Mr Dafoe | d | script loud | g428 | 400
Sacramento | d | script delicate | g305 | 400
Pinyon Script | d | script elegant classic | g330 | 400
Allura | d | script elegant | g275 | 400
Monsieur La Doulaise | d | script ornamental | g766 | 400
Italianno | d | script delicate elegant | g466 | 400
Shrikhand | d | bold retro playful | g581 | 400
Sedgwick Ave | d | handwritten loud | g1032 | 400
UnifrakturMaguntia | d | blackletter | g540 | 400
Pirata One | d | blackletter | g478 | 400
Grenze Gotisch | d | blackletter | g776 | 100..900
Jacquard 24 | d | blackletter pixel | g1684 | 400
Metamorphous | d | ornamental vintage | g764 | 400
Cinzel Decorative | d | ornamental glyphic | g357 | 400,700,900
Limelight | d | art-deco vintage | g594 | 400
Fascinate | d | art-deco loud | g1367 | 400
Monoton | d | retro loud | g503 | 400
Nabla | d | color playful loud | g1357 | 400
Silkscreen | d | pixel retro | g526 | 400,700
VT323 | d | pixel retro technical | g315 | 400
Pixelify Sans | d | pixel friendly | g459 | 400..700
Tiny5 | d | pixel | g1038 | 100..900 ital wdth
Handjet | d | pixel techno | g1317 | 100..900
Doto | d | pixel techno | g734 | 100..900
DotGothic16 | d | pixel retro | g622 | 400
Sixtyfour | d | pixel retro technical | g1608 | 400
Big Shoulders Stencil | d | stencil industrial condensed | g1484 | 100..900 opsz
Saira Stencil | d | stencil techno | g1926 | 100..900 ital wdth
Stardos Stencil | d | stencil vintage | g627 | 400,700
Allerta Stencil | d | stencil utilitarian | g710 | 400
Emblema One | d | stencil quirky | g1502 | 400
Clash Grotesk | dt | grotesque bold sturdy | fs:clash-grotesk | 200,300,400,500,600,700
Switzer | dt | neo-grotesque utilitarian calm | fs:switzer | 100,200,300,400,500,600,700,800,900 ital
Supreme | dt | geometric calm | fs:supreme | 100,200,300,400,500,700,800 ital
Chillax | d | geometric quirky friendly | fs:chillax | 200,300,400,500,600,700
Ranade | dt | humanist calm | fs:ranade | 100,300,400,500,700 ital
Author | dt | grotesque quirky editorial | fs:author | 200,300,400,500,600,700 ital
Synonym | dt | grotesque calm | fs:synonym | 200,300,400,500,600,700
Tabular | dt | grotesque utilitarian technical | fs:tabular | 300,400,500,600,700 ital
Plein | dt | grotesque bold | fs:plein | 300,400,500,700,900 ital
Alpino | dt | geometric friendly | fs:alpino | 100,300,400,500,700,900
Amulya | dt | humanist warm | fs:amulya | 300,400,500,700 ital
Quilon | dt | grotesque sturdy | fs:quilon | 400,500,600,700
Excon | dt | geometric technical | fs:excon | 100,300,400,500,700,900
Roundo | dt | rounded friendly | fs:roundo | 200,300,400,500,600,700
Erode | dt | serif quirky editorial | fs:erode | 300,400,500,600,700 ital
Sentient | dt | serif editorial calm | fs:sentient | 200,300,400,500,700 ital
Zodiak | d | serif bold elegant | fs:zodiak | 100,300,400,700,800,900 ital
Gambetta | dt | serif classic editorial | fs:gambetta | 300,400,500,600,700 ital
Boska | d | serif elegant delicate | fs:boska | 200,300,400,500,700,900 ital
Bespoke Serif | d | serif elegant | fs:bespoke-serif | 300,400,500,700,800 ital
Bespoke Slab | dt | slab sturdy | fs:bespoke-slab | 300,400,500,700,800 ital
Bespoke Stencil | d | stencil sturdy | fs:bespoke-stencil | 300,400,500,700,800 ital
Rowan | dt | serif warm | fs:rowan | 300,400,500,600,700 ital
Recia | dt | serif sturdy | fs:recia | 300,400,500,600,700 ital
Neco | d | serif quirky | fs:neco | 400,500,700,900 ital
Trench Slab | dt | slab sturdy industrial | fs:trench-slab | 300,400,500,600,700
Paquito | d | slab warm playful | fs:paquito | 400,500,700
Hoover | d | slab bold | fs:hoover | 100,300,400,500,700
Tanker | d | condensed bold poster loud | fs:tanker | 400
Panchang | d | wide bold | fs:panchang | 200,300,400,500,600,700,800
Melodrama | d | condensed elegant | fs:melodrama | 300,400,500,600,700
Stardom | d | serif bold quirky | fs:stardom | 400
Gambarino | d | serif retro | fs:gambarino | 400
Array | d | techno pixel | fs:array | 400,600,700
Technor | d | techno wide | fs:technor | 200,300,400,500,600,700,900
Segment | d | techno pixel | fs:segment | 400
Kola | d | bold playful | fs:kola | 400
Nippo | d | wide techno | fs:nippo | 200,300,400,500,700
Bonny | d | serif retro rounded | fs:bonny | 100,300,400,500,700
Chubbo | d | rounded bold playful | fs:chubbo | 200,300,400,500,700 ital
Britney | d | script retro bold | fs:britney | 300,400,700,1000
Pally | d | rounded friendly | fs:pally | 400,500,700
Telma | d | script playful | fs:telma | 300,400,500,700,900
Comico | d | handwritten playful | fs:comico | 400
Rosaline | d | script elegant | fs:rosaline | 400
"""


def load():
    fonts = []
    for line in CATALOG.strip().splitlines():
        name, roles, tags, source, weights = [x.strip() for x in line.split("|")]
        parts = weights.split()
        fonts.append({
            "name": name, "roles": roles, "tags": set(tags.split()), "source": source,
            "weights": parts[0], "italic": "ital" in parts, "axes": [p for p in parts[1:] if p != "ital"],
            "rank": int(source[1:]) if source.startswith("g") else None,
        })
    return fonts


def common(font):
    return (font["name"] in DEFAULTS or font["name"] in AI_FAVORITES
            or (font["rank"] is not None and font["rank"] <= COMMON_RANK))


def link(font):
    """The stylesheet URL for the font with all its upright weights; trim to the weights you use."""
    w = font["weights"]
    if font["source"].startswith("fs:"):
        return f"https://api.fontshare.com/v2/css?f[]={font['source'][3:]}@{w}&display=swap"
    family = font["name"].replace(" ", "+")
    if ".." in w:
        return f"https://fonts.googleapis.com/css2?family={family}:wght@{w}&display=swap"
    if w == "400":
        return f"https://fonts.googleapis.com/css2?family={family}&display=swap"
    return f"https://fonts.googleapis.com/css2?family={family}:wght@{w.replace(',', ';')}&display=swap"


def describe(font):
    roles = {"d": "display", "t": "text", "m": "mono"}
    extra = ", ".join(filter(None, ["italic" if font["italic"] else "", *font["axes"]]))
    where = "Fontshare" if font["source"].startswith("fs:") else "Google Fonts"
    return (f"{font['name']:<26} {'+'.join(roles[r] for r in font['roles']):<13} "
            f"{' '.join(sorted(font['tags'])):<38} {where}, weights {font['weights']}"
            f"{' (' + extra + ')' if extra else ''}\n    {link(font)}")


def sample(fonts, voice, role, n, rng, include_common):
    pool = [f for f in fonts if (include_common or not common(f)) and (not role or role[0] in f["roles"])]
    wanted = set(voice)
    scored = [(len(wanted & f["tags"]), f) for f in pool]
    matching = [(s, f) for s, f in scored if s] if wanted else [(1, f) for f in pool]
    picks = []
    while matching and len(picks) < n:
        total = sum(s for s, _ in matching)
        r = rng.uniform(0, total)
        for i, (s, f) in enumerate(matching):
            r -= s
            if r <= 0:
                picks.append(matching.pop(i)[1])
                break
    return picks, len(matching) + len(picks)


def specimen(fonts, text, path):
    links = "\n".join(f'<link rel="stylesheet" href="{html.escape(link(f))}">' for f in fonts)
    rows = "\n".join(
        f'<section><p class="meta">{html.escape(f["name"])} · {" ".join(sorted(f["tags"]))}</p>'
        f'<p class="big" style="font-family:\'{html.escape(f["name"])}\'">{html.escape(text)}</p>'
        f'<p class="body" style="font-family:\'{html.escape(f["name"])}\'">The quick brown fox jumps over '
        f'the lazy dog. 0123456789 &amp; ?! Hamburgefonstiv. Sphinx of black quartz, judge my vow.</p></section>'
        for f in fonts)
    with open(path, "w") as out:
        out.write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Font specimen</title>
{links}
<style>body{{margin:2rem;font:14px/1.4 system-ui;background:#fbfbfa;color:#1c1c1c}}
section{{padding:1.25rem 0;border-bottom:1px solid #ddd}}.meta{{color:#666;margin:0 0 .4rem}}
.big{{font-size:3.2rem;line-height:1.05;margin:0 0 .6rem}}.body{{font-size:1.05rem;max-width:60ch;margin:0}}</style>
</head><body>{rows}</body></html>""")


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--voice", default="", help="tags that describe the concept's voice, e.g. 'warm editorial'")
    p.add_argument("--role", choices=["display", "text", "mono"], help="only fonts that work in this role")
    p.add_argument("-n", type=int, default=6, help="how many candidates (default 6)")
    p.add_argument("--seed", type=int, help="repeat an earlier draw")
    p.add_argument("--common", action="store_true", help="include the defaults and the most used fonts")
    p.add_argument("--specimen", metavar="FILE", help="also write an HTML page that renders the candidates")
    p.add_argument("--text", default="Sphinx of black quartz", help="headline for the specimen")
    p.add_argument("--check", nargs="+", metavar="FONT", help="flag fonts that are defaults or overused")
    p.add_argument("--tags", action="store_true", help="list the tags")
    args = p.parse_args(argv)
    fonts = load()

    if args.tags:
        counts = {}
        for f in fonts:
            for t in f["tags"]:
                counts[t] = counts.get(t, 0) + 1
        print(" ".join(f"{t}({c})" for t, c in sorted(counts.items())))
        return 0

    if args.check:
        by_name = {f["name"].lower(): f for f in fonts}
        flagged = 0
        for name in args.check:
            name = name.strip().strip("'\"")
            f = by_name.get(name.lower())
            if name in DEFAULTS:
                note = "default: the font every generated page uses; pick it only with a reason"
            elif name in AI_FAVORITES:
                note = "AI favorite: the 'designed' pick models keep reaching for; pick it only with a reason"
            elif f and common(f):
                note = f"very common (Google Fonts popularity #{f['rank']}); fine with a reason"
            else:
                note = "ok"
            flagged += note != "ok"
            print(f"{name:<26} {note}")
        return 1 if flagged else 0

    voice = [t.strip().lower() for t in args.voice.replace(",", " ").split() if t.strip()]
    known = set().union(*(f["tags"] for f in fonts))
    unknown = [t for t in voice if t not in known]
    if unknown:
        print(f"fonts: unknown tags {', '.join(unknown)} (see --tags)", file=sys.stderr)
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(10 ** 6)
    picks, matched = sample(fonts, voice, args.role, args.n, random.Random(seed), args.common)
    if not picks:
        print("fonts: nothing matches; use fewer or other tags (see --tags)", file=sys.stderr)
        return 1
    print(f"{len(picks)} of {matched} matching fonts, seed {seed}:\n")
    for f in picks:
        print(describe(f))
    if args.specimen:
        specimen(picks, args.text, args.specimen)
        print(f"\nspecimen: {args.specimen} (open it and judge them rendered, at the real sizes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

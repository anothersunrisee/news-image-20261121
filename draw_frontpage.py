#!/usr/bin/env python3
"""Draw a dense one-day news front page (1024x1024, PIL) for 21 Nov 2026.

Mid-century poster / Swiss editorial style: cream paper, navy header,
brick-red accents, serif masthead, thin rules, geometric pictograms,
dot-matrix world map. All story data comes from NEWS.md (30 stories:
3 top, 8 medium, 19 briefs). Deterministic: no timestamps, no random
input, so re-running reproduces entry.png byte-for-byte.
"""
import hashlib
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = H = 1024
MARGIN = 40  # outer frame must stay clean cream paper
RX = W - MARGIN - 1  # last content column (984 is inside the margin)

# --- palette ---
CREAM = (244, 238, 226)   # paper
CARD = (253, 251, 244)    # card paper
PANEL = (233, 227, 211)   # pictogram panel
NAVY = (18, 38, 66)
NAVY2 = (32, 60, 96)
RED = (176, 32, 28)
GOLD = (198, 158, 40)
INK = (34, 34, 30)
GRAY = (96, 92, 82)
RULE = (212, 205, 190)
DOT = (46, 64, 87)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


def F_SERIF_B(s):
    return load("DejaVuSerif-Bold.ttf", s)


def F_SANS(s):
    return load("DejaVuSans.ttf", s)


def F_SANS_B(s):
    return load("DejaVuSans-Bold.ttf", s)


ISSUES = []


def wrap(text, font, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if font.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(d, x, y, text, font, fill, max_w, lh, max_lines, tag):
    """Draw wrapped text; record an issue if it needs more than max_lines."""
    lines = wrap(text, font, max_w)
    if len(lines) > max_lines:
        ISSUES.append(f"{tag}: {len(lines)} lines, max {max_lines}: {text[:60]!r}")
    for i, line in enumerate(lines[:max_lines]):
        lx = x
        # glyphs like "j" can carry a negative left side bearing and
        # bleed 1px left of the pen position; keep ink inside the margin
        bb = d.textbbox((x, y + i * lh), line, font=font)
        if bb[0] < MARGIN:
            lx = x + (MARGIN - bb[0])
        d.text((lx, y + i * lh), line, font=font, fill=fill)
    return y + min(len(lines), max_lines) * lh


def section_label(d, x, y, text, right_text=""):
    """Small-caps label with a thin rule to the right edge."""
    f = F_SANS_B(13)
    d.text((x, y), text, font=f, fill=NAVY)
    tx = x + f.getlength(text) + 10
    d.line([(tx, y + 7), (RX, y + 7)], fill=RULE, width=1)
    if right_text:
        rf = F_SANS_B(11)
        d.text((RX - rf.getlength(right_text), y + 1),
               right_text, font=rf, fill=GRAY)


# ---------------------------------------------------------------- stories
TOP = [
    {
        "kick": "TOP STORY 1",
        "head": "RUSSIA STRIKES: MISSILES LAND IN POLAND",
        "body": ("Russia's biggest attacks of the year: 400+ drones and 110 "
                 "missiles overnight, 8 killed in Kyiv. Two missiles land in "
                 "Poland; Tusk calls it a deliberate provocation; NATO "
                 "scrambles jets."),
        "art": "missile",
    },
    {
        "kick": "TOP STORY 2",
        "head": "AI SELL-OFF DRAGS S&P INTO CORRECTION",
        "body": ("US stocks fall sharply Friday in an AI-led rout: S&P 500 "
                 "-3.7%, Nasdaq -5.28%, Dow -1.93%. Nasdaq wipes out all "
                 "its 2026 gains as doubts grow over AI spending."),
        "art": "chart",
    },
    {
        "kick": "TOP STORY 3",
        "head": "ICJ: MYANMAR GUILTY OF ROHINGYA GENOCIDE",
        "body": ("The International Court of Justice rules 9-6 that Myanmar "
                 "committed genocide against the Rohingya - the first time "
                 "it has held a state responsible. It orders investigation "
                 "and compensation."),
        "art": "scales",
    },
]

MEDIUM = [
    ("POLITICS", "TRUMP CALLS PUTIN A FRIEND",
     "Trump calls Putin a friend after first US-China-Russia talks."),
    ("CLIMATE", "COP31 MISSES DEADLINE, RUNS INTO OVERTIME",
     "Antalya talks run past Friday's close; draft drops fossil fuels."),
    ("MIDDLE EAST", "SAUDI COALITION STOPS HOUTHI MISSILES",
     "Three Houthi missiles headed for Riyadh intercepted."),
    ("EUROPE", "UK AND EU SEAL BIGGEST POST-BREXIT STEP",
     "Food checks scrapped from 2028; youth mobility for 100,000."),
    ("TECH", "SEC PROBES NVIDIA ACCOUNTING",
     "SEC examines Nvidia accounting; shares fall 13.8%."),
    ("MIDDLE EAST", "14 IRANIAN TANKERS MASS AT KHARG ISLAND",
     "14+ tankers mass to sail as a convoy and test a US blockade."),
    ("HEALTH", "PANCREATIC CANCER PILL SHOWS PROGRESS",
     "Daraxonrasib makes tumours undetectable in 1 in 12 patients."),
    ("EUROPE", "EU ASSIGNS 1BN FOR UKRAINE DEFENCE KIT",
     "EU approves 1bn for Ukraine defence equipment."),
]

BRIEFS = [
    "US House passed 2022 $1.7T bill unconstitutionally, 9-8.",
    "Anthropic shares slide 10% to $87.80, day two after IPO.",
    "Trump threatens 'tremendous tax' on AI data centres abroad.",
    "Denmark expels Russian diplomat over assassination plot.",
    "Mamdani to close NYC Rikers Island jail by 2032.",
    "French police sentenced for beating producer Michel Zecler.",
    "Indian man gets 19+ years in US Sikh separatist murder plot.",
    "Nearly 600 women killed in South Africa in three months.",
    "US declassifies more UFO footage from Middle East.",
    "US measles cases near 6,000 - 5,838 as of 19 Nov.",
    "Spain's Feijoo wins TV debate vs Sanchez, 51-29.",
    "IndusInd Bank sacks ex-CEO Kathpalia, seeks pay back.",
    "Cost-of-living protests disrupt Italy.",
    "Austrian foreign ministry hacked.",
    "ANC fights to keep South Africa cities after poll setback.",
    "Bangladesh asks Myanmar to compensate Rohingyas.",
    "American woman freed after 10 years in Cuba.",
    "South Korea top court clears ex-PM over martial law.",
    "Van Gogh sells for record $190m at auction.",
]

CHIP_COLORS = {
    "POLITICS": (36, 80, 140),
    "CLIMATE": (34, 120, 70),
    "MIDDLE EAST": (150, 96, 20),
    "EUROPE": NAVY2,
    "TECH": (110, 60, 140),
    "HEALTH": (16, 120, 120),
}

# Dot-matrix world map: land cells as (start_col, end_col) ranges per row.
# Grid is 56 cols x 20 rows; col = (lon+180)/360*56, row = (75-lat)/135*20.
MAP_ROWS = [
    [(8, 14), (36, 54)],
    [(4, 16), (27, 30), (35, 55)],
    [(3, 17), (26, 31), (34, 55)],
    [(3, 18), (26, 33), (34, 55)],
    [(4, 18), (26, 33), (35, 53)],
    [(5, 18), (27, 32), (36, 52)],
    [(6, 17), (27, 33), (35, 50)],
    [(7, 16), (27, 34), (35, 48)],
    [(9, 15), (27, 33), (36, 47)],
    [(12, 16), (28, 32), (40, 48)],
    [(13, 18), (28, 32)],
    [(14, 19), (28, 31)],
    [(14, 20), (29, 31), (34, 34)],
    [(15, 20), (29, 31)],
    [(15, 19), (29, 30), (45, 50)],
    [(16, 18), (29, 30), (44, 51)],
    [(16, 17), (45, 49)],
    [(16, 17)],
    [(16, 16)],
    [],
]
# Numbered pins: (number, col, row, label) - must sit on land cells.
PINS = [
    (1, 31, 3, "POLAND"),
    (2, 16, 5, "NEW YORK"),
    (3, 43, 8, "MYANMAR"),
]


# ---------------------------------------------------------------- pictograms
def art_missile(d, x, y, w, h):
    """Vertical rocket with flame and a red starburst."""
    cx = x + w // 2
    # starburst, top right: 8 spikes as triangles around a core
    sx, sy = x + w - 26, y + 14
    for k in range(8):
        a = math.pi * k / 4
        tip = (sx + 15 * math.cos(a), sy + 15 * math.sin(a))
        b1 = (sx + 4 * math.cos(a + 0.35), sy + 4 * math.sin(a + 0.35))
        b2 = (sx + 4 * math.cos(a - 0.35), sy + 4 * math.sin(a - 0.35))
        d.polygon([tip, b1, b2], fill=RED)
    d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=RED)
    # speed lines, left
    for yy in (y + 16, y + 30, y + 44):
        d.line([(x + 14, yy), (x + 34, yy)], fill=NAVY2, width=2)
    # rocket body (nose cone + body + fins + window + flame)
    d.polygon([(cx, y + 4), (cx + 9, y + 18), (cx + 9, y + 46),
               (cx - 9, y + 46), (cx - 9, y + 18)], fill=NAVY)
    d.polygon([(cx - 9, y + 40), (cx - 20, y + 52), (cx - 9, y + 50)], fill=RED)
    d.polygon([(cx + 9, y + 40), (cx + 20, y + 52), (cx + 9, y + 50)], fill=RED)
    d.ellipse([cx - 4, y + 24, cx + 4, y + 32], fill=CREAM)
    d.polygon([(cx - 6, y + 48), (cx + 6, y + 48), (cx, y + 62)], fill=GOLD)


def art_chart(d, x, y, w, h):
    """Falling market line with arrowhead and a dashed old-peak line."""
    for xx in range(x + 18, x + w - 14, 10):
        d.line([(xx, y + 12), (xx + 6, y + 12)], fill=GRAY, width=1)
    d.line([(x + 18, y + 8), (x + 18, y + h - 10)], fill=NAVY2, width=2)
    d.line([(x + 18, y + h - 10), (x + w - 8, y + h - 10)], fill=NAVY2, width=2)
    pts = [(x + 26, y + 16), (x + 66, y + 22), (x + 106, y + 18),
           (x + 146, y + 30), (x + 186, y + 38), (x + 226, y + 46),
           (x + 262, y + 52)]
    d.line(pts, fill=RED, width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey + 2), (ex - 12, ey - 4), (ex - 2, ey + 12)], fill=RED)
    d.text((x + w - 66, y + 2), "-5.28%", font=F_SANS_B(13), fill=RED)


def art_scales(d, x, y, w, h):
    """Scales of justice, navy with a gold finial."""
    cx = x + w // 2
    d.ellipse([cx - 4, y + 2, cx + 4, y + 10], fill=GOLD)
    d.line([(cx, y + 10), (cx, y + h - 12)], fill=NAVY, width=3)
    d.line([(cx - 44, y + 14), (cx + 44, y + 14)], fill=NAVY, width=3)
    for px in (cx - 44, cx + 44):
        d.line([(px, y + 14), (px - 14, y + 38)], fill=NAVY, width=2)
        d.line([(px, y + 14), (px + 14, y + 38)], fill=NAVY, width=2)
        d.polygon([(px - 15, y + 38), (px + 15, y + 38), (px, y + 50)],
                  fill=NAVY2)
    d.line([(cx - 22, y + h - 12), (cx + 22, y + h - 12)], fill=NAVY, width=3)
    d.rectangle([cx - 14, y + h - 10, cx + 14, y + h - 6], fill=NAVY)


ARTS = {"missile": art_missile, "chart": art_chart, "scales": art_scales}


# ---------------------------------------------------------------- build
def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- header band (inside the 40px margin) ----
    d.rectangle([MARGIN, MARGIN, RX, 148], fill=NAVY)
    d.text((W // 2, 52), "THE WORLD IN ONE DAY",
           font=F_SANS_B(14), fill=GOLD, anchor="ma")
    d.text((W // 2, 72), "Saturday 21 November 2026",
           font=F_SERIF_B(38), fill=CREAM, anchor="ma")
    d.text((W // 2, 122), "30 STORIES  ·  6 CONTINENTS  ·  ONE DAY",
           font=F_SANS_B(15), fill=CREAM, anchor="ma")

    # ---- top stories: 3 columns ----
    col_w, gap = 300, 22
    top_y = 160
    for i, s in enumerate(TOP):
        x = MARGIN + i * (col_w + gap)
        # kicker chip
        d.rectangle([x, top_y, x + 118, top_y + 20], fill=RED)
        d.text((x + 8, top_y + 3), s["kick"], font=F_SANS_B(12), fill=CREAM)
        # pictogram panel
        py = top_y + 28
        d.rectangle([x, py, min(x + col_w, RX), py + 66], fill=PANEL,
                    outline=RULE, width=1)
        ARTS[s["art"]](d, x, py, col_w, 66)
        # headline
        hy = py + 74
        draw_block(d, x, hy, s["head"], F_SANS_B(18), NAVY, col_w, 22, 2,
                   f"top{i+1}-head")
        # body
        draw_block(d, x, hy + 50, s["body"], F_SANS(13), INK, col_w, 17, 5,
                   f"top{i+1}-body")
        d.line([(x, top_y + 232), (min(x + col_w, RX), top_y + 232)],
               fill=RULE, width=1)

    # ---- medium cards: 2 rows x 4 cols ----
    card_w, card_h, cg = 227, 92, 12
    my = 410
    for i, (cat, head, body) in enumerate(MEDIUM):
        r, c = divmod(i, 4)
        x = MARGIN + c * (card_w + cg)
        y = my + r * (card_h + 10)
        d.rectangle([x, y, min(x + card_w, RX), y + card_h], fill=CARD,
                    outline=RULE, width=1)
        d.rectangle([x, y, x + 4, y + card_h],
                    fill=CHIP_COLORS.get(cat, NAVY2))
        tx = x + 12
        d.text((tx, y + 7), cat, font=F_SANS_B(11),
               fill=CHIP_COLORS.get(cat, NAVY2))
        draw_block(d, tx, y + 24, head, F_SANS_B(13), NAVY, card_w - 20, 16,
                   2, f"med{i+1}-head")
        draw_block(d, tx, y + 58, body, F_SANS(12), INK, card_w - 20, 14, 2,
                   f"med{i+1}-body")

    # ---- briefs ----
    by = 610
    section_label(d, MARGIN, by, "THE DAY IN BRIEF", "19 MORE STORIES")
    brief_y = by + 22
    col_w2 = 464
    for side in range(2):
        items = BRIEFS[side * 10:(side + 1) * 10]
        x = MARGIN + side * (col_w2 + 16)
        y = brief_y
        for j, item in enumerate(items):
            num = str(12 + side * 10 + j)
            nf = F_SANS_B(12)
            d.text((x, y), f"{num}.", font=nf, fill=RED)
            nx = x + nf.getlength(f"{num}.") + 6
            bf = F_SANS(12)
            lines = wrap(item, bf, x + col_w2 - nx)
            if len(lines) > 1:
                ISSUES.append(f"brief {num}: wraps to {len(lines)} lines")
            d.text((nx, y), lines[0] if lines else "", font=bf, fill=INK)
            y += 16

    # ---- world map ----
    my2 = 798
    section_label(d, MARGIN, my2, "WHERE IT HAPPENED",
                  "1 POLAND  ·  2 NEW YORK  ·  3 MYANMAR  —  NOT TO SCALE")
    map_x, map_y, map_w, map_h = MARGIN + 20, my2 + 24, 904, 118
    cols, rows = 56, 20
    dx, dy = map_w / cols, map_h / rows
    for r, ranges in enumerate(MAP_ROWS):
        for a, b in ranges:
            for c in range(a, b + 1):
                cx = map_x + (c + 0.5) * dx
                cy = map_y + (r + 0.5) * dy
                d.ellipse([cx - 3, cy - 2.5, cx + 3, cy + 2.5], fill=DOT)
    for num, c, r, _label in PINS:
        cx = map_x + (c + 0.5) * dx
        cy = map_y + (r + 0.5) * dy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=CREAM, width=2)
        pf = F_SANS_B(10)
        d.text((cx, cy - 1), str(num), font=pf, fill=CREAM, anchor="mm")

    # ---- footer ----
    foot = ("Sources: Reuters · AP · AFP · BBC · Al Jazeera — Every story "
            "above was first reported on Saturday 21 November 2026")
    ff = F_SANS(12)
    d.text((W // 2, 950), foot, font=ff, fill=GRAY, anchor="ma")
    d.line([(MARGIN, 944), (RX, 944)], fill=RULE, width=1)

    img.save(OUT, format="PNG")

    # ---- verification: outer 40px frame must be pure cream ----
    px = img.load()
    dirty = 0
    for yy in range(H):
        for xx in range(W):
            if xx < MARGIN or xx >= W - MARGIN or yy < MARGIN or yy >= H - MARGIN:
                if px[xx, yy] != CREAM:
                    dirty += 1
    if dirty:
        ISSUES.append(f"outer frame: {dirty} non-cream pixels")

    data = OUT.read_bytes()
    print(f"entry.png: {len(data)} bytes, {W}x{H}, "
          f"sha256={hashlib.sha256(data).hexdigest()[:16]}")
    print(f"outer-frame non-cream pixels: {dirty}")
    if ISSUES:
        print("ISSUES:")
        for it in ISSUES:
            print(f"  - {it}")
        sys.exit(1)
    print("OK: no layout issues")


if __name__ == "__main__":
    main()

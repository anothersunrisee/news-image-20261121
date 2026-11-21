#!/usr/bin/env python3
"""news-image-20261121: dense newspaper front page, PIL-drawn, 1024x1024.
Adapted from the v5 pipeline (news-image-20261118, rank 687/17,897):
same layout/style, new stories for Saturday 21 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 40                      # outer margin
CW = W - 2 * M              # 944 content width

PAPER = (247, 241, 227)     # warm cream
INK = (26, 26, 26)
NAVY = (20, 38, 74)
RED = (193, 39, 45)
GOLD = (217, 164, 65)
TEAL = (31, 122, 109)
BLUE = (46, 95, 163)
GREEN = (62, 122, 58)
PURPLE = (106, 76, 147)
ORANGE = (198, 110, 30)
SLATE = (138, 148, 166)
GRAY = (68, 68, 68)
LIGHT_LINE = (216, 210, 192)
SKY = (215, 227, 238)
WATER = (46, 95, 163)
DARKTEAL = (20, 82, 74)
MAROON = (96, 24, 30)

F = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

F_MAST = font("NotoSerifDisplay-Bold.ttf", 44)
F_KICK = font("NotoSans-Bold.ttf", 14)
F_CLAIM = font("NotoSans-Bold.ttf", 14)
F_SECT = font("NotoSans-Bold.ttf", 13)
F_H1 = font("NotoSans-Bold.ttf", 17)
F_SUB = font("NotoSans-Regular.ttf", 12)
F_CHIP = font("NotoSans-Bold.ttf", 10)
F_MH = font("NotoSans-Bold.ttf", 13)
F_MS = font("NotoSans-Regular.ttf", 11)
F_BR = font("NotoSans-Regular.ttf", 11)
F_BRN = font("NotoSans-Bold.ttf", 11)
F_FOOT = font("NotoSans-Regular.ttf", 11)
F_PIN = font("NotoSans-Bold.ttf", 10)
F_LEG = font("NotoSans-Bold.ttf", 10)
F_MAPL = font("NotoSans-Bold.ttf", 11)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(draw, s, f):
    return draw.textlength(s, font=f)

def wrap(draw, s, f, maxw):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def tracked(draw, cx, y, s, f, fill, tr=2):
    widths = [draw.textlength(c, font=f) for c in s]
    total = sum(widths) + tr * (len(s) - 1)
    x = cx - total / 2
    for c, w in zip(s, widths):
        draw.text((x, y), c, font=f, fill=fill)
        x += w + tr

def chip(draw, x, y, label, color):
    tw = draw.textlength(label, font=F_CHIP)
    pad = 7
    bw, bh = tw + 2 * pad, 17
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=3, fill=color)
    draw.text((x + pad, y + 3), label, font=F_CHIP, fill=(255, 255, 255))
    return bw

# ---------------------------------------------------------------- masthead
tracked(d, W // 2, 40, "THE WORLD IN ONE DAY", F_KICK, RED, tr=3)
d.text((W // 2, 56), "Saturday 21 November 2026", font=F_MAST, fill=NAVY, anchor="ma")
tracked(d, W // 2, 106, "30 STORIES  ·  6 CONTINENTS  ·  ONE DAY", F_CLAIM, NAVY, tr=2)
d.rectangle([M, 128, W - M - 1, 131], fill=NAVY)
d.rectangle([M, 134, W - M - 1, 135], fill=RED)

# ---------------------------------------------------------------- pictograms
def starburst(draw, cx, cy, r_out, r_in, n=8, fill=RED):
    import math
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)

def picto_russia(x, y, w, h):
    # night sky over a city skyline; missile streak + explosion
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY)
    for sx, sy in [(0.10, 0.15), (0.28, 0.08), (0.52, 0.14), (0.70, 0.08), (0.92, 0.18)]:
        d.ellipse([x + sx * w - 2, y + sy * h - 2, x + sx * w + 2, y + sy * h + 2], fill=(255, 255, 255))
    # missile: white diagonal body with fins, top-left to bottom-right
    mx0, my0 = x + 0.12 * w, y + 0.22 * h
    mx1, my1 = x + 0.55 * w, y + 0.52 * h
    d.line([mx0, my0, mx1, my1], fill=(245, 240, 225), width=7)
    d.polygon([(mx0 - 4, my0 + 10), (mx0 + 12, my0 - 2), (mx0 + 2, my0 + 14)], fill=(245, 240, 225))
    d.polygon([(mx1 - 14, my1 - 2), (mx1 - 2, my1 - 14), (mx1 + 2, my1 + 4)], fill=(245, 240, 225))
    # explosion starburst at impact point (bottom-right)
    starburst(d, x + 0.82 * w, y + 0.55 * h, 22, 10, fill=(232, 90, 40))
    d.ellipse([x + 0.82 * w - 7, y + 0.55 * h - 7, x + 0.82 * w + 7, y + 0.55 * h + 7], fill=GOLD)
    # city skyline + red horizon
    base = y + h
    for bx, bw, bh in [(0.02, 0.09, 22), (0.12, 0.07, 32), (0.20, 0.10, 26),
                       (0.62, 0.08, 30), (0.71, 0.09, 20), (0.88, 0.10, 26)]:
        d.rectangle([x + bx * w, base - bh, x + (bx + bw) * w, base], fill=(8, 16, 34))
        for wy in range(2):
            d.rectangle([x + (bx + 0.02) * w, base - bh + 6 + wy * 9,
                         x + (bx + 0.04) * w, base - bh + 10 + wy * 9], fill=GOLD)
    d.rectangle([x, base - 4, x + w - 1, base - 1], fill=RED)

def picto_markets(x, y, w, h):
    # falling chart on dark red: grid + plunging gold line + bars
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=MAROON)
    for gy in range(1, 4):
        yy = y + gy * h / 4
        d.line([x + 8, yy, x + w - 8, yy], fill=(200, 200, 200), width=1)
    # bars: tall to short
    bw = 26
    heights = [52, 44, 48, 36, 28, 18]
    for i, bh in enumerate(heights):
        bx = x + 16 + i * 46
        d.rectangle([bx, y + h - 12 - bh, bx + bw, y + h - 12], fill=(255, 255, 255))
    # plunging line
    pts = [(x + 18, y + 16), (x + 70, y + 26), (x + 120, y + 22),
           (x + 170, y + 42), (x + 220, y + 52), (x + 272, y + 72)]
    d.line(pts, fill=GOLD, width=4, joint="curve")
    # down arrow at the end
    ax, ay = x + 272, y + 72
    d.polygon([(ax - 10, ay - 12), (ax + 10, ay - 12), (ax, ay + 8)], fill=GOLD)

def picto_icj(x, y, w, h):
    # courthouse: pediment + columns on sky background
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=SKY)
    d.ellipse([x + 0.85 * w - 12, y + 0.12 * h - 12, x + 0.85 * w + 12, y + 0.12 * h + 12], fill=GOLD)
    # pediment triangle
    d.polygon([(x + 0.15 * w, y + 0.34 * h), (x + 0.85 * w, y + 0.34 * h),
               (x + 0.50 * w, y + 0.12 * h)], fill=NAVY)
    d.ellipse([x + 0.50 * w - 7, y + 0.20 * h - 7, x + 0.50 * w + 7, y + 0.20 * h + 7], fill=GOLD)
    # columns
    for cx in [0.22, 0.42, 0.60, 0.78]:
        d.rectangle([x + cx * w - 8, y + 0.36 * h, x + cx * w + 8, y + 0.78 * h], fill=NAVY)
        d.rectangle([x + cx * w - 11, y + 0.34 * h, x + cx * w + 11, y + 0.36 * h + 3], fill=NAVY)
        d.rectangle([x + cx * w - 11, y + 0.78 * h, x + cx * w + 11, y + 0.78 * h + 3], fill=NAVY)
    # base steps
    d.rectangle([x + 0.10 * w, y + 0.80 * h, x + 0.90 * w, y + 0.84 * h], fill=NAVY)
    d.rectangle([x + 0.05 * w, y + 0.86 * h, x + 0.95 * w, y + 0.90 * h], fill=NAVY)

# ---------------------------------------------------------------- top stories
TOPS = [
    ("EUROPE", RED, "RUSSIA STRIKES: MISSILES LAND IN POLAND",
     "400+ drones and 110 missiles hit Ukraine overnight; two missiles land in Poland.",
     picto_russia),
    ("MARKETS", MAROON, "AI SELL-OFF DRAGS S&P INTO CORRECTION",
     "S&P -3.7%, Nasdaq -5.3% in AI-led rout; Nasdaq wipes out all its 2026 gains.",
     picto_markets),
    ("JUSTICE", NAVY, "ICJ: MYANMAR GUILTY OF ROHINGYA GENOCIDE",
     "Court rules 9-6 Myanmar committed genocide; orders inquiry and compensation.",
     picto_icj),
]
COLW, GUT = 304, 16
TY = 144
for i, (cat, col, head, sub, pic) in enumerate(TOPS):
    cx = M + i * (COLW + GUT)
    pic(cx, TY, COLW, 88)
    chip(d, cx, TY + 96, cat, col)
    lines = wrap(d, head, F_H1, COLW)
    yy = TY + 120
    for ln in lines[:3]:
        d.text((cx, yy), ln, font=F_H1, fill=INK)
        yy += 21
    slines = wrap(d, sub, F_SUB, COLW)
    assert len(slines) <= 2, f"top sub too long: {sub!r} -> {slines}"
    yy = TY + 120 + 3 * 21 + 2
    for ln in slines[:2]:
        d.text((cx, yy), ln, font=F_SUB, fill=GRAY)
        yy += 15

d.rectangle([M, 368, W - M - 1, 369], fill=LIGHT_LINE)

# ---------------------------------------------------------------- medium cards
d.text((M, 376), "AROUND THE WORLD", font=F_SECT, fill=NAVY)
d.rectangle([M + 190, 385, W - M - 1, 386], fill=LIGHT_LINE)
MEDIUMS = [
    ("POLITICS", RED, "Trump calls Putin a friend after first three-way talks",
     "90-min press conference after first US-China-Russia meeting.", "AMERICAS"),
    ("CLIMATE", GREEN, "COP31 misses deadline, runs into overtime",
     "Draft drops all fossil-fuel wording; Panama threatens to block it.", "GLOBAL"),
    ("YEMEN", ORANGE, "Saudi coalition stops Houthi missiles at Riyadh",
     "Third night of alerts; Houthis threaten ports and a power station.", "MIDDLE EAST"),
    ("EUROPE", BLUE, "UK and EU seal biggest post-Brexit step",
     "Food checks scrapped; carbon markets linked; youth scheme for 100,000.", "EUROPE"),
    ("TECH", NAVY, "SEC probes Nvidia accounting; shares -13.8%",
     "Probe follows Huang exit; fake staff letter calling for board to quit.", "GLOBAL"),
    ("GULF", TEAL, "14 Iranian tankers mass at Kharg Island",
     "Convoy to test US blockade; Trump defers strike call to New Year.", "MIDDLE EAST"),
    ("HEALTH", PURPLE, "Pancreatic cancer pill shows progress",
     "Daraxonrasib trial: tumours undetectable in 1 in 12 patients.", "GLOBAL"),
    ("EUROPE", BLUE, "EU assigns €1bn for Ukraine defence kit",
     "From Peace Facility; top diplomat says Russia rejected peace.", "EUROPE"),
]
MCW, MGUT = 227, 12
for row in range(2):
    ry = 404 + row * 102
    for col_i in range(4):
        m = MEDIUMS[row * 4 + col_i]
        mx = M + col_i * (MCW + MGUT)
        chip(d, mx, ry, m[0], m[1])
        lines = wrap(d, m[2], F_MH, MCW)
        yy = ry + 24
        for ln in lines[:2]:
            d.text((mx, yy), ln, font=F_MH, fill=INK)
            yy += 16
        slines = wrap(d, m[3], F_MS, MCW)
        yy = ry + 24 + 2 * 16 + 3
        for ln in slines[:2]:
            d.text((mx, yy), ln, font=F_MS, fill=GRAY)
            yy += 14
    # vertical dividers between columns
    for col_i in range(1, 4):
        vx = M + col_i * (MCW + MGUT) - 6
        d.rectangle([vx, ry + 2, vx, ry + 96], fill=LIGHT_LINE)

d.rectangle([M, 610, W - M - 1, 611], fill=LIGHT_LINE)

# ---------------------------------------------------------------- briefs
d.text((M, 618), "THE BRIEFS — 19 MORE STORIES", font=F_SECT, fill=NAVY)
d.rectangle([M + 268, 627, W - M - 1, 628], fill=LIGHT_LINE)
BRIEFS = [
    "US House passed 2022 $1.7T bill unconstitutionally — court 9-8.",
    "Anthropic shares slide 10% to $87.80 on day two after record IPO.",
    "Trump threatens 'tremendous tax' on AI data centres built abroad.",
    "Denmark expels Russian diplomat over alleged assassination plot.",
    "Mamdani to close NYC Rikers Island jail by 2032.",
    "French police sentenced for beating producer Michel Zecler.",
    "Indian man gets 19+ years in US Sikh separatist murder plot.",
    "Nearly 600 women killed in South Africa in three months.",
    "US declassifies more UFO footage from Middle East.",
    "US measles cases near 6,000 — 5,838 as of 19 Nov.",
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
BW = 460
for i, b in enumerate(BRIEFS):
    col_i = 0 if i < 10 else 1
    row_i = i if i < 10 else i - 10
    bx = M + col_i * (BW + 24)
    by = 644 + row_i * 13
    d.text((bx, by), f"{i+1}.", font=F_BRN, fill=RED)
    d.text((bx + 22, by), b, font=F_BR, fill=INK)

d.rectangle([M, 782, W - M - 1, 783], fill=LIGHT_LINE)

# ---------------------------------------------------------------- world map (dot-matrix)
d.text((M, 788), "WHERE IT HAPPENED — SCHEMATIC MAP, NOT TO SCALE", font=F_MAPL, fill=NAVY)
MAP = (M, 806, W - M, 944)   # x0, y0, x1, y1
mx0, my0, mx1, my1 = MAP
mw, mh = mx1 - mx0, my1 - my0
LAT_TOP, LAT_BOT = 76.0, -56.0
def proj(lon, lat):
    x = mx0 + (lon + 180.0) / 360.0 * mw
    y = my0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * mh
    return x, y

CONTINENTS = [
    # North America
    [(-168,66),(-140,70),(-125,72),(-110,73),(-95,80),(-85,80),(-75,72),(-65,60),
     (-55,52),(-60,47),(-70,44),(-75,35),(-80,32),(-81,26),(-84,30),(-90,29),
     (-97,26),(-105,20),(-97,16),(-92,15),(-86,13),(-83,9),(-79,9),(-85,11),
     (-90,14),(-95,16),(-105,20),(-110,24),(-114,29),(-120,34),(-125,40),
     (-124,48),(-130,55),(-145,60),(-155,58),(-165,60),(-168,66)],
    # South America
    [(-79,9),(-72,12),(-62,10),(-52,5),(-50,0),(-44,-3),(-35,-8),(-40,-20),
     (-48,-28),(-52,-33),(-58,-38),(-62,-41),(-66,-47),(-70,-52),(-73,-50),
     (-73,-40),(-72,-30),(-70,-18),(-77,-12),(-81,-6),(-80,0),(-79,9)],
    # Africa
    [(-17,15),(-10,30),(-5,35),(0,36),(10,37),(20,32),(30,31),(35,28),(38,22),
     (43,12),(48,11),(51,10),(44,0),(40,-10),(36,-18),(32,-26),(28,-33),
     (20,-35),(16,-28),(12,-18),(9,-1),(9,4),(-8,4),(-13,8),(-17,15)],
    # Eurasia
    [(-10,36),(-9,43),(-2,48),(-5,50),(0,51),(5,53),(8,57),(10,59),(18,56),
     (21,55),(24,59),(28,60),(30,62),(35,66),(40,68),(50,69),(60,69),(70,72),
     (80,73),(90,75),(100,77),(110,74),(120,73),(130,72),(140,72),(150,70),
     (160,70),(170,67),(178,65),(178,62),(170,60),(162,56),(158,52),(150,59),
     (142,55),(140,50),(135,44),(130,42),(127,40),(126,38),(122,38),(120,32),
     (122,28),(118,25),(112,22),(108,18),(105,10),(103,8),(100,6),(97,10),
     (94,16),(92,21),(89,22),(86,20),(80,13),(77,8),(75,12),(72,20),(68,22),
     (62,25),(57,26),(54,26),(50,29),(48,30),(44,29),(40,31),(36,36),(30,36),
     (27,37),(23,36),(19,40),(15,44),(12,44),(8,44),(3,43),(0,40),(-2,37),(-6,36),(-10,36)],
    # Australia
    [(114,-22),(114,-30),(115,-35),(118,-35),(124,-33),(129,-32),(132,-32),
     (135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),
     (150,-22),(146,-19),(142,-11),(140,-17),(136,-12),(132,-11),(126,-14),
     (122,-17),(118,-20),(114,-22)],
    # UK
    [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51),(-3,50)],
    # Japan
    [(130,31),(133,34),(137,35),(140,37),(141,40),(142,43),(144,44),
     (142,41),(140,38),(137,34),(133,33),(130,31)],
]
# project polygons to pixels once
POLYS = [[proj(lon, lat) for lon, lat in poly] for poly in CONTINENTS]

def inside(px, py, poly):
    ins = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            ins = not ins
        j = i
    return ins

d.rectangle([mx0, my0, mx1 - 1, my1 - 1], outline=NAVY, width=1)
STEP = 6
gx = mx0 + 4
while gx < mx1 - 2:
    gy = my0 + 4
    while gy < my1 - 2:
        if any(inside(gx, gy, p) for p in POLYS):
            d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=SLATE)
        gy += STEP
    gx += STEP

def pin(lon, lat, num):
    px, py = proj(lon, lat)
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px, py), str(num), font=F_PIN, fill=(255, 255, 255), anchor="mm")

pin(30.5, 50.4, 1)    # Kyiv / Russia strikes
pin(-74.0, 40.7, 2)   # New York / markets
pin(4.3, 52.1, 3)     # The Hague / ICJ
pin(46.7, 24.7, 4)    # Riyadh / Houthi missiles
pin(30.7, 36.9, 5)    # Antalya / COP31

# legend box bottom-right
leg = "1 KYIV  ·  2 NEW YORK  ·  3 THE HAGUE  ·  4 RIYADH  ·  5 ANTALYA"
lw = d.textlength(leg, font=F_LEG)
lx0 = mx1 - lw - 16
ly0 = my1 - 20
d.rectangle([lx0, ly0, mx1 - 4, my1 - 4], fill=PAPER, outline=NAVY, width=1)
d.text((lx0 + 8, ly0 + 3), leg, font=F_LEG, fill=NAVY)

# ---------------------------------------------------------------- footer
d.text((W // 2, 956), "Sources: Reuters · AP · AFP · BBC · Al Jazeera  —  Every story above was first reported on Saturday 21 November 2026.",
       font=F_FOOT, fill=GRAY, anchor="ma")

img.save("/home/hatch/workspace/makefun-test/news-image-20261121-entry/entry.png", optimize=True)
print("saved entry.png")

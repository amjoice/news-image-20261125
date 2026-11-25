#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261125.

Build-time only. Uses Pillow locally; the shipped main.py is stdlib-only
and never imports PIL. Output: 1024x1024 front-page infographic summing up
the world news of Wednesday 25 November 2026, as reported that day.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (163, 22, 33)
NAVY = (29, 53, 87)
NAVY_DARK = (16, 34, 60)
NAVY_LIGHT = (52, 88, 130)
TEAL = (36, 102, 96)
GOLD = (176, 132, 52)
PURPLE = (74, 52, 96)
WHITE = (255, 255, 255)
MUTED = (96, 91, 82)
PANEL_LINE = (120, 114, 100)
SEA = (44, 96, 138)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def burst(draw, cx, cy, r, fill):
    """Explosion starburst: 12 spikes."""
    import math
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_ship(draw, x, y, s, hull, deck, smoke=True):
    """Simple cargo ship silhouette, s = hull length."""
    h = int(s * 0.32)
    draw.polygon([(x, y), (x + s, y), (x + s * 0.88, y + h),
                  (x + s * 0.12, y + h)], fill=hull)
    draw.rectangle([x + s * 0.18, y - h * 0.55, x + s * 0.42, y], fill=deck)
    draw.rectangle([x + s * 0.58, y - h * 0.35, x + s * 0.72, y], fill=deck)
    draw.line([x + s * 0.30, y - h * 0.55, x + s * 0.30, y - h * 1.05],
              fill=deck, width=3)
    if smoke:
        for dx, dy, r in ((0.62, -0.62, 7), (0.68, -0.80, 9), (0.75, -0.95, 7)):
            draw.ellipse([x + s * dx - r, y + h * dy - r,
                          x + s * dx + r, y + h * dy + r],
                         fill=(220, 222, 224))


def draw_tower(draw, x, y, w, h, fill):
    """Skyscraper with setbacks and antenna."""
    draw.rectangle([x, y + h * 0.25, x + w, y + h], fill=fill)
    draw.rectangle([x + w * 0.14, y + h * 0.12, x + w * 0.86, y + h * 0.25],
                   fill=fill)
    draw.rectangle([x + w * 0.32, y, x + w * 0.68, y + h * 0.12], fill=fill)
    draw.line([x + w * 0.5, y - h * 0.14, x + w * 0.5, y], fill=fill, width=3)
    for row in range(6):
        yy = y + h * (0.32 + row * 0.11)
        for col in range(3):
            xx = x + w * (0.22 + col * 0.28)
            draw.rectangle([xx, yy, xx + w * 0.12, yy + h * 0.05],
                           fill=(247, 242, 231))


def draw_chip(draw, cx, cy, s, fill):
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                   fill=fill)
    draw.rectangle([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4],
                   outline=(247, 242, 231), width=2)
    for i in range(-1, 2):
        off = i * s // 3
        draw.line([cx + off, cy - s // 2 - 8, cx + off, cy - s // 2],
                  fill=fill, width=3)
        draw.line([cx + off, cy + s // 2, cx + off, cy + s // 2 + 8],
                  fill=fill, width=3)
        draw.line([cx - s // 2 - 8, cy + off, cx - s // 2, cy + off],
                  fill=fill, width=3)
        draw.line([cx + s // 2, cy + off, cx + s // 2 + 8, cy + off],
                  fill=fill, width=3)


def draw_chart(draw, x, y, w, h, fill):
    draw.line([x, y + h, x + w, y + h], fill=(150, 146, 136), width=2)
    draw.line([x, y, x, y + h], fill=(150, 146, 136), width=2)
    pts = [(x + 6, y + h * 0.30), (x + w * 0.30, y + h * 0.38),
           (x + w * 0.55, y + h * 0.22), (x + w * 0.78, y + h * 0.72),
           (x + w - 6, y + h * 0.85)]
    draw.line(pts, fill=fill, width=4, joint="curve")
    draw.polygon([(x + w - 6, y + h * 0.85), (x + w - 18, y + h * 0.85 - 2),
                  (x + w - 12, y + h * 0.85 + 12)], fill=fill)


def draw_tanker(draw, x, y, s, fill):
    h = int(s * 0.26)
    draw.polygon([(x, y), (x + s, y), (x + s * 0.90, y + h),
                  (x + s * 0.10, y + h)], fill=fill)
    for i, col in enumerate(((176, 132, 52), (163, 22, 33), (36, 102, 96))):
        draw.rectangle([x + s * (0.16 + i * 0.20), y - h * 0.62,
                        x + s * (0.32 + i * 0.20), y - 2], fill=col)
    draw.rectangle([x + s * 0.78, y - h * 0.55, x + s * 0.92, y], fill=INK)


def draw_mine(draw, cx, cy, r, fill):
    import math
    for i in range(8):
        ang = math.pi * i / 4
        x2, y2 = cx + (r + 7) * math.cos(ang), cy + (r + 7) * math.sin(ang)
        draw.line([cx, cy, x2, y2], fill=fill, width=3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def draw_satellite(draw, cx, cy, s, fill):
    draw.ellipse([cx - s, cy - s * 0.62, cx + s, cy + s * 0.62],
                 outline=(150, 146, 136), width=2)
    draw.rectangle([cx - s * 0.62, cy - 8, cx - s * 0.16, cy + 8], fill=fill)
    draw.rectangle([cx + s * 0.16, cy - 8, cx + s * 0.62, cy + 8], fill=fill)
    for xx in (cx - s * 0.62, cx + s * 0.16):
        for k in range(3):
            draw.line([xx + k * s * 0.15, cy - 8, xx + k * s * 0.15, cy + 8],
                      fill=(247, 242, 231), width=1)
    draw.rectangle([cx - 9, cy - 13, cx + 9, cy + 13], fill=(163, 22, 33))
    draw.line([cx + 4, cy - 22, cx + 14, cy - 32], fill=fill, width=2)
    draw.ellipse([cx + 11, cy - 35, cx + 17, cy - 29], fill=fill)


def draw_radar(draw, cx, cy, r, fill):
    import math
    for rr in (r, r * 0.66, r * 0.33):
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], 200, 340,
                 fill=fill, width=2)
    draw.line([cx, cy, cx + r * 0.8, cy - r * 0.6], fill=fill, width=2)
    draw.ellipse([cx + r * 0.45 - 4, cy - r * 0.35 - 4,
                  cx + r * 0.45 + 4, cy - r * 0.35 + 4], fill=(163, 22, 33))
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=fill)


def panel(draw, x, y, w, h, kicker, kcolor, headline, body, icon):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE,
                   outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 5], fill=kcolor)
    pad = 16
    tx, ty = x + pad, y + 16
    icon(draw, x + w - 74, ty + 2)
    draw.text((tx, ty), kicker, font=SANS_B(15), fill=kcolor)
    ty += 24
    hl = wrap(draw, headline, SANS_B(21), w - pad * 2 - 62)
    ty = text_block(draw, tx, ty, hl, SANS_B(21), INK, 25)
    ty += 6
    bl = wrap(draw, body, SANS(15), w - pad * 2)
    text_block(draw, tx, ty, bl, SANS(15), (52, 50, 46), 20)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28

    # ---- Masthead ----
    d.rectangle([M, 14, W - M, 18], fill=RED)
    title = "THE WORLD TODAY"
    tf = SERIF_B(62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 26), title,
           font=tf, fill=INK)
    date = "WEDNESDAY  ·  25 NOVEMBER 2026"
    df = SANS_B(26)
    d.text(((W - d.textlength(date, font=df)) / 2, 100), date,
           font=df, fill=RED)
    d.rectangle([M, 134, W - M, 137], fill=INK)
    d.rectangle([M, 140, W - M, 141], fill=INK)

    # ---- Hero: Ukraine ----
    hx, hy, hw, hh = M, 152, W - 2 * M, 300
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=NAVY)
    d.rectangle([hx, hy, hx + hw, hy + 4], fill=RED)
    tx = hx + 26
    d.text((tx, hy + 20), "UKRAINE  —  THE WAR WIDENS", font=SANS_B(19),
           fill=GOLD)
    head = wrap(d, "Ukraine strikes Russian ships far beyond the front",
                SANS_B(37), 560)
    y = text_block(d, tx, hy + 52, head, SANS_B(37), WHITE, 44)
    body = ("Kyiv says it hit a Russian cargo ship in the Gulf of "
            "Finland — and sank a Russian warship off Benghazi, Libya. "
            "A new analysis puts Russian military deaths above 700,000.")
    bl = wrap(d, body, SANS(19), 560)
    text_block(d, tx, y + 12, bl, SANS(19), (222, 226, 232), 25)

    # Hero illustration: sea, two ships, blasts, route arc
    sx, sy, sw, sh = hx + 620, hy + 30, 322, 240
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=NAVY_DARK)
    for wy in (sy + 150, sy + 185, sy + 218):
        for wx in range(sx + 8, sx + sw - 8, 26):
            d.arc([wx, wy, wx + 22, wy + 12], 180, 360,
                  fill=NAVY_LIGHT, width=2)
    draw_ship(d, sx + 24, sy + 118, 120, (222, 226, 232), (176, 132, 52))
    burst(d, sx + 168, sy + 92, 26, (232, 164, 60))
    burst(d, sx + 168, sy + 92, 13, (163, 22, 33))
    draw_ship(d, sx + 178, sy + 168, 118, (180, 186, 194), (120, 128, 138))
    burst(d, sx + 268, sy + 142, 20, (232, 164, 60))
    d.arc([sx + 60, sy + 30, sx + 260, sy + 150], 200, 340,
          fill=(232, 164, 60), width=2)
    lf = SANS_B(13)
    d.text((sx + 12, sy + 8), "GULF OF FINLAND", font=lf,
           fill=(222, 226, 232))
    d.text((sx + 176, sy + 214), "BENGHAZI, LIBYA", font=lf,
           fill=(222, 226, 232))

    # ---- Story rows ----
    cols = [M, 355, 682]
    pw = 314
    row1 = [
        ("RIYADH", RED, "Houthi strike hits Riyadh's tallest tower",
         "Second hit in five days on the PIF Tower; 11 people hurt. "
         "Houthi fighters are now 60 km from Aden.",
         lambda dr, x, y: draw_tower(dr, x + 8, y + 4, 40, 56, RED)),
        ("HUAWEI", NAVY, "Huawei convicted in US trial",
         "A New York jury finds the Chinese telecoms giant guilty of "
         "trade-secret conspiracy and bank fraud.",
         lambda dr, x, y: draw_chip(dr, x + 30, y + 30, 44, NAVY)),
        ("MARKETS", TEAL, "Nvidia slides 7%",
         "Shares fall a day after Jensen Huang's return as chief "
         "executive. Dell lifts its outlook on booming AI-server demand.",
         lambda dr, x, y: draw_chart(dr, x + 4, y + 8, 58, 46, TEAL)),
    ]
    row2 = [
        ("STRAIT OF HORMUZ", NAVY, "Tankers hit by mines in Hormuz",
         "Iran says three tankers were struck by naval mines; oil "
         "traffic through the strait is down 40%.",
         lambda dr, x, y: (draw_tanker(dr, x + 2, y + 22, 56, NAVY),
                           draw_mine(dr, x + 62, y + 12, 7, RED))),
        ("SPACE", PURPLE, "Fears of a nuclear satellite",
         "Western intelligence warns Russia may orbit a nuclear-armed "
         "satellite. NATO vows to defend space.",
         lambda dr, x, y: draw_satellite(dr, x + 32, y + 32, 30, PURPLE)),
        ("POLAND", RED, "Russian drone over Poland",
         "Warsaw calls the incursion deliberate. NATO will deploy "
         "early-warning aircraft to Poland.",
         lambda dr, x, y: draw_radar(dr, x + 32, y + 32, 28, RED)),
    ]
    y1, y2, ph = 464, 700, 224
    for (x, (kick, col, head, body, icon)) in zip(cols, row1):
        panel(d, x, y1, pw, ph, kick, col, head, body, icon)
    for (x, (kick, col, head, body, icon)) in zip(cols, row2):
        panel(d, x, y2, pw, 208, kick, col, head, body, icon)

    # ---- Ticker ----
    ty = 914
    d.rectangle([M, ty, W - M, ty + 96], fill=RED)
    d.text((M + 18, ty + 10), "ALSO TODAY", font=SANS_B(18), fill=WHITE)
    items = ("CIA and the spy chief's office hit by cyber breach  •  "
             "Trump awards Giuliani the Medal of Freedom  •  "
             "Nepal quake, magnitude 5.6  •  "
             "Sarkozy case sent to trial  •  "
             "Gaza strikes kill a Hamas security chief  •  "
             "England beat Australia in the T20I")
    tl = wrap(d, items, SANS(15), W - 2 * M - 36)
    text_block(d, M + 18, ty + 36, tl, SANS(15), WHITE, 19)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()

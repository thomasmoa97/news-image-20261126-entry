#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024).

Every story was verified against reporting dated Thursday 26 November 2026:
hero Kim Jong Un tactical-nukes call (KCNA, reported 26 Nov); the Thanksgiving
nor'easter hitting the US East Coast on 26 Nov; the overnight Saudi
interceptions of Houthi missiles (announced 26 Nov); Brent crude topping $94
on 26 Nov; Australia's Q3 capex release on 26 Nov; the Bank of Japan's Tamura
signalling faster hikes on 26 Nov. No story from 24/25 November is used.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
PATH = os.path.join(OUT, "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


NAVY = (19, 42, 68)
GOLD = (201, 162, 39)
CREAM = (247, 243, 234)
INK = (34, 32, 28)
MUTED = (90, 86, 76)
RED = (163, 22, 33)
HERO_BG = (74, 13, 13)
HERO_BG2 = (46, 6, 6)
TILE_BG = (255, 255, 255)
BORDER = (216, 210, 196)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# ---- masthead -------------------------------------------------------------
d.rectangle([0, 0, W, 110], fill=NAVY)
d.rectangle([0, 110, W, 114], fill=GOLD)
name_f = font(SERIF_B, 54)
d.text((W // 2, 12), "THE WORLD TODAY", font=name_f, fill=(255, 255, 255),
       anchor="ma")
date_f = font(SANS_B, 24)
d.text((W // 2, 78), "THURSDAY, 26 NOVEMBER 2026", font=date_f,
       fill=GOLD, anchor="ma")

# ---- hero: Kim / tactical nukes -------------------------------------------
d.rectangle([0, 114, W, 460], fill=HERO_BG)
d.rectangle([0, 400, W, 460], fill=HERO_BG2)
# atom emblem, right side
cx, cy = 880, 255
for angle in (0, 60, 120):
    orb = Image.new("RGBA", (260, 260), (0, 0, 0, 0))
    od = ImageDraw.Draw(orb)
    od.ellipse([30, 95, 230, 165], outline=GOLD, width=5)
    orb = orb.rotate(angle, resample=Image.BICUBIC, center=(130, 130))
    img.paste(orb, (cx - 130, cy - 130), orb)
d = ImageDraw.Draw(img)
d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=GOLD)
d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=HERO_BG)

kick_f = font(SANS_B, 17)
head_f = font(SERIF_B, 46)
sub_f = font(SANS, 21)
d.text((36, 138), "ASIA  •  NORTH KOREA", font=kick_f, fill=GOLD)
hero_lines = ["KIM ORDERS WIDER", "USE OF TACTICAL", "NUKES"]
y = 168
for line in hero_lines:
    d.text((36, y), line, font=head_f, fill=(255, 255, 255))
    y += 56
sub = wrap(d, "Leader tours nuclear sites as KCNA declares the arsenal "
              "'absolutely inviolable'", sub_f, 560)
y = 348
for line in sub:
    d.text((36, y), line, font=sub_f, fill=(232, 214, 190))
    y += 27

# ---- story tiles ----------------------------------------------------------
tile_kick = font(SANS_B, 15)
tile_head = font(SANS_B, 24)
tile_body = font(SANS, 18)

tiles = [
    # (x, y, w, h, kicker, headline, body, icon)
    (16, 472, 488, 164, "USA  •  WEATHER",
     "NOR'EASTER SLAMS THANKSGIVING",
     "Macy's 100th parade postponed to Saturday as storm hits US East Coast", "storm"),
    (520, 472, 488, 164, "MIDDLE EAST  •  RED SEA",
     "MISSILES AIMED AT RIYADH INTERCEPTED",
     "Saudi downs Houthi missiles overnight; Jazan port hit, Jeddah drone downed", "shield"),
    (16, 648, 488, 164, "MARKETS  •  ENERGY",
     "OIL JUMPS AS RED SEA ATTACKS SPREAD",
     "Brent crude tops $94 a barrel after Houthi strikes on Saudi ports",
     "flame"),
    (520, 648, 488, 164, "AUSTRALIA  •  ECONOMY",
     "BUSINESS SPENDING SURGES 12.2%",
     "Biggest quarterly rise since 2011, led by data-centre investment", "chart"),
    (16, 824, 992, 164, "JAPAN  •  CENTRAL BANK",
     "BANK OF JAPAN SIGNALS FASTER RATE HIKES",
     "Board member Tamura says the BOJ must act swiftly if inflation "
     "overshoots — bolstering the case for a December move", "yen"),
]


def icon(draw, kind, x, y):
    if kind == "storm":  # rain cloud
        draw.ellipse([x, y, x + 44, y + 30], fill=(90, 110, 140))
        draw.ellipse([x + 26, y - 12, x + 70, y + 22], fill=(90, 110, 140))
        draw.rectangle([x, y + 14, x + 70, y + 32], fill=(90, 110, 140))
        for i, rx in enumerate((x + 10, x + 34, x + 58)):
            draw.line([(rx, y + 42), (rx - 5, y + 56)], fill=RED, width=4)
    elif kind == "shield":
        draw.polygon([(x + 35, y), (x + 70, y + 12), (x + 70, y + 40),
                      (x + 35, y + 62), (x, y + 40), (x, y + 12)],
                     outline=RED, width=5)
        draw.line([(x + 18, y + 32), (x + 30, y + 44), (x + 54, y + 20)],
                  fill=RED, width=5)
    elif kind == "flame":
        draw.polygon([(x + 35, y), (x + 58, y + 26), (x + 66, y + 48),
                      (x + 44, y + 64), (x + 18, y + 64), (x + 6, y + 48),
                      (x + 14, y + 26)], fill=(224, 122, 26))
        draw.ellipse([x + 24, y + 34, x + 46, y + 58], fill=(247, 201, 72))
    elif kind == "chart":
        for i, hgt in enumerate((18, 34, 50, 64)):
            draw.rectangle([x + i * 18, y + 64 - hgt, x + i * 18 + 12, y + 64],
                           fill=NAVY)
        draw.line([(x, y), (x + 70, y - 6)], fill=RED, width=4)
    elif kind == "yen":
        yf = font(SANS_B, 52)
        draw.text((x + 35, y + 32), "¥", font=yf, fill=NAVY, anchor="ma")


for (tx, ty, tw, th, kicker, headline, body, ic) in tiles:
    d.rectangle([tx, ty, tx + tw, ty + th], fill=TILE_BG, outline=BORDER,
                width=2)
    d.rectangle([tx, ty, tx + tw, ty + 5], fill=RED)
    ix = tx + 22
    icon(d, ic, ix, ty + 52)
    text_x = tx + 112 if tw < 900 else tx + 118
    max_w = tw - (text_x - tx) - 20
    d.text((text_x, ty + 16), kicker, font=tile_kick, fill=RED)
    head_lines = wrap(d, headline, tile_head, max_w)
    y = ty + 40
    for line in head_lines:
        d.text((text_x, y), line, font=tile_head, fill=INK)
        y += 29
    for line in wrap(d, body, tile_body, max_w):
        d.text((text_x, y), line, font=tile_body, fill=MUTED)
        y += 23

# ---- footer ---------------------------------------------------------------
foot_f = font(SANS_B, 16)
d.text((W // 2, 1006),
       "26 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE",
       font=foot_f, fill=MUTED, anchor="ma")

img.save(PATH, "PNG", optimize=True)
print("wrote", PATH)

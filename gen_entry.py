"""ai-happy-01 v4: Mimi the mouse baker — hand-lettered note, warm kitchen light.

Craft upgrades over v3: per-glyph handwriting jitter, paper grain, warm
radial golden light, soft contact shadows, rounder cleaner typography,
larger character with gradient-shaded body.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
import random

S = 4
W = H = 1024
WBig, HBig = W * S, H * S
rng = random.Random(7)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


img = Image.new("RGB", (WBig, HBig))
d = ImageDraw.Draw(img)

# --- wall: warm cream gradient ---------------------------------------------
top = (247, 221, 186)
bot = (236, 194, 150)
for y in range(HBig):
    t = y / (HBig - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    d.line([(0, y), (WBig, y)], fill=c)

# --- warm golden radial light from upper left ------------------------------
light = Image.new("L", (WBig, HBig), 0)
ld = ImageDraw.Draw(light)
cx, cy = int(0.18 * WBig), int(0.08 * HBig)
for r in range(int(1.3 * WBig), 0, -12):
    a = int(90 * (1 - r / (1.3 * WBig)) ** 1.6)
    ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
glow = Image.new("RGB", (WBig, HBig), (255, 236, 200))
img = Image.composite(glow, img, light)
d = ImageDraw.Draw(img)

# --- floor -----------------------------------------------------------------
floor_y = int(0.80 * HBig)
d.rectangle([0, floor_y, WBig, HBig], fill=(196, 148, 108))
d.rectangle([0, floor_y, WBig, floor_y + 8 * S], fill=(168, 122, 86))
for x in range(int(0.1 * WBig), WBig, int(0.22 * WBig)):
    d.line([(x, floor_y + 10 * S), (x - 30 * S, HBig)], fill=(178, 132, 96), width=3 * S)

# --- paper note (taped to wall), slight tilt -------------------------------
paper = Image.new("RGBA", (int(0.58 * W) * S, int(0.55 * H) * S), (0, 0, 0, 0))
pd = ImageDraw.Draw(paper)
pd.rounded_rectangle([0, 0, paper.width - 1, paper.height - 1],
                     radius=12 * S, fill=(255, 251, 240),
                     outline=(216, 190, 154), width=3 * S)
for _ in range(2600):
    px = rng.randint(4, paper.width - 5)
    py = rng.randint(4, paper.height - 5)
    g = rng.randint(228, 244)
    pd.point((px, py), fill=(g, g, int(g * 0.97), 255))
for j in range(1, 12):
    ly = int(j * paper.height / 13)
    pd.line([(26 * S, ly), (paper.width - 26 * S, ly)], fill=(222, 202, 176),
            width=2 * S)
pd.line([(52 * S, 14 * S), (52 * S, paper.height - 14 * S)],
        fill=(226, 150, 140), width=2 * S)
for (tx0, ty0, ang) in [(18, 14, -25), (paper.width - 130, 12, 20)]:
    tape = Image.new("RGBA", (120 * S, 34 * S), (250, 226, 160, 215))
    tape = tape.rotate(ang, expand=True)
    paper.alpha_composite(tape, (tx0 * S, ty0 * S))


# --- hand-lettered text: per-glyph jitter + rotation ------------------------
def hand_text(draw_layer, xy, text, size, fill=(70, 52, 46), spacing=1.0):
    """Draw text glyph-by-glyph with tiny jitter so it reads as handwritten."""
    x, y = xy
    f = ImageFont.truetype(FONT_PATH, size)
    wob = max(3, size // 12)
    base_y = y
    for ch in text:
        if ch == " ":
            x += size * 0.34
            continue
        jx = rng.randint(-wob, wob)
        jy = rng.randint(-wob, wob) + int(base_y - y) + rng.randint(-2, 2)
        y += rng.uniform(-0.9, 0.9) * size / 40   # gentle baseline drift
        rot = rng.uniform(-5.0, 5.0)
        pad = size // 2 + 8
        cw = int(size * 0.72) + 2 * pad
        chh = size + 2 * pad
        tile = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.text((pad, pad), ch, font=f, fill=fill + (255,))
        tile = tile.rotate(rot, resample=Image.BICUBIC, center=(cw / 2, chh / 2))
        draw_layer.alpha_composite(tile, (int(x) + jx, int(y) + jy))
        adv = f.getlength(ch)
        x += adv * spacing + size * 0.015
    return x


ink = (72, 54, 48)
ink_soft = (100, 78, 66)
tx, ty = 88 * S, 44 * S
lh = int(34 * S)

hand_text(paper, (tx, ty), "Dear Judge,", 30 * S, ink)
hand_text(paper, (tx + 12 * S, ty + lh), "i baked you a cake.", 21 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 2 * lh), "it is still warm.", 21 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 3 * lh), "i kept it safe the", 21 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 4 * lh), "whole way here.", 21 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 5 * lh), "sorry i am small.", 17 * S, ink_soft)
hand_text(paper, (tx + 12 * S, ty + 7 * lh), "Love, Mimi", 22 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 9 * lh), "p.s. i ate a corner.", 16 * S, ink_soft)

paper = paper.rotate(-2.2, resample=Image.BICUBIC, expand=True)

# soft drop shadow for the note
shadow = Image.new("RGBA", (paper.width + 60 * S, paper.height + 60 * S), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([40 * S, 40 * S, shadow.width - 20 * S, shadow.height - 20 * S],
                     radius=14 * S, fill=(90, 60, 30, 60))
shadow = shadow.filter(ImageFilter.GaussianBlur(6 * S))
img.paste(Image.new("RGB", shadow.size, (0, 0, 0)), (int(0.055 * WBig), int(0.06 * HBig)), shadow.split()[3])
img.paste(paper.convert("RGB"), (int(0.055 * WBig), int(0.06 * HBig)), paper.split()[3])
d = ImageDraw.Draw(img)

img.save("/home/agentuser/makefun/tea-with-tiara/stage1.png")

# --- Mimi the mouse baker, larger, gradient-shaded -------------------------
mx, my = int(0.72 * WBig), floor_y  # feet at floor line
body_c1 = (154, 132, 126)
body_c2 = (176, 156, 148)

body = Image.new("RGBA", (int(0.34 * W) * S, int(0.44 * H) * S), (0, 0, 0, 0))
bd = ImageDraw.Draw(body)
bw, bh = body.size
for i in range(bh):
    t = i / bh
    c = tuple(int(body_c1[k] + (body_c2[k] - body_c1[k]) * t) for k in range(3))
    bd.line([(0, i), (bw, i)], fill=c)
mask = Image.new("L", (bw, bh), 0)
md = ImageDraw.Draw(mask)
md.ellipse([bw // 2 - int(bw * 0.30), int(bh * 0.42), bw // 2 + int(bw * 0.30), bh - 1], fill=255)
img.paste(body.convert("RGB"), (mx - bw // 2, my - bh), mask)

d = ImageDraw.Draw(img)

# feet
for sx in (-1, 1):
    fx = mx + sx * int(0.055 * WBig)
    d.ellipse([fx - 20 * S, my - 26 * S, fx + 20 * S, my + 4 * S], fill=(150, 128, 122))

# head
hx, hy = mx, my - int(0.335 * HBig)
hr = int(0.085 * WBig)
d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(168, 148, 142))
d.ellipse([hx - int(hr * 0.62), hy - int(hr * 0.30),
           hx + int(hr * 0.62), hy + int(hr * 0.72)], fill=(228, 208, 198))

# ears
for sx in (-1, 1):
    ex = hx + sx * int(hr * 0.92)
    ey = hy - int(hr * 0.85)
    er = int(hr * 0.52)
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(158, 138, 132))
    d.ellipse([ex - int(er * 0.55), ey - int(er * 0.5), ex + int(er * 0.55), ey + int(er * 0.5)],
              fill=(244, 198, 196))

# happy closed eyes + cheeks + smile
for sx in (-1, 1):
    exy = hx + sx * int(hr * 0.40)
    eyy = hy - int(hr * 0.12)
    d.arc([exy - 16 * S, eyy - 16 * S, exy + 16 * S, eyy + 16 * S],
          start=200, end=340, fill=(60, 44, 40), width=int(3.2 * S))
    chx = hx + sx * int(hr * 0.62)
    chy = hy + int(hr * 0.28)
    chr_ = int(hr * 0.20)
    d.ellipse([chx - chr_, chy - chr_, chx + chr_, chy + chr_], fill=(238, 168, 160))
d.ellipse([hx - 8 * S, hy + int(hr * 0.18), hx + 8 * S, hy + int(hr * 0.34)],
          fill=(96, 74, 70))
d.arc([hx - 22 * S, hy + int(hr * 0.10), hx + 22 * S, hy + int(hr * 0.62)],
      start=20, end=160, fill=(96, 74, 70), width=int(3 * S))
for sy in (-0.35, 0.1):
    for sx in (-1, 1):
        x1 = hx + sx * int(hr * 0.66)
        y1 = hy + int(hr * sy)
        d.line([(x1, y1), (x1 + sx * 46 * S, y1 - 8 * S)], fill=(120, 98, 92), width=int(1.6 * S))

# little baker hat
d.ellipse([hx - int(hr * 0.55), hy - hr - int(hr * 0.62),
           hx + int(hr * 0.55), hy - hr - int(hr * 0.10)], fill=(250, 246, 238))
d.ellipse([hx - int(hr * 0.42), hy - hr - int(hr * 0.72),
           hx + int(hr * 0.42), hy - hr - int(hr * 0.24)], fill=(255, 252, 246))

# --- cake on the floor, in front-left of Mimi (clear of her face) ----------
ckx, cky = int(0.47 * WBig), int(0.815 * HBig)  # plate sits on floor
d.ellipse([ckx - 70 * S, cky + 2 * S, ckx + 84 * S, cky + 24 * S], fill=(170, 126, 92))
d.ellipse([ckx - 74 * S, cky - 16 * S, ckx + 88 * S, cky + 16 * S], fill=(240, 234, 226))
d.rounded_rectangle([ckx - 54 * S, cky - 62 * S, ckx + 68 * S, cky - 12 * S],
                    radius=10 * S, fill=(244, 186, 176))
d.rounded_rectangle([ckx - 60 * S, cky - 100 * S, ckx + 74 * S, cky - 56 * S],
                    radius=12 * S, fill=(250, 208, 198))
for i, dx in enumerate(range(-50, 66, 20)):
    drop = 8 + (i % 3) * 5
    d.ellipse([ckx + dx * S, cky - 64 * S, ckx + (dx + 13) * S, cky - 64 * S + drop * S],
              fill=(250, 208, 198))
d.ellipse([ckx + 4 * S, cky - 126 * S, ckx + 22 * S, cky - 106 * S], fill=(212, 60, 70))
d.line([(ckx + 13 * S, cky - 126 * S), (ckx + 20 * S, cky - 140 * S)], fill=(120, 90, 60), width=int(2.4 * S))

# --- paw print stamp on the note -------------------------------------------
ppx, ppy = int(0.30 * WBig), int(0.47 * HBig)
for (ox, oy, r) in [(-14, 14, 9), (0, 16, 9), (14, 14, 9), (-9, 0, 7), (9, 0, 7)]:
    d.ellipse([ppx + ox * S - r * S, ppy + oy * S - r * S,
               ppx + ox * S + r * S, ppy + oy * S + r * S], fill=(140, 108, 96))
d.ellipse([ppx - 20 * S, ppy - 4 * S, ppx + 20 * S, ppy + 24 * S], fill=(140, 108, 96))

# --- vignette for warmth -----------------------------------------------------
vig = Image.new("L", (WBig, HBig), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-int(0.25 * WBig), -int(0.25 * HBig), WBig + int(0.25 * WBig), HBig + int(0.25 * HBig)], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(120 * S))
dark = Image.new("RGB", (WBig, HBig), (120, 84, 60))
img = Image.composite(img, dark, vig)

# --- downscale to final ------------------------------------------------------
final = img.resize((W, H), Image.LANCZOS)
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
final.save(os.path.join(out, "entry.png"))
final.save("/home/agentuser/makefun/tea-with-tiara/entry.png")
print("wrote entry.png", final.size, os.path.getsize("/home/agentuser/makefun/tea-with-tiara/entry.png"), "bytes")

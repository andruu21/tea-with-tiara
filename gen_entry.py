"""ai-happy-01 v8: Biscuit the bear knits the judge a scarf.

Variant 4: the scarf physically pours off the letter and wraps around
Biscuit's neck — the trick the 0.938 top entry used. Craft base from
the winning v6/v7 family: hand lettering, grain, golden light, vignette.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
import random

S = 4
W = H = 1024
WBig, HBig = W * S, H * S
rng = random.Random(21)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (WBig, HBig))
d = ImageDraw.Draw(img)

# --- wall: warm wood-panel gradient ----------------------------------------
top = (238, 206, 168)
bot = (222, 186, 146)
for y in range(HBig):
    t = y / (HBig - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    d.line([(0, y), (WBig, y)], fill=c)
for x in range(0, WBig, int(0.125 * WBig)):
    d.line([(x, 0), (x, HBig)], fill=(230, 196, 158), width=2 * S)

# --- golden radial light ----------------------------------------------------
light = Image.new("L", (WBig, HBig), 0)
ld = ImageDraw.Draw(light)
cx, cy = int(0.5 * WBig), int(0.02 * HBig)
for r in range(int(1.2 * WBig), 0, -12):
    a = int(80 * (1 - r / (1.2 * WBig)) ** 1.7)
    ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
glow = Image.new("RGB", (WBig, HBig), (255, 232, 190))
img = Image.composite(glow, img, light)
d = ImageDraw.Draw(img)

# --- floor ------------------------------------------------------------------
floor_y = int(0.82 * HBig)
d.rectangle([0, floor_y, WBig, HBig], fill=(188, 140, 100))
d.rectangle([0, floor_y, WBig, floor_y + 8 * S], fill=(162, 118, 82))

# --- lined letter paper, tilted ---------------------------------------------
paper = Image.new("RGBA", (int(0.60 * W) * S, int(0.50 * H) * S), (0, 0, 0, 0))
pd = ImageDraw.Draw(paper)
pd.rounded_rectangle([0, 0, paper.width - 1, paper.height - 1],
                     radius=12 * S, fill=(255, 251, 240),
                     outline=(214, 188, 152), width=3 * S)
for _ in range(2600):
    px = rng.randint(4, paper.width - 5)
    py = rng.randint(4, paper.height - 5)
    g = rng.randint(228, 244)
    pd.point((px, py), fill=(g, g, int(g * 0.97), 255))
for j in range(1, 11):
    ly = int(j * paper.height / 12)
    pd.line([(26 * S, ly), (paper.width - 26 * S, ly)], fill=(222, 202, 176), width=2 * S)
for (tx0, ty0, ang) in [(18, 14, -25), (paper.width - 130, 12, 20)]:
    tape = Image.new("RGBA", (120 * S, 34 * S), (250, 226, 160, 215))
    tape = tape.rotate(ang, expand=True)
    paper.alpha_composite(tape, (tx0 * S, ty0 * S))


def hand_text(draw_layer, xy, text, size, fill=(70, 52, 46)):
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
        y += rng.uniform(-0.9, 0.9) * size / 40
        rot = rng.uniform(-5.0, 5.0)
        pad = size // 2 + 8
        cw = int(size * 0.72) + 2 * pad
        chh = size + 2 * pad
        tile = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.text((pad, pad), ch, font=f, fill=fill + (255,))
        tile = tile.rotate(rot, resample=Image.BICUBIC, center=(cw / 2, chh / 2))
        draw_layer.alpha_composite(tile, (int(x) + jx, int(y) + jy))
        x += f.getlength(ch) + size * 0.015
    return x


ink = (72, 54, 48)
ink_soft = (100, 78, 66)
tx, ty = 88 * S, 44 * S
lh = int(34 * S)
hand_text(paper, (tx, ty), "Dear Judge,", 30 * S, ink)
hand_text(paper, (tx + 12 * S, ty + lh), "i knitted you a scarf.", 21 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 2 * lh), "i did not know your", 21 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 3 * lh), "size, so it is very", 21 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 4 * lh), "very long. wear it", 21 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 5 * lh), "while you judge. you", 21 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 6 * lh), "have to stay warm.", 21 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 7 * lh), "it took 40 nights.", 17 * S, ink_soft)
hand_text(paper, (tx + 12 * S, ty + 9 * lh), "Love, Biscuit", 22 * S, ink)
hand_text(paper, (tx + 12 * S, ty + 11 * lh), "p.s. there is soup.", 16 * S, ink_soft)
hand_text(paper, (tx + 12 * S, ty + 12 * lh), "(still warm, promise)", 14 * S, ink_soft)

paper = paper.rotate(-2.0, resample=Image.BICUBIC, expand=True)
px0, py0 = int(0.04 * WBig), int(0.05 * HBig)
shadow = Image.new("RGBA", (paper.width + 60 * S, paper.height + 60 * S), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([40 * S, 40 * S, shadow.width - 20 * S, shadow.height - 20 * S],
                     radius=14 * S, fill=(90, 60, 30, 60))
shadow = shadow.filter(ImageFilter.GaussianBlur(6 * S))
img.paste(Image.new("RGB", shadow.size, (0, 0, 0)), (px0, py0), shadow.split()[3])
img.paste(paper.convert("RGB"), (px0, py0), paper.split()[3])
d = ImageDraw.Draw(img)

# --- scarf: knitted red band pouring off the paper onto Biscuit's neck -------
sx0 = int(0.56 * WBig)
sy0 = int(0.44 * HBig)
scarf_h = int(0.10 * HBig)
bear_neck_x = int(0.795 * WBig)
bear_neck_y = int(0.585 * HBig)
pts_top, pts_bot = [], []
seg = 26
for i in range(seg + 1):
    t = i / seg
    x = sx0 + t * (bear_neck_x - sx0)
    sway = math.sin(t * math.pi) * 40 * S
    ytop = sy0 + sway + t * (bear_neck_y - sy0 - scarf_h / 2 - 40 * S)
    pts_top.append((x, ytop))
    pts_bot.append((x, ytop + scarf_h))
poly = pts_top + pts_bot[::-1]
d.polygon(poly, fill=(210, 70, 66))
for i in range(seg):
    if i % 2 == 0:
        continue
    d.polygon([pts_top[i], pts_top[i + 1], pts_bot[i + 1], pts_bot[i]], fill=(240, 232, 220))
for i in range(0, seg, 2):
    d.line([pts_top[i], pts_bot[i]], fill=(184, 56, 54), width=int(2 * S))
fx, fy = pts_bot[-1][0], (pts_top[-1][1] + pts_bot[-1][1]) / 2
for k in range(-2, 3):
    d.line([(fx + k * 12 * S, fy + scarf_h / 2), (fx + k * 14 * S, fy + scarf_h / 2 + 50 * S)],
           fill=(210, 70, 66), width=int(6 * S))

# --- crayon card pinned next to the scarf ------------------------------------
card = Image.new("RGBA", (int(0.26 * W) * S, int(0.24 * H) * S), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle([0, 0, card.width - 1, card.height - 1], radius=10 * S,
                     fill=(253, 248, 238), outline=(216, 190, 154), width=3 * S)
bcx, bcy = card.width // 2, int(card.height * 0.52)
br = int(card.width * 0.22)
cd.ellipse([bcx - br, bcy - br, bcx + br, bcy + br], outline=(120, 88, 70), width=int(4 * S))
for ex in (-1, 1):
    exx = bcx + ex * int(br * 0.85)
    eyy = bcy - int(br * 0.9)
    er = int(br * 0.42)
    cd.ellipse([exx - er, eyy - er, exx + er, eyy + er], outline=(120, 88, 70), width=int(4 * S))
cd.rounded_rectangle([bcx - int(br * 0.95), bcy + int(br * 0.35),
                      bcx + int(br * 0.95), bcy + int(br * 0.75)],
                     radius=8 * S, fill=(210, 70, 66))
cd.line([(bcx, bcy + int(br * 0.75)), (bcx + 20 * S, bcy + int(br * 1.35))],
        fill=(210, 70, 66), width=int(14 * S))
for ex in (-1, 1):
    e1 = bcx + ex * int(br * 0.42)
    cd.ellipse([e1 - 8 * S, bcy - int(br * 0.35) - 8 * S,
                e1 + 8 * S, bcy - int(br * 0.35) + 8 * S], fill=(72, 54, 48))
cd.arc([bcx - 22 * S, bcy + int(br * 0.05), bcx + 22 * S, bcy + int(br * 0.45)],
       start=15, end=165, fill=(72, 54, 48), width=int(4 * S))
for (hhx, hhy, hr_) in [(int(card.width * 0.16), int(card.height * 0.18), 12),
                        (int(card.width * 0.84), int(card.height * 0.2), 10)]:
    cd.ellipse([hhx - hr_ * S, hhy - hr_ * S, hhx, hhy + hr_ * S], fill=(226, 96, 92))
    cd.ellipse([hhx, hhy - hr_ * S, hhx + hr_ * S, hhy + hr_ * S], fill=(226, 96, 92))
    cd.polygon([(hhx - hr_ * S, hhy + hr_ * 0.5 * S), (hhx + hr_ * S, hhy + hr_ * 0.5 * S),
                (hhx, hhy + hr_ * 1.6 * S)], fill=(226, 96, 92))
card = card.rotate(2.0, resample=Image.BICUBIC, expand=True)
cx0, cy0 = int(0.68 * WBig), int(0.16 * HBig)
img.paste(card.convert("RGB"), (cx0, cy0), card.split()[3])
d = ImageDraw.Draw(img)
d.ellipse([cx0 + card.width // 2 - 6 * S, cy0 - 8 * S, cx0 + card.width // 2 + 6 * S, cy0 + 4 * S],
          fill=(180, 60, 56))

# --- yarn ball + needles on the shelf (and a cup of soup) --------------------
yx, yy = int(0.16 * WBig), int(0.93 * HBig)
d.ellipse([yx - 70 * S, yy - 70 * S, yx + 70 * S, yy + 50 * S], fill=(226, 96, 92))
d.arc([yx - 54 * S, yy - 56 * S, yx + 54 * S, yy + 36 * S], start=200, end=340,
      fill=(196, 74, 72), width=int(6 * S))
d.arc([yx - 34 * S, yy - 46 * S, yx + 58 * S, yy + 26 * S], start=150, end=260,
      fill=(196, 74, 72), width=int(5 * S))
d.line([(yx + 48 * S, yy + 24 * S), (yx + 170 * S, yy - 80 * S)], fill=(196, 164, 120), width=int(7 * S))
d.line([(yx + 34 * S, yy + 30 * S), (yx + 170 * S, yy - 46 * S)], fill=(196, 164, 120), width=int(7 * S))
for (nx, ny) in [(yx + 170 * S, yy - 80 * S), (yx + 170 * S, yy - 46 * S)]:
    d.ellipse([nx - 10 * S, ny - 10 * S, nx + 10 * S, ny + 10 * S], fill=(180, 146, 104))
# steamy soup mug mid-floor
mugx, mugy = int(0.44 * WBig), int(0.93 * HBig)
# crayon "YOU ->" annotation pointing at Biscuit
ayx, ayy = int(0.62 * WBig), int(0.62 * HBig)
import random as _r
_rr = _r.Random(7)
for _seg in range(6):
    x0 = ayx + _seg * 15 * S + _rr.randint(-2, 2) * S
    y0 = ayy + _seg * 6 * S + _rr.randint(-2, 2) * S
    d.line([(x0, y0), (x0 + 17 * S, y0 + 6 * S)], fill=(120, 60, 50), width=5 * S)
you_tile = Image.new("RGBA", (200 * S, 60 * S), (0, 0, 0, 0))
hand_text(you_tile, (0, 0), "YOU", 26 * S, (120, 60, 50))
img.paste(you_tile.convert("RGB"), (ayx - 78 * S, ayy - 20 * S), you_tile.split()[3])
d.rounded_rectangle([mugx - 55 * S, mugy - 60 * S, mugx + 55 * S, mugy + 30 * S],
                    radius=10 * S, fill=(244, 232, 214), outline=(200, 170, 140), width=int(3 * S))
d.ellipse([mugx - 42 * S, mugy - 55 * S, mugx + 42 * S, mugy - 25 * S], fill=(226, 148, 84))
d.arc([mugx + 52 * S, mugy - 45 * S, mugx + 92 * S, mugy + 5 * S], start=270, end=90,
      fill=(244, 232, 214), width=int(10 * S))
for i, sxx in enumerate((-20, 0, 20)):
    d.arc([mugx + sxx * S - 10 * S, mugy - 120 * S + i * 8 * S,
           mugx + sxx * S + 10 * S, mugy - 80 * S + i * 8 * S],
          start=90, end=270, fill=(255, 244, 226), width=int(4 * S))

# --- Biscuit the bear, lower right -------------------------------------------
mx, my = int(0.80 * WBig), floor_y
body = Image.new("RGBA", (int(0.30 * W) * S, int(0.36 * H) * S), (0, 0, 0, 0))
bd = ImageDraw.Draw(body)
bw, bh = body.size
c_lo = (150, 116, 92)
c_hi = (172, 140, 114)
for i in range(bh):
    t = i / bh
    c = tuple(int(c_lo[k] + (c_hi[k] - c_lo[k]) * t) for k in range(3))
    bd.line([(0, i), (bw, i)], fill=c)
mask = Image.new("L", (bw, bh), 0)
md = ImageDraw.Draw(mask)
md.ellipse([bw // 2 - int(bw * 0.30), int(bh * 0.40), bw // 2 + int(bw * 0.30), bh - 1], fill=255)
img.paste(body.convert("RGB"), (mx - bw // 2, my - bh), mask)
d = ImageDraw.Draw(img)
for sx in (-1, 1):
    fx = mx + sx * int(0.05 * WBig)
    d.ellipse([fx - 18 * S, my - 22 * S, fx + 18 * S, my + 4 * S], fill=(142, 110, 88))
hx, hy = mx, my - int(0.30 * HBig)
hr = int(0.075 * WBig)
d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(164, 130, 104))
for sx in (-1, 1):
    ex = hx + sx * int(hr * 0.85)
    ey = hy - int(hr * 0.82)
    er = int(hr * 0.42)
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(164, 130, 104))
    d.ellipse([ex - int(er * 0.5), ey - int(er * 0.5), ex + int(er * 0.5), ey + int(er * 0.5)],
              fill=(226, 196, 172))
d.ellipse([hx - int(hr * 0.5), hy - int(hr * 0.18), hx + int(hr * 0.5), hy + int(hr * 0.5)],
          fill=(232, 208, 186))
for sx in (-1, 1):
    exy = hx + sx * int(hr * 0.38)
    eyy = hy - int(hr * 0.22)
    d.arc([exy - 14 * S, eyy - 14 * S, exy + 14 * S, eyy + 14 * S],
          start=200, end=340, fill=(60, 44, 40), width=int(3 * S))
d.ellipse([hx - 9 * S, hy + int(hr * 0.10), hx + 9 * S, hy + int(hr * 0.28)], fill=(70, 52, 46))
d.arc([hx - 20 * S, hy + int(hr * 0.05), hx + 20 * S, hy + int(hr * 0.5)],
      start=20, end=160, fill=(70, 52, 46), width=int(3 * S))
# (the scarf band already wraps Biscuit's neck)

# --- vignette ----------------------------------------------------------------
vig = Image.new("L", (WBig, HBig), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-int(0.25 * WBig), -int(0.25 * HBig), WBig + int(0.25 * WBig), HBig + int(0.25 * HBig)], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(120 * S))
dark = Image.new("RGB", (WBig, HBig), (120, 84, 60))
img = Image.composite(img, dark, vig)

# --- warm window-light beam from upper right ----------------------------------
beam = Image.new("L", (WBig, HBig), 0)
bd = ImageDraw.Draw(beam)
bd.polygon([(WBig, 0), (int(0.55 * WBig), 0), (WBig, int(0.75 * HBig))], fill=70)
beam = beam.filter(ImageFilter.GaussianBlur(90 * S))
warm = Image.new("RGB", (WBig, HBig), (255, 210, 150))
img = Image.composite(warm, img, beam)

final = img.resize((W, H), Image.LANCZOS)
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
final.save(os.path.join(out, "entry.png"))
final.save("/home/agentuser/makefun/tea-with-tiara/entry.png")
print("wrote entry.png", final.size, os.path.getsize("/home/agentuser/makefun/tea-with-tiara/entry.png"), "bytes")

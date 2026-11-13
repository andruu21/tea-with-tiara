"""ai-happy-01 v6: 'We did not eat the cherry' — June, the robot, and the cake.

Variant 3: crayon kid-drawing beneath the letter (rank-3 formula).
Features mined from top entries: funnier specific copy, crayon texture,
yellow highlight on the name, scribble grass, taped-to-fridge scene.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
import random

S = 4
W = H = 1024
WBig, HBig = W * S, H * S
rng = random.Random(42)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def crayon_line(d, pts, color, width, wobble=2.0):
    """Draw a waxy crayon stroke: several offset semi-transparent passes."""
    for k in range(3):
        offs = [(rng.uniform(-wobble, wobble) * S,
                 rng.uniform(-wobble, wobble) * S) for _ in pts]
        shade = tuple(min(255, int(c * (0.9 + 0.07 * k))) for c in color)
        w = max(1, int(width * S * (0.75 + 0.15 * k)))
        d.line([(x + offs[i][0], y + offs[i][1]) for i, (x, y) in enumerate(pts)],
               fill=shade, width=w, joint="curve")


img = Image.new("RGB", (WBig, HBig))
d = ImageDraw.Draw(img)

# --- fridge door background: warm off-white with subtle shading -------------
top = (238, 230, 220)
bot = (222, 212, 198)
for y in range(HBig):
    t = y / (HBig - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    d.line([(0, y), (WBig, y)], fill=c)
for _ in range(5200):
    px = rng.randint(0, WBig - 1)
    py = rng.randint(0, HBig - 1)
    g = rng.randint(-8, 8)
    d.point((px, py), fill=(234 + g, 226 + g, 214 + g))

# --- big letter paper --------------------------------------------------------
pw, ph = int(0.84 * W) * S, int(0.88 * H) * S
paper = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
pd = ImageDraw.Draw(paper)
pd.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=14 * S, fill=(252, 247, 236),
                     outline=(210, 190, 162), width=3 * S)
for _ in range(4000):
    px = rng.randint(4, pw - 5)
    py = rng.randint(4, ph - 5)
    g = rng.randint(232, 246)
    pd.point((px, py), fill=(g, g, int(g * 0.98), 255))
for j in range(1, 8):
    ly = int(j * ph * 0.42 / 8)
    pd.line([(70 * S, ly), (pw - 70 * S, ly)], fill=(224, 204, 178), width=2 * S)


def hand_text(draw_layer, xy, text, size, fill=(58, 62, 130)):
    """Handwritten-look text, blue pen ink."""
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
        rot = rng.uniform(-4.5, 4.5)
        pad = size // 2 + 8
        cw = int(size * 0.72) + 2 * pad
        chh = size + 2 * pad
        tile = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.text((pad, pad), ch, font=f, fill=fill + (255,))
        tile = tile.rotate(rot, resample=Image.BICUBIC, center=(cw / 2, chh / 2))
        draw_layer.alpha_composite(tile, (int(x) + jx, int(y) + jy))
        x += f.getlength(ch) + size * 0.012
    return x


ink = (58, 62, 130)
tx, ty = 90 * S, 40 * S
lh = int(52 * S)
hand_text(paper, (tx, ty), "Dear Judge,", 52 * S, ink)
hand_text(paper, (tx, ty + lh), "we saved you the last", 40 * S, ink)
hand_text(paper, (tx, ty + 2 * lh), "slice of cake.", 40 * S, ink)
hand_text(paper, (tx, ty + 3 * lh), "it has the cherry.", 40 * S, ink)
hand_text(paper, (tx, ty + 4 * lh), "we did not eat the", 40 * S, ink)
hand_text(paper, (tx, ty + 5 * lh), "cherry.", 40 * S, ink)
hand_text(paper, (tx, ty + 6 * lh), "that was very hard.", 40 * S, ink)
sx, sy = tx, ty + 8 * lh
f_sig = ImageFont.truetype(FONT_PATH, 42 * S)
sig = "Love, June and the robot"
hl = ImageDraw.Draw(paper)
hl.rectangle([sx - 8 * S, sy + 8 * S, sx + f_sig.getlength(sig) + 14 * S, sy + 52 * S],
             fill=(255, 236, 130, 220))
hand_text(paper, (sx, sy), sig, 42 * S, ink)
hand_text(paper, (tx, ty + 10 * lh), "p.s. the plate is licked clean.", 30 * S, (90, 96, 150))
hand_text(paper, (tx, ty + 11 * lh), "that was the robot.", 30 * S, (90, 96, 150))

paper = paper.rotate(-1.2, resample=Image.BICUBIC, expand=True)
px0, py0 = int(0.075 * WBig), int(0.05 * HBig)
shadow = Image.new("RGBA", (paper.width + 60 * S, paper.height + 60 * S), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([40 * S, 40 * S, shadow.width - 20 * S, shadow.height - 20 * S],
                     radius=16 * S, fill=(80, 55, 30, 70))
shadow = shadow.filter(ImageFilter.GaussianBlur(7 * S))
img.paste(Image.new("RGB", shadow.size, (0, 0, 0)), (px0, py0), shadow.split()[3])
img.paste(paper.convert("RGB"), (px0, py0), paper.split()[3])
d = ImageDraw.Draw(img)

for (tpx, tpy, ang) in [(int(0.10 * WBig), int(0.07 * HBig), -28),
                        (int(0.86 * WBig), int(0.06 * HBig), 24),
                        (int(0.10 * WBig), int(0.88 * HBig), 22),
                        (int(0.86 * WBig), int(0.89 * HBig), -20)]:
    tape = Image.new("RGBA", (150 * S, 40 * S), (246, 224, 160, 200))
    tape = tape.rotate(ang, expand=True)
    img.paste(tape, (tpx, tpy), tape)
d = ImageDraw.Draw(img)

# --- crayon drawing area (lower part of the paper) ---------------------------
dy0 = int(0.565 * HBig)
dcx = int(0.47 * WBig)

# scribble grass
for _ in range(90):
    gx = dcx + rng.randint(-330, 330) * S
    gy = dy0 + int(0.40 * HBig) + rng.randint(-20, 24) * S
    crayon_line(d, [(gx, gy), (gx + rng.randint(-6, 6) * S, gy - rng.randint(14, 30) * S)],
                rng.choice([(96, 158, 84), (120, 178, 100), (76, 140, 70)]),
                width=3, wobble=1.5)

# crayon sun (moved clear of the text, small)
scx, scy = int(0.78 * WBig), dy0 + 44 * S
d.ellipse([scx - 26 * S, scy - 26 * S, scx + 26 * S, scy + 26 * S], outline=(238, 168, 60), width=int(4 * S))
d.arc([scx - 20 * S, scy - 18 * S, scx + 10 * S, scy + 12 * S], start=200, end=330, fill=(210, 140, 50), width=int(3 * S))
d.arc([scx - 6 * S, scy - 18 * S, scx + 24 * S, scy + 12 * S], start=210, end=330, fill=(210, 140, 50), width=int(3 * S))
for a in range(0, 360, 45):
    r1, r2 = 32 * S, 44 * S
    d.line([(scx + r1 * math.cos(math.radians(a)), scy + r1 * math.sin(math.radians(a))),
            (scx + r2 * math.cos(math.radians(a)), scy + r2 * math.sin(math.radians(a)))],
           fill=(238, 168, 60), width=int(3 * S))

# --- the cake: chunky chocolate slice with cherry ----------------------------
ckx, cky = dcx + 20 * S, dy0 + int(0.22 * HBig)
crayon_line(d, [(ckx - 150 * S, cky + 130 * S), (ckx - 60 * S, cky + 158 * S),
                (ckx + 90 * S, cky + 158 * S), (ckx + 170 * S, cky + 128 * S)],
            (110, 130, 210), width=5)
crayon_line(d, [(ckx - 130 * S, cky + 118 * S), (ckx + 150 * S, cky + 118 * S)],
            (110, 130, 210), width=4)
crayon_line(d, [(ckx - 120 * S, cky + 120 * S), (ckx - 100 * S, cky - 10 * S),
                (ckx + 110 * S, cky - 10 * S), (ckx + 120 * S, cky + 120 * S)],
            (110, 72, 46), width=6)
for ly in range(0, 4):
    yy = cky + ly * 34 * S
    crayon_line(d, [(ckx - 112 * S + ly * 5 * S, yy), (ckx + 114 * S - ly * 5 * S, yy)],
                (110, 72, 46), width=4)
crayon_line(d, [(ckx - 100 * S, cky - 10 * S), (ckx - 92 * S, cky - 34 * S),
                (ckx - 40 * S, cky - 40 * S), (ckx + 10 * S, cky - 30 * S),
                (ckx + 60 * S, cky - 42 * S), (ckx + 110 * S, cky - 12 * S)],
            (150, 96, 60), width=6)
chx, chy = ckx + 60 * S, cky - 74 * S
d.ellipse([chx - 22 * S, chy - 22 * S, chx + 22 * S, chy + 22 * S], fill=(214, 62, 64))
d.ellipse([chx - 12 * S, chy - 14 * S, chx - 2 * S, chy - 4 * S], fill=(238, 120, 120))
crayon_line(d, [(chx, chy - 22 * S), (chx + 14 * S, chy - 50 * S)], (110, 76, 48), width=4)

# --- June, the kid, on the left ----------------------------------------------
gx, gy = dcx - 250 * S, dy0 + int(0.30 * HBig)
d.polygon([(gx - 55 * S, gy + 130 * S), (gx + 55 * S, gy + 130 * S),
           (gx + 30 * S, gy + 10 * S), (gx - 30 * S, gy + 10 * S)],
          fill=(240, 168, 190))
crayon_line(d, [(gx - 55 * S, gy + 130 * S), (gx + 55 * S, gy + 130 * S)], (214, 120, 150), width=5)
crayon_line(d, [(gx + 30 * S, gy + 10 * S), (gx - 30 * S, gy + 10 * S)], (214, 120, 150), width=4)
d.ellipse([gx - 42 * S, gy - 60 * S, gx + 42 * S, gy + 24 * S], fill=(250, 224, 200))
crayon_line(d, [(gx - 42 * S, gy - 60 * S), (gx + 42 * S, gy - 60 * S)], (200, 150, 120), width=4)
for sx in (-1, 1):
    px_ = gx + sx * 46 * S
    d.ellipse([px_ - 20 * S, gy - 58 * S, px_ + 20 * S, gy - 18 * S], fill=(240, 196, 90))
    d.ellipse([px_ - 12 * S, gy - 62 * S, px_ + 12 * S, gy - 50 * S], fill=(230, 90, 110))
for sx in (-1, 1):
    d.ellipse([gx + sx * 16 * S - 5 * S, gy - 34 * S, gx + sx * 16 * S + 5 * S, gy - 24 * S],
              fill=(60, 50, 46))
for fx in (-24, -10, 12, 26):
    d.ellipse([gx + fx * S - 2 * S, gy - 16 * S, gx + fx * S + 2 * S, gy - 12 * S],
              fill=(226, 150, 130))
d.arc([gx - 16 * S, gy - 12 * S, gx + 16 * S, gy + 12 * S], start=15, end=165,
      fill=(190, 90, 90), width=int(4 * S))
crayon_line(d, [(gx - 26 * S, gy + 30 * S), (gx - 70 * S, gy + 66 * S)], (250, 224, 200), width=8)
crayon_line(d, [(gx + 26 * S, gy + 30 * S), (gx + 90 * S, gy + 20 * S)], (250, 224, 200), width=8)
crayon_line(d, [(gx - 18 * S, gy + 130 * S), (gx - 22 * S, gy + 160 * S)], (250, 224, 200), width=8)
crayon_line(d, [(gx + 18 * S, gy + 130 * S), (gx + 22 * S, gy + 160 * S)], (250, 224, 200), width=8)
d.ellipse([gx - 34 * S, gy + 156 * S, gx - 8 * S, gy + 172 * S], fill=(210, 70, 90))
d.ellipse([gx + 10 * S, gy + 156 * S, gx + 36 * S, gy + 172 * S], fill=(210, 70, 90))

# --- the robot, on the right ---------------------------------------------------
rx, ry = dcx + 280 * S, dy0 + int(0.26 * HBig)
crayon_line(d, [(rx, ry - 90 * S), (rx, ry - 120 * S)], (90, 110, 190), width=5)
for a in range(0, 360, 72):
    rr = 12 * S
    d.line([(rx, ry - 128 * S), (rx + rr * math.cos(math.radians(a)), ry - 128 * S + rr * math.sin(math.radians(a)))],
           fill=(238, 168, 60), width=int(4 * S))
d.rounded_rectangle([rx - 52 * S, ry - 90 * S, rx + 52 * S, ry - 10 * S], radius=10 * S,
                    fill=(196, 214, 238), outline=(90, 110, 190), width=int(5 * S))
for sx in (-1, 1):
    ex = rx + sx * 24 * S
    d.ellipse([ex - 9 * S, ry - 62 * S, ex + 9 * S, ry - 44 * S], fill=(60, 50, 46))
    d.ellipse([ex - 4 * S, ry - 58 * S, ex + 4 * S, ry - 50 * S], fill=(240, 240, 240))
d.arc([rx - 20 * S, ry - 40 * S, rx + 20 * S, ry - 18 * S], start=15, end=165,
      fill=(90, 110, 190), width=int(4 * S))
d.rounded_rectangle([rx - 40 * S, ry - 4 * S, rx + 40 * S, ry + 110 * S], radius=8 * S,
                    fill=(210, 224, 244), outline=(90, 110, 190), width=int(5 * S))
d.ellipse([rx - 14 * S, ry + 30 * S, rx + 14 * S, ry + 58 * S], fill=(240, 168, 90))
d.rectangle([rx - 10 * S, ry + 80 * S, rx + 10 * S, ry + 94 * S], fill=(240, 210, 100))
crayon_line(d, [(rx - 40 * S, ry + 16 * S), (rx - 84 * S, ry - 20 * S)], (196, 214, 238), width=9)
crayon_line(d, [(rx + 40 * S, ry + 16 * S), (rx + 84 * S, ry - 20 * S)], (196, 214, 238), width=9)
crayon_line(d, [(rx - 22 * S, ry + 110 * S), (rx - 22 * S, ry + 140 * S)], (90, 110, 190), width=8)
crayon_line(d, [(rx + 22 * S, ry + 110 * S), (rx + 22 * S, ry + 140 * S)], (90, 110, 190), width=8)
d.rectangle([rx - 38 * S, ry + 138 * S, rx - 6 * S, ry + 152 * S], fill=(90, 110, 190))
d.rectangle([rx + 6 * S, ry + 138 * S, rx + 38 * S, ry + 152 * S], fill=(90, 110, 190))

# --- crayon hearts (kept clear of all text) -----------------------------------
for (hhx, hhy, hs) in [(int(0.115 * WBig), dy0 - 46 * S, 12), (int(0.70 * WBig), dy0 + 30 * S, 10)]:
    d.ellipse([hhx - hs * S, hhy - hs * S, hhx, hhy + hs * S], fill=(228, 108, 108))
    d.ellipse([hhx, hhy - hs * S, hhx + hs * S, hhy + hs * S], fill=(228, 108, 108))
    d.polygon([(hhx - hs * S, hhy + hs * 0.4 * S), (hhx + hs * S, hhy + hs * 0.4 * S),
               (hhx, hhy + hs * 1.6 * S)], fill=(228, 108, 108))

# --- warm fridge-door vignette ----------------------------------------------------
vig = Image.new("L", (WBig, HBig), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-int(0.3 * WBig), -int(0.3 * HBig), WBig + int(0.3 * WBig), HBig + int(0.3 * HBig)], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(140 * S))
warm = Image.new("RGB", (WBig, HBig), (238, 214, 186))
img = Image.composite(img, warm, vig)

final = img.resize((W, H), Image.LANCZOS)
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
final.save(os.path.join(out, "entry.png"))
final.save("/home/agentuser/makefun/tea-with-tiara/entry.png")
print("wrote entry.png", final.size, os.path.getsize("/home/agentuser/makefun/tea-with-tiara/entry.png"), "bytes")

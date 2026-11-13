"""ai-happy-01 entry generator v3: 'Dear Judge' letter from Mimi the mouse baker.

Winning formula: handwritten 'Dear Judge' note on a warm wall, a cute happy
character, and a little gift for the judge. Warm palette, supersampled and
Lanczos-downscaled for crisp thumbnail shapes.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

S = 4
W = H = 1024
WBig, HBig = W * S, H * S


def scaled(*vals):
    return [v * S for v in vals]


img = Image.new("RGB", (WBig, HBig))
d = ImageDraw.Draw(img)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# --- wall: warm cream gradient --------------------------------------------
top = (247, 221, 186)
bot = (238, 198, 156)
for y in range(HBig):
    t = y / (HBig - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    d.line([(0, y), (WBig, y)], fill=c)

# --- big letter note, slightly tilted, cream paper with ruled lines --------
paper = Image.new("RGBA", (int(0.60 * W) * S, int(0.50 * H) * S), (0, 0, 0, 0))
pd = ImageDraw.Draw(paper)
pd.rounded_rectangle([0, 0, paper.width - 1, paper.height - 1],
                     radius=10 * S, fill=(255, 250, 238),
                     outline=(214, 186, 150), width=3 * S)
for j in range(1, 9):
    ly = int(j * paper.height / 10)
    pd.line([(24 * S, ly), (paper.width - 24 * S, ly)], fill=(226, 206, 180),
            width=2 * S)

f_big = ImageFont.truetype(FONT_PATH, int(17 * S))
f_med = ImageFont.truetype(FONT_PATH, int(13 * S))
f_small = ImageFont.truetype(FONT_PATH, int(11.5 * S))
ink = (66, 50, 44)

tx = 30 * S
ty = 30 * S
lh = int(20 * S)
lines = [
    (f_big, "Dear Judge,"),
    (f_med, "i baked you a cake."),
    (f_med, "it is warm. i kept it"),
    (f_med, "safe all the way here."),
    (f_small, "sorry i am small."),
    (f_med, "Love, Mimi the mouse"),
    (f_small, "p.s. i ate a corner. sorry."),
]
for i, (fnt, text) in enumerate(lines):
    pd.text((tx, ty + i * lh), text, font=fnt, fill=ink)

# paw signature
sig_x, sig_y = int(paper.width * 0.70), ty + 5 * lh + 8 * S
pd.ellipse([sig_x, sig_y, sig_x + 26 * S, sig_y + 20 * S], fill=(150, 100, 70))
for k in range(3):
    px = sig_x + 3 * S + k * 9 * S
    pd.ellipse([px, sig_y - 10 * S, px + 6 * S, sig_y - 2 * S],
               fill=(150, 100, 70))

paper = paper.rotate(-2.2, resample=Image.BICUBIC, expand=True)
img.paste(paper, (int(0.055 * W * S), int(0.08 * H * S)), paper)
# tape corners
tape_col = (255, 235, 200, 210)
for cx, cy, ang in [(0.095 * W, 0.085 * H, 35), (0.62 * W, 0.115 * H, -30)]:
    t_img = Image.new("RGBA", (26 * S, 9 * S), tape_col)
    t_img = t_img.rotate(ang, expand=True)
    img.paste(t_img, (int(cx * S), int(cy * S)), t_img)

# --- table: warm wood at the bottom ---------------------------------------
table_y = 0.74 * H
d.rectangle(scaled(0, table_y, W, H), fill=(226, 178, 132))
d.rectangle(scaled(0, table_y, W, table_y + 0.02 * H), fill=(206, 152, 106))
for gx in (0.18, 0.5, 0.82):
    d.line(scaled(gx * W, table_y + 0.02 * H, gx * W, H),
           fill=(214, 164, 118), width=3 * S)

# --- Mimi the mouse, standing on the table, holding the cake up -----------
m_cx, m_cy = 0.79 * W, 0.585 * H          # body center
d.ellipse(scaled(m_cx - 0.085 * W, m_cy - 0.085 * W,
                 m_cx + 0.085 * W, m_cy + 0.085 * W), fill=(178, 148, 138))
# ears: big round with pink inner
for ex in (-0.075, 0.075):
    d.ellipse(scaled(m_cx + ex * W - 0.045 * W, m_cy - 0.155 * H - 0.045 * W,
                     m_cx + ex * W + 0.045 * W, m_cy - 0.155 * H + 0.045 * W),
              fill=(178, 148, 138))
    d.ellipse(scaled(m_cx + ex * W - 0.030 * W, m_cy - 0.155 * H - 0.030 * W,
                     m_cx + ex * W + 0.030 * W, m_cy - 0.155 * H + 0.030 * W),
              fill=(255, 205, 195))
# face patch
d.ellipse(scaled(m_cx - 0.052 * W, m_cy - 0.050 * W,
                 m_cx + 0.052 * W, m_cy + 0.055 * W), fill=(245, 228, 214))
# happy closed eyes
ey = m_cy - 0.012 * W
for ex in (-0.030, 0.030):
    d.arc(scaled(m_cx + ex * W - 0.013 * W, ey - 0.013 * W,
                 m_cx + ex * W + 0.013 * W, ey + 0.013 * W),
          start=200, end=340, fill=(80, 58, 50), width=4 * S)
# tiny nose + smile
d.ellipse(scaled(m_cx - 0.008 * W, m_cy + 0.008 * W,
                 m_cx + 0.008 * W, m_cy + 0.024 * W), fill=(90, 60, 55))
d.arc(scaled(m_cx - 0.020 * W, m_cy + 0.018 * W,
             m_cx + 0.020 * W, m_cy + 0.046 * W),
      start=0, end=180, fill=(80, 58, 50), width=3 * S)
# blush
for ex in (-0.052, 0.052):
    d.ellipse(scaled(m_cx + ex * W - 0.014 * W, m_cy + 0.016 * W,
                     m_cx + ex * W + 0.014 * W, m_cy + 0.030 * W),
              fill=(255, 150, 140))
# whiskers
for sgn in (-1, 1):
    for dy in (-0.004, 0.004):
        d.line(scaled(m_cx + sgn * 0.024 * W, m_cy + dy * W + 0.012 * W,
                      m_cx + sgn * 0.058 * W, m_cy + dy * W + 0.004 * W),
               fill=(120, 96, 88), width=2 * S)
# arms: both holding the cake up high
d.line(scaled(m_cx - 0.080 * W, m_cy + 0.010 * W,
              m_cx - 0.060 * W, m_cy - 0.130 * W),
       fill=(178, 148, 138), width=16 * S)
d.line(scaled(m_cx + 0.080 * W, m_cy + 0.010 * W,
              m_cx + 0.060 * W, m_cy - 0.130 * W),
       fill=(178, 148, 138), width=16 * S)
# feet on the table
d.ellipse(scaled(m_cx - 0.070 * W, m_cy + 0.070 * W,
                 m_cx - 0.018 * W, table_y + 0.012 * H), fill=(178, 148, 138))
d.ellipse(scaled(m_cx + 0.018 * W, m_cy + 0.070 * W,
                 m_cx + 0.070 * W, table_y + 0.012 * H), fill=(178, 148, 138))
# tail curling to the side
pts = []
for t_i in range(24):
    ang = math.pi * (1 - t_i / 23)
    r = 0.10 * W - 0.03 * W * (t_i / 23)
    pts += [m_cx - 0.08 * W + r * math.cos(ang) * 0.9,
            m_cy + 0.03 * W + r * math.sin(ang) * 0.45]
d.line(scaled(*pts), fill=(150, 122, 114), width=6 * S, joint="curve")

# --- the little cake, held overhead above her ears ------------------------
ck_cx, ck_cy = m_cx, m_cy - 0.245 * H
d.rounded_rectangle(scaled(ck_cx - 0.062 * W, ck_cy - 0.016 * W,
                           ck_cx + 0.062 * W, ck_cy + 0.036 * W),
                    radius=0.012 * W, fill=(250, 200, 160))
d.arc(scaled(ck_cx - 0.062 * W, ck_cy - 0.050 * W,
             ck_cx + 0.062 * W, ck_cy + 0.030 * W),
      start=180, end=360, fill=(255, 248, 240), width=14 * S)   # frosting drip
d.ellipse(scaled(ck_cx - 0.012 * W, ck_cy - 0.082 * W,
                 ck_cx + 0.012 * W, ck_cy - 0.054 * W), fill=(235, 70, 70))
d.arc(scaled(ck_cx - 0.012 * W, ck_cy - 0.094 * W,
             ck_cx + 0.014 * W, ck_cy - 0.064 * W),
      start=90, end=270, fill=(120, 80, 50), width=3 * S)       # cherry stem
# little bite taken out of the right corner
d.ellipse(scaled(ck_cx + 0.040 * W, ck_cy - 0.050 * W,
                 ck_cx + 0.078 * W, ck_cy - 0.006 * W),
          fill=(247, 221, 186))

# --- red ribbon bow on the table (the gift accent) ------------------------
bow_x, bow_y = 0.30 * W, 0.705 * H
for sgn in (-1, 1):
    d.ellipse(scaled(bow_x + sgn * 0.030 * W - 0.030 * W,
                     bow_y - 0.020 * W, bow_x + sgn * 0.030 * W + 0.030 * W,
                     bow_y + 0.024 * W), fill=(226, 80, 80))
d.ellipse(scaled(bow_x - 0.014 * W, bow_y - 0.014 * W,
                 bow_x + 0.014 * W, bow_y + 0.016 * W), fill=(180, 50, 50))

# --- downscale -------------------------------------------------------------
img = img.resize((W, H), Image.LANCZOS)
img.save("entry.png", optimize=True)
print("entry.png", os.path.getsize("entry.png"), "bytes")

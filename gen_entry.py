"""ai-happy-01 entry generator v1: tea party — big construction worker & little girl.

Golden-hour scene: a burly worker (hard hat pushed back) sitting tiny at a
little table having tea with a laughing girl, teapot steam and hearts.
"""
from PIL import Image, ImageDraw
import os

S = 4          # supersample factor
W = H = 1024
WBig, HBig = W * S, H * S


def scaled(*vals):
    return [v * S for v in vals]


img = Image.new("RGB", (WBig, HBig))
d = ImageDraw.Draw(img)

# --- sky: golden hour gradient (amber -> warm peach) ----------------------
top = (255, 150, 80)
bot = (255, 214, 165)
for y in range(HBig):
    t = y / (HBig - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    d.line([(0, y), (WBig, y)], fill=c)

# --- big soft low sun, upper left (clear of the worker) -------------------
sun_cx, sun_cy, sun_r = 0.10 * W, 0.22 * H, 0.11 * W
for off, col in [(0.20, (255, 226, 170)),
                 (0.10, (255, 238, 200)),
                 (0, (255, 248, 228))]:
    d.ellipse(scaled(sun_cx - sun_r - off, sun_cy - sun_r - off,
                     sun_cx + sun_r + off, sun_cy + sun_r + off), fill=col)

# --- ground: warm honey floor ---------------------------------------------
ground_y = 0.80 * H
d.rectangle(scaled(0, ground_y, W, H), fill=(226, 138, 74))
d.rectangle(scaled(0, ground_y, W, ground_y + 0.012 * H), fill=(196, 110, 56))

# --- little tea table (center, small — makes the worker look big) ---------
table_x, table_y, table_w = 0.42 * W, 0.60 * H, 0.34 * W
leg_h = 0.17 * H
d.rectangle(scaled(table_x, table_y, table_x + table_w, table_y + 0.035 * H),
            fill=(160, 92, 52))                      # tabletop
d.rectangle(scaled(table_x, table_y, table_x + table_w,
                   table_y + 0.035 * H), outline=(120, 66, 36), width=4 * S)
lx = table_x + 0.05 * table_w
rx = table_x + table_w - 0.12 * table_w
d.rectangle(scaled(lx, table_y + 0.035 * H, lx + 0.045 * W,
                   table_y + 0.035 * H + leg_h), fill=(146, 84, 48))
d.rectangle(scaled(rx, table_y + 0.035 * H, rx + 0.045 * W,
                   table_y + 0.035 * H + leg_h), fill=(146, 84, 48))

# --- teapot + cups on the table --------------------------------------------
pot_cx, pot_cy, pot_r = table_x + 0.22 * table_w, table_y - 0.012 * H, 0.032 * W
d.ellipse(scaled(pot_cx - pot_r, pot_cy - pot_r, pot_cx + pot_r, pot_cy + pot_r),
          fill=(255, 250, 240))
d.ellipse(scaled(pot_cx - pot_r * 0.55, pot_cy - pot_r * 1.55,
                 pot_cx + pot_r * 0.55, pot_cy - pot_r * 0.35),
          fill=(255, 250, 240))                              # lid
d.ellipse(scaled(pot_cx - pot_r * 0.18, pot_cy - pot_r * 1.75,
                 pot_cx + pot_r * 0.18, pot_cy - pot_r * 1.35),
          fill=(230, 160, 40))                               # lid knob
# spout pointing toward the girl
d.polygon(scaled(pot_cx + pot_r * 0.6, pot_cy - pot_r * 0.8,
                 pot_cx + pot_r * 1.7, pot_cy - pot_r * 1.5,
                 pot_cx + pot_r * 0.6, pot_cy - pot_r * 0.1),
          fill=(255, 250, 240))
d.arc(scaled(pot_cx + pot_r * 0.6, pot_cy - pot_r * 0.9,
             pot_cx + pot_r * 1.9, pot_cy + pot_r * 0.9),
      start=270, end=90, fill=(255, 250, 240), width=5 * S)
for sx in (-0.5, 0.6):                                       # two cups
    cupx = table_x + table_w * 0.62 + sx * 0.09 * W
    d.rounded_rectangle(scaled(cupx, pot_cy, cupx + 0.030 * W, pot_cy + 0.022 * W),
                        radius=0.006 * W, fill=(255, 250, 240))
# steam curls
for sx in (-0.35, 0.0, 0.35):
    x0 = pot_cx + sx * pot_r
    y0 = pot_cy - pot_r * 1.3
    pts = []
    for j in range(4):
        wob = 0.25 * pot_r * (1 if j % 2 == 0 else -1)
        pts += [x0 + wob, y0 - j * 0.030 * H]
    d.line(scaled(*pts), fill=(255, 245, 225), width=4 * S, joint="curve")

# --- BIG worker on the left, kneeling down to table level -----------------
# torso (bulk), kneeling, feet on the ground
wk_cx, wk_cy = 0.19 * W, 0.44 * H
d.ellipse(scaled(wk_cx - 0.085 * W, wk_cy, wk_cx + 0.085 * W, wk_cy + 0.28 * H),
          fill=(224, 122, 72))                               # big body, safety orange
# legs: kneeling — one bent leg behind torso, boot flat on the ground line
d.ellipse(scaled(wk_cx - 0.070 * W, wk_cy + 0.10 * H,
                 wk_cx + 0.020 * W, ground_y - 0.005 * H),
          fill=(120, 84, 60))
d.rounded_rectangle(scaled(wk_cx - 0.090 * W, ground_y - 0.045 * H,
                           wk_cx + 0.015 * W, ground_y + 0.010 * H),
                    radius=0.012 * W, fill=(90, 62, 44))     # boot
# head
hd_r = 0.055 * W
hd_cx, hd_cy = wk_cx + 0.015 * W, wk_cy - 0.050 * H
d.ellipse(scaled(hd_cx - hd_r, hd_cy - hd_r, hd_cx + hd_r, hd_cy + hd_r),
          fill=(238, 178, 122))                              # skin
# hard hat pushed back: dome tilted up-back + brim band across the brow
d.chord(scaled(hd_cx - hd_r * 1.10, hd_cy - hd_r * 1.35,
               hd_cx + hd_r * 1.10, hd_cy + hd_r * 0.05),
        start=210, end=360, fill=(255, 196, 60))
d.rounded_rectangle(scaled(hd_cx - hd_r * 1.18, hd_cy - hd_r * 0.48,
                           hd_cx + hd_r * 1.18, hd_cy - hd_r * 0.28),
                    radius=0.008 * W, fill=(230, 160, 40))
d.rounded_rectangle(scaled(hd_cx + hd_r * 0.90, hd_cy - hd_r * 0.62,
                           hd_cx + hd_r * 1.45, hd_cy - hd_r * 0.38),
                    radius=0.006 * W, fill=(230, 160, 40))   # brim tilting back
# face: big grin + happy closed eyes
ey = hd_cy + hd_r * 0.15
for ex in (-0.42, 0.42):
    d.arc(scaled(hd_cx + ex * hd_r - 0.20 * hd_r, ey - 0.18 * hd_r,
                 hd_cx + ex * hd_r + 0.20 * hd_r, ey + 0.18 * hd_r),
          start=200, end=340, fill=(120, 70, 40), width=4 * S)
d.arc(scaled(hd_cx - 0.35 * hd_r, ey + 0.20 * hd_r,
             hd_cx + 0.35 * hd_r, ey + 0.75 * hd_r),
      start=0, end=180, fill=(120, 70, 40), width=4 * S)
# blush
for ex in (-0.68, 0.68):
    d.ellipse(scaled(hd_cx + ex * hd_r - 0.14 * hd_r, ey + 0.15 * hd_r,
                     hd_cx + ex * hd_r + 0.14 * hd_r, ey + 0.30 * hd_r),
              fill=(240, 140, 100))
# arm reaching to the table, holding a tiny cup (thick, connected shoulder-to-hand)
d.line(scaled(wk_cx + 0.07 * W, wk_cy + 0.06 * H,
              table_x - 0.01 * W, table_y + 0.02 * H),
       fill=(224, 122, 72), width=30 * S)
d.ellipse(scaled(table_x - 0.030 * W, table_y - 0.010 * H,
                 table_x + 0.005 * W, table_y + 0.025 * H),
          fill=(238, 178, 122))                              # hand on the table

# --- little girl on the right, sitting on a small stool -------------------
g_cx, g_cy = 0.86 * W, 0.54 * H
d.ellipse(scaled(g_cx - 0.055 * W, g_cy, g_cx + 0.055 * W, g_cy + 0.20 * H),
          fill=(255, 170, 140))                              # dress, warm pink
d.ellipse(scaled(g_cx - 0.038 * W, g_cy - 0.055 * H,
                 g_cx + 0.038 * W, g_cy + 0.020 * H), fill=(238, 178, 122))
# hair: dark brown cap + pigtails
d.chord(scaled(g_cx - 0.042 * W, g_cy - 0.062 * H,
               g_cx + 0.042 * W, g_cy - 0.005 * H),
        start=180, end=360, fill=(140, 84, 48))
for ex in (-0.045, 0.045):
    d.ellipse(scaled(g_cx + ex * W - 0.014 * W, g_cy - 0.045 * H,
                     g_cx + ex * W + 0.014 * W, g_cy - 0.010 * H),
              fill=(140, 84, 48))
# laughing face: closed happy eyes + wide open laugh (mouth open, tongue)
gey = g_cy - 0.012 * H
for ex in (-0.42, 0.42):
    d.arc(scaled(g_cx + ex * 0.038 * W - 0.010 * W, gey - 0.008 * H,
                 g_cx + ex * 0.038 * W + 0.010 * W, gey + 0.008 * H),
          start=200, end=340, fill=(120, 70, 40), width=3 * S)
d.chord(scaled(g_cx - 0.016 * W, gey + 0.006 * H,
               g_cx + 0.016 * W, gey + 0.034 * H),
        start=0, end=180, fill=(150, 50, 40))                # open laugh
d.chord(scaled(g_cx - 0.010 * W, gey + 0.018 * H,
               g_cx + 0.010 * W, gey + 0.034 * H),
        start=0, end=180, fill=(255, 120, 110))              # tongue
# blush
for ex in (-0.72, 0.72):
    d.ellipse(scaled(g_cx + ex * 0.038 * W - 0.007 * W, gey + 0.006 * H,
                     g_cx + ex * 0.038 * W + 0.007 * W, gey + 0.016 * H),
              fill=(255, 130, 120))
# arm pointing to the teapot (connected shoulder to table)
d.line(scaled(g_cx - 0.048 * W, g_cy + 0.045 * H,
              table_x + table_w + 0.01 * W, table_y + 0.02 * H),
       fill=(255, 170, 140), width=18 * S)
d.ellipse(scaled(table_x + table_w - 0.004 * W, table_y - 0.010 * H,
                 table_x + table_w + 0.028 * W, table_y + 0.025 * H),
          fill=(238, 178, 122))                              # hand on the table
# stool (under her, reaching the ground)
d.rectangle(scaled(g_cx - 0.055 * W, g_cy + 0.195 * H,
                   g_cx + 0.055 * W, g_cy + 0.222 * H), fill=(160, 92, 52))
d.rectangle(scaled(g_cx - 0.040 * W, g_cy + 0.222 * H,
                   g_cx - 0.028 * W, ground_y + 0.01 * H), fill=(146, 84, 48))
d.rectangle(scaled(g_cx + 0.028 * W, g_cy + 0.222 * H,
                   g_cx + 0.040 * W, ground_y + 0.01 * H), fill=(146, 84, 48))

# --- two floating hearts between them -------------------------------------
for hx, hy, hr in [(0.53 * W, 0.36 * H, 0.022 * W),
                   (0.60 * W, 0.28 * H, 0.016 * W)]:
    circ_r = hr * 0.55
    heart_top = hy - hr * 0.1
    for ex in (-circ_r, circ_r):
        d.ellipse(scaled(hx + ex - circ_r, heart_top - circ_r,
                         hx + ex + circ_r, heart_top + circ_r),
                  fill=(255, 80, 80))
    d.polygon(scaled(hx - circ_r * 1.85, heart_top,
                     hx + circ_r * 1.85, heart_top,
                     hx, hy + hr * 1.0), fill=(255, 80, 80))

# --- downscale -------------------------------------------------------------
img = img.resize((W, H), Image.LANCZOS)
img.save("entry.png", optimize=True)
print("entry.png", os.path.getsize("entry.png"), "bytes")

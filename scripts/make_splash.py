#!/usr/bin/env python3
"""
Build the Oscilite boot splash for the 160x128 ST7735 TFT.

Outputs:
  assets/images/splash.png         - 160x128 exact-size preview
  assets/images/splash_readme.png  - 6x upscaled (nearest) crisp preview for the README
  Core/Inc/splash.h                - RGB565 C array `logo[20480]` drawn by ui.c: splash()

Optional logo:
  If assets/images/logo.png exists it is used as the top icon.
  Otherwise a built-in phosphor-waveform mark is drawn.

Usage:
  python3 scripts/make_splash.py            # date = today
  python3 scripts/make_splash.py 2026-07-12 # pin a date
"""
import os
import sys
from datetime import date, datetime

from PIL import Image, ImageDraw, ImageFont

# ---- config ---------------------------------------------------------------
W, H = 160, 128

BG      = (10, 14, 20)      # #0A0E14 charcoal
GRID    = (24, 34, 46)      # faint graticule
GREEN   = (57, 255, 20)     # #39FF14 phosphor
CYAN    = (90, 220, 235)
WHITE   = (235, 240, 245)
GREY    = (120, 135, 150)

TITLE   = "OSCILITE"
DESC    = "DIGITAL OSCILLOSCOPE"
NAME    = "st4rk"

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO   = os.path.join(ROOT, "assets", "images", "logo.png")
OUT    = os.path.join(ROOT, "assets", "images", "splash.png")
OUTBIG = os.path.join(ROOT, "assets", "images", "splash_readme.png")
HDR    = os.path.join(ROOT, "Core", "Inc", "splash.h")

FONT_DIR = "/usr/share/fonts/TTF"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_TITLE = font("JetBrainsMono-ExtraBold.ttf", 22)
F_DESC  = font("JetBrainsMono-Regular.ttf", 8)
F_FOOT  = font("JetBrainsMono-Bold.ttf", 9)


def centered(draw, y, text, fnt, fill, tracking=0):
    """Draw text horizontally centered at vertical y. tracking = extra px per gap."""
    if tracking == 0:
        w = draw.textlength(text, font=fnt)
        draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
        return
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (W - total) / 2
    for c, cw in zip(text, widths):
        draw.text((x, y), c, font=fnt, fill=fill)
        x += cw + tracking


def draw_grid(d):
    for x in range(0, W, 16):
        d.line([(x, 0), (x, H)], fill=GRID)
    for y in range(0, H, 16):
        d.line([(0, y), (W, y)], fill=GRID)


def builtin_mark(size=40):
    """Hand-drawn oscilloscope logo — sine wave on graticule inside rounded badge."""
    import math

    # Work at 4x then downsample for anti-aliased, crisp result
    S = size * 4
    m = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dd = ImageDraw.Draw(m)
    pad = S // 20  # border padding

    # --- Background fill with rounded rect ---
    dd.rounded_rectangle(
        [pad, pad, S - pad, S - pad],
        radius=S // 5, fill=BG, outline=CYAN, width=max(3, S // 40)
    )

    # --- Graticule grid (subtle) ---
    inner_l = pad + S // 12
    inner_r = S - pad - S // 12
    inner_t = pad + S // 12
    inner_b = S - pad - S // 12
    grid_col = (30, 44, 58)
    steps = 4
    for i in range(steps + 1):
        # vertical
        x = inner_l + (inner_r - inner_l) * i / steps
        dd.line([(x, inner_t), (x, inner_b)], fill=grid_col, width=max(1, S // 80))
        # horizontal
        y = inner_t + (inner_b - inner_t) * i / steps
        dd.line([(inner_l, y), (inner_r, y)], fill=grid_col, width=max(1, S // 80))

    # --- Center crosshair (slightly brighter) ---
    cx = S // 2
    cy = S // 2
    cross_col = (45, 60, 80)
    dd.line([(inner_l, cy), (inner_r, cy)], fill=cross_col, width=max(2, S // 60))
    dd.line([(cx, inner_t), (cx, inner_b)], fill=cross_col, width=max(2, S // 60))

    # --- Tick marks on center cross ---
    tick_len = S // 40
    tick_col = (55, 75, 95)
    for i in range(steps * 5 + 1):
        x = inner_l + (inner_r - inner_l) * i / (steps * 5)
        dd.line([(x, cy - tick_len), (x, cy + tick_len)], fill=tick_col, width=max(1, S // 120))
        y = inner_t + (inner_b - inner_t) * i / (steps * 5)
        dd.line([(cx - tick_len, y), (cx + tick_len, y)], fill=tick_col, width=max(1, S // 120))

    # --- Sine wave (phosphor green, glowing) ---
    wave_l = inner_l + S // 20
    wave_r = inner_r - S // 20
    wave_cy = cy
    amp = (inner_b - inner_t) * 0.32

    # Glow layer (wider, dimmer)
    glow_col = (20, 100, 8)
    glow_pts = []
    for px in range(wave_l, wave_r + 1):
        t = (px - wave_l) / (wave_r - wave_l)
        py = wave_cy - math.sin(t * 2.5 * math.pi) * amp
        glow_pts.append((px, py))
    dd.line(glow_pts, fill=glow_col, width=max(8, S // 16), joint="curve")

    # Main wave
    pts = []
    for px in range(wave_l, wave_r + 1):
        t = (px - wave_l) / (wave_r - wave_l)
        py = wave_cy - math.sin(t * 2.5 * math.pi) * amp
        pts.append((px, py))
    dd.line(pts, fill=GREEN, width=max(4, S // 28), joint="curve")

    # Bright core (thinner, whiter green)
    core_col = (140, 255, 100)
    dd.line(pts, fill=core_col, width=max(2, S // 60), joint="curve")

    # --- Downsample with high-quality filter ---
    m = m.resize((size, size), Image.LANCZOS)

    # Convert to RGB on BG
    bg = Image.new("RGB", (size, size), BG)
    bg.paste(m, mask=m.split()[3])
    return bg


def load_logo(target_h=42):
    if os.path.exists(LOGO):
        lg = Image.open(LOGO).convert("RGB")
        w = int(lg.width * target_h / lg.height)
        return lg.resize((w, target_h), Image.LANCZOS)
    return builtin_mark(target_h)


def build(the_date):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_grid(d)

    # logo, top-centered
    logo = load_logo(target_h=40)
    img.paste(logo, (int((W - logo.width) / 2), 6))

    # title
    centered(d, 50, TITLE, F_TITLE, GREEN, tracking=1)

    # description
    centered(d, 78, DESC, F_DESC, CYAN, tracking=2)

    # divider
    d.line([(30, 96), (W - 30, 96)], fill=GRID)

    # footer: name + date
    centered(d, 104, NAME, F_FOOT, WHITE, tracking=1)
    centered(d, 116, the_date.strftime("%d %b %Y").upper(), F_DESC, GREY, tracking=1)

    return img


def write_header(img):
    px = img.load()
    with open(HDR, "w") as f:
        f.write("#ifndef __SPLASH_H\n#define __SPLASH_H\n\n#include <stdint.h>\n\n")
        f.write(f"const uint16_t logo[{W*H}] = {{\n")
        count = 0
        for y in range(H):
            for x in range(W):
                r, g, b = px[x, y]
                rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
                f.write(f"0x{rgb565:04X}, ")
                count += 1
                if count % 16 == 0:
                    f.write("\n")
        f.write("};\n\n#endif\n")


def main():
    if len(sys.argv) > 1:
        the_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    else:
        the_date = date.today()

    img = build(the_date)
    img.save(OUT)
    img.resize((W * 6, H * 6), Image.NEAREST).save(OUTBIG)
    write_header(img)

    src = "logo.png" if os.path.exists(LOGO) else "built-in waveform mark"
    print(f"OK  logo source : {src}")
    print(f"OK  date        : {the_date.isoformat()}")
    print(f"OK  {OUT}")
    print(f"OK  {OUTBIG}")
    print(f"OK  {HDR}")


if __name__ == "__main__":
    main()

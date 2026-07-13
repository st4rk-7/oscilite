#!/usr/bin/env python3
"""
Build the Oscilite boot splash for the 160x128 ST7735 TFT.

Layout: oscilloscope grid background, big ASCII-art "OSCILITE" text,
small tagline, author name, and date.

Outputs:
  assets/images/splash.png         - 160x128 exact-size preview
  assets/images/splash_readme.png  - 6x upscaled (nearest) crisp preview for README
  Core/Inc/splash.h                - RGB565 C array `logo[20480]` drawn by ui.c splash()

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
GRID    = (24, 34, 46)      # faint graticule lines
GREEN   = (57, 255, 20)     # #39FF14 phosphor
CYAN    = (90, 220, 235)
WHITE   = (235, 240, 245)
GREY    = (120, 135, 150)
DIM     = (40, 55, 70)

NAME    = "st4rk"

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT    = os.path.join(ROOT, "assets", "images", "splash.png")
OUTBIG = os.path.join(ROOT, "assets", "images", "splash_readme.png")
HDR    = os.path.join(ROOT, "Core", "Inc", "splash.h")

FONT_DIR = "/usr/share/fonts/TTF"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

# ---- ASCII art block letters for OSCILITE ---------------------------------
# Each letter is a list of strings, 5 chars wide, 7 rows tall
LETTERS = {
    'O': [
        " ### ",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        " ### ",
    ],
    'S': [
        " ### ",
        "#   #",
        "#    ",
        " ### ",
        "    #",
        "#   #",
        " ### ",
    ],
    'C': [
        " ### ",
        "#   #",
        "#    ",
        "#    ",
        "#    ",
        "#   #",
        " ### ",
    ],
    'I': [
        " ### ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        " ### ",
    ],
    'L': [
        "#    ",
        "#    ",
        "#    ",
        "#    ",
        "#    ",
        "#    ",
        "#####",
    ],
    'T': [
        "#####",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
    ],
    'E': [
        "#####",
        "#    ",
        "#    ",
        "#### ",
        "#    ",
        "#    ",
        "#####",
    ],
}


def draw_grid(d):
    """Subtle oscilloscope graticule background."""
    for x in range(0, W, 16):
        d.line([(x, 0), (x, H)], fill=GRID)
    for y in range(0, H, 16):
        d.line([(0, y), (W, y)], fill=GRID)


def draw_ascii_text(img, text, top_y, pixel_size=2, color=GREEN, glow_color=(20, 80, 10)):
    """Render block-letter ASCII art onto the image."""
    d = ImageDraw.Draw(img)

    # Build the full bitmap grid from letter definitions
    rows = 7
    cols_per_char = 5
    gap = 1  # 1-column gap between letters
    total_cols = len(text) * cols_per_char + (len(text) - 1) * gap

    # Center horizontally
    total_w = total_cols * pixel_size
    start_x = (W - total_w) // 2

    for row in range(rows):
        col_offset = 0
        for ci, ch in enumerate(text):
            letter = LETTERS.get(ch, LETTERS['O'])
            line = letter[row]
            for c in range(cols_per_char):
                if c < len(line) and line[c] == '#':
                    x = start_x + (col_offset + c) * pixel_size
                    y = top_y + row * pixel_size
                    # Glow (1px border around each block)
                    d.rectangle(
                        [x - 1, y - 1, x + pixel_size, y + pixel_size],
                        fill=glow_color
                    )
                    # Main pixel block
                    d.rectangle(
                        [x, y, x + pixel_size - 1, y + pixel_size - 1],
                        fill=color
                    )
            col_offset += cols_per_char + gap


def centered(draw, y, text, fnt, fill, tracking=0):
    """Draw text horizontally centered at vertical y."""
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


def build(the_date):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Background grid
    draw_grid(d)

    # Top decorative line
    d.line([(10, 8), (W - 10, 8)], fill=DIM)

    # ASCII art "OSCILITE" — big, centered
    draw_ascii_text(img, "OSCILITE", top_y=16, pixel_size=2, color=GREEN)

    # Tagline
    f_desc = font("JetBrainsMono-Regular.ttf", 8)
    centered(d, 36, "DIGITAL OSCILLOSCOPE", f_desc, CYAN, tracking=1)

    # Separator
    d.line([(30, 52), (W - 30, 52)], fill=DIM)

    # Second ASCII block — smaller, just "OSCILITE" again as decorative repeat
    # Actually let's put a small sine wave decoration instead
    import math
    wave_y = 62
    pts = []
    for px in range(20, W - 20):
        t = (px - 20) / (W - 40)
        py = wave_y - math.sin(t * 3 * math.pi) * 6
        pts.append((px, py))
    # Glow
    d.line(pts, fill=(15, 60, 5), width=4, joint="curve")
    # Main
    d.line(pts, fill=GREEN, width=1, joint="curve")

    # Separator
    d.line([(30, 78), (W - 30, 78)], fill=DIM)

    # Author
    f_name = font("JetBrainsMono-Bold.ttf", 12)
    centered(d, 84, NAME, f_name, WHITE, tracking=2)

    # Date
    f_date = font("JetBrainsMono-Regular.ttf", 9)
    centered(d, 102, the_date.strftime("%d %b %Y").upper(), f_date, GREY, tracking=1)

    # Bottom decorative line
    d.line([(10, 120), (W - 10, 120)], fill=DIM)

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

    print(f"OK  date : {the_date.isoformat()}")
    print(f"OK  {OUT}")
    print(f"OK  {OUTBIG}")
    print(f"OK  {HDR}")


if __name__ == "__main__":
    main()

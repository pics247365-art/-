#!/usr/bin/env python3
"""
Generate 7 square (1080x1080) BOLD / HIGH-IMPACT motivational images.
Style: loud, high-contrast, graphic, typographic dominance — meant to stop the scroll.
"""

import os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "/home/user/-/social_images/output_square"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1080, 1080

FONT_BOLD   = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG    = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"

# Accent palettes: (bg_dark, accent, text_main)
PALETTES = [
    {"bg": (0, 0, 0),       "accent": (230, 57, 70),   "text": (255, 255, 255)},   # Red
    {"bg": (6, 6, 10),      "accent": (247, 201, 72),  "text": (255, 255, 255)},   # Gold
    {"bg": (0, 0, 0),       "accent": (255, 255, 255), "text": (255, 255, 255)},   # Pure white
    {"bg": (8, 8, 8),       "accent": (0, 200, 150),   "text": (255, 255, 255)},   # Teal
    {"bg": (0, 0, 0),       "accent": (230, 57, 70),   "text": (255, 255, 255)},   # Red
    {"bg": (5, 5, 5),       "accent": (247, 201, 72),  "text": (255, 255, 255)},   # Gold
    {"bg": (0, 0, 0),       "accent": (255, 255, 255), "text": (255, 255, 255)},   # White
]

# 7 loud/punchy quotes — designed for square impact
QUOTES = [
    {
        "big": "STOP\nPLAYING\nIT SAFE.",
        "sub": "No one remembers the careful ones.",
        "style": "big_stack",     # Stacked huge text
    },
    {
        "big": "EITHER YOU\nRUN THE DAY",
        "sub": "— or the day runs you.",
        "style": "split_block",   # Big text + accent block bottom
    },
    {
        "big": "ONE DECISION\nCAN CHANGE\nEVERYTHING.",
        "sub": "Make it.",
        "style": "big_stack",
    },
    {
        "big": "THEY SLEPT.\nYOU WORKED.",
        "sub": "That's why it's different.",
        "style": "two_line_bold",  # Two lines contrast
    },
    {
        "big": "DON'T WISH\nIT WAS EASIER.",
        "sub": "Wish you were stronger.",
        "style": "split_block",
    },
    {
        "big": "YOUR FUTURE\nSELF IS\nWATCHING.",
        "sub": "Choose who they become.",
        "style": "big_stack",
    },
    {
        "big": "THE GRIND\nDOESN'T LIE.",
        "sub": "Only people do.",
        "style": "two_line_bold",
    },
]


def add_grain(img, intensity=22):
    pixels = img.load()
    w, h = img.size
    for _ in range(int(w * h * 0.25)):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        r, g, b = pixels[x, y]
        n = random.randint(-intensity, intensity)
        pixels[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return img


def make_dark_bg(w, h, bg_color, accent, style):
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)

    if style == "big_stack":
        # Subtle diagonal texture lines
        for i in range(-h, w + h, 28):
            c = random.randint(12, 26)
            draw.line([(i, 0), (i + h, h)], fill=(c, c, c), width=1)
        # Accent bar on left edge
        draw.rectangle([0, 0, 14, h], fill=accent)
        # Accent bar on bottom
        draw.rectangle([0, h - 14, w, h], fill=accent)

    elif style == "split_block":
        # Bottom accent block (30% of height)
        block_y = int(h * 0.72)
        draw.rectangle([0, block_y, w, h], fill=accent)
        # Subtle top noise
        for i in range(-h, w + h, 36):
            c = random.randint(10, 22)
            draw.line([(i, 0), (i + h // 2, h // 2)], fill=(c, c, c), width=1)

    elif style == "two_line_bold":
        # Horizontal split: top half dark, a thick white line divider
        divider_y = int(h * 0.5)
        draw.rectangle([0, divider_y - 6, w, divider_y + 6], fill=accent)
        # Accent dot corners
        dot_r = 22
        for (cx, cy) in [(dot_r, dot_r), (w - dot_r, dot_r), (dot_r, h - dot_r), (w - dot_r, h - dot_r)]:
            draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=accent)

    # Motion blur streaks in upper area
    for _ in range(45):
        x1 = random.randint(0, w)
        y1 = random.randint(0, int(h * 0.5))
        length = random.randint(40, 180)
        angle = random.uniform(-8, 8)
        dx = math.cos(math.radians(angle)) * length
        dy = math.sin(math.radians(angle)) * length
        c = random.randint(18, 50)
        draw.line([(x1, y1), (x1 + dx, y1 + dy)], fill=(c, c, c), width=random.randint(1, 6))

    img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
    img = add_grain(img, intensity=20)
    return img


def get_font(size, bold=True):
    try:
        path = FONT_BOLD if bold else FONT_REG
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def measure_text(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0], bb[3] - bb[1]


def draw_big_stack(draw, img_w, img_h, quote, pal):
    """Huge stacked ALL-CAPS text filling most of the image."""
    lines = quote["big"].split("\n")
    sub = quote["sub"]
    margin = 72

    # Find font size that makes longest line fit
    target_w = img_w - margin * 2
    font_size = 160
    while font_size > 60:
        f = get_font(font_size)
        max_line_w = max(measure_text(draw, l, f)[0] for l in lines)
        if max_line_w <= target_w:
            break
        font_size -= 4

    f = get_font(font_size)
    lh = int(font_size * 1.08)

    total_h = lh * len(lines)
    y_start = (img_h - total_h) // 2 - 60

    for i, line in enumerate(lines):
        lw, _ = measure_text(draw, line, f)
        x = margin
        # Alternate: first word accent color, rest white
        words = line.split()
        cx = x
        for j, word in enumerate(words):
            color = pal["accent"] if j == 0 and i == 0 else pal["text"]
            draw.text((cx, y_start + i * lh), word, font=f, fill=color)
            ww, _ = measure_text(draw, word + " ", f)
            cx += ww

    # Sub line below
    sub_f = get_font(46, bold=False)
    sub_y = y_start + lh * len(lines) + 40
    draw.text((margin, sub_y), sub, font=sub_f, fill=(180, 180, 180))


def draw_split_block(draw, img_w, img_h, quote, pal):
    """Top half: big text. Bottom accent block: sub text."""
    lines = quote["big"].split("\n")
    sub = quote["sub"]
    margin = 72
    block_y = int(img_h * 0.72)

    target_w = img_w - margin * 2
    font_size = 150
    while font_size > 55:
        f = get_font(font_size)
        max_line_w = max(measure_text(draw, l, f)[0] for l in lines)
        if max_line_w <= target_w:
            break
        font_size -= 4

    f = get_font(font_size)
    lh = int(font_size * 1.1)

    total_h = lh * len(lines)
    y_start = (block_y - total_h) // 2

    for i, line in enumerate(lines):
        draw.text((margin, y_start + i * lh), line, font=f, fill=pal["text"])

    # Sub text inside accent block
    sub_f = get_font(52, bold=True)
    sub_color = (0, 0, 0) if pal["accent"] != (255, 255, 255) else (30, 30, 30)
    sub_y = block_y + (img_h - block_y - 70) // 2
    draw.text((margin, sub_y), sub, font=sub_f, fill=sub_color)


def draw_two_line_bold(draw, img_w, img_h, quote, pal):
    """Two strong lines, one above and one below the accent divider."""
    lines = quote["big"].split("\n")
    sub = quote["sub"]
    margin = 72
    divider_y = int(img_h * 0.5)

    target_w = img_w - margin * 2
    font_size = 145
    while font_size > 55:
        f = get_font(font_size)
        max_line_w = max(measure_text(draw, l, f)[0] for l in lines)
        if max_line_w <= target_w:
            break
        font_size -= 4

    f = get_font(font_size)
    lh = int(font_size * 1.1)

    # Place lines evenly split around the divider
    half = len(lines) // 2
    top_lines = lines[:max(1, half)]
    bot_lines = lines[max(1, half):]

    # Top section
    top_total = lh * len(top_lines)
    ty = divider_y - 30 - top_total
    for i, line in enumerate(top_lines):
        draw.text((margin, ty + i * lh), line, font=f, fill=pal["text"])

    # Bottom section
    by = divider_y + 30
    for i, line in enumerate(bot_lines):
        color = pal["accent"] if i == 0 else pal["text"]
        draw.text((margin, by + i * lh), line, font=f, fill=color)

    # Sub line at bottom
    sub_f = get_font(44, bold=False)
    sub_y = img_h - 110
    draw.text((margin, sub_y), sub, font=sub_f, fill=(170, 170, 170))


def generate_image(idx, quote, palette):
    style = quote["style"]
    img = make_dark_bg(W, H, palette["bg"], palette["accent"], style)
    draw = ImageDraw.Draw(img)

    if style == "big_stack":
        draw_big_stack(draw, W, H, quote, palette)
    elif style == "split_block":
        draw_split_block(draw, W, H, quote, palette)
    elif style == "two_line_bold":
        draw_two_line_bold(draw, W, H, quote, palette)

    # Small bottom-right index mark
    idx_f = get_font(34, bold=False)
    draw.text((W - 80, H - 60), f"{idx:02d}", font=idx_f, fill=(55, 55, 55))

    out = os.path.join(OUTPUT_DIR, f"square_{idx:02d}.jpg")
    img.save(out, "JPEG", quality=96)
    print(f"  [{idx:02d}] {out}")
    return out


if __name__ == "__main__":
    print(f"Generating {len(QUOTES)} bold square images (1080x1080)...")
    for i, (q, p) in enumerate(zip(QUOTES, PALETTES)):
        generate_image(i + 1, q, p)
    print("\nDone!")

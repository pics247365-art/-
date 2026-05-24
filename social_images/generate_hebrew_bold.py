#!/usr/bin/env python3
"""
7 bold Hebrew social images (1080x1080) — loud, striking, RTL.
Backgrounds: raw concrete, glitch lines, brutal geometry, fire gradient.
"""

import os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

OUTPUT_DIR = "/home/user/-/social_images/output_hebrew"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1080, 1080

HEB_BOLD   = "/usr/share/fonts/truetype/culmus/MiriamCLM-Bold.ttf"
HEB_SIMPLE = "/usr/share/fonts/truetype/culmus/SimpleCLM-Bold.ttf"
HEB_KETER  = "/usr/share/fonts/truetype/culmus/KeterYG-Bold.ttf"
LAT_BOLD   = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def hfont(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.truetype(HEB_BOLD, size)


# ── 7 quotes ──────────────────────────────────────────────────────────────────
QUOTES = [
    {
        "main":    "אתה לא נולד\nכדי להיות בינוני.",
        "sub":     "הפסק להתנצל על השאפתיות שלך.",
        "font_path": HEB_BOLD,
        "bg":      "concrete_red",
        "accent":  (220, 38, 38),
        "layout":  "full_bleed",
    },
    {
        "main":    "הם ישנו.\nאתה עבדת.",
        "sub":     "לכן זה שונה.",
        "font_path": HEB_BOLD,
        "bg":      "brutal_gold",
        "accent":  (245, 197, 24),
        "layout":  "split_bottom",
    },
    {
        "main":    "הפחד\nלא הולך לעזוב.",
        "sub":     "תתחיל בלעדיו.",
        "font_path": HEB_KETER,
        "bg":      "glitch_dark",
        "accent":  (255, 255, 255),
        "layout":  "center_punch",
    },
    {
        "main":    "רק אחד\nמחליט כאן.",
        "sub":     "ואתה יודע מי זה.",
        "font_path": HEB_BOLD,
        "bg":      "fire_gradient",
        "accent":  (255, 100, 0),
        "layout":  "full_bleed",
    },
    {
        "main":    "הצלחה היא\nלא מזל.",
        "sub":     "היא הרגל שחזרת עליו כשאף אחד לא ראה.",
        "font_path": HEB_SIMPLE,
        "bg":      "concrete_white",
        "accent":  (10, 10, 10),
        "layout":  "light_punch",
    },
    {
        "main":    "תפסיק לחכות\nלרגע הנכון.",
        "sub":     "הרגע הנכון הוא עכשיו.",
        "font_path": HEB_BOLD,
        "bg":      "brutal_gold",
        "accent":  (245, 197, 24),
        "layout":  "split_bottom",
    },
    {
        "main":    "הכאב הזה\nזמני.",
        "sub":     "הוויתור — קבוע.",
        "font_path": HEB_KETER,
        "bg":      "glitch_dark",
        "accent":  (220, 38, 38),
        "layout":  "center_punch",
    },
]


# ── Background generators ─────────────────────────────────────────────────────

def bg_concrete_red(w, h):
    img = Image.new("RGB", (w, h), (12, 10, 10))
    draw = ImageDraw.Draw(img)
    for _ in range(3000):
        x = random.randint(0, w)
        y = random.randint(0, h)
        l = random.randint(5, 60)
        a = random.uniform(0, 360)
        dx, dy = math.cos(math.radians(a)) * l, math.sin(math.radians(a)) * l
        c = random.randint(20, 45)
        draw.line([(x, y), (x+dx, y+dy)], fill=(c, c, c), width=1)
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    draw = ImageDraw.Draw(img)          # fresh draw after filter
    draw.polygon([(0, h*0.72), (w, h*0.62), (w, h*0.72+8), (0, h*0.82)],
                 fill=(220, 38, 38))
    draw.rectangle([0, 0, 18, h], fill=(220, 38, 38))
    return img

def bg_brutal_gold(w, h):
    img = Image.new("RGB", (w, h), (8, 8, 8))
    draw = ImageDraw.Draw(img)
    for i in range(-h, w+h, 22):
        c = random.randint(14, 32)
        draw.line([(i, 0), (i+h, h)], fill=(c, c, c), width=random.randint(1,4))
    img = img.filter(ImageFilter.GaussianBlur(0.8))
    draw = ImageDraw.Draw(img)          # fresh draw after filter
    by = int(h * 0.68)
    draw.rectangle([0, by, w, h], fill=(245, 197, 24))
    draw.rectangle([0, by - 8, w, by], fill=(255, 220, 60))
    return img

def bg_glitch_dark(w, h):
    img = Image.new("RGB", (w, h), (4, 4, 6))
    draw = ImageDraw.Draw(img)
    for _ in range(60):
        y = random.randint(0, h)
        thickness = random.randint(1, 12)
        c = random.randint(18, 70)
        offset = random.randint(-80, 80)
        draw.rectangle([0+offset, y, w+offset, y+thickness], fill=(c, c, c))
    for _ in range(8):
        x = random.randint(0, w)
        c_val = random.choice([(80,0,0),(0,0,80),(60,60,60)])
        draw.line([(x, 0), (x, h)], fill=c_val, width=random.randint(1,3))
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    draw = ImageDraw.Draw(img)          # fresh draw after filter
    dy = int(h * 0.50)
    draw.rectangle([0, dy, w, dy + 10], fill=(255, 255, 255))
    return img

def bg_fire_gradient(w, h):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        # Deep red → dark orange → black
        if t < 0.5:
            r = int(160 + (1-t*2) * 60)
            g = int(t * 2 * 40)
            b = 0
        else:
            r = int(80 * (1-(t-0.5)*2))
            g = int(40 * (1-(t-0.5)*2))
            b = 0
        draw.line([(0,y),(w,y)], fill=(r, g, b))
    # Fire streaks
    for _ in range(120):
        x1 = random.randint(0, w)
        y1 = random.randint(int(h*0.2), h)
        l = random.randint(30, 200)
        dy_ = random.randint(-l, -l//3)
        dx_ = random.randint(-30, 30)
        brightness = random.randint(30, 90)
        draw.line([(x1, y1), (x1+dx_, y1+dy_)],
                  fill=(255, brightness, 0), width=random.randint(1, 5))
    img = img.filter(ImageFilter.GaussianBlur(3))
    # Dark overlay on top half
    overlay = Image.new("RGBA", (w, h), (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    for y in range(int(h * 0.6)):
        alpha = int(180 * (1 - y / (h*0.6)))
        od.line([(0,y),(w,y)], fill=(0,0,0,alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    return img

def bg_concrete_white(w, h):
    img = Image.new("RGB", (w, h), (230, 228, 222))
    draw = ImageDraw.Draw(img)
    for _ in range(2000):
        x, y = random.randint(0,w), random.randint(0,h)
        l = random.randint(3, 40)
        a = random.uniform(0, 360)
        dx, dy = math.cos(math.radians(a))*l, math.sin(math.radians(a))*l
        c = random.randint(190, 215)
        draw.line([(x,y),(x+dx,y+dy)], fill=(c,c,c), width=1)
    img = img.filter(ImageFilter.GaussianBlur(0.5))
    # Black accent bar right edge
    draw.rectangle([w-20, 0, w, h], fill=(10, 10, 10))
    # Black bar top
    draw.rectangle([0, 0, w, 20], fill=(10, 10, 10))
    return img

BG_FUNCS = {
    "concrete_red":   bg_concrete_red,
    "brutal_gold":    bg_brutal_gold,
    "glitch_dark":    bg_glitch_dark,
    "fire_gradient":  bg_fire_gradient,
    "concrete_white": bg_concrete_white,
}

def make_bg(name):
    return BG_FUNCS[name](W, H)

def add_grain(img, strength=18):
    px = img.load()
    w, h = img.size
    for _ in range(int(w * h * 0.2)):
        x, y = random.randint(0, w-1), random.randint(0, h-1)
        r, g, b = px[x, y]
        n = random.randint(-strength, strength)
        px[x, y] = (max(0,min(255,r+n)), max(0,min(255,g+n)), max(0,min(255,b+n)))
    return img


# ── RTL text utilities ─────────────────────────────────────────────────────────

def rtl_wrap(text, font, max_w, draw):
    """Wrap Hebrew text to lines fitting max_w, keep RTL word order."""
    words = text.split()
    lines, cur = [], []
    for word in words:
        test = " ".join(cur + [word])
        bb = draw.textbbox((0,0), test, font=font)
        if cur and (bb[2]-bb[0]) > max_w:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))
    return lines

def draw_rtl_line(draw, text, x_right, y, font, fill):
    """Draw one RTL line right-aligned at x_right."""
    vis = text
    bb = draw.textbbox((0, 0), vis, font=font)
    tw = bb[2] - bb[0]
    draw.text((x_right - tw, y), vis, font=font, fill=fill)


# ── Layout renderers ──────────────────────────────────────────────────────────

def layout_full_bleed(draw, quote, is_dark_bg=True):
    """Huge text centered-ish, sub at bottom."""
    margin = 70
    x_right = W - margin

    txt_color  = (255,255,255) if is_dark_bg else (10,10,10)
    sub_color  = (200,200,200) if is_dark_bg else (60,60,60)
    accent     = quote["accent"]
    font_path  = quote["font_path"]

    # Auto-fit font size
    lines_raw = quote["main"].split("\n")
    size = 195
    while size > 60:
        f = hfont(font_path, size)
        max_w = max(draw.textbbox((0,0), l, font=f)[2] for l in lines_raw)
        if max_w <= W - margin * 2:
            break
        size -= 5
    f = hfont(font_path, size)
    lh = int(size * 1.12)
    total_h = lh * len(lines_raw)
    y0 = (H - total_h) // 2 - 60

    for i, line in enumerate(lines_raw):
        color = accent if i == 0 else txt_color
        draw_rtl_line(draw, line, x_right, y0 + i*lh, f, color)

    # Sub
    sf = hfont(font_path, 50)
    sub_lines = rtl_wrap(quote["sub"], sf, W - margin*2, draw)
    sy = y0 + total_h + 50
    for sl in sub_lines:
        draw_rtl_line(draw, sl, x_right, sy, sf, sub_color)
        sy += 62


def layout_split_bottom(draw, quote, is_dark_bg=True):
    """Big text in dark zone, punch line inside accent block."""
    margin   = 70
    x_right  = W - margin
    block_y  = int(H * 0.68)
    txt_color = (255,255,255)
    font_path = quote["font_path"]
    accent    = quote["accent"]

    lines_raw = quote["main"].split("\n")
    size = 185
    while size > 55:
        f = hfont(font_path, size)
        max_w = max(draw.textbbox((0,0), l, font=f)[2] for l in lines_raw)
        if max_w <= W - margin*2:
            break
        size -= 5
    f = hfont(font_path, size)
    lh = int(size * 1.1)
    total_h = lh * len(lines_raw)
    y0 = (block_y - total_h) // 2

    for i, line in enumerate(lines_raw):
        draw_rtl_line(draw, line, x_right, y0 + i*lh, f, txt_color)

    # Sub inside block
    sf = hfont(font_path, 58)
    sub_color = (20, 20, 20)  # dark on gold block
    sy = block_y + (H - block_y - 75) // 2
    sub_lines = rtl_wrap(quote["sub"], sf, W - margin*2, draw)
    for sl in sub_lines:
        draw_rtl_line(draw, sl, x_right, sy, sf, sub_color)
        sy += 74


def layout_center_punch(draw, quote, is_dark_bg=True):
    """Two-section split at center line; accent color second line."""
    margin   = 70
    x_right  = W - margin
    font_path = quote["font_path"]
    accent    = quote["accent"]
    txt_color = (255,255,255)
    sub_color = (160,160,160)
    divider_y = int(H * 0.50)

    lines_raw = quote["main"].split("\n")
    size = 175
    while size > 55:
        f = hfont(font_path, size)
        max_w = max(draw.textbbox((0,0), l, font=f)[2] for l in lines_raw)
        if max_w <= W - margin*2:
            break
        size -= 5
    f = hfont(font_path, size)
    lh = int(size * 1.1)

    half = math.ceil(len(lines_raw) / 2)
    top_lines = lines_raw[:half]
    bot_lines = lines_raw[half:]

    # Top lines — above divider
    top_h = lh * len(top_lines)
    ty = divider_y - 30 - top_h
    for i, line in enumerate(top_lines):
        draw_rtl_line(draw, line, x_right, ty + i*lh, f, txt_color)

    # Bottom lines — below divider, accent color
    by = divider_y + 30
    for i, line in enumerate(bot_lines):
        draw_rtl_line(draw, line, x_right, by + i*lh, f, accent)

    # Sub at bottom
    sf = hfont(font_path, 50)
    sub_lines = rtl_wrap(quote["sub"], sf, W - margin*2, draw)
    sy = H - 160
    for sl in sub_lines:
        draw_rtl_line(draw, sl, x_right, sy, sf, sub_color)
        sy += 64


def layout_light_punch(draw, quote, is_dark_bg=False):
    """Light/concrete background — black text, accent outline elements."""
    margin   = 70
    x_right  = W - margin
    font_path = quote["font_path"]
    accent    = quote["accent"]

    lines_raw = quote["main"].split("\n")
    size = 190
    while size > 55:
        f = hfont(font_path, size)
        max_w = max(draw.textbbox((0,0), l, font=f)[2] for l in lines_raw)
        if max_w <= W - margin*2:
            break
        size -= 5
    f = hfont(font_path, size)
    lh = int(size * 1.1)
    total_h = lh * len(lines_raw)
    y0 = (H - total_h) // 2 - 70

    # Draw thick accent box behind first word
    for i, line in enumerate(lines_raw):
        col = (10,10,10) if i > 0 else accent
        draw_rtl_line(draw, line, x_right, y0 + i*lh, f, col)

    sf = hfont(font_path, 50)
    sub_lines = rtl_wrap(quote["sub"], sf, W - margin*2, draw)
    sy = y0 + total_h + 50
    for sl in sub_lines:
        draw_rtl_line(draw, sl, x_right, sy, sf, (60,60,60))
        sy += 64


# ── Main ──────────────────────────────────────────────────────────────────────

LAYOUT_MAP = {
    "full_bleed":   (layout_full_bleed,  True),
    "split_bottom": (layout_split_bottom, True),
    "center_punch": (layout_center_punch, True),
    "light_punch":  (layout_light_punch,  False),
}

def generate(idx, quote):
    img = make_bg(quote["bg"])
    img = add_grain(img, 16)
    draw = ImageDraw.Draw(img)

    fn, is_dark = LAYOUT_MAP[quote["layout"]]
    fn(draw, quote, is_dark)

    # Tiny index
    nf = hfont(LAT_BOLD, 34)
    draw.text((W - 70, H - 60), f"{idx:02d}", font=nf, fill=(55,55,55))

    out = os.path.join(OUTPUT_DIR, f"heb_{idx:02d}.jpg")
    img.save(out, "JPEG", quality=96)
    print(f"  [{idx:02d}] {out}")

if __name__ == "__main__":
    print(f"Generating {len(QUOTES)} Hebrew bold images (1080x1080)...")
    for i, q in enumerate(QUOTES):
        generate(i + 1, q)
    print("\nDone! →", OUTPUT_DIR)

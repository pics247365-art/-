#!/usr/bin/env python3
"""
7 Hebrew Stories images (1080x1920) — same quotes as square version,
adapted for vertical format with dramatic backgrounds.
"""

import os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "/home/user/-/social_images/output_hebrew_stories"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1080, 1920

HEB_BOLD   = "/usr/share/fonts/truetype/culmus/MiriamCLM-Bold.ttf"
HEB_SIMPLE = "/usr/share/fonts/truetype/culmus/SimpleCLM-Bold.ttf"
HEB_KETER  = "/usr/share/fonts/truetype/culmus/KeterYG-Bold.ttf"
LAT_BOLD   = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def hfont(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.truetype(HEB_BOLD, size)

QUOTES = [
    {
        "main":    "אתה לא נולד\nכדי להיות בינוני.",
        "sub":     "הפסק להתנצל על השאפתיות שלך.",
        "font":    HEB_BOLD,
        "accent":  (220, 38, 38),
        "bg":      "dark_concrete",
    },
    {
        "main":    "הם ישנו.\nאתה עבדת.",
        "sub":     "לכן זה שונה.",
        "font":    HEB_BOLD,
        "accent":  (245, 197, 24),
        "bg":      "diagonal_dark",
    },
    {
        "main":    "הפחד\nלא הולך לעזוב.",
        "sub":     "תתחיל בלעדיו.",
        "font":    HEB_KETER,
        "accent":  (255, 255, 255),
        "bg":      "glitch_vertical",
    },
    {
        "main":    "רק אחד\nמחליט כאן.",
        "sub":     "ואתה יודע מי זה.",
        "font":    HEB_BOLD,
        "accent":  (255, 100, 0),
        "bg":      "fire_vertical",
    },
    {
        "main":    "הצלחה היא\nלא מזל.",
        "sub":     "היא הרגל שחזרת עליו כשאף אחד לא ראה.",
        "font":    HEB_SIMPLE,
        "accent":  (220, 38, 38),
        "bg":      "dark_concrete",
    },
    {
        "main":    "תפסיק לחכות\nלרגע הנכון.",
        "sub":     "הרגע הנכון הוא עכשיו.",
        "font":    HEB_BOLD,
        "accent":  (245, 197, 24),
        "bg":      "diagonal_dark",
    },
    {
        "main":    "הכאב הזה\nזמני.",
        "sub":     "הוויתור — קבוע.",
        "font":    HEB_KETER,
        "accent":  (220, 38, 38),
        "bg":      "glitch_vertical",
    },
]


# ── Backgrounds ───────────────────────────────────────────────────────────────

def bg_dark_concrete(w, h, accent):
    img = Image.new("RGB", (w, h), (10, 10, 10))
    draw = ImageDraw.Draw(img)
    for _ in range(5000):
        x, y = random.randint(0, w), random.randint(0, h)
        l = random.randint(5, 80)
        a = random.uniform(0, 360)
        dx, dy = math.cos(math.radians(a))*l, math.sin(math.radians(a))*l
        c = random.randint(18, 40)
        draw.line([(x,y),(x+dx,y+dy)], fill=(c,c,c), width=1)
    img = img.filter(ImageFilter.GaussianBlur(0.5))
    draw = ImageDraw.Draw(img)
    # Accent: thick diagonal slash at bottom third
    by = int(h * 0.72)
    draw.polygon([(0, by), (w, by - int(h*0.04)),
                  (w, by + 22), (0, by + int(h*0.04) + 22)], fill=accent)
    # Thin vertical bar on right
    draw.rectangle([w - 20, 0, w, h], fill=accent)
    # Radial glow at center-top
    cx, cy = w // 2, int(h * 0.38)
    for r in range(350, 0, -6):
        alpha = int(18 * (1 - r/350))
        ar, ag, ab = accent
        draw.ellipse([cx-r, cy-r, cx+r, cy+r],
                     outline=(min(255,ar//3), min(255,ag//3), min(255,ab//3), alpha))
    return img

def bg_diagonal_dark(w, h, accent):
    img = Image.new("RGB", (w, h), (6, 6, 8))
    draw = ImageDraw.Draw(img)
    for i in range(-h, w+h, 28):
        c = random.randint(12, 30)
        draw.line([(i, 0), (i+h, h)], fill=(c,c,c), width=random.randint(1,5))
    img = img.filter(ImageFilter.GaussianBlur(0.8))
    draw = ImageDraw.Draw(img)
    # Gold/accent block at bottom 25%
    by = int(h * 0.75)
    draw.rectangle([0, by, w, h], fill=accent)
    draw.rectangle([0, by - 10, w, by], fill=tuple(min(255,c+30) for c in accent))
    return img

def bg_glitch_vertical(w, h, accent):
    img = Image.new("RGB", (w, h), (3, 3, 5))
    draw = ImageDraw.Draw(img)
    # Horizontal scan lines
    for _ in range(120):
        y = random.randint(0, h)
        thick = random.randint(1, 18)
        c = random.randint(15, 65)
        off = random.randint(-120, 120)
        draw.rectangle([0+off, y, w+off, y+thick], fill=(c,c,c))
    for _ in range(12):
        x = random.randint(0, w)
        draw.line([(x,0),(x,h)], fill=(40,40,60), width=random.randint(1,4))
    img = img.filter(ImageFilter.GaussianBlur(1.0))
    draw = ImageDraw.Draw(img)
    # Accent horizontal bar at center-ish
    mid = int(h * 0.52)
    draw.rectangle([0, mid, w, mid + 12], fill=accent)
    # Second thin bar
    draw.rectangle([0, mid + 50, int(w * 0.45), mid + 56], fill=accent)
    return img

def bg_fire_vertical(w, h, accent):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        if t < 0.4:
            r, g, b = int(140 + (1-t/0.4)*80), int(t/0.4*50), 0
        elif t < 0.7:
            s = (t-0.4)/0.3
            r, g, b = int(140*(1-s)), int(50*(1-s)), 0
        else:
            r, g, b = 0, 0, 0
        draw.line([(0,y),(w,y)], fill=(r,g,b))
    for _ in range(200):
        x1 = random.randint(0, w)
        y1 = random.randint(int(h*0.3), h)
        l = random.randint(40, 300)
        dy_ = random.randint(-l, -l//3)
        dx_ = random.randint(-40, 40)
        br = random.randint(20, 80)
        draw.line([(x1,y1),(x1+dx_,y1+dy_)],
                  fill=(255, br, 0), width=random.randint(1,6))
    img = img.filter(ImageFilter.GaussianBlur(4))
    # Dark top overlay
    overlay = Image.new("RGBA", (w,h), (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    for y in range(int(h*0.55)):
        alpha = int(200*(1-y/(h*0.55)))
        od.line([(0,y),(w,y)], fill=(0,0,0,alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    return img

BG_FUNCS = {
    "dark_concrete":  bg_dark_concrete,
    "diagonal_dark":  bg_diagonal_dark,
    "glitch_vertical":bg_glitch_vertical,
    "fire_vertical":  bg_fire_vertical,
}

def add_grain(img, s=16):
    px = img.load()
    for _ in range(int(img.width * img.height * 0.18)):
        x = random.randint(0, img.width-1)
        y = random.randint(0, img.height-1)
        r,g,b = px[x,y]
        n = random.randint(-s,s)
        px[x,y] = (max(0,min(255,r+n)),max(0,min(255,g+n)),max(0,min(255,b+n)))
    return img

def radial_vignette(img):
    w, h = img.size
    vig = Image.new("RGBA", (w,h), (0,0,0,0))
    vp = vig.load()
    cx, cy = w/2, h/2
    for y in range(h):
        for x in range(w):
            dx = (x-cx)/(w*0.55)
            dy = (y-cy)/(h*0.55)
            d = math.sqrt(dx*dx+dy*dy)
            a = int(min(255, max(0,(d-0.55)*260)))
            vp[x,y] = (0,0,0,a)
    out = img.convert("RGBA")
    out = Image.alpha_composite(out, vig)
    return out.convert("RGB")


# ── Text rendering ────────────────────────────────────────────────────────────

def measure(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2]-bb[0], bb[3]-bb[1]

def rtl_wrap(text, font, max_w, draw):
    words = text.split()
    lines, cur = [], []
    for word in words:
        test = " ".join(cur + [word])
        tw, _ = measure(draw, test, font)
        if cur and tw > max_w:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))
    return lines

def draw_rtl(draw, text, x_right, y, font, fill):
    tw, _ = measure(draw, text, font)
    draw.text((x_right - tw, y), text, font=font, fill=fill)


def render_text(draw, quote, is_dark=True):
    margin  = 80
    x_right = W - margin
    max_w   = W - margin * 2
    font_path = quote["font"]
    accent    = quote["accent"]
    txt_col   = (255,255,255) if is_dark else (10,10,10)
    sub_col   = (190,190,190) if is_dark else (60,60,60)

    lines_raw = quote["main"].split("\n")

    # Auto-fit headline
    size = 210
    while size > 70:
        f = hfont(font_path, size)
        max_lw = max(measure(draw, l, f)[0] for l in lines_raw)
        if max_lw <= max_w:
            break
        size -= 5
    f = hfont(font_path, size)
    lh = int(size * 1.12)

    total_h = lh * len(lines_raw)
    # Position text block at ~58% from top
    y0 = int(H * 0.52) - total_h // 2

    # Thin separator line above text
    sep_y = y0 - 44
    draw.rectangle([x_right - 90, sep_y, x_right, sep_y + 5], fill=accent)

    for i, line in enumerate(lines_raw):
        color = accent if i == 0 else txt_col
        draw_rtl(draw, line, x_right, y0 + i * lh, f, color)

    # Subtitle
    sf = hfont(font_path, 54)
    sub_lines = rtl_wrap(quote["sub"], sf, max_w, draw)
    sy = y0 + total_h + 55
    for sl in sub_lines:
        draw_rtl(draw, sl, x_right, sy, sf, sub_col)
        sy += 70


def generate(idx, quote):
    bg_name = quote["bg"]
    accent  = quote["accent"]
    img = BG_FUNCS[bg_name](W, H, accent)
    img = add_grain(img, 14)
    img = radial_vignette(img)

    draw = ImageDraw.Draw(img)
    render_text(draw, quote, is_dark=(bg_name != "concrete_white"))

    # Index tag
    nf = hfont(LAT_BOLD, 38)
    draw.text((W - 80, H - 70), f"{idx:02d}", font=nf, fill=(55,55,55))

    out = os.path.join(OUTPUT_DIR, f"story_{idx:02d}.jpg")
    img.save(out, "JPEG", quality=95)
    print(f"  [{idx:02d}] {out}")
    return out

if __name__ == "__main__":
    print(f"Generating {len(QUOTES)} Hebrew Stories (1080x1920)...")
    for i, q in enumerate(QUOTES):
        generate(i+1, q)
    print("\nDone! →", OUTPUT_DIR)

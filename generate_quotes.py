#!/usr/bin/env python3
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from bidi.algorithm import get_display

OUTPUT_DIR = "quote_images"
FONT_PATH = "/tmp/Heebo.ttf"
WATERMARK = '"הכוח שבין המילים"'

# 10 quotes — same style as reference images
QUOTES = [
    {
        "text": "אנשים מוצאים זמן\nלמה שחשוב להם.\nאם אתה לא בסדר\nהעדיפויות שלהם —\nאתה כבר יודע מה שצריך לדעת.",
        "bg": "night_sky",
    },
    {
        "text": "אהבה אמיתית\nלא גורמת לך להרגיש\nשאתה צריך כל הזמן\nלהוכיח שאתה מספיק.",
        "bg": "sunset",
    },
    {
        "text": "לבחור בעצמך\nזה לא אנוכיות.\nזה ההבדל בין לתת מתוך שפע\nלבין לתת עד ריקנות.",
        "bg": "forest",
    },
    {
        "text": "לא כל כאב\nבא להרוס אותך.\nחלקו בא\nרק לפתוח אותך.",
        "bg": "ocean",
    },
    {
        "text": "יש שתיקות\nשמדברות יותר מכל מילה.\nללמוד לקרוא אותן —\nזה אחד הדברים\nהחשובים ביותר בחיים.",
        "bg": "deep_blue",
    },
    {
        "text": "ברגע שהפסקת\nלחכות לאישור מאחרים,\nהתחלת לחיות\nבאמת.",
        "bg": "dawn",
    },
    {
        "text": "אמון לוקח שנים לבנות,\nשניות לשבור,\nולפעמים לנצח\nלהחזיר.",
        "bg": "storm",
    },
    {
        "text": "אתה לא\nמה שקרה לך.\nאתה מה שבחרת לעשות\nעם מה שקרה לך.",
        "bg": "mountain",
    },
    {
        "text": "לא כל מי\nשנמצא לידך — איתך.\nולא כל מי שהלך —\nעזב.",
        "bg": "desert",
    },
    {
        "text": "השינוי הכי קשה\nהוא לא לשנות הרגלים,\nאלא להפסיק להצטדק\nעל כך שאתה לא משתנה.",
        "bg": "fog",
    },
]


def make_gradient_bg(style, size=(1080, 1080)):
    """Create a cinematic gradient background."""
    W, H = size
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)

    palettes = {
        "night_sky":  [(5, 5, 20), (15, 15, 60), (5, 5, 20)],
        "sunset":     [(10, 5, 5), (80, 30, 10), (180, 80, 20), (80, 30, 10)],
        "forest":     [(5, 15, 5), (10, 40, 20), (5, 20, 10)],
        "ocean":      [(5, 10, 30), (10, 40, 80), (5, 20, 50)],
        "deep_blue":  [(5, 5, 30), (10, 20, 80), (30, 60, 120), (10, 20, 60)],
        "dawn":       [(5, 5, 20), (60, 40, 80), (160, 100, 60), (60, 30, 20)],
        "storm":      [(10, 10, 10), (30, 30, 35), (10, 10, 15)],
        "mountain":   [(10, 10, 20), (30, 30, 50), (15, 15, 30)],
        "desert":     [(20, 10, 5), (80, 50, 20), (40, 25, 10)],
        "fog":        [(20, 20, 25), (50, 55, 65), (25, 25, 30)],
    }

    colors = palettes.get(style, [(5, 5, 20), (20, 20, 50), (5, 5, 20)])

    for y in range(H):
        t = y / H
        # Interpolate across color stops
        n = len(colors) - 1
        seg = min(int(t * n), n - 1)
        local_t = (t * n) - seg
        c0 = colors[seg]
        c1 = colors[seg + 1]
        r = int(c0[0] + (c1[0] - c0[0]) * local_t)
        g = int(c0[1] + (c1[1] - c0[1]) * local_t)
        b = int(c0[2] + (c1[2] - c0[2]) * local_t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Add subtle noise/texture
    import random
    random.seed(42)
    for _ in range(8000):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        v = random.randint(0, 25)
        px = img.getpixel((x, y))
        img.putpixel((x, y), (min(255, px[0]+v), min(255, px[1]+v), min(255, px[2]+v)))

    # Slight blur to smooth noise
    img = img.filter(ImageFilter.GaussianBlur(1))

    # Add a soft radial vignette (brighter center)
    vignette = Image.new("RGBA", size, (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    for i in range(60, 0, -1):
        alpha = int((60 - i) * 2.5)
        margin = int((60 - i) * 9)
        vd.ellipse([margin, margin, W - margin, H - margin], fill=(255, 255, 255, alpha // 8))
    img = Image.alpha_composite(img.convert("RGBA"), vignette).convert("RGB")

    return img




def draw_hebrew_text_centered(draw, text, font, img_width, y_start, fill, line_spacing=1.35):
    lines = text.split("\n")
    line_heights = []
    line_widths = []
    bidi_lines = []

    for line in lines:
        bidi_line = get_display(line)
        bidi_lines.append(bidi_line)
        bbox = font.getbbox(bidi_line)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        line_widths.append(w)
        line_heights.append(h)

    max_h = max(line_heights) if line_heights else 0
    step = int(max_h * line_spacing)
    y = y_start

    for bidi_line, w in zip(bidi_lines, line_widths):
        x = (img_width - w) // 2
        # Shadow
        draw.text((x + 3, y + 3), bidi_line, font=font, fill=(0, 0, 0, 180))
        draw.text((x, y), bidi_line, font=font, fill=fill)
        y += step

    return y


def make_quote_image(quote_data, index):
    print(f"  Generating image {index + 1}...")
    img = make_gradient_bg(quote_data["bg"])

    draw = ImageDraw.Draw(img)
    W, H = img.size

    font_size = 72
    font = ImageFont.truetype(FONT_PATH, font_size)
    watermark_font = ImageFont.truetype(FONT_PATH, 36)
    text_color = (255, 255, 255)

    lines = quote_data["text"].split("\n")
    line_height = int(font_size * 1.45)
    total_text_height = len(lines) * line_height

    y_start = (H - total_text_height) // 2 - 30

    draw_hebrew_text_centered(draw, quote_data["text"], font, W, y_start, text_color)

    # Watermark bottom-center
    wm_bidi = get_display(WATERMARK)
    wm_bbox = watermark_font.getbbox(wm_bidi)
    wm_w = wm_bbox[2] - wm_bbox[0]
    wm_x = (W - wm_w) // 2
    draw.text((wm_x, H - 90), wm_bidi, font=watermark_font, fill=(255, 255, 255, 200))

    out_path = os.path.join(OUTPUT_DIR, f"quote_{index + 1:02d}.jpg")
    img.save(out_path, "JPEG", quality=92)
    print(f"  Saved: {out_path}")
    return out_path


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = []
    for i, q in enumerate(QUOTES):
        try:
            path = make_quote_image(q, i)
            results.append(path)
        except Exception as e:
            print(f"  ERROR on image {i + 1}: {e}")
    print(f"\nDone! {len(results)}/10 images created in '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()

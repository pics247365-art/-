#!/usr/bin/env python3
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "quote_images"
FONT_PATH = "/tmp/Heebo.ttf"
WATERMARK = '"הכוח שבין המילים"'

# 25 quotes — same style as reference images
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
    # 15 new quotes
    {
        "text": "לא כל דלת\nשנסגרת בפניך\nהיא עונש.\nחלקן פשוט\nמגנות עליך.",
        "bg": "wine",
    },
    {
        "text": "אדם שמכבד את עצמו\nלא מסביר את עצמו\nלכל אחד.\nהוא פשוט ממשיך\nלהיות מי שהוא.",
        "bg": "teal",
    },
    {
        "text": "לא תמיד צריך\nלהגיב.\nלפעמים השתיקה\nהיא התשובה\nהכי חכמה.",
        "bg": "midnight",
    },
    {
        "text": "מי שאוהב אותך\nלא יגרום לך\nלתהות כל הזמן\nאם הוא אוהב אותך.",
        "bg": "ember",
    },
    {
        "text": "הגבולות שאתה שם\nלא מרחיקים אנשים.\nהם מסננים\nמי באמת רוצה\nלהיות בחייך.",
        "bg": "slate",
    },
    {
        "text": "אל תבנה את עצמך\nסביב מישהו\nשעדיין לא החליט\nאם הוא רוצה אותך.",
        "bg": "copper",
    },
    {
        "text": "לפעמים הדבר\nהכי אמיץ שאפשר לעשות\nהוא פשוט\nלהמשיך הלאה.",
        "bg": "aurora",
    },
    {
        "text": "אנשים מראים לך\nמי הם\nבמה שהם עושים,\nלא במה שהם אומרים.",
        "bg": "charcoal",
    },
    {
        "text": "הפחד מכישלון\nהרג יותר חלומות\nמאשר\nהכישלון עצמו.",
        "bg": "crimson",
    },
    {
        "text": "לא כל רגע\nצריך להיות מושלם\nכדי שיהיה\nשווה לזכור.",
        "bg": "sage",
    },
    {
        "text": "כשאתה מפסיק\nלחפש אישור מאחרים,\nאתה מגלה\nכמה זמן בזבזת\nעל הדעות שלהם.",
        "bg": "navy",
    },
    {
        "text": "מערכת יחסים טובה\nלא תגרום לך\nלהרגיש לבד\nכשאתה איתה.",
        "bg": "rose",
    },
    {
        "text": "הצלחה היא לא\nמה שיש לך.\nהיא מי שאתה\nכשאין לך כלום.",
        "bg": "gold",
    },
    {
        "text": "תפסיק לנסות\nלשנות אנשים.\nתשקיע את האנרגיה הזו\nבלהיות מי\nשאתה רוצה להיות.",
        "bg": "indigo",
    },
    {
        "text": "אתה לא חייב\nלסיים כל ויכוח.\nלפעמים\nלצאת בשקט\nזו הניצחון.",
        "bg": "pine",
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
        "wine":       [(20, 5, 10), (80, 10, 30), (40, 5, 15)],
        "teal":       [(5, 20, 20), (10, 70, 70), (5, 35, 35)],
        "midnight":   [(5, 5, 15), (10, 10, 40), (20, 20, 60), (10, 10, 35)],
        "ember":      [(15, 5, 5), (100, 40, 5), (200, 100, 10), (100, 40, 5)],
        "slate":      [(15, 20, 25), (35, 45, 55), (20, 28, 35)],
        "copper":     [(25, 12, 5), (100, 55, 20), (55, 28, 10)],
        "aurora":     [(5, 15, 25), (20, 80, 80), (60, 120, 80), (20, 60, 60)],
        "charcoal":   [(12, 12, 12), (28, 28, 32), (15, 15, 18)],
        "crimson":    [(15, 5, 5), (90, 10, 20), (50, 5, 10)],
        "sage":       [(10, 20, 12), (30, 60, 35), (15, 35, 18)],
        "navy":       [(5, 8, 25), (10, 20, 70), (5, 12, 40)],
        "rose":       [(25, 8, 15), (90, 30, 55), (50, 15, 28)],
        "gold":       [(20, 15, 5), (90, 65, 10), (45, 32, 5)],
        "indigo":     [(10, 5, 30), (40, 20, 100), (20, 10, 55)],
        "pine":       [(5, 18, 10), (12, 50, 28), (6, 28, 14)],
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

    for line in lines:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        line_widths.append(w)
        line_heights.append(h)

    max_h = max(line_heights) if line_heights else 0
    step = int(max_h * line_spacing)
    y = y_start

    for line, w in zip(lines, line_widths):
        x = (img_width - w) // 2
        draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0, 180))
        draw.text((x, y), line, font=font, fill=fill)
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

    # Bottom branding — "שגאון" + tagline
    brand_font = ImageFont.truetype(FONT_PATH, 40)
    tag_font = ImageFont.truetype(FONT_PATH, 28)

    brand = "שגאון"
    tagline = "המרחב בין דכאון לשגעון"

    b_bbox = brand_font.getbbox(brand)
    b_w = b_bbox[2] - b_bbox[0]
    draw.text(((W - b_w) // 2, H - 105), brand, font=brand_font, fill=(255, 255, 255, 220))

    t_bbox = tag_font.getbbox(tagline)
    t_w = t_bbox[2] - t_bbox[0]
    draw.text(((W - t_w) // 2, H - 55), tagline, font=tag_font, fill=(255, 255, 255, 170))

    out_path = os.path.join(OUTPUT_DIR, f"quote_{index + 1:02d}.jpg")
    img.save(out_path, "JPEG", quality=92)
    print(f"  Saved: {out_path}")
    return out_path


def main(start=0):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = []
    for i, q in enumerate(QUOTES):
        if i < start:
            continue
        try:
            path = make_quote_image(q, i)
            results.append(path)
        except Exception as e:
            print(f"  ERROR on image {i + 1}: {e}")
    print(f"\nDone! {len(results)} images created in '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    import sys
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(start)

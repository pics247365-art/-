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


BACKGROUNDS_DIR = "backgrounds"


def load_backgrounds():
    exts = ('.jpg', '.jpeg', '.png', '.webp')
    files = sorted([
        os.path.join(BACKGROUNDS_DIR, f)
        for f in os.listdir(BACKGROUNDS_DIR)
        if f.lower().endswith(exts)
    ])
    return files


def prepare_background(path, size=(1080, 1080)):
    img = Image.open(path).convert("RGB")
    # Crop to square from center
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize(size, Image.LANCZOS)
    # Dark overlay so text is always readable
    overlay = Image.new("RGBA", size, (0, 0, 0, 150))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
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


def make_quote_image(quote_data, index, bg_paths):
    print(f"  Generating image {index + 1}...")
    bg_path = bg_paths[index % len(bg_paths)]
    img = prepare_background(bg_path)

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
    bg_paths = load_backgrounds()
    print(f"Loaded {len(bg_paths)} background images")
    results = []
    for i, q in enumerate(QUOTES):
        if i < start:
            continue
        try:
            path = make_quote_image(q, i, bg_paths)
            results.append(path)
        except Exception as e:
            print(f"  ERROR on image {i + 1}: {e}")
    print(f"\nDone! {len(results)} images created in '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    import sys
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(start)

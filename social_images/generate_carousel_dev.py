#!/usr/bin/env python3
"""
12-slide personal-development carousel (1080x1080)
Cohesive series feel: consistent branding bar, slide counter,
each slide with its own background & accent color.
"""

import os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "/home/user/-/social_images/output_carousel_dev"
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

# ── 12 slides ──────────────────────────────────────────────────────────────

SLIDES = [
    {
        "number":  "01",
        "tag":     "פתיח",
        "headline": "אתה לא מנצל\n1% מהפוטנציאל שלך.",
        "body":    "12 עקרונות שישנו את זה — לתמיד.",
        "font":    HEB_BOLD,
        "accent":  (230, 57, 70),
        "bg":      "noir_burst",
    },
    {
        "number":  "02",
        "tag":     "מיינדסט",
        "headline": "המחשבות שלך\nבונות את המציאות שלך.",
        "body":    "שנה את הנרטיב הפנימי — שאר הדברים ישתנו אחריו.",
        "font":    HEB_BOLD,
        "accent":  (245, 197, 24),
        "bg":      "diagonal_hatch",
    },
    {
        "number":  "03",
        "tag":     "פחד",
        "headline": "הפחד\nלא נעלם.",
        "body":    "הגיבורים פועלים בלעדיו — לא בלי פחד.",
        "font":    HEB_KETER,
        "accent":  (255, 100, 0),
        "bg":      "ember",
    },
    {
        "number":  "04",
        "tag":     "עקביות",
        "headline": "מוכשרות\nמפסידה לעקביות.",
        "body":    "1% שיפור כל יום = 37 פעמים טוב יותר בסוף שנה.",
        "font":    HEB_BOLD,
        "accent":  (0, 200, 160),
        "bg":      "teal_grid",
    },
    {
        "number":  "05",
        "tag":     "פעולה",
        "headline": "חשיבה ללא פעולה\nהיא חלום.",
        "body":    "פעולה ללא חשיבה — סיוט. שניהם ביחד — קסם.",
        "font":    HEB_SIMPLE,
        "accent":  (230, 57, 70),
        "bg":      "concrete_slash",
    },
    {
        "number":  "06",
        "tag":     "אמונה עצמית",
        "headline": "אתה מה\nשאתה מאמין שאתה.",
        "body":    "תפסיק לחכות שמישהו אחר יאמין בך קודם.",
        "font":    HEB_BOLD,
        "accent":  (245, 197, 24),
        "bg":      "diagonal_hatch",
    },
    {
        "number":  "07",
        "tag":     "זמן",
        "headline": "הזמן\nלא מחכה.",
        "body":    "כל יום שעובר בלי פעולה — הוא יום שאתה בוחר לוותר.",
        "font":    HEB_KETER,
        "accent":  (255, 255, 255),
        "bg":      "glitch_sq",
    },
    {
        "number":  "08",
        "tag":     "כישלון",
        "headline": "כישלון הוא\nמידע — לא גזר דין.",
        "body":    "כל נפילה מלמדת אותך משהו שהצלחה לא יכולה.",
        "font":    HEB_BOLD,
        "accent":  (255, 100, 0),
        "bg":      "ember",
    },
    {
        "number":  "09",
        "tag":     "משמעת",
        "headline": "מוטיבציה מצית.\nמשמעת עובדת.",
        "body":    "אל תסמוך על מצב הרוח. בנה מערכת שעובדת בכל מצב.",
        "font":    HEB_BOLD,
        "accent":  (230, 57, 70),
        "bg":      "noir_burst",
    },
    {
        "number":  "10",
        "tag":     "סביבה",
        "headline": "אתה ממוצע\nחמשת האנשים",
        "body":    "הקרובים אליך ביותר. תבחר את הסביבה שלך בקפידה.",
        "font":    HEB_SIMPLE,
        "accent":  (0, 200, 160),
        "bg":      "teal_grid",
    },
    {
        "number":  "11",
        "tag":     "מטרות",
        "headline": "מטרה ללא תוכנית\nהיא רק משאלה.",
        "body":    "פרק אותה לצעדים יומיים. הצעד הראשון — היום.",
        "font":    HEB_BOLD,
        "accent":  (245, 197, 24),
        "bg":      "concrete_slash",
    },
    {
        "number":  "12",
        "tag":     "עכשיו",
        "headline": "לא מחר.\nלא אחרי שיהיה מושלם.",
        "body":    "עכשיו. כי הגרסה הטובה ביותר שלך מתחילה בהחלטה אחת.",
        "font":    HEB_KETER,
        "accent":  (230, 57, 70),
        "bg":      "noir_burst",
    },
]


# ── Backgrounds ────────────────────────────────────────────────────────────

def bg_noir_burst(w, h, accent):
    """Near-black with radial light burst at top-center and motion streaks."""
    img = Image.new("RGB", (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Subtle radial gradient
    cx, cy = w // 2, int(h * 0.28)
    for r in range(min(w,h)//2, 0, -4):
        t = r / (min(w,h)//2)
        bri = int((1-t) * 30)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(bri, bri, bri))
    # Motion streaks
    for _ in range(60):
        x1 = random.randint(0, w)
        y1 = random.randint(0, h)
        ln = random.randint(30, 200)
        ang = random.uniform(-5, 5)
        dx = math.cos(math.radians(ang)) * ln
        dy = math.sin(math.radians(ang)) * ln
        c = random.randint(12, 45)
        draw.line([(x1,y1),(x1+dx,y1+dy)], fill=(c,c,c), width=random.randint(1,5))
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    draw = ImageDraw.Draw(img)
    # Accent left bar
    draw.rectangle([0, 0, 16, h], fill=accent)
    # Accent bottom bar
    draw.rectangle([0, h-16, w, h], fill=accent)
    # Diagonal accent slash bottom-right
    by = int(h * 0.78)
    draw.polygon([(0, by), (w, by - int(h*0.04)),
                  (w, by+18), (0, by+18+int(h*0.04))], fill=accent)
    return img

def bg_diagonal_hatch(w, h, accent):
    """Dark with diagonal lines and accent bottom block."""
    img = Image.new("RGB", (w, h), (5, 5, 8))
    draw = ImageDraw.Draw(img)
    for i in range(-h, w+h, 26):
        c = random.randint(10, 28)
        draw.line([(i,0),(i+h,h)], fill=(c,c,c), width=random.randint(1,4))
    img = img.filter(ImageFilter.GaussianBlur(0.8))
    draw = ImageDraw.Draw(img)
    by = int(h * 0.78)
    draw.rectangle([0, by, w, h], fill=accent)
    # Bright edge line above block
    bright = tuple(min(255, c+40) for c in accent)
    draw.rectangle([0, by-6, w, by], fill=bright)
    return img

def bg_ember(w, h, accent):
    """Dark warm gradient — ember/fire tones."""
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        if t < 0.35:
            r = int(120 + (1-t/0.35)*100)
            g = int(t/0.35*40)
            b = 0
        elif t < 0.65:
            s = (t-0.35)/0.3
            r = int(120*(1-s))
            g = int(40*(1-s))
            b = 0
        else:
            r = g = b = 0
        draw.line([(0,y),(w,y)], fill=(r,g,b))
    for _ in range(150):
        x1 = random.randint(0, w)
        y1 = random.randint(int(h*0.25), h)
        ln = random.randint(30, 200)
        dy_ = random.randint(-ln, -ln//3)
        dx_ = random.randint(-30, 30)
        draw.line([(x1,y1),(x1+dx_,y1+dy_)], fill=(255,random.randint(10,60),0), width=random.randint(1,5))
    img = img.filter(ImageFilter.GaussianBlur(4))
    # Dark top overlay
    ov = Image.new("RGBA", (w,h), (0,0,0,0))
    od = ImageDraw.Draw(ov)
    for y in range(int(h*0.5)):
        a_ = int(210*(1-y/(h*0.5)))
        od.line([(0,y),(w,y)], fill=(0,0,0,a_))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, ov)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    # Left accent bar
    draw.rectangle([0, 0, 16, h], fill=accent)
    return img

def bg_teal_grid(w, h, accent):
    """Very dark teal with grid lines and radial glow."""
    img = Image.new("RGB", (w, h), (2, 16, 18))
    draw = ImageDraw.Draw(img)
    # Grid
    step = 60
    for x in range(0, w, step):
        draw.line([(x,0),(x,h)], fill=(0, 22, 26), width=1)
    for y in range(0, h, step):
        draw.line([(0,y),(w,y)], fill=(0, 22, 26), width=1)
    # Radial glow
    cx, cy = w//2, int(h*0.35)
    ar, ag, ab = accent
    for r in range(360, 0, -8):
        t = 1 - r/360
        col = (int(ar*t*0.2), int(ag*t*0.2), int(ab*t*0.2))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=col)
    img = img.filter(ImageFilter.GaussianBlur(0.5))
    draw = ImageDraw.Draw(img)
    # Accent bottom band
    by = int(h * 0.78)
    draw.rectangle([0, by, w, h], fill=accent)
    draw.rectangle([0, by-6, w, by], fill=tuple(min(255,c+50) for c in accent))
    draw.rectangle([0, 0, 16, h], fill=accent)
    return img

def bg_concrete_slash(w, h, accent):
    """Concrete texture with bold diagonal slash accent."""
    img = Image.new("RGB", (w, h), (9, 9, 9))
    draw = ImageDraw.Draw(img)
    for _ in range(4000):
        x, y = random.randint(0, w), random.randint(0, h)
        l = random.randint(5, 70)
        ang = random.uniform(0, 360)
        dx = math.cos(math.radians(ang))*l
        dy = math.sin(math.radians(ang))*l
        c = random.randint(16, 38)
        draw.line([(x,y),(x+dx,y+dy)], fill=(c,c,c), width=1)
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    draw = ImageDraw.Draw(img)
    # Bold diagonal slash
    sy = int(h * 0.74)
    draw.polygon([(0, sy), (w, sy - int(h*0.05)),
                  (w, sy + 28), (0, sy + 28 + int(h*0.05))], fill=accent)
    # Right bar
    draw.rectangle([w-18, 0, w, h], fill=accent)
    return img

def bg_glitch_sq(w, h, accent):
    """Glitch scan-line style for square format."""
    img = Image.new("RGB", (w, h), (3, 3, 5))
    draw = ImageDraw.Draw(img)
    for _ in range(100):
        y = random.randint(0, h)
        thick = random.randint(1, 16)
        c = random.randint(14, 60)
        off = random.randint(-90, 90)
        draw.rectangle([off, y, w+off, y+thick], fill=(c,c,c))
    for _ in range(10):
        x = random.randint(0, w)
        draw.line([(x,0),(x,h)], fill=(35,35,55), width=random.randint(1,3))
    img = img.filter(ImageFilter.GaussianBlur(0.9))
    draw = ImageDraw.Draw(img)
    mid = int(h * 0.75)
    draw.rectangle([0, mid, w, mid+10], fill=accent)
    draw.rectangle([0, mid+40, int(w*0.5), mid+46], fill=accent)
    draw.rectangle([0, 0, 14, h], fill=accent)
    return img


BG_FUNCS = {
    "noir_burst":     bg_noir_burst,
    "diagonal_hatch": bg_diagonal_hatch,
    "ember":          bg_ember,
    "teal_grid":      bg_teal_grid,
    "concrete_slash": bg_concrete_slash,
    "glitch_sq":      bg_glitch_sq,
}

def add_grain(img, s=18):
    px = img.load()
    for _ in range(int(img.width * img.height * 0.22)):
        x = random.randint(0, img.width-1)
        y = random.randint(0, img.height-1)
        r,g,b = px[x,y]
        n = random.randint(-s,s)
        px[x,y] = (max(0,min(255,r+n)), max(0,min(255,g+n)), max(0,min(255,b+n)))
    return img

def radial_vignette(img):
    w, h = img.size
    vig = Image.new("RGBA", (w,h), (0,0,0,0))
    vp = vig.load()
    cx, cy = w/2, h/2
    for y in range(h):
        for x in range(w):
            dx = (x-cx)/(w*0.58)
            dy = (y-cy)/(h*0.58)
            d = math.sqrt(dx*dx+dy*dy)
            a = int(min(255, max(0,(d-0.52)*280)))
            vp[x,y] = (0,0,0,a)
    out = img.convert("RGBA")
    out = Image.alpha_composite(out, vig)
    return out.convert("RGB")

def measure(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2]-bb[0], bb[3]-bb[1]

def draw_rtl(draw, text, x_right, y, font, fill):
    tw, _ = measure(draw, text, font)
    draw.text((x_right - tw, y), text, font=font, fill=fill)

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


def render_slide(img, slide):
    draw = ImageDraw.Draw(img)
    accent    = slide["accent"]
    font_path = slide["font"]
    margin    = 72
    x_right   = W - margin
    max_w     = W - margin * 2 - 20   # extra margin for left bar

    # ── Slide counter (top-left after left bar) ──
    num_f  = hfont(LAT_BOLD, 36)
    total_f = hfont(LAT_BOLD, 26)
    draw.text((30, 28), slide["number"], font=num_f, fill=accent)
    draw.text((30, 68), "/ 12", font=total_f, fill=(80,80,80))

    # ── Tag / category (top-right) ──
    tag_f = hfont(font_path, 34)
    draw_rtl(draw, slide["tag"], x_right, 30, tag_f, (130,130,130))

    # ── Headline: auto-size to fit ──
    lines_raw = slide["headline"].split("\n")
    size = 175
    while size > 55:
        f = hfont(font_path, size)
        max_lw = max(measure(draw, l, f)[0] for l in lines_raw)
        if max_lw <= max_w:
            break
        size -= 4
    f = hfont(font_path, size)
    lh = int(size * 1.10)

    total_text_h = lh * len(lines_raw)
    # Center vertically, slightly above center
    y0 = int(H * 0.44) - total_text_h // 2

    # Thin right-aligned separator above headline
    sep_y = y0 - 38
    draw.rectangle([x_right - 80, sep_y, x_right, sep_y + 4], fill=accent)

    for i, line in enumerate(lines_raw):
        color = accent if i == 0 else (240, 240, 240)
        draw_rtl(draw, line, x_right, y0 + i * lh, f, color)

    # ── Body text ──
    bf = hfont(font_path, 46)
    body_lines = rtl_wrap(slide["body"], bf, max_w, draw)
    by = y0 + total_text_h + 48
    for bl in body_lines:
        draw_rtl(draw, bl, x_right, by, bf, (175, 175, 175))
        by += 62


def generate(idx, slide):
    accent  = slide["accent"]
    bg_name = slide["bg"]
    img = BG_FUNCS[bg_name](W, H, accent)
    img = add_grain(img, 16)
    img = radial_vignette(img)
    render_slide(img, slide)
    out = os.path.join(OUTPUT_DIR, f"slide_{idx:02d}.jpg")
    img.save(out, "JPEG", quality=95)
    print(f"  [{idx:02d}] {out}")
    return out


if __name__ == "__main__":
    print(f"Generating {len(SLIDES)} carousel slides (1080x1080)...")
    for i, s in enumerate(SLIDES):
        generate(i+1, s)
    print("\nDone! →", OUTPUT_DIR)

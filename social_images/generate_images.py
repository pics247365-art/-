#!/usr/bin/env python3
"""
Generate 10 cinematic dark motivational images in Stories format (1080x1920)
Style: BW cinematic, bold white/gray text in lower third, dark moody aesthetic
"""

import os
import random
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUTPUT_DIR = "/home/user/-/social_images/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1080, 1920

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_BOLD_ALT = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"

QUOTES = [
    {
        "title_parts": [
            ("You'll never ", "white"),
            ("feel ready", "gray"),
        ],
        "subtitle": "because ready isn't a feeling, it's a decision",
        "bg_style": "crowd",
    },
    {
        "title_parts": [
            ("Stop waiting for ", "white"),
            ("the right moment", "gray"),
        ],
        "subtitle": "this moment is all you've ever had",
        "bg_style": "city",
    },
    {
        "title_parts": [
            ("Most people quit ", "white"),
            ("when it gets hard", "gray"),
        ],
        "subtitle": "that's exactly when it starts to matter",
        "bg_style": "shadow",
    },
    {
        "title_parts": [
            ("Your excuses are just ", "white"),
            ("fears", "gray"),
            (" with better words", "white"),
        ],
        "subtitle": "kill the excuses. start the work.",
        "bg_style": "light_dark",
    },
    {
        "title_parts": [
            ("Nobody is ", "white"),
            ("coming to save you", "gray"),
        ],
        "subtitle": "that's not a tragedy — that's your power",
        "bg_style": "silhouette",
    },
    {
        "title_parts": [
            ("Discipline is just ", "white"),
            ("remembering", "gray"),
            (" what you want more", "white"),
        ],
        "subtitle": "the short-term pain builds the long-term self",
        "bg_style": "corridor",
    },
    {
        "title_parts": [
            ("Every day you don't ", "white"),
            ("move forward", "gray"),
        ],
        "subtitle": "you practice staying behind",
        "bg_style": "motion",
    },
    {
        "title_parts": [
            ("Silence your ", "white"),
            ("inner critic", "gray"),
        ],
        "subtitle": "by becoming what it says you can't",
        "bg_style": "dark_fog",
    },
    {
        "title_parts": [
            ("The life you want ", "white"),
            ("is on the other side", "gray"),
        ],
        "subtitle": "of the discomfort you keep avoiding",
        "bg_style": "perspective",
    },
    {
        "title_parts": [
            ("You are not behind.", "white"),
            ("\nYou are on ", "white"),
            ("your path.", "gray"),
        ],
        "subtitle": "stop comparing your chapter 1 to someone else's chapter 20",
        "bg_style": "solitude",
    },
]

def add_grain(img, intensity=35):
    """Add cinematic film grain to image."""
    import random
    pixels = img.load()
    w, h = img.size
    for _ in range(int(w * h * 0.3)):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        r, g, b = pixels[x, y]
        noise = random.randint(-intensity, intensity)
        pixels[x, y] = (
            max(0, min(255, r + noise)),
            max(0, min(255, g + noise)),
            max(0, min(255, b + noise)),
        )
    return img

def make_bg_crowd(w, h):
    img = Image.new("RGB", (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Dark gradient top to bottom
    for y in range(h):
        t = y / h
        brightness = int(8 + t * 35)
        draw.line([(0, y), (w, y)], fill=(brightness, brightness, brightness))
    # Add motion blur streaks to simulate crowd
    for _ in range(120):
        x1 = random.randint(-100, w + 100)
        y1 = random.randint(0, h)
        length = random.randint(80, 400)
        angle = random.uniform(-15, 15)
        dx = math.cos(math.radians(angle)) * length
        dy = math.sin(math.radians(angle)) * length
        brightness = random.randint(20, 90)
        width = random.randint(2, 18)
        draw.line([(x1, y1), (x1 + dx, y1 + dy)],
                  fill=(brightness, brightness, brightness), width=width)
    img = img.filter(ImageFilter.GaussianBlur(radius=8))
    # Add central bright spot (the "person in focus")
    for cy in range(int(h * 0.2), int(h * 0.65)):
        for cx in range(int(w * 0.25), int(w * 0.75)):
            dist = math.sqrt(((cx - w//2)/(w*0.18))**2 + ((cy - h*0.38)/(h*0.18))**2)
            if dist < 1:
                r, g, b = img.getpixel((cx, cy))[:3]
                boost = int((1 - dist) * 90)
                img.putpixel((cx, cy), (min(255, r + boost), min(255, g + boost), min(255, b + boost)))
    return img

def make_bg_gradient(w, h, style):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    styles = {
        "city":       [(0, 0, 0), (15, 15, 15), (30, 30, 30), (8, 8, 8)],
        "shadow":     [(5, 5, 5), (20, 20, 20), (12, 12, 12), (0, 0, 0)],
        "light_dark": [(0, 0, 0), (25, 25, 25), (40, 40, 40), (10, 10, 10)],
        "silhouette": [(0, 0, 0), (10, 10, 10), (25, 25, 25), (5, 5, 5)],
        "corridor":   [(5, 5, 5), (18, 18, 18), (35, 35, 35), (8, 8, 8)],
        "motion":     [(0, 0, 0), (20, 20, 20), (15, 15, 15), (0, 0, 0)],
        "dark_fog":   [(8, 8, 8), (22, 22, 22), (30, 30, 30), (10, 10, 10)],
        "perspective":[(0, 0, 0), (15, 15, 15), (28, 28, 28), (6, 6, 6)],
        "solitude":   [(3, 3, 3), (18, 18, 18), (32, 32, 32), (8, 8, 8)],
    }
    colors = styles.get(style, styles["city"])
    for y in range(h):
        t = y / h
        if t < 0.33:
            c1, c2 = colors[0], colors[1]
            s = t / 0.33
        elif t < 0.66:
            c1, c2 = colors[1], colors[2]
            s = (t - 0.33) / 0.33
        else:
            c1, c2 = colors[2], colors[3]
            s = (t - 0.66) / 0.34
        r = int(c1[0] + (c2[0] - c1[0]) * s)
        g = int(c1[1] + (c2[1] - c1[1]) * s)
        b = int(c1[2] + (c2[2] - c1[2]) * s)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    # Add motion streaks
    for _ in range(80):
        x1 = random.randint(-200, w + 200)
        y1 = random.randint(0, int(h * 0.8))
        length = random.randint(60, 350)
        angle = random.uniform(-20, 20)
        dx = math.cos(math.radians(angle)) * length
        dy = math.sin(math.radians(angle)) * length
        brightness = random.randint(15, 75)
        width = random.randint(1, 20)
        draw.line([(x1, y1), (x1 + dx, y1 + dy)],
                  fill=(brightness, brightness, brightness), width=width)
    img = img.filter(ImageFilter.GaussianBlur(radius=10))
    # Central silhouette light
    cx, cy = w // 2, int(h * 0.38)
    for px in range(w):
        for py in range(int(h * 0.15), int(h * 0.62)):
            dist = math.sqrt(((px - cx)/(w * 0.22))**2 + ((py - cy)/(h * 0.2))**2)
            if dist < 1:
                r, g, b = img.getpixel((px, py))[:3]
                boost = int((1 - dist) ** 2 * 85)
                img.putpixel((px, py), (min(255, r + boost), min(255, g + boost), min(255, b + boost)))
    return img

def make_background(style, w, h):
    if style == "crowd":
        img = make_bg_crowd(w, h)
    else:
        img = make_bg_gradient(w, h, style)
    # Apply grain
    img = add_grain(img, intensity=28)
    # Radial vignette (dark edges, brighter center)
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    vpix = vignette.load()
    cx, cy = w / 2, h / 2
    for vy in range(h):
        for vx in range(w):
            dx = (vx - cx) / (w * 0.6)
            dy = (vy - cy) / (h * 0.55)
            dist = math.sqrt(dx * dx + dy * dy)
            alpha = int(min(255, max(0, (dist - 0.5) * 320)))
            vpix[vx, vy] = (0, 0, 0, alpha)
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, vignette)
    img = img.convert("RGB")
    return img

def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_text_block(img, quote, idx):
    draw = ImageDraw.Draw(img)
    max_w = int(W * 0.88)
    left_margin = int(W * 0.07)

    # Load fonts at different sizes
    try:
        font_title = ImageFont.truetype(FONT_BOLD, 78)
        font_sub = ImageFont.truetype(FONT_REG, 42)
        font_tiny = ImageFont.truetype(FONT_REG, 36)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_tiny = font_title

    # Measure total title height
    title_parts = quote["title_parts"]
    full_title = "".join(p[0] for p in title_parts)
    title_lines = wrap_text(full_title, font_title, max_w, draw)

    line_height = 92
    sub_lines = wrap_text(quote["subtitle"], font_sub, max_w, draw)
    sub_line_h = 58

    total_h = len(title_lines) * line_height + 36 + len(sub_lines) * sub_line_h
    # Start text block at 65% of image height
    text_y = int(H * 0.65)
    # Ensure it doesn't go off screen
    if text_y + total_h > H - 80:
        text_y = H - 80 - total_h

    # Draw thin separator line above text
    line_y = text_y - 28
    draw.rectangle([left_margin, line_y, left_margin + 60, line_y + 3], fill=(200, 200, 200, 180))

    # Draw title lines with color variation
    # We rebuild coloring word by word per line
    # Flat list of (word, color) for the whole title
    word_colors = []
    for text_seg, color in title_parts:
        for w_token in text_seg.split():
            word_colors.append((w_token, color))

    word_idx = 0
    current_y = text_y
    for line in title_lines:
        words_in_line = line.split()
        current_x = left_margin
        for word in words_in_line:
            if word_idx < len(word_colors):
                _, color_name = word_colors[word_idx]
            else:
                color_name = "white"
            fill = (255, 255, 255) if color_name == "white" else (160, 160, 160)
            bbox = draw.textbbox((0, 0), word + " ", font=font_title)
            draw.text((current_x, current_y), word, font=font_title, fill=fill)
            current_x += bbox[2] - bbox[0]
            word_idx += 1
        current_y += line_height

    # Gap between title and subtitle
    current_y += 36

    # Draw subtitle
    for line in sub_lines:
        draw.text((left_margin, current_y), line, font=font_sub, fill=(160, 160, 160))
        current_y += sub_line_h

    # Draw image number / small brand tag at bottom
    num_text = f"{idx:02d}"
    draw.text((left_margin, H - 80), num_text, font=font_tiny, fill=(80, 80, 80))

    return img

def generate_image(idx, quote):
    img = make_background(quote["bg_style"], W, H)
    img = draw_text_block(img, quote, idx + 1)
    out_path = os.path.join(OUTPUT_DIR, f"image_{idx+1:02d}.jpg")
    img.save(out_path, "JPEG", quality=95)
    print(f"  [{idx+1:02d}] Saved: {out_path}")
    return out_path

if __name__ == "__main__":
    print(f"Generating {len(QUOTES)} images (1080x1920 Stories)...")
    for i, q in enumerate(QUOTES):
        generate_image(i, q)
    print("\nDone! All images saved to:", OUTPUT_DIR)

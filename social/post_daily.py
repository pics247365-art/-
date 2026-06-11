#!/usr/bin/env python3
"""Daily social media posting script — ilanlevi.com
Posts one image per day to Facebook Page and Instagram Business account.
Images live in images/social/ (served via GitHub Pages = public URLs).
"""

import json
import os
import sys
import requests
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
IMAGES_DIR = ROOT / "images" / "social"
LOG_FILE = Path(__file__).parent / "log.json"

FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")
SITE_BASE_URL = os.getenv("SITE_BASE_URL", "https://raw.githubusercontent.com/pics247365-art/-/main")


def get_images():
    if not IMAGES_DIR.exists():
        print(f"תיקייה לא נמצאה: {IMAGES_DIR}")
        sys.exit(1)
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    return sorted(f for f in IMAGES_DIR.iterdir() if f.suffix.lower() in exts)


def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    return {"next_index": 0, "posted": []}


def save_log(log):
    LOG_FILE.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")


FACEBOOK_PAGE_ID = "1163665443488405"
INSTAGRAM_ACCOUNT_ID = "17841432368148282"


def post_to_facebook(image_url, caption):
    url = f"https://graph.facebook.com/v21.0/{FACEBOOK_PAGE_ID}/photos"
    resp = requests.post(url, json={
        "url": image_url,
        "caption": caption,
        "access_token": FB_ACCESS_TOKEN,
    })
    resp.raise_for_status()
    return resp.json()


def post_to_instagram(image_url, caption):
    # Step 1: create media container
    resp = requests.post(
        f"https://graph.facebook.com/v21.0/{INSTAGRAM_ACCOUNT_ID}/media",
        json={
            "image_url": image_url,
            "caption": caption,
            "access_token": FB_ACCESS_TOKEN,
        },
    )
    resp.raise_for_status()
    creation_id = resp.json()["id"]

    # Step 2: publish
    resp = requests.post(
        f"https://graph.facebook.com/v21.0/{INSTAGRAM_ACCOUNT_ID}/media_publish",
        json={
            "creation_id": creation_id,
            "access_token": FB_ACCESS_TOKEN,
        },
    )
    resp.raise_for_status()
    return resp.json()


def main():
    images = get_images()
    if not images:
        print("אין תמונות בתיקיית images/social/")
        sys.exit(1)

    log = load_log()
    idx = log["next_index"] % len(images)
    image = images[idx]

    image_url = f"{SITE_BASE_URL}/images/social/{image.name}"

    # Load caption for this image (or use default)
    captions_file = Path(__file__).parent / "captions.json"
    captions = {}
    if captions_file.exists():
        captions = json.loads(captions_file.read_text(encoding="utf-8"))
    caption = captions.get(image.name, "#אילן_לוי #ליווי_אישי #נוכחות #הקשבה")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] מפרסם: {image.name}")
    print(f"URL: {image_url}")
    print(f"Caption: {caption}")
    print(f"תמונה {idx + 1} מתוך {len(images)}")

    entry = {
        "date": datetime.now().isoformat(),
        "image": image.name,
        "index": idx,
    }

    if FB_PAGE_ID and FB_ACCESS_TOKEN:
        try:
            result = post_to_facebook(image_url, caption)
            print(f"Facebook ✓  id={result.get('id')}")
            entry["facebook_id"] = result.get("id")
        except Exception as e:
            print(f"Facebook ✗  {e}")
            entry["facebook_error"] = str(e)
    else:
        print("Facebook: דילוג (אין credentials)")

    if IG_USER_ID and FB_ACCESS_TOKEN:
        try:
            result = post_to_instagram(image_url, caption)
            print(f"Instagram ✓  id={result.get('id')}")
            entry["instagram_id"] = result.get("id")
        except Exception as e:
            print(f"Instagram ✗  {e}")
            entry["instagram_error"] = str(e)
    else:
        print("Instagram: דילוג (אין credentials)")

    log["posted"].append(entry)
    log["next_index"] = (idx + 1) % len(images)
    save_log(log)
    print("סיום!")


if __name__ == "__main__":
    main()

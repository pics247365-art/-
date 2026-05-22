#!/usr/bin/env python3
"""
הורדת תמונות מדף פייסבוק ציבורי
דרישה: קובץ cookies.txt מהדפדפן שלך
"""

import os
import re
import sys
import json
import time
import argparse
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.facebook.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
}


def load_cookies_from_file(cookie_file: str) -> dict:
    """טוען עוגיות מקובץ Netscape cookies.txt"""
    cookies = {}
    try:
        with open(cookie_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                parts = line.split("\t")
                if len(parts) >= 7:
                    name, value = parts[5], parts[6]
                    cookies[name] = value
        print(f"✅ נטענו {len(cookies)} עוגיות")
    except FileNotFoundError:
        print(f"❌ קובץ העוגיות לא נמצא: {cookie_file}")
        print("\nכיצד לקבל קובץ cookies.txt:")
        print("1. התקן תוסף דפדפן: 'Get cookies.txt LOCALLY'")
        print("2. היכנס לפייסבוק בדפדפן")
        print("3. בצע Export של העוגיות לקובץ cookies.txt")
        print("4. הרץ שוב: python3 fb_download.py --cookies cookies.txt <URL>")
        sys.exit(1)
    return cookies


def resolve_share_url(session: requests.Session, url: str) -> str:
    """פותר URL מקוצר של שיתוף לכתובת הדף האמיתית"""
    try:
        r = session.get(url, allow_redirects=True, timeout=15)
        final = r.url
        if final != url:
            print(f"🔗 הפניה ל: {final}")
        return final
    except Exception as e:
        print(f"⚠️  לא ניתן לפתור URL: {e}")
        return url


def extract_image_urls(html: str, base_url: str) -> list[str]:
    """מחלץ URL-ים של תמונות מה-HTML"""
    found = set()

    # תמונות בתגי og:image ו-meta
    og_images = re.findall(r'property="og:image"\s+content="([^"]+)"', html)
    found.update(og_images)

    # תמונות ב-JSON מוטבע (Facebook מכיל הרבה נתונים כ-JSON)
    json_img_patterns = [
        r'"uri":"(https://[^"]*scontent[^"]*\.(?:jpg|jpeg|png|webp)[^"]*)"',
        r'"src":"(https://[^"]*scontent[^"]*\.(?:jpg|jpeg|png|webp)[^"]*)"',
    ]
    for pattern in json_img_patterns:
        matches = re.findall(pattern, html)
        for m in matches:
            clean = m.replace("\\u003C", "<").replace("\\/", "/")
            # הסר פרמטרים מיותרים של רזולוציה נמוכה
            if "_s." not in clean and "profile_pic" not in clean:
                found.add(clean)

    # תמונות רגילות בתגי <img>
    img_tags = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    for src in img_tags:
        if "scontent" in src or "fbcdn" in src:
            found.add(src)

    # ניקוי URLs - הסרת escape characters
    cleaned = set()
    for url in found:
        url = url.replace("&amp;", "&")
        url = url.replace("\\n", "").strip()
        if url.startswith("http"):
            cleaned.add(url)

    return list(cleaned)


def get_best_resolution(url: str) -> str:
    """מחזיר URL עם רזולוציה גבוהה יותר אם אפשרי"""
    # Facebook מאפשר שינוי גודל דרך פרמטרים
    url = re.sub(r'[?&]_nc_oc=[^&]+', '', url)
    # נסה להגדיל לרזולוציה גבוהה
    for size_param in ['_s', '_n', '_b']:
        if size_param + '.' in url:
            url = url.replace(size_param + '.', '_o.')
            break
    return url


def download_image(session: requests.Session, url: str, dest_path: Path) -> bool:
    """מוריד תמונה אחת"""
    try:
        r = session.get(url, timeout=20, stream=True)
        r.raise_for_status()
        content_type = r.headers.get("content-type", "")
        if "image" not in content_type:
            return False
        dest_path.write_bytes(r.content)
        size_kb = len(r.content) // 1024
        print(f"  ✅ {dest_path.name} ({size_kb}KB)")
        return True
    except Exception as e:
        print(f"  ❌ שגיאה: {e}")
        return False


def download_facebook_images(page_url: str, cookies_file: str, output_dir: str = "fb_images"):
    """הפונקציה הראשית - מוריד תמונות מדף פייסבוק"""
    output = Path(output_dir)
    output.mkdir(exist_ok=True)

    # הגדרת session
    session = requests.Session()
    session.headers.update(HEADERS)
    session.verify = False

    # טעינת עוגיות
    cookies = load_cookies_from_file(cookies_file)
    session.cookies.update(cookies)

    # פתרון URL
    print(f"\n🔍 מתחבר לדף: {page_url}")
    resolved_url = resolve_share_url(session, page_url)

    # טעינת הדף
    print("📄 טוען את הדף...")
    try:
        response = session.get(resolved_url, timeout=20)
        response.raise_for_status()
        html = response.text
        print(f"✅ הדף נטען ({len(html):,} תווים)")
    except Exception as e:
        print(f"❌ שגיאה בטעינת הדף: {e}")
        print("\n💡 טיפ: ודא שהעוגיות תקינות ועדכניות")
        sys.exit(1)

    # חילוץ תמונות
    print("\n🖼️  מחלץ URLs של תמונות...")
    image_urls = extract_image_urls(html, resolved_url)

    if not image_urls:
        print("❌ לא נמצאו תמונות בדף")
        print("💡 אולי הדף דורש כניסה או שהעוגיות פגו")

        # שמירת HTML לבדיקה
        debug_file = output / "debug_page.html"
        debug_file.write_text(html[:50000], encoding="utf-8")
        print(f"🔧 HTML נשמר לבדיקה: {debug_file}")
        return

    print(f"📋 נמצאו {len(image_urls)} תמונות")

    # הורדה
    print(f"\n⬇️  מוריד תמונות ל: {output}/")
    downloaded = 0
    for i, img_url in enumerate(image_urls, 1):
        # קביעת שם קובץ
        parsed = urlparse(img_url)
        ext = Path(parsed.path).suffix or ".jpg"
        if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            ext = ".jpg"
        filename = f"image_{i:03d}{ext}"
        dest = output / filename

        print(f"[{i}/{len(image_urls)}] {filename}")

        # נסה רזולוציה גבוהה
        high_res_url = get_best_resolution(img_url)

        if download_image(session, high_res_url, dest):
            downloaded += 1
        elif high_res_url != img_url:
            # חזרה ל-URL המקורי
            download_image(session, img_url, dest)
            downloaded += 1

        time.sleep(0.5)  # נימוס - עיכוב קטן בין הורדות

    print(f"\n🎉 הסתיים! הורדו {downloaded}/{len(image_urls)} תמונות")
    print(f"📁 תמונות נשמרו ב: {output.absolute()}")


def main():
    parser = argparse.ArgumentParser(
        description="הורדת תמונות מדף פייסבוק ציבורי",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
דוגמאות שימוש:
  python3 fb_download.py --cookies cookies.txt https://www.facebook.com/share/1ANe4VjCSd/
  python3 fb_download.py --cookies cookies.txt --output ./my_photos https://www.facebook.com/YourPageName

כיצד לקבל קובץ cookies.txt:
  1. התקן בדפדפן: 'Get cookies.txt LOCALLY' (Chrome/Firefox)
  2. היכנס לפייסבוק
  3. לחץ על התוסף ובחר Export
  4. שמור כ-cookies.txt באותה תיקייה
        """
    )
    parser.add_argument("url", help="URL של דף הפייסבוק")
    parser.add_argument("--cookies", default="cookies.txt", help="נתיב לקובץ cookies.txt (ברירת מחדל: cookies.txt)")
    parser.add_argument("--output", default="fb_images", help="תיקיית יעד לתמונות (ברירת מחדל: fb_images)")

    args = parser.parse_args()

    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    download_facebook_images(args.url, args.cookies, args.output)


if __name__ == "__main__":
    main()

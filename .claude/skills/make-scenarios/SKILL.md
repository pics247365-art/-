---
name: make-scenarios
description: >
  בונה סנריו ב-Make.com עבור אילן — מכיר את כל החיבורים, ה-IDs, מבנה
  הגיליון, ופלאגין Make MCP. מחליף את make-skills הרשמי שנחסם.
---

# סקיל — בניית סנריו ב-Make

## פרטי חשבון Make
- **TeamID:** 2531873

## חיבורים פעילים
| שירות | Connection ID |
|--------|--------------|
| OpenAI (GPT-4o + Image) | 10300574 |
| Google Sheets | 10300565 |
| Google Drive | 10198899 |
| Facebook + Instagram | 10198979 |
| Telegram | 10404147 |

## הסנריו הקיימים
| שם | ID | תדירות | מצב |
|----|-----|---------|-----|
| ייצור תוכן חודשי - כלבנות | 7229920 | On-demand | לא פעיל |
| פרסום יומי + עדכון טלגרם | 7229940 | יומי 08:00 | לא פעיל |
| פייפליין תוכן AI - כלבנות | 7144009 | — | לא תקין |

## גיליון Google Sheets — תכנון חודשי
- **Spreadsheet ID:** `1bH5iwzLs3ok3DTQ_bNsG_g8WU5HrAb0WzTDyLjWGlfM`
- **Sheet name:** תכנון חודשי
- **עמודות:** A=תאריך | B=טקסט | C=imgbb URL | D=Drive File ID | E=סטטוס
- **ערכי סטטוס:** ממתין לאישור → מאושר → פורסם

## Google Drive — תיקיית תמונות
- **Folder ID:** `1-WZs3jiXqW2zEjvvwF_LQWXtdb_KdzUE`

## פייסבוק
- **Page ID:** `1217172458156408`

## ערכים שחסרים (placeholder)
- `YOUR_IMGBB_API_KEY` — נרשם ב-imgbb.com → API
- `YOUR_INSTAGRAM_ACCOUNT_ID` — בודקים ב-Make בחיבור Instagram
- `YOUR_TELEGRAM_CHAT_ID` — שולחים הודעה לבוט ומקבלים

## נוסחאות IML שימושיות
```
תאריך יחסי:     {{formatDate(addDays(now; 1.i - 1); "DD/MM/YYYY")}}
תאריך היום:     {{formatDate(now; "DD/MM/YYYY")}}
```

## כשמתבקשים לבנות סנריו
1. הגדר מה הסנריו עושה (trigger + action)
2. בחר מודולים מאומתים — לעולם אל תמציא שמות מודולים
3. וודא connection ID נכון לכל מודול
4. הוסף scheduling מתאים
5. שלח דרך `mcp__Make__scenarios_create`
6. בדוק `isinvalid: false` בתשובה

## מודולים מאומתים (שנבדקו ועובדים)
- `builtin:BasicRepeater` v1
- `openai-gpt-3:CreateCompletion` v1
- `openai-gpt-3:GenerateImage` v1
- `http:ActionSendData` v3
- `google-drive:uploadAFile` v4
- `google-drive:getAFile` v4
- `google-sheets:addRow` v2
- `google-sheets:filterRows` v2
- `google-sheets:updateRow` v2
- `facebook-pages:CreatePostWithPhotos` v6
- `instagram-business:CreatePostPhoto` v1
- `telegram:SendReplyMessage` v1

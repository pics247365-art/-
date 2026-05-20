'use strict';

/* ── CONSTANTS ── */
const API_URL   = 'https://api.anthropic.com/v1/messages';
const MODEL     = 'claude-sonnet-4-6';
const MAX_TOKENS = 1024;
const MAX_HISTORY = 20;  // מספר הודעות מקסימלי בהיסטוריה

const SYSTEM_PROMPT = `שמך הוא "לב" ואתה חבר אוהב, חכם וסבלני, שמלווה אנשים בשעות של בדידות, עצב, או קושי.
אתה פונה בעיקר לאנשים מבוגרים (גיל השלישי) ולאנשים המתמודדים עם אתגרים נפשיים.

מי אתה:
• חבר אמיתי שמקשיב ואכפת לו — לא מטפל, לא רופא, לא פסיכולוג
• מדבר עברית פשוטה, חמה וברורה — משפטים קצרים ונגישים
• מלא כבוד, אהבה וסבלנות אינסופית לכל אדם

כיצד אתה מנהל שיחה:
• תמיד מתחיל בהקשבה ואישור הרגשות לפני כל ייעוץ — הרגשה חייבת להיות מוכרת קודם
• שואל שאלות עדינות ופתוחות: "ספר לי עוד", "מה עובר עליך?", "איך זה מרגיש אצלך?"
• משקף את מה שנאמר כדי שהאדם ירגיש נשמע ומובן: "אני שומע שאתה מרגיש..."
• מכיר בכאב ובקושי מבלי להגזים או למזער אותו
• מכניס תקווה ואור בצורה טבעית, לא מאולצת ולא מתחסדת
• לא ממהר ולא לוחץ — כל אדם בקצב שלו, וזה בסדר גמור
• כותב בדרך כלל 2 עד 4 משפטים — לא יותר, כדי לא להציף

עקרונות מ-CBT (טיפול קוגניטיבי-התנהגותי):
• כשמישהו חושב מחשבה שלילית חוזרת, עוזר לבחון אותה בעדינות: "האם יש דרך אחרת להסתכל על זה?"
• מחפש ומזכיר חוזקות מהסיפור שנאמר: "אני שומע כמה חוזק יש בך — עברת כבר דברים קשים ועמדת בהם"
• מעודד פעולות קטנות ומשמחות: "מה דבר קטן אחד שיכול להביא לך קצת שמחה היום?"
• עוזר לפרק דאגות גדולות לצעדים קטנים ואפשריים
• מחפש ראיות לדברים טובים שאולי לא שמו לב אליהם

עקרונות מ-NLP (תכנות נוירו-לשוני):
• משתמש בשפה חיובית וממוקדת-עתיד: "מה יכול לעזור" ולא "מה לא עובד"
• משקף את השפה שהאדם עצמו השתמש בה — זה בונה אמון ומרגיש מוכר
• עוזר לאדם לחבר בין קושי עכשווי לבין כוחות פנימיים שכבר הוכיח שיש לו
• מוצא חוויות חיוביות מהעבר ועוזר לחזק אותן כמשאב
• משתמש לפעמים בהדמיה עדינה: "בוא נדמיין יחד..."

גבולות חשובים:
• אם יש ביטוי כלשהו של מחשבות לפגיעה עצמית, קח אותן ברצינות מלאה ואמור:
  "אני שומע אותך, וזה חשוב מאד — חשוב שתשוחח עכשיו עם מישהו שיכול לעזור.
   אנא פנה לקו החם ער"ן: 1201 — שם יש אנשים שרוצים לשמוע, 24 שעות ביממה."
• לשאלות על תרופות, מינונים, טיפולים רפואיים: "לנושא הזה חשוב לדבר עם רופא — הם יכולים לעזור הרבה יותר ממני"
• תמיד כנה לגבי מה אתה: חבר שמקשיב ואוהב, לא איש מקצוע

סגנון כתיבה:
• משפטים קצרים וברורים — שפה פשוטה, ללא מינוח מקצועי
• חמימות אמיתית וכנה — לא מחניפה
• לפעמים שימוש ב"יקירי" או "חבר יקר" — רק כשזה מרגיש טבעי ולא מתנשא
• לפעמים סיום בשאלה עדינה להמשך השיחה`;

const WELCOME = `שלום, שמחה שהגעת 💚

אני לב — ואני כאן בשבילך, בלי שיפוטים ובלי לחץ.

אפשר לספר לי מה על לבך. איך אתה מרגיש היום?`;

/* ── STATE ── */
let messages  = [];
let apiKey    = '';
let isTyping  = false;
let fontSize  = 19;     // px

/* ── DOM ── */
const $  = id => document.getElementById(id);
const setupScreen   = $('setup-screen');
const chatScreen    = $('chat-screen');
const apiKeyInput   = $('api-key-input');
const setupBtn      = $('setup-btn');
const setupError    = $('setup-error');
const msgContainer  = $('messages');
const msgInput      = $('message-input');
const sendBtn       = $('send-btn');
const typingEl      = $('typing-indicator');
const settingsBtn   = $('settings-btn');
const clearBtn      = $('clear-btn');
const fontUpBtn     = $('font-up-btn');
const fontDownBtn   = $('font-down-btn');
const confirmDialog = $('confirm-dialog');
const confirmText   = $('confirm-text');
const confirmYes    = $('confirm-yes');
const confirmNo     = $('confirm-no');

/* ── INIT ── */
function init() {
  // ?reset בכתובת מאפשר לבן משפחה לעדכן את הקוד
  const params = new URLSearchParams(window.location.search);
  if (params.has('reset')) {
    localStorage.removeItem('lev_api_key');
    window.history.replaceState({}, '', window.location.pathname);
  }

  const saved = localStorage.getItem('lev_api_key');
  const savedFont = parseInt(localStorage.getItem('lev_font_size'), 10);
  if (savedFont && savedFont >= 15 && savedFont <= 28) {
    fontSize = savedFont;
    document.documentElement.style.setProperty('--base-size', fontSize + 'px');
  }

  if (saved) {
    apiKey = saved;
    showChat();
    addWelcome();
  } else {
    showSetup();
  }

  bindEvents();
}

/* ── EVENT BINDING ── */
function bindEvents() {
  setupBtn.addEventListener('click', handleSetup);
  apiKeyInput.addEventListener('keydown', e => { if (e.key === 'Enter') handleSetup(); });

  sendBtn.addEventListener('click', handleSend);
  msgInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
  });
  msgInput.addEventListener('input', autoResize);

  settingsBtn.addEventListener('click', () => {
    showConfirm('לאפס את מפתח הגישה ולצאת?', () => {
      localStorage.removeItem('lev_api_key');
      apiKey = '';
      messages = [];
      msgContainer.innerHTML = '';
      showSetup();
    });
  });

  clearBtn.addEventListener('click', () => {
    showConfirm('להתחיל שיחה חדשה?', () => {
      messages = [];
      msgContainer.innerHTML = '';
      addWelcome();
    });
  });

  fontUpBtn.addEventListener('click', () => changeFontSize(2));
  fontDownBtn.addEventListener('click', () => changeFontSize(-2));
}

/* ── FONT SIZE ── */
function changeFontSize(delta) {
  fontSize = Math.max(15, Math.min(28, fontSize + delta));
  document.documentElement.style.setProperty('--base-size', fontSize + 'px');
  localStorage.setItem('lev_font_size', fontSize);
}

/* ── CONFIRM DIALOG ── */
let resolveConfirm = null;

function showConfirm(text, onYes) {
  confirmText.textContent = text;
  confirmDialog.classList.remove('hidden');
  confirmYes.onclick = () => { confirmDialog.classList.add('hidden'); onYes(); };
  confirmNo.onclick  = () => { confirmDialog.classList.add('hidden'); };
}

/* ── SCREENS ── */
function showSetup() {
  setupScreen.classList.remove('hidden');
  chatScreen.classList.add('hidden');
  setTimeout(() => apiKeyInput.focus(), 100);
}

function showChat() {
  setupScreen.classList.add('hidden');
  chatScreen.classList.remove('hidden');
}

/* ── SETUP ── */
function handleSetup() {
  const key = apiKeyInput.value.trim();
  if (key.length < 20) {
    setupError.classList.remove('hidden');
    apiKeyInput.focus();
    return;
  }
  setupError.classList.add('hidden');
  localStorage.setItem('lev_api_key', key);
  apiKey = key;
  showChat();
  addWelcome();
}

/* ── WELCOME ── */
function addWelcome() {
  addMessageToUI('ai', WELCOME);
  messages = [];
}

/* ── MESSAGE UI ── */
function addMessageToUI(role, text) {
  const wrap = document.createElement('div');
  wrap.className = `message ${role === 'user' ? 'user' : 'ai'}`;

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  bubble.textContent = text;

  const time = document.createElement('div');
  time.className = 'message-time';
  const now = new Date();
  time.textContent = now.toLocaleTimeString('he-IL', { hour: '2-digit', minute: '2-digit' });

  wrap.appendChild(bubble);
  wrap.appendChild(time);
  msgContainer.appendChild(wrap);
  scrollDown();
}

function scrollDown() {
  msgContainer.scrollTop = msgContainer.scrollHeight;
}

function autoResize() {
  msgInput.style.height = 'auto';
  msgInput.style.height = Math.min(msgInput.scrollHeight, 130) + 'px';
}

/* ── TYPING INDICATOR ── */
function showTyping()  { typingEl.classList.remove('hidden'); scrollDown(); }
function hideTyping()  { typingEl.classList.add('hidden'); }

/* ── SEND MESSAGE ── */
async function handleSend() {
  const text = msgInput.value.trim();
  if (!text || isTyping) return;

  msgInput.value = '';
  autoResize();
  addMessageToUI('user', text);
  messages.push({ role: 'user', content: text });

  /* חתוך היסטוריה ישנה כדי לא לחרוג ממגבלת tokens */
  if (messages.length > MAX_HISTORY) {
    messages = messages.slice(messages.length - MAX_HISTORY);
  }

  isTyping = true;
  sendBtn.disabled = true;
  showTyping();

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true'
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: MAX_TOKENS,
        system: SYSTEM_PROMPT,
        messages
      })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err?.error?.message || `שגיאה ${res.status}`);
    }

    const data  = await res.json();
    const reply = data?.content?.[0]?.text?.trim() || 'מצטער, לא הצלחתי להבין. נסה שוב.';
    messages.push({ role: 'assistant', content: reply });
    hideTyping();
    addMessageToUI('ai', reply);

  } catch (err) {
    console.error('שגיאת API:', err);
    hideTyping();

    const isAuthError = err.message?.includes('401') || err.message?.toLowerCase().includes('auth');
    const errMsg = isAuthError
      ? 'המפתח אינו תקין. לחץ על כפתור ההגדרות כדי לעדכן.'
      : 'נתקלתי בקושי טכני. אנא נסה שוב בעוד רגע.';

    addMessageToUI('ai', errMsg);
  } finally {
    isTyping = false;
    sendBtn.disabled = false;
    msgInput.focus();
  }
}

/* ── START ── */
document.addEventListener('DOMContentLoaded', init);

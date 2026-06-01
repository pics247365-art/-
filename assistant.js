/* ======================================
   עוזר חכם – Hebrew AI Assistant Logic
   ====================================== */

'use strict';

// ── State ─────────────────────────────────
const state = {
  isRecording: false,
  finalText: '',
  interimText: '',
  selectedType: null,
  items: [],
  filter: 'all',
  recognition: null,
  toastTimer: null,
};

// ── Hebrew Detection Patterns ─────────────
const PATTERNS = {
  task: {
    keywords: [
      'לעשות','לקנות','לשלוח','להביא','לתקן','לארגן','לנקות','לשלם',
      'להוריד','להעלות','לפתור','לטפל','לדאוג','לבדוק','לגמור','לסיים',
      'להכין','להגיש','לכתוב','לקרוא','לענות','לחזור','לפנות','לסדר',
      'להזמין','לשנות','לעדכן','לרשום','לאסוף','לבשל','לנהוג',
    ],
    phrases: [
      'צריך ל','חייב ל','חייבת ל','אני צריך','אני חייב','אני חייבת',
      'יש לי לעשות','צריכה ל','צריכים ל','צריך לי','חייב לי',
    ],
  },
  reminder: {
    keywords: [
      'תזכורת','להזכיר','לזכור','לא לשכוח','מחר','היום','בשעה',
      'בתאריך','בשבוע','בחודש','בפגישה','בערב','בבוקר','בצהריים',
      'בראשון','בשני','בשלישי','ברביעי','בחמישי','בשישי','בשבת',
      'בחנוכה','בפסח','בקיץ','בחורף','שעה','דקות','יום','שבת',
    ],
    phrases: [
      'לא לשכוח','תזכיר לי','תזכרי לי','תזכירי לי','מחר ב','היום ב',
      'ב-','בשעה ','זמן ל','להגיע ל','לא לאחר','לפני ה',
    ],
  },
  idea: {
    keywords: [
      'רעיון','אפשר','אולי','מה אם','למה לא','חשבתי','יכול להיות',
      'אפשרות','הצעה','תוכנית','להמציא','לפתח','ליצור','לבנות',
      'לנסות','לחקור','מעניין','כדאי','שווה','יהיה מגניב','חלומי',
    ],
    phrases: [
      'מה אם','למה לא','חשבתי על','יש לי רעיון','אולי אפשר',
      'מה דעתך','מה אם היינו','יכולנו','היה כיף','מגניב שיהיה',
    ],
  },
};

// ── Detection engine ──────────────────────
function detectType(text) {
  const lower = text.toLowerCase();
  const scores = { task: 0, reminder: 0, idea: 0 };

  for (const [type, cfg] of Object.entries(PATTERNS)) {
    for (const kw of cfg.keywords) {
      if (lower.includes(kw)) scores[type] += 1;
    }
    for (const ph of cfg.phrases) {
      if (lower.includes(ph)) scores[type] += 2;
    }
  }

  const best = Object.entries(scores).reduce((a, b) => (b[1] > a[1] ? b : a));
  return best[1] > 0 ? best[0] : 'idea'; // default to idea
}

// ── Elements ──────────────────────────────
const els = {
  statusText:       document.getElementById('statusText'),
  waveformWrap:     document.getElementById('waveformWrap'),
  waveform:         document.getElementById('waveform'),
  transcriptFinal:  document.getElementById('transcriptFinal'),
  transcriptInterim:document.getElementById('transcriptInterim'),
  cursor:           document.getElementById('cursor'),
  recordBtn:        document.getElementById('recordBtn'),
  recordRipple:     document.getElementById('recordRipple'),
  recordLabel:      document.getElementById('recordLabel'),
  micIcon:          document.querySelector('.mic-icon'),
  stopIcon:         document.querySelector('.stop-icon'),
  saveArea:         document.getElementById('saveArea'),
  typeBadges:       document.getElementById('typeBadges'),
  saveBtn:          document.getElementById('saveBtn'),
  discardBtn:       document.getElementById('discardBtn'),
  cardsList:        document.getElementById('cardsList'),
  emptyState:       document.getElementById('emptyState'),
  filterTabs:       document.getElementById('filterTabs'),
  statPill:         document.getElementById('statPill'),
  taskCount:        document.getElementById('taskCount'),
  reminderCount:    document.getElementById('reminderCount'),
  ideaCount:        document.getElementById('ideaCount'),
  toast:            document.getElementById('toast'),
  clearAllBtn:      document.getElementById('clearAllBtn'),
  noSupportOverlay: document.getElementById('noSupportOverlay'),
};

// ── Speech Recognition Setup ──────────────
function initRecognition() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    els.noSupportOverlay.classList.remove('hidden');
    return null;
  }

  const recognition = new SR();
  recognition.lang = 'he-IL';
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    state.isRecording = true;
    setRecordingUI(true);
  };

  recognition.onresult = (e) => {
    let interim = '';
    let final = state.finalText;

    for (let i = e.resultIndex; i < e.results.length; i++) {
      const t = e.results[i][0].transcript;
      if (e.results[i].isFinal) {
        final += (final ? ' ' : '') + t;
      } else {
        interim = t;
      }
    }

    state.finalText = final;
    state.interimText = interim;
    updateTranscriptDisplay();
  };

  recognition.onerror = (e) => {
    if (e.error === 'no-speech') return;
    if (e.error === 'aborted') return;
    console.warn('Speech error:', e.error);
    stopRecording();
    showToast('שגיאה בזיהוי קול: ' + e.error);
  };

  recognition.onend = () => {
    if (state.isRecording) {
      // Try to restart if we stopped unexpectedly
      try { recognition.start(); } catch (_) { stopRecording(); }
    }
  };

  return recognition;
}

// ── Recording control ─────────────────────
function startRecording() {
  state.finalText = '';
  state.interimText = '';
  updateTranscriptDisplay();
  els.saveArea.classList.add('hidden');

  if (!state.recognition) {
    state.recognition = initRecognition();
    if (!state.recognition) return;
  }

  try {
    state.recognition.start();
  } catch (e) {
    // already started
  }
}

function stopRecording() {
  state.isRecording = false;
  setRecordingUI(false);

  if (state.recognition) {
    try { state.recognition.stop(); } catch (_) {}
  }

  const fullText = (state.finalText + ' ' + state.interimText).trim();
  state.finalText = fullText;
  state.interimText = '';
  updateTranscriptDisplay();

  if (fullText.length > 1) {
    showSaveArea(fullText);
  }
}

function toggleRecording() {
  if (state.isRecording) {
    stopRecording();
  } else {
    startRecording();
  }
}

// ── UI state helpers ──────────────────────
function setRecordingUI(active) {
  els.recordBtn.classList.toggle('recording', active);
  els.recordRipple.classList.toggle('active', active);
  els.waveformWrap.classList.toggle('active', active);
  els.waveform.classList.toggle('animated', active);
  els.cursor.classList.toggle('visible', active);
  els.micIcon.style.display  = active ? 'none' : 'block';
  els.stopIcon.style.display = active ? 'block' : 'none';
  els.recordLabel.textContent = active ? 'מקשיב...' : 'לחץ להקלטה';
  els.statusText.textContent  = active ? '🎙️ מקשיב...' : 'לחץ על הכפתור ודבר בעברית';
  els.statusText.className = 'status-text' + (active ? ' recording' : '');
}

function updateTranscriptDisplay() {
  els.transcriptFinal.textContent  = state.finalText;
  els.transcriptInterim.textContent = state.interimText
    ? (state.finalText ? ' ' : '') + state.interimText
    : '';
}

function showSaveArea(text) {
  const detected = detectType(text);
  state.selectedType = detected;

  document.querySelectorAll('.type-btn').forEach(btn => {
    const isSelected = btn.dataset.type === detected;
    btn.classList.toggle('selected', isSelected);
    btn.setAttribute('aria-checked', isSelected ? 'true' : 'false');
  });

  els.saveArea.classList.remove('hidden');
  els.statusText.textContent = 'בחר סוג ושמור';
  els.statusText.className = 'status-text success';
}

// ── Type selection ────────────────────────
document.querySelectorAll('.type-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    state.selectedType = btn.dataset.type;
    document.querySelectorAll('.type-btn').forEach(b => {
      const isSelected = b === btn;
      b.classList.toggle('selected', isSelected);
      b.setAttribute('aria-checked', isSelected ? 'true' : 'false');
    });
  });
});

// ── Save / Discard ────────────────────────
els.saveBtn.addEventListener('click', () => {
  const text = state.finalText.trim();
  if (!text) return;

  const item = {
    id:        Date.now(),
    text,
    type:      state.selectedType || 'idea',
    completed: false,
    createdAt: new Date().toISOString(),
  };

  state.items.unshift(item);
  saveToStorage();
  renderCards();
  updateSummary();

  // Reset
  state.finalText = '';
  state.interimText = '';
  state.selectedType = null;
  updateTranscriptDisplay();
  els.saveArea.classList.add('hidden');
  els.statusText.textContent = 'לחץ על הכפתור ודבר בעברית';
  els.statusText.className = 'status-text';

  const labels = { task: 'משימה נשמרה 📋', reminder: 'תזכורת נשמרה 🔔', idea: 'רעיון נשמר 💡' };
  showToast(labels[item.type] || 'נשמר');
});

els.discardBtn.addEventListener('click', () => {
  state.finalText = '';
  state.interimText = '';
  state.selectedType = null;
  updateTranscriptDisplay();
  els.saveArea.classList.add('hidden');
  els.statusText.textContent = 'לחץ על הכפתור ודבר בעברית';
  els.statusText.className = 'status-text';
});

// ── Record button ─────────────────────────
els.recordBtn.addEventListener('click', toggleRecording);

// ── Filter tabs ───────────────────────────
els.filterTabs.addEventListener('click', (e) => {
  const tab = e.target.closest('.filter-tab');
  if (!tab) return;
  state.filter = tab.dataset.filter;
  document.querySelectorAll('.filter-tab').forEach(t => {
    t.classList.toggle('active', t === tab);
    t.setAttribute('aria-selected', t === tab ? 'true' : 'false');
  });
  renderCards();
});

// ── Clear all ─────────────────────────────
els.clearAllBtn.addEventListener('click', () => {
  if (state.items.length === 0) return;
  if (!confirm('למחוק את כל הפריטים?')) return;
  state.items = [];
  saveToStorage();
  renderCards();
  updateSummary();
  showToast('הלוח נוקה');
});

// ── Cards render ──────────────────────────
function renderCards() {
  const filtered = state.filter === 'all'
    ? state.items
    : state.items.filter(i => i.type === state.filter);

  // Keep empty state element but remove all cards
  const cards = els.cardsList.querySelectorAll('.card-item');
  cards.forEach(c => c.remove());

  if (filtered.length === 0) {
    els.emptyState.style.display = '';
    return;
  }

  els.emptyState.style.display = 'none';

  filtered.forEach(item => {
    const card = buildCard(item);
    els.cardsList.appendChild(card);
  });
}

function buildCard(item) {
  const div = document.createElement('div');
  div.className = `card-item ${item.type}-card${item.completed ? ' completed' : ''}`;
  div.dataset.id = item.id;
  div.setAttribute('role', 'listitem');

  const time = formatTime(item.createdAt);
  const labels = { task: 'משימה', reminder: 'תזכורת', idea: 'רעיון' };
  const emojis = { task: '📋', reminder: '🔔', idea: '💡' };

  div.innerHTML = `
    <button class="card-check" aria-label="סמן כ${item.completed ? 'לא ' : ''}הושלם">${item.completed ? '✓' : ''}</button>
    <div class="card-body">
      <p class="card-text">${escapeHTML(item.text)}</p>
      <div class="card-meta">
        <span class="card-type-badge ${item.type}-badge">${emojis[item.type]} ${labels[item.type]}</span>
        <span class="card-time">${time}</span>
      </div>
    </div>
    <button class="card-delete" aria-label="מחק פריט">
      <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
      </svg>
    </button>
  `;

  div.querySelector('.card-check').addEventListener('click', () => toggleComplete(item.id));
  div.querySelector('.card-delete').addEventListener('click', () => deleteItem(item.id));

  return div;
}

function toggleComplete(id) {
  const item = state.items.find(i => i.id === id);
  if (!item) return;
  item.completed = !item.completed;
  saveToStorage();
  renderCards();
  updateSummary();
}

function deleteItem(id) {
  state.items = state.items.filter(i => i.id !== id);
  saveToStorage();
  renderCards();
  updateSummary();
  showToast('פריט נמחק');
}

// ── Summary counts ────────────────────────
function updateSummary() {
  const total = state.items.length;
  const tasks     = state.items.filter(i => i.type === 'task').length;
  const reminders = state.items.filter(i => i.type === 'reminder').length;
  const ideas     = state.items.filter(i => i.type === 'idea').length;

  els.statPill.textContent = `${total} פריטים`;
  els.taskCount.innerHTML     = `📋 <span>${tasks}</span>`;
  els.reminderCount.innerHTML = `🔔 <span>${reminders}</span>`;
  els.ideaCount.innerHTML     = `💡 <span>${ideas}</span>`;
}

// ── Toast ─────────────────────────────────
function showToast(msg) {
  clearTimeout(state.toastTimer);
  els.toast.textContent = msg;
  els.toast.classList.add('show');
  state.toastTimer = setTimeout(() => els.toast.classList.remove('show'), 2400);
}

// ── LocalStorage ──────────────────────────
function saveToStorage() {
  try {
    localStorage.setItem('hebrewAssistant_items', JSON.stringify(state.items));
  } catch (_) {}
}

function loadFromStorage() {
  try {
    const stored = localStorage.getItem('hebrewAssistant_items');
    if (stored) state.items = JSON.parse(stored);
  } catch (_) {
    state.items = [];
  }
}

// ── Helpers ───────────────────────────────
function escapeHTML(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function formatTime(iso) {
  const d = new Date(iso);
  const now = new Date();
  const diff = now - d;

  if (diff < 60000)    return 'עכשיו';
  if (diff < 3600000)  return `לפני ${Math.floor(diff/60000)} דקות`;
  if (diff < 86400000) return `לפני ${Math.floor(diff/3600000)} שעות`;

  return d.toLocaleDateString('he-IL', { day:'numeric', month:'short' });
}

// ── Service Worker registration ───────────
function registerSW() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js')
      .catch(err => console.warn('SW registration failed:', err));
  }
}

// ── Init ──────────────────────────────────
function init() {
  loadFromStorage();
  renderCards();
  updateSummary();
  registerSW();

  // Check speech support
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    els.noSupportOverlay.classList.remove('hidden');
  }
}

init();

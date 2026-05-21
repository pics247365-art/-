/* Service Worker – Hebrew AI Assistant PWA */
const CACHE = 'hebrew-assistant-v1';
const ASSETS = [
  '/assistant.html',
  '/assistant.css',
  '/assistant.js',
  '/manifest.json',
  '/icon.svg',
];

// Install: cache core assets
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

// Activate: clear old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch: cache-first for assets, network-first for fonts/API
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // Skip non-GET, external origins except Google Fonts
  if (e.request.method !== 'GET') return;
  if (url.origin !== location.origin && !url.hostname.includes('googleapis.com') && !url.hostname.includes('gstatic.com')) return;

  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;

      return fetch(e.request).then(res => {
        // Cache same-origin assets and fonts
        if (res.ok && (url.origin === location.origin || url.hostname.includes('gstatic.com'))) {
          const clone = res.clone();
          caches.open(CACHE).then(cache => cache.put(e.request, clone));
        }
        return res;
      }).catch(() => cached || new Response('Offline', { status: 503 }));
    })
  );
});

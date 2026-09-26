// Service worker de AuryApp — generado por core/pwa.py (no editar la versión a mano).
const VERSION = {{ version|safe }};
const CACHE = 'auryapp-' + VERSION;
const STATIC_PREFIX = {{ static_url|safe }};
const PRECACHE = {{ precache|safe }};

const OFFLINE_HTML = `<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Sin conexión — AuryApp</title>
<style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
font-family:system-ui,sans-serif;background:#1a6fc4;color:#fff;text-align:center;padding:24px}
button{margin-top:16px;padding:10px 20px;border:0;border-radius:8px;font-size:16px;color:#1a6fc4;background:#fff}</style>
</head><body><div><h1>Sin conexión</h1><p>AuryApp necesita internet para mostrar los datos al día.</p>
<button onclick="location.reload()">Reintentar</button></div></body></html>`;

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      // Si algún estático falla, el SW se instala igual (la caché es solo para ir sin conexión)
      .then((cache) => Promise.all(PRECACHE.map((url) => cache.add(url).catch(() => null))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k.startsWith('auryapp-') && k !== CACHE).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;                  // POST, etc.: sin tocar
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;   // CDN, APIs externas: sin tocar

  // Páginas: siempre de red, nunca en caché. Sin conexión, aviso.
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req).catch(() => new Response(OFFLINE_HTML, {
        status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' },
      }))
    );
    return;
  }

  // Estáticos: red primero revalidando con el servidor; la copia solo sin conexión.
  if (url.pathname.startsWith(STATIC_PREFIX)) {
    event.respondWith(
      fetch(req, { cache: 'no-cache' })
        .then((resp) => {
          if (resp.ok) {
            const copia = resp.clone();
            caches.open(CACHE).then((cache) => cache.put(req, copia));
          }
          return resp;
        })
        .catch(() => caches.match(req))
    );
  }
  // Todo lo demás (JSON de la app, descargas, admin...): comportamiento normal del navegador.
});

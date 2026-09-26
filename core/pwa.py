"""PWA / TWA: manifest y service worker servidos desde la raíz (scope '/').

Estrategia de caché (para que las actualizaciones se vean al momento):
- HTML: SIEMPRE de red, nunca se guarda en caché (datos personales + siempre la última versión).
  Sin conexión se muestra un aviso.
- /static/: red primero con revalidación (cache: 'no-cache'); la copia solo se usa sin conexión.
- VERSION cambia en cada despliegue (K_REVISION de Cloud Run) → sw.js distinto → el navegador
  instala el nuevo y borra las cachés viejas. Nunca se fuerza una recarga de la página.
"""
import json
import os
import time

from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.templatetags.static import static

# Cloud Run pone K_REVISION distinto en cada despliegue; en local, la hora de arranque.
VERSION = os.environ.get('K_REVISION') or f'local-{int(time.time())}'

PRECACHE = [
    'css/main.css',
    'js/functions.js',
    'img/icons/favicon-32.png',
    'img/icons/icon-192.png',
]


def manifest(request):
    data = {
        'name': 'AuryApp · Beach Club',
        'short_name': 'AuryApp',
        'description': 'Gestión interna del beach club',
        'id': '/',
        'start_url': '/',
        'scope': '/',
        'display': 'standalone',
        'orientation': 'any',
        'background_color': '#1a6fc4',
        'theme_color': '#1a6fc4',
        'lang': 'es',
        'icons': [
            {'src': static('img/icons/icon-192.png'), 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
            {'src': static('img/icons/icon-512.png'), 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
            {'src': static('img/icons/icon-maskable-512.png'), 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        ],
    }
    resp = JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    resp['Content-Type'] = 'application/manifest+json'
    resp['Cache-Control'] = 'no-cache'
    return resp


def service_worker(request):
    # json.dumps da literales JS válidos y legibles (escapejs convertiría '-' en -)
    js = render_to_string('core/sw.js', {
        'version': json.dumps(VERSION),
        'precache': json.dumps([static(p) for p in PRECACHE]),
        'static_url': json.dumps(static('')),
    })
    resp = HttpResponse(js, content_type='application/javascript; charset=utf-8')
    # El propio sw.js nunca se cachea: así el navegador ve la versión nueva en cuanto se despliega
    resp['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return resp

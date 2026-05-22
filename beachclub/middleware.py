from django.conf import settings
from django.shortcuts import redirect

RUTAS_PUBLICAS = [settings.LOGIN_URL, '/registro/', '/admin/', '/static/', '/media/']

class LoginRequeridoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            ruta = request.path_info
            if not any(ruta.startswith(p) for p in RUTAS_PUBLICAS):
                return redirect(f"{settings.LOGIN_URL}?next={ruta}")
        response = self.get_response(request)
        # Fabric.js necesita unsafe-eval para cargar el canvas desde JSON
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data: blob: https:; "
            "connect-src 'self' https://cdn.jsdelivr.net https://api.open-meteo.com; "
            "frame-ancestors 'none';"
        )
        # HSTS: fuerza HTTPS durante 1 año (solo en producción)
        from django.conf import settings as _s
        if not _s.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        # Controla qué URL se filtra al salir de la app hacia links externos
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        # Deshabilita acceso a cámara, micro y geolocalización explícitamente
        response['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=()'
        return response

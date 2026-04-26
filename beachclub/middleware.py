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
        return response

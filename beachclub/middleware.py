from django.conf import settings
from django.shortcuts import redirect

RUTAS_PUBLICAS = [settings.LOGIN_URL, '/admin/']

class LoginRequeridoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            ruta = request.path_info
            if not any(ruta.startswith(p) for p in RUTAS_PUBLICAS):
                return redirect(f"{settings.LOGIN_URL}?next={ruta}")
        return self.get_response(request)

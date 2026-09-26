"""
URL configuration for beachclub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views, logout as auth_logout
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.templatetags.static import static as static_url
from core.views import registro
from core import pwa

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def favicon_view(request):
    # La URL del estático se resuelve en cada petición, no al importar urls.py
    return redirect(static_url('img/icons/favicon.ico'), permanent=True)

urlpatterns = [
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # Los navegadores piden /favicon.ico por su cuenta (pública en el middleware)
    path('favicon.ico', favicon_view),
    # PWA/TWA: en la raíz para que el service worker controle toda la app (públicas en el middleware)
    path('manifest.webmanifest', pwa.manifest, name='manifest'),
    path('sw.js', pwa.service_worker, name='service_worker'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registro, name='registro'),
    path('', include('core.urls')),
    path('personal/', include('personal.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/json/', views.eventos_json, name='eventos_json'),
    path('calendario/', views.calendario, name='calendario'),
]
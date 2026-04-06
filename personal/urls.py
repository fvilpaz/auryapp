from django.urls import path
from . import views

urlpatterns = [
    path('cuadrante/', views.cuadrante, name='cuadrante'),
]
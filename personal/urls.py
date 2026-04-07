from django.urls import path
from . import views

urlpatterns = [
    path('cuadrante/', views.cuadrante, name='cuadrante'),
    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('empleados/nuevo/', views.nuevo_empleado, name='nuevo_empleado'),
    path('empleados/<int:pk>/editar/', views.editar_empleado, name='editar_empleado'),
    path('turno/guardar/', views.guardar_turno, name='guardar_turno'),
]
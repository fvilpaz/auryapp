from django.urls import path
from . import views

urlpatterns = [
    path('cuadrante/', views.cuadrante, name='cuadrante'),
    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('empleados/nuevo/', views.nuevo_empleado, name='nuevo_empleado'),
    path('empleados/<int:pk>/', views.detalle_empleado, name='detalle_empleado'),
    path('empleados/<int:pk>/editar/', views.editar_empleado, name='editar_empleado'),
    path('turno/guardar/', views.guardar_turno, name='guardar_turno'),
    path('turno/posiciones/', views.guardar_posiciones, name='guardar_posiciones'),
    path('empleados/<int:pk>/solicitud/', views.nueva_solicitud, name='nueva_solicitud'),
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('solicitudes/nueva/', views.crear_solicitud, name='crear_solicitud'),
    path('vencimientos/', views.lista_vencimientos, name='lista_vencimientos'),
    path('vacaciones/', views.lista_vacaciones, name='lista_vacaciones'),
    path('dias-sueltos/', views.lista_dias_sueltos, name='lista_dias_sueltos'),
    path('solicitudes/<int:pk>/aprobar/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('solicitudes/<int:pk>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
]

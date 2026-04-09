from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/nuevo/', views.nuevo_evento, name='nuevo_evento'),
    path('eventos/<int:pk>/', views.detalle_evento, name='detalle_evento'),
    path('eventos/<int:pk>/editar/', views.editar_evento, name='editar_evento'),
    path('eventos/<int:pk>/eliminar/', views.eliminar_evento, name='eliminar_evento'),
    path('eventos/<int:pk>/documentos/subir/', views.subir_documento, name='subir_documento'),
    path('eventos/documentos/<int:doc_pk>/eliminar/', views.eliminar_documento, name='eliminar_documento'),
    path('eventos/json/', views.eventos_json, name='eventos_json'),
    path('calendario/', views.calendario, name='calendario'),
    path('espacios/', views.lista_espacios, name='lista_espacios'),
    path('espacios/<int:pk>/', views.detalle_espacio, name='detalle_espacio'),
    path('espacios/<int:pk>/asignar/', views.asignar_empleado, name='asignar_empleado'),
    path('espacios/<int:pk>/desasignar/<int:turno_id>/', views.desasignar_empleado, name='desasignar_empleado'),
    path('espacios/<int:pk>/mover/<int:turno_id>/', views.mover_empleado, name='mover_empleado'),
    path('tareas/<int:pk>/toggle/', views.toggle_tarea, name='toggle_tarea'),
    path('agenda/', views.agenda, name='agenda'),
    path('agenda/<int:pk>/eliminar/', views.eliminar_nota, name='eliminar_nota'),
    path('pedidos/', views.lista_espacios, name='pedidos'),
    path('pedidos/<int:pk>/', views.pedidos_espacio, name='pedidos_espacio'),
    path('pedidos/<int:pk>/nuevo/', views.nuevo_articulo, name='nuevo_articulo'),
    path('pedidos/articulo/<int:pk>/editar/', views.editar_articulo, name='editar_articulo'),
    path('pedidos/articulo/<int:pk>/eliminar/', views.eliminar_articulo, name='eliminar_articulo'),
    path('pedidos/articulo/<int:pk>/cantidad/', views.actualizar_cantidad, name='actualizar_cantidad'),
]
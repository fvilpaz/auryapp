from django.contrib import admin
from .models import Empleado, Turno

# Register your models here.

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos', 'rol', 'telefono', 'activo']
    list_filter = ['rol', 'activo']
    list_editable = ['activo']

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'fecha', 'hora_inicio', 'hora_fin', 'horas', 'estado', 'espacio']
    list_filter = ['fecha', 'estado', 'espacio']
    ordering = ['-fecha', 'empleado']
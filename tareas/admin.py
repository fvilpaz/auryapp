from django.contrib import admin
from .models import TareaPlantilla, TareaDelDia

# Register your models here.

@admin.register(TareaPlantilla)
class TareaPlantillaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'espacio', 'momento', 'orden', 'activa']
    list_filter = ['espacio', 'momento']
    list_editable = ['orden', 'activa']
    ordering = ['espacio', 'momento', 'orden']

@admin.register(TareaDelDia)
class TareaDelDiaAdmin(admin.ModelAdmin):
    list_display = ['plantilla', 'fecha', 'completada', 'completada_por', 'hora_completada']
    list_filter = ['fecha', 'completada', 'plantilla__espacio']
    ordering = ['-fecha']
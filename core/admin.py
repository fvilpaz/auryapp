from django.contrib import admin
from .models import Espacio, Evento

# Register your models here.

@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_editable = ['activo']

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'cliente', 'tipo', 'concepto', 'personas']
    list_filter = ['tipo', 'concepto']
    ordering = ['fecha']

from django.contrib import admin
from .models import Espacio

# Register your models here.

@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_editable = ['activo']

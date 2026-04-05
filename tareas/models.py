from django.db import models
from core.models import Espacio

# Create your models here.

class TareaPlantilla(models.Model):

    MOMENTO_CHOICES = [
        ('apertura', 'Apertura'),
        ('cierre', 'Cierre'),
    ]

    nombre = models.CharField(max_length=200)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, related_name='tareas_plantilla')
    momento = models.CharField(max_length=10, choices=MOMENTO_CHOICES)
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tarea plantilla'
        verbose_name_plural = 'Tareas plantilla'
        ordering = ['espacio', 'momento', 'orden']

    def __str__(self):
        return f"{self.espacio} — {self.get_momento_display()} — {self.nombre}"


class TareaDelDia(models.Model):

    plantilla = models.ForeignKey(TareaPlantilla, on_delete=models.CASCADE, related_name='instancias')
    fecha = models.DateField()
    completada = models.BooleanField(default=False)
    completada_por = models.CharField(max_length=100, blank=True)
    hora_completada = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Tarea del día'
        verbose_name_plural = 'Tareas del día'
        ordering = ['fecha', 'plantilla__momento', 'plantilla__orden']

    def __str__(self):
        return f"{self.plantilla} — {self.fecha}"
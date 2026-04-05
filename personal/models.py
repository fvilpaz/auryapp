from django.db import models
from core.models import Espacio

# Create your models here.

class Empleado(models.Model):

    ROL_CHOICES = [
        ('maitre', 'Maître'),
        ('jefe_sector', 'Jefe de sector'),
        ('camarero', 'Camarero'),
    ]

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100, blank=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} — {self.get_rol_display()}"


class Turno(models.Model):

    ESTADO_CHOICES = [
        ('trabajo', 'Trabajo'),
        ('libre', 'Día libre'),
        ('inamovible', 'Inamovible'),
        ('vacaciones', 'Vacaciones'),
        ('libre_vacaciones', 'Libre vacaciones'),
        ('finde_largo', 'Finde largo'),
        ('baja', 'Baja'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='turnos')
    fecha = models.DateField()
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    horas = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='trabajo')
    espacio = models.ForeignKey(Espacio, on_delete=models.SET_NULL, null=True, blank=True, related_name='turnos')

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        ordering = ['fecha', 'empleado']

    def __str__(self):
        return f"{self.empleado.nombre} — {self.fecha} — {self.get_estado_display()}"
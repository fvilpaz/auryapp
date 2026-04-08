from django.db import models
from core.models import Espacio

# Create your models here.

class Empleado(models.Model):

    CONTRATO_CHOICES = [
        ('indefinido', 'Indefinido'),
        ('temporal', 'Temporal'),
        ('fijo_discontinuo', 'Fijo discontinuo'),
        ('obra_servicio', 'Obra y servicio'),
        ('practicas', 'Prácticas'),
    ]

    ROL_CHOICES = [
        ('maitre', 'Maître'),
        ('segundo_maitre', 'Segundo Maître'),
        ('jefe_sector', 'Jefe de sector'),
        ('camarero', 'Camarero'),
        ('ayudante_camarero', 'Ayudante de camarero'),
    ]

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100, blank=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    posicion = models.PositiveIntegerField(default=0)
    tipo_contrato = models.CharField(max_length=20, choices=CONTRATO_CHOICES, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['posicion', 'nombre']

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


class SolicitudAusencia(models.Model):

    TIPO_CHOICES = [
        ('vacaciones', 'Vacaciones'),
        ('libre', 'Día libre'),
        ('inamovible', 'Libre inamovible'),
        ('libre_vacaciones', 'Libre vacaciones'),
        ('finde_largo', 'Finde largo'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='solicitudes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='vacaciones')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    notas = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Solicitud de ausencia'
        verbose_name_plural = 'Solicitudes de ausencia'
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"{self.empleado.nombre} — {self.get_tipo_display()} — {self.fecha_inicio} a {self.fecha_fin}"
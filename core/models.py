from django.db import models

# Create your models here.

class Espacio(models.Model):

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Espacio'
        verbose_name_plural = 'Espacios'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Evento(models.Model):

    TIPO_CHOICES = [
        ('boda', 'Boda'),
        ('graduacion', 'Graduación'),
        ('comunion', 'Comunión'),
        ('gala', 'Gala'),
        ('preboda', 'Preboda'),
        ('otro', 'Otro'),
    ]

    CONCEPTO_CHOICES = [
        ('cena', 'Cena'),
        ('comida', 'Comida'),
        ('almuerzo', 'Almuerzo'),
        ('barbacoa', 'Barbacoa'),
        ('cocktail', 'Cocktail'),
        ('barra', 'Barra'),
        ('ceremonia', 'Ceremonia'),
        ('otro', 'Otro'),
    ]

    cliente = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha = models.DateField()
    espacios = models.ManyToManyField(Espacio, related_name='eventos')
    concepto = models.CharField(max_length=20, choices=CONCEPTO_CHOICES)
    personas = models.PositiveIntegerField()
    notas = models.TextField(blank=True)
    plano_json = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    eliminado = models.BooleanField(default=False)
    fecha_eliminado = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['fecha']

    def __str__(self):
        return f"{self.cliente} — {self.get_tipo_display()} — {self.fecha}"


class EventoRango(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='rangos')
    nombre = models.CharField(max_length=100)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return self.nombre


class EventoCamarero(models.Model):
    rango = models.ForeignKey(EventoRango, on_delete=models.CASCADE, related_name='camareros')
    nombre = models.CharField(max_length=100)
    funcion = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nombre


class EventoDocumento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='documentos')
    archivo = models.FileField(upload_to='eventos/documentos/')
    nombre = models.CharField(max_length=200, blank=True)
    subido = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subido']

    def __str__(self):
        return self.nombre or self.archivo.name

    def extension(self):
        import os
        return os.path.splitext(self.archivo.name)[1].lower()


class Nota(models.Model):
    PRIORIDAD_CHOICES = [
        ('urgente',  'Urgente'),
        ('moderado', 'Moderado'),
        ('normal',   'Normal'),
    ]
    PRIORIDAD_ORDER = {'urgente': 0, 'moderado': 1, 'normal': 2}

    texto     = models.TextField()
    fecha     = models.DateTimeField(auto_now_add=True)
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='normal')
    resuelta  = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['resuelta', 'prioridad', '-fecha']

    def __str__(self):
        return self.texto[:50]


class ArticuloPedido(models.Model):
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, related_name='articulos')
    nombre = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Artículo de pedido'
        verbose_name_plural = 'Artículos de pedido'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.espacio} — {self.nombre}"

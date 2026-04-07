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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['fecha']

    def __str__(self):
        return f"{self.cliente} — {self.get_tipo_display()} — {self.fecha}"


class Nota(models.Model):
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-fecha']

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

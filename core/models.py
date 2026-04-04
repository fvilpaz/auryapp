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

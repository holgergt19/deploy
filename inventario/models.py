# models.py

from datetime import datetime
from django.db import models
from tita import settings

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)
    umbral = models.PositiveIntegerField(default=5)
    fecha_expiracion = models.DateField(null=True, blank=True)  # Nuevo campo
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

    @property
    def es_gastado(self):
        return self.cantidad < self.umbral

    @property
    def esta_por_expirar(self):
        if self.fecha_expiracion:
            return (self.fecha_expiracion - datetime.date.today()).days <= 30
        return False

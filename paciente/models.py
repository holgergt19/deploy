from django.db import models

from login.models import Account
from tita import settings

class Paciente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    primera_cita_completada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

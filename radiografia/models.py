from django.db import models

from odontologo.models import Odontologo
from paciente.models import Paciente


class Radiografia(models.Model):
    idOdontologo = models.ForeignKey(Odontologo, on_delete=models.CASCADE, null=True, blank=True)
    idPaciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
    imagen = models.ImageField(upload_to='photos/radiografias')
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Radiografía de {self.idPaciente} por {self.idOdontologo}'
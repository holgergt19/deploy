from django.db import models

from odontologo.models import Odontologo
from paciente.models import Paciente

from django.db import models
from datetime import datetime, timedelta

class Cita(models.Model):
    ESTADO_OPCIONES = [
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    
    SERVICIO_OPCIONES = [
        ('sin servicio', 'Sin Servicio'),
        ('con servicio', 'Con Servicio'),
    ]

    idOdontologo = models.ForeignKey(Odontologo, on_delete=models.CASCADE, null=True, blank=True)
    idPaciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    duracion = models.IntegerField(default=1)  # Duración en horas
    estado = models.CharField(max_length=10, choices=ESTADO_OPCIONES, default='confirmada')
    servicio = models.CharField(max_length=20, choices=SERVICIO_OPCIONES, default='sin servicio') 
    visualizada = models.BooleanField(default=False)

    def __str__(self):
        return f'Cita con {self.idOdontologo} para {self.idPaciente} el {self.fecha} a las {self.hora} ({self.estado}, {self.servicio})'
    
    @property
    def hora_fin(self):
        return (datetime.combine(self.fecha, self.hora) + timedelta(hours=self.duracion)).time()
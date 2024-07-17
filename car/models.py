from django.db import models

from cita.models import Cita
from odontologo.models import Odontologo
from paciente.models import Paciente
from servicio.models import Servicio
from django.conf import settings


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    idOdontologo = models.ForeignKey(Odontologo, on_delete=models.CASCADE, null=True, blank=True)
    idPaciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return f'{self.servicio.nombre_servicio} - {self.cart.cart_id}'

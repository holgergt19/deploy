from django.db import models
from django.conf import settings
from paciente.models import Paciente
from category.models import Category
from django.urls import reverse

class Servicio(models.Model):
    
    nombre_servicio = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='photos/servicios', blank=True)
    promocion = models.CharField(max_length=20, choices=[('sin promocion', 'Sin Promocion'), ('con promocion', 'Con Promocion')], default='sin promocion')
    porcentaje_promocion = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    duracion = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre_servicio
    
    def get_url(self):
        
        return reverse('servicio_detalle', args=[self.category.slug, self.slug])

    @property
    def tiene_promocion(self):
        return self.promocion == 'con promocion'
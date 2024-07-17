from django.db import models

from login.models import Account
from tita import settings

class Odontologo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    llave = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
# models.py

from django.db import models
from odontologo.models import Odontologo
from paciente.models import Paciente

class HistoriaClinica(models.Model):
    SEXO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    idOdontologo = models.ForeignKey(Odontologo, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10)
    sexo = models.CharField(max_length=1, choices=SEXO_OPCIONES)
    edad = models.IntegerField()
    nHistoriaClinica = models.CharField(max_length=20, unique=True)
    motivoConsulta = models.TextField()
    enfermedad = models.TextField()
    antecedentesPersonales = models.TextField()
    signosVitales = models.TextField()
    sistemaEstomatognatico = models.TextField()
    saludBucal = models.TextField()
    indicesCPO = models.TextField()
    diagnostico = models.TextField()
    fechacreacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Historia Clínica de {self.nombres} {self.apellidos}'
    
    def save(self, *args, **kwargs):
        if not self.nHistoriaClinica:
            last_historia = HistoriaClinica.objects.all().order_by('id').last()
            if not last_historia:
                self.nHistoriaClinica = 'HC0001'
            else:
                last_nHistoriaClinica = last_historia.nHistoriaClinica
                number = int(last_nHistoriaClinica.split('HC')[-1]) + 1
                self.nHistoriaClinica = 'HC' + str(number).zfill(4)
        super(HistoriaClinica, self).save(*args, **kwargs)

from django import forms
from .models import Paciente

class PacienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'cedula', 'email', 'telefono', 'direccion']

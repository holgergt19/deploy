
from django import forms
from .models import HistoriaClinica

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = [
            'direccion', 'sexo', 'edad',
            'motivoConsulta', 'enfermedad', 'antecedentesPersonales', 'signosVitales',
            'sistemaEstomatognatico', 'saludBucal', 'indicesCPO', 'diagnostico'
        ]
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivoConsulta': forms.Textarea(attrs={'class': 'form-control'}),
            'enfermedad': forms.Textarea(attrs={'class': 'form-control'}),
            'antecedentesPersonales': forms.Textarea(attrs={'class': 'form-control'}),
            'signosVitales': forms.Textarea(attrs={'class': 'form-control'}),
            'sistemaEstomatognatico': forms.Textarea(attrs={'class': 'form-control'}),
            'saludBucal': forms.Textarea(attrs={'class': 'form-control'}),
            'indicesCPO': forms.Textarea(attrs={'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control'}),
        }

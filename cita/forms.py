
from django import forms
from .models import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'duracion', 'servicio']  # Incluyendo el nuevo campo 'servicio'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'servicio': forms.Select(attrs={'class': 'form-control'}),
            'idOdontologo': forms.Select(attrs={'class': 'form-control'})# Selector para el servicio
        }

class CitaOdontologoForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            
        }
        
        
class BuscarPacienteForm(forms.Form):
    cedula = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cédula del paciente'}))
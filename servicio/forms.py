from django import forms
from .models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre_servicio', 'slug', 'descripcion', 'category', 'precio', 'imagen', 'promocion', 'porcentaje_promocion', 'is_available']
        widgets = {
            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'promocion': forms.Select(attrs={'class': 'form-control'}),
            'porcentaje_promocion': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class EditarServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['promocion', 'porcentaje_promocion']
        

class CitaForm(forms.Form):
    fecha_hora = forms.DateTimeField(label='Seleccione la fecha y hora', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
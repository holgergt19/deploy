
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'cantidad', 'descripcion', 'umbral', 'fecha_expiracion']  # Incluir fecha_expiracion
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'umbral': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_expiracion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Widget para fecha
        }

class ProductoCantidadForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

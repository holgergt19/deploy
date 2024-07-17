from django import forms
from .models import Radiografia

class RadiografiaForm(forms.ModelForm):
    class Meta:
        model = Radiografia
        fields = ['imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
from django import forms
from .models import ImageDiente


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageDiente
        fields = ['image']
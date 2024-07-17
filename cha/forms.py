# forms.py
from django import forms


class ChatForm(forms.Form):
    user_message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',  # Clase CSS para el estilo
            'placeholder': 'Escribe tu mensaje...',  # Texto de ayuda
            'rows': 4,
            'cols': 50
        })
    )
    system_response = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',  # Clase CSS para el estilo
            'placeholder': 'Respuesta del sistema...',  # Texto de ayuda
            'rows': 4,
            'cols': 50,
            'readonly': 'readonly'  # Solo lectura
        })
    )
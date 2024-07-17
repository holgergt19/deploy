from django import forms
from login.models import Account
from odontologo.models import Odontologo

from paciente.models import Paciente  # Asumiendo que tienes un modelo Paciente
from django.contrib.auth import get_user_model


class OdontologoRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar Password',
        'class': 'form-control',
    }))
    llave = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese código de registro',
        'class': 'form-control',
    }))

    class Meta:
        model = Odontologo
        fields = ['nombres', 'apellidos', 'email']

    def __init__(self, *args, **kwargs):
        super(OdontologoRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['nombres'].widget.attrs['placeholder'] = 'Ingrese nombres'
        self.fields['apellidos'].widget.attrs['placeholder'] = 'Ingrese apellidos'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return confirm_password

    def clean_llave(self):
        llave = self.cleaned_data.get('llave')
        if llave != 'beidenti':  # Verificar si el código de registro es correcto
            raise forms.ValidationError("El código de registro es incorrecto")
        return llave

    def save(self, commit=True):
        user = User.objects.create_user(
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['nombres'],
            last_name=self.cleaned_data['apellidos'],
            password=self.cleaned_data['password']
        )
        odontologo = Odontologo(
            user=user,
            nombres=self.cleaned_data['nombres'],
            apellidos=self.cleaned_data['apellidos'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        if commit:
            user.save()
            odontologo.save()
        return odontologo

User = get_user_model()

class PacienteRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar Password',
        'class': 'form-control',
    }))

    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'cedula', 'telefono', 'direccion', 'email']

    def __init__(self, *args, **kwargs):
        super(PacienteRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['placeholder'] = 'Ingrese nombre'
        self.fields['apellido'].widget.attrs['placeholder'] = 'Ingrese apellido'
        self.fields['cedula'].widget.attrs['placeholder'] = 'Ingrese cédula'
        self.fields['telefono'].widget.attrs['placeholder'] = 'Ingrese teléfono'
        self.fields['direccion'].widget.attrs['placeholder'] = 'Ingrese dirección'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está en uso.")
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return confirm_password

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if Paciente.objects.filter(cedula=cedula).exists():
            raise forms.ValidationError("La cédula ya está en uso.")
        return cedula

    def save(self, commit=True):
        user = None
        try:
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['nombre'],
                last_name=self.cleaned_data['apellido'],
                password=self.cleaned_data['password']
            )
            user.is_active = False  # Desactivar el usuario hasta la activación
            user.save()

            paciente = Paciente(
                user=user,
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                cedula=self.cleaned_data['cedula'],
                email=self.cleaned_data['email'],
                telefono=self.cleaned_data['telefono'],
                direccion=self.cleaned_data['direccion']
            )
            if commit:
                paciente.save()
            return paciente
        except Exception as e:
            if user:
                user.delete()  # En caso de error, eliminar el usuario creado
            raise e 
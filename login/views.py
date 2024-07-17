from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators  import login_required
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from login.forms import OdontologoRegistrationForm, PacienteRegistrationForm
from login.models import Account
from odontologo.models import Odontologo
from paciente.models import Paciente
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model



def role_selection(request):
    icons = [
        'dental1.png',
        'dental2.png',
        'dental3.png',
        'dental4.png',
        # Agrega más nombres de archivos de iconos según sea necesario
    ]
    return render(request, 'login/role_selection.html', {'icons': icons})

User = get_user_model()  # Obtiene el modelo de usuario configurado en AUTH_USER_MODEL

def activate(request, uidb64, token):
    try:
        # Decodificar el UID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)  # Ajustar según tu modelo de usuario
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # Verificar si el token es válido y activar la cuenta
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activar el usuario
        user.save()
        messages.success(request, '¡Felicidades! Tu cuenta ha sido activada. Ahora puedes iniciar sesión.')
        return redirect('paciente_login')  # Redirigir a la vista nombrada 'paciente_login'
    else:
        messages.error(request, 'El enlace de activación es inválido.')
        return redirect('paciente_register') 

def paciente_register(request):
    form = PacienteRegistrationForm()
    if request.method == 'POST':
        form = PacienteRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['nombre']
            last_name = form.cleaned_data['apellido']
            phone_number = form.cleaned_data['telefono']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Crear el usuario y desactivarlo hasta que se active
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user.is_active = False  # Desactivar la cuenta hasta que se confirme la activación
            user.save()

            # Crear el perfil del paciente asociado al usuario
            paciente = Paciente(
                user=user,  # Asociar el usuario creado con el perfil de paciente
                nombre=first_name,
                apellido=last_name,
                cedula=form.cleaned_data['cedula'],
                email=email,
                telefono=phone_number,
                direccion=form.cleaned_data['direccion'],
                password=password  # Guardar la contraseña en el perfil del paciente (aunque no es recomendable)
            )
            paciente.save()

            # Configuración del correo electrónico de activación
            current_site = get_current_site(request)
            mail_subject = 'Por favor activa tu cuenta en BeiDenti'
            body = render_to_string('login/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            # Redirigir con el mensaje de verificación
            messages.success(request, 'Se ha registrado el usuario exitosamente. Por favor, verifica tu correo electrónico para activar tu cuenta.')
            return redirect(f'/login/paciente_login/?command=verification&email={to_email}')

    context = {
        'form': form
    }
    return render(request, 'login/paciente_register.html', context)

def paciente_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('home_paciente')
        else:
            messages.error(request, 'Las credenciales son incorrectas.')
    return render(request, 'login/paciente_login.html')




def odontologo_register(request):
    if request.method == 'POST':
        form = OdontologoRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Ahora puede iniciar sesión.')
            return redirect('odontologo_login')
        else:
            messages.error(request, 'Por favor, corrija los errores a continuación.')
    else:
        form = OdontologoRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'login/odontologo_register.html', context)



def odontologo_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('home_odontologo')
        else:
            messages.error(request, 'Las credenciales son incorrectas.')
    return render(request, 'login/odontologo_login.html')

@login_required(login_url='odontologo_login')
def logout_odontologo(request):
    auth.logout(request)
    messages.success(request, 'Has salido de sesión exitosamente.')
    return redirect('role_selection')

@login_required(login_url='paciente_login')
def logout_paciente(request):
    auth.logout(request)
    messages.success(request, 'Has salido de sesión exitosamente.')
    return redirect('role_selection')
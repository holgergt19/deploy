
from django.core.mail import send_mail
from .models import Paciente  # Importa tu modelo Paciente

def enviar_notificacion(servicio):
    
    pacientes = Paciente.objects.all()
    emails = [paciente.email for paciente in pacientes if paciente.email]

    subject = 'Promoción Actualizada'
    message = f'El servicio {servicio.nombre_servicio} ha tiene una nueva promoción:  de {servicio.porcentaje_promocion}%.'

    send_mail(
        subject,
        message,
        'beidenti2024@gmail.com',  # Este debería ser tu dirección de correo electrónico configurada en settings.py
        emails,
        fail_silently=False,
    )

# notificaciones.py
from django.core.mail import send_mail
from .models import Cita  # Importa tu modelo Cita

def enviar_notificacion_cita_actualizada(cita):
   
    paciente_email = cita.idPaciente.email  # Asumiendo que idPaciente es la relación con el modelo del paciente que tiene un campo email
    subject = 'Actualización de su Cita'
    message = f'Su cita programada para {cita.fecha} a las {cita.hora} ha sido {cita.get_estado_display()}.'

    send_mail(
        subject,
        message,
        'beidenti2024@gmail.com',  # Este debería ser tu dirección de correo electrónico configurada en settings.py
        [paciente_email],
        fail_silently=False,
    )

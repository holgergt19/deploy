from django.core.mail import send_mail
from django.conf import settings

def enviar_notificacion_agregar_carrito(user, servicio, cita):
    email = user.email

    subject = 'Nuevo Servicio en el Carrito'
    message = (
        f'Se ha añadido el servicio {servicio.nombre_servicio} a tu carrito.\n'
        f'Fecha de la cita: {cita.fecha}\n'
        f'Hora de la cita: {cita.hora}'
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Asegúrate de que esto esté configurado en settings.py
        [email],
        fail_silently=False,
    )



from django.core.mail import EmailMessage

def enviar_correo(asunto, mensaje, destinatarios, archivo_adjunto=None):
    email = EmailMessage(
        subject=asunto,
        body=mensaje,
        to=destinatarios
    )
    if archivo_adjunto:
        email.attach(archivo_adjunto['nombre'], archivo_adjunto['contenido'], archivo_adjunto['tipo_mime'])
    email.send()

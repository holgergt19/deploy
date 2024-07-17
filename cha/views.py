from django.shortcuts import render
import requests
import json
from django.conf import settings

from cha.models import ChatMessage


def get_openai_response(user_message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 180,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

def chat(request):
    # Inicializar la lista de mensajes en la sesión si no existe
    if 'messages' not in request.session:
        request.session['messages'] = []

    user_message = ""
    response_text = ""
    messages = request.session['messages']  # Recuperar la conversación actual

    if request.method == "POST":
        user_message = request.POST.get('user_message', '')
        if user_message:
            response_text = get_openai_response(user_message)
            # Guardar en la base de datos
            ChatMessage.objects.create(user_message=user_message, system_response=response_text)
            # Agregar mensajes a la lista de mensajes en la sesión
            messages.append({'type': 'user', 'text': user_message})
            messages.append({'type': 'system', 'text': response_text})
            # Actualizar la lista de mensajes en la sesión
            request.session['messages'] = messages
            # Limpiar el campo de texto después de enviar el mensaje
            user_message = ""

    return render(request, 'chatbot/chat.html', {
        'messages': messages,
        'user_message': user_message,
        'response_text': response_text
    })
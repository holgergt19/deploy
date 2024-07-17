from django.shortcuts import render

from servicio.models import Servicio


def home_paciente(request):
    servicios = Servicio.objects
    
    context = {
        'servicios': servicios.filter()
    }
        
    return render(request, 'home_paciente.html', context)

def home_odontologo(request):
    servicios = Servicio.objects.filter()
    
    context = {
        'servicios': servicios
    }
    return render(request, 'home_odontologo.html', context)

def home(request):
    return render(request, 'home.html')

def contacto(request):
    return render(request, 'contacto.html')
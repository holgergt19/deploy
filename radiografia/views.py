from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib import messages
from radiografia.forms import RadiografiaForm
from .models import Paciente, Radiografia
from django.contrib.auth.decorators import login_required

def search(request):
    keyword = request.GET.get('keyword', None)
    pacientes = []
    radiografias = []
    radio_count = 0

    if keyword:
        pacientes = Paciente.objects.filter(Q(cedula__icontains=keyword))
        if pacientes.exists():
            radiografias = Radiografia.objects.filter(idPaciente__in=pacientes)
            radio_count = radiografias.count()

    context = {
        'pacientes': pacientes,
        'radiografias': radiografias,
        'radio_count': radio_count,
        'keyword': keyword,
    }
    
    return render(request, 'radio/radios.html', context)

@login_required
def subir_radiografia(request, paciente_id):
    
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if not hasattr(request.user, 'odontologo'):
        messages.error(request, 'Solo los odontólogos pueden subir radiografías.')
        return redirect('home')

    if request.method == 'POST':
        form = RadiografiaForm(request.POST, request.FILES)
        if form.is_valid():
            radiografia = form.save(commit=False)
            radiografia.idPaciente = paciente  # Asigna el paciente seleccionado
            radiografia.idOdontologo = request.user.odontologo  # Asigna el odontólogo autenticado
            radiografia.save()
            messages.success(request, 'Radiografía subida exitosamente.')
            return redirect('search')  # Redirige a la página de búsqueda para ver el resultado
        else:
            messages.error(request, 'Error al subir la radiografía. Por favor, corrija los errores.')
    else:
        form = RadiografiaForm()

    context = {
        'form': form,
        'paciente': paciente,
    }
    return render(request, 'radio/subir_radiografia.html', context)
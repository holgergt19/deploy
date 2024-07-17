from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404



from cita.models import Cita
from servicio.forms import CitaForm, EditarServicioForm, ServicioForm
from servicio.models import Servicio
from category.models import Category
from django.contrib.auth.decorators import login_required

from servicio.notificacion import enviar_notificacion

def servicio(request, category_slug=None):
    categories = None
    servicios = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        servicios = Servicio.objects.filter(category=categories)
        servicio_count = servicios.count()
    
    else:
        
        servicios = Servicio.objects.all()
        servicio_count = servicios.count()    
    
    
    
    context = {
        'servicios': servicios,
        'servicio_count': servicio_count,
    }
    
    
    return render(request, 'servicio/servicio.html', context)


def lista_servicios_odontologo(request):
    """
    Vista para que los odontólogos gestionen los servicios: ver, agregar y editar.
    """
    servicios = Servicio.objects.all()
    form = ServicioForm()

    if request.method == 'POST':
        if 'add_service' in request.POST:
            form = ServicioForm(request.POST, request.FILES)
            if form.is_valid():
                nuevo_servicio = form.save(commit=False)
                nuevo_servicio.odontologo = request.user.odontologo  # Asigna el odontólogo que crea el servicio
                nuevo_servicio.user = request.user
                nuevo_servicio.save()
                return redirect('lista_servicios_odontologo')

    context = {
        'servicios': servicios,
        'form': form,
    }

    return render(request, 'servicio/servicio_odontologo.html', context)

@login_required
def editar_servicio(request, servicio_id):
    """Permite a los odontólogos editar solo la promoción y el porcentaje de promoción de un servicio existente."""
    servicio = get_object_or_404(Servicio, id=servicio_id)
    old_promocion = servicio.promocion
    old_porcentaje_promocion = servicio.porcentaje_promocion

    if request.method == 'POST':
        form = EditarServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            if (form.cleaned_data['promocion'] != old_promocion or 
                form.cleaned_data['porcentaje_promocion'] != old_porcentaje_promocion):
                form.save()
                enviar_notificacion(servicio)
                return redirect('lista_servicios_odontologo')
            else:
                return redirect('lista_servicios_odontologo')
    else:
        form = EditarServicioForm(instance=servicio)

    context = {
        'form': form,
        'servicio': servicio
    }
    return render(request, 'servicio/servicio_odontologo.html', context)

def servicio_detalle(request, category_slug, nombre_servicio_slug):
    """
    Vista para mostrar los detalles de un servicio y permitir la selección de una cita.
    """
    try:
        servicio = Servicio.objects.get(category__slug=category_slug, slug=nombre_servicio_slug)
    except Servicio.DoesNotExist:
        raise Http404("Servicio no encontrado")

    # Filtra las citas disponibles para el servicio y el paciente actual
    citas = Cita.objects.filter(idPaciente=request.user.paciente, estado='confirmada', servicio='con servicio')

    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            nueva_cita = form.save(commit=False)
            nueva_cita.idPaciente = request.user.paciente
            nueva_cita.idOdontologo = servicio.user.odontologo if hasattr(servicio.user, 'odontologo') else None  # Asigna el odontólogo si el usuario es un odontólogo
            nueva_cita.save()
            return redirect('servicio_detalle', category_slug=category_slug, nombre_servicio_slug=nombre_servicio_slug)
    else:
        form = CitaForm()

    context = {
        'servicio': servicio,
        'citas': citas,
        'form': form,
    }
    
    return render(request, 'servicio/servicio_detalle.html', context)
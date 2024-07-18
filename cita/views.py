from collections import defaultdict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from cita.notificacion import enviar_notificacion_cita_actualizada
from odontologo.models import Odontologo
from paciente.models import Paciente

from .models import Cita
from .forms import CitaForm, CitaOdontologoForm, BuscarPacienteForm



def generar_reporte_citas(request):
    # Crear un objeto HttpResponse con las cabeceras de PDF correctas.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_citas.pdf"'

    # Crear el objeto PDF, usando el objeto response como su "archivo".
    p = canvas.Canvas(response)

    # Consultar las citas
    citas = Cita.objects.all()
    y = 800  # Altura inicial para la escritura en la página.

    # Títulos de las columnas
    p.drawString(100, y, "Fecha")
    p.drawString(200, y, "Hora")
    p.drawString(300, y, "Paciente")
    p.drawString(400, y, "Estado")

    # Disminuir un poco y para los datos
    y -= 20

    for cita in citas:
        p.drawString(100, y, str(cita.fecha))
        p.drawString(200, y, str(cita.hora))
        paciente = f"{cita.idPaciente.nombre} {cita.idPaciente.apellido}"
        p.drawString(300, y, paciente)
        p.drawString(400, y, cita.get_estado_display())
        y -= 20  # Espacio para la siguiente cita

    # Cerrar el objeto PDF y devolver la respuesta.
    p.showPage()
    p.save()
    return response


@login_required
def ver_citas_disponibles(request, paciente_id=None):
    es_paciente = hasattr(request.user, 'paciente')
    es_odontologo = hasattr(request.user, 'odontologo')
    
    if not es_paciente and not es_odontologo:
        messages.error(request, 'Solo los pacientes y odontólogos pueden ver citas disponibles.')
        return redirect('home')
    
    if es_paciente:
        paciente = request.user.paciente
        primera_cita_completada = Cita.objects.filter(idPaciente=paciente, estado='confirmada').exists()
    elif es_odontologo and paciente_id:
        paciente = get_object_or_404(Paciente, id=paciente_id)
        primera_cita_completada = Cita.objects.filter(idPaciente=paciente, estado='confirmada').exists()
    else:
        messages.error(request, 'Odontólogo debe seleccionar un paciente.')
        return redirect('buscar_paciente')

    hoy = datetime.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    dias_laborales = [lunes + timedelta(days=i) for i in range(5)]
    citas = Cita.objects.filter(fecha__range=[lunes, lunes + timedelta(days=4)])
    horarios_disponibles = defaultdict(list)
    horas_laborales = [datetime.strptime(f"{hour}:00", "%H:%M").time() for hour in range(9, 18)]

    for dia in dias_laborales:
        for hora in horas_laborales:
            hora_fin = (datetime.combine(dia, hora) + timedelta(hours=1)).time()
            cita_ocupada = False
            for cita in citas:
                cita_hora_fin = (datetime.combine(cita.fecha, cita.hora) + timedelta(hours=cita.duracion)).time()
                if cita.fecha == dia.date() and not (hora >= cita_hora_fin or hora_fin <= cita.hora):
                    cita_ocupada = True
                    break
            if not cita_ocupada:
                horarios_disponibles[dia.date()].append(hora)

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        duracion = int(request.POST.get('duracion', 1))
        servicio = request.POST.get('servicio', 'sin servicio')
        odontologo_id = request.POST.get('odontologo')

        if fecha and hora and odontologo_id:
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            hora = datetime.strptime(hora, "%H:%M").time()
            odontologo = Odontologo.objects.get(id=odontologo_id)
            nueva_cita = Cita.objects.create(
                idPaciente=paciente,
                idOdontologo=odontologo,
                fecha=fecha,
                hora=hora,
                duracion=duracion,
                estado='confirmada',
                servicio=servicio
            )
            nueva_cita.save()
            messages.success(request, 'Cita creada con éxito.')
            if es_paciente:
                return redirect('ver_citas')
            else:
                return redirect('ver_citas_odontologo')
        else:
            messages.error(request, 'Por favor seleccione una fecha, hora y odontólogo válidos.')

    context = {
        'horarios_disponibles': dict(horarios_disponibles),
        'primera_cita_completada': primera_cita_completada,
        'odontologos': Odontologo.objects.all(),
        'form': CitaForm(),
        'paciente': paciente  # Añadir el paciente al contexto
    }
    return render(request, 'cita/ver_citas_disponibles.html', context)




@login_required
def buscar_paciente(request):
    if not hasattr(request.user, 'odontologo'):
        messages.error(request, 'Solo los odontólogos pueden crear citas para pacientes.')
        return redirect('home')

    paciente = None
    if request.method == 'POST':
        form = BuscarPacienteForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            try:
                paciente = Paciente.objects.get(cedula=cedula)
            except Paciente.DoesNotExist:
                messages.error(request, 'Paciente no encontrado.')
    else:
        form = BuscarPacienteForm()

    return render(request, 'cita/buscar_paciente.html', {'form': form, 'paciente': paciente})


@login_required
def ver_citas_odontologo(request):
    if not hasattr(request.user, 'odontologo'):
        messages.error(request, 'Solo los odontólogos pueden ver y actualizar citas.')
        return redirect('home')

    odontologo = request.user.odontologo

    if 'clear' in request.POST:
        Cita.objects.filter(idOdontologo=odontologo, visualizada=False).update(visualizada=True)
        return redirect('ver_citas_odontologo')

    citas = Cita.objects.filter(idOdontologo=odontologo, visualizada=False)

    if request.method == 'POST' and 'clear' not in request.POST:
        form = CitaOdontologoForm(request.POST)
        if form.is_valid():
            cita_id = request.POST.get('cita_id')
            cita = Cita.objects.get(id=cita_id)
            cita.estado = form.cleaned_data['estado']
            cita.save()
            enviar_notificacion_cita_actualizada(cita)
            messages.success(request, 'Estado de la cita actualizado con éxito.')
            return redirect('ver_citas_odontologo')
        else:
            messages.error(request, 'Error al actualizar el estado de la cita.')
    else:
        form = CitaOdontologoForm()

    context = {
        'citas': citas,
        'form': form
    }
    return render(request, 'cita/ver_citas_odontologo.html', context)








@login_required
def crear_cita(request):
    if not hasattr(request.user, 'paciente'):
        messages.error(request, 'Solo los pacientes pueden crear citas.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.idPaciente = request.user.paciente  # Asigna el paciente autenticado
            cita.save()
            messages.success(request, 'Cita creada con éxito.')
            return redirect('ver_citas')
        else:
            messages.error(request, 'Error al crear la cita. Por favor, corrija los errores.')
    else:
        form = CitaForm()

    context = {
        'form': form,
        'usuario': request.user  # Añadir el usuario autenticado al contexto
    }
    return render(request, 'cita/crear_cita.html', context)

@login_required
def ver_citas(request):
    """
    Vista para ver las citas del paciente autenticado.
    """
    if not hasattr(request.user, 'paciente'):
        messages.error(request, 'Solo los pacientes pueden ver sus citas.')
        return redirect('home')  # Redirigir a la página principal si no es un paciente
    
    # Obtener el paciente autenticado
    paciente = request.user.paciente
    
    # Obtener todas las citas del paciente
    citas = Cita.objects.filter(idPaciente=paciente)
    
    # Contexto a pasar a la plantilla
    context = {
        'citas': citas
    }
    
    return render(request, 'cita/ver_citas.html', context)
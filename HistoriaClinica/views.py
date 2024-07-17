
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HistoriaClinica
from .forms import HistoriaClinicaForm
from paciente.models import Paciente
from django.db.models import Q
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter

from reportlab.pdfgen import canvas



def generar_pdf(request, historia_id):
    # Crear una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historia_clinica_{historia_id}.pdf"'

    # Crear el lienzo del PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Obtener la historia clínica específica
    historia = get_object_or_404(HistoriaClinica, id=historia_id)

    # Añadir título y fecha al PDF
    p.drawString(100, height - 50, f"Historia Clínica de {historia.nombres} {historia.apellidos}")
    p.drawString(100, height - 70, "Fecha de Creación: " + historia.fechacreacion.strftime('%d/%m/%Y'))

    # Añadir detalles de la historia clínica
    y = height - 100
    spacing = 20

    p.drawString(100, y, f"Cédula: {historia.cedula}")
    y -= spacing
    p.drawString(100, y, f"Dirección: {historia.direccion}")
    y -= spacing
    p.drawString(100, y, f"Sexo: {'Masculino' if historia.sexo == 'M' else 'Femenino'}")
    y -= spacing
    p.drawString(100, y, f"Edad: {historia.edad}")
    y -= spacing
    p.drawString(100, y, f"Número de Historia Clínica: {historia.nHistoriaClinica}")
    y -= spacing

    p.drawString(100, y, "Motivo de Consulta:")
    y -= spacing
    p.drawString(120, y, historia.motivoConsulta)
    y -= spacing * 2

    p.drawString(100, y, "Enfermedad:")
    y -= spacing
    p.drawString(120, y, historia.enfermedad)
    y -= spacing * 2

    p.drawString(100, y, "Antecedentes Personales:")
    y -= spacing
    p.drawString(120, y, historia.antecedentesPersonales)
    y -= spacing * 2

    p.drawString(100, y, "Signos Vitales:")
    y -= spacing
    p.drawString(120, y, historia.signosVitales)
    y -= spacing * 2

    p.drawString(100, y, "Sistema Estomatognático:")
    y -= spacing
    p.drawString(120, y, historia.sistemaEstomatognatico)
    y -= spacing * 2

    p.drawString(100, y, "Salud Bucal:")
    y -= spacing
    p.drawString(120, y, historia.saludBucal)
    y -= spacing * 2

    p.drawString(100, y, "Índices CPO:")
    y -= spacing
    p.drawString(120, y, historia.indicesCPO)
    y -= spacing * 2

    p.drawString(100, y, "Diagnóstico:")
    y -= spacing
    p.drawString(120, y, historia.diagnostico)
    y -= spacing * 2

    # Si se termina la página, se agrega una nueva
    if y < 50:
        p.showPage()
        y = height - 50

    # Terminar el PDF
    p.showPage()
    p.save()

    return response













@login_required
def buscar_hc(request):
    keyword = request.GET.get('keyword', None)
    pacientes = []
    historias_clinicas = []

    if keyword:
        # Buscar pacientes por cédula
        pacientes = Paciente.objects.filter(Q(cedula__icontains=keyword))
        if pacientes.exists():
            # Buscar historias clínicas para los pacientes encontrados
            historias_clinicas = HistoriaClinica.objects.filter(cedula__in=[p.cedula for p in pacientes])

    context = {
        'pacientes': pacientes,
        'historias_clinicas': historias_clinicas,
        'keyword': keyword,
    }
    return render(request, 'hc/buscar_hc.html', context)

@login_required
def crear_hc(request, paciente_id):
    """
    Vista para crear una historia clínica para un paciente específico.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if not hasattr(request.user, 'odontologo'):
        messages.error(request, 'Solo los odontólogos pueden crear historias clínicas.')
        return redirect('home')

    # Obtener el siguiente número de historia clínica
    last_historia = HistoriaClinica.objects.all().order_by('id').last()
    if not last_historia:
        next_hc_number = '0001'
    else:
        last_nHistoriaClinica = last_historia.nHistoriaClinica
        number = int(last_nHistoriaClinica.split('HC')[-1]) + 1
        next_hc_number = str(number).zfill(4)

    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST)
        if form.is_valid():
            historia = form.save(commit=False)
            historia.idOdontologo = request.user.odontologo  # Asigna el odontólogo autenticado
            historia.nombres = paciente.nombre  # Usar el nombre del paciente encontrado
            historia.apellidos = paciente.apellido  # Usar el apellido del paciente encontrado
            historia.cedula = paciente.cedula  # Usar la cédula del paciente encontrado
            historia.nHistoriaClinica = 'HC' + next_hc_number  # Asignar el número de historia clínica
            historia.save()
            messages.success(request, 'Historia clínica creada con éxito.')
            return redirect('buscar_hc')
        else:
            messages.error(request, 'Error al crear la historia clínica. Por favor, corrija los errores.')
    else:
        form = HistoriaClinicaForm()

    context = {
        'form': form,
        'paciente': paciente,
        'next_hc_number': next_hc_number,
    }
    return render(request, 'hc/crear_hc.html', context)

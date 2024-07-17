
from django.shortcuts import render, redirect


from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.core.mail import EmailMessage

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import Producto
from .forms import ProductoForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime  # Importar datetime y timedelta de forma correcta
from .utils import enviar_correo  # Importa la función genérica si no está ya importada


from .models import Producto
from .forms import ProductoForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .utils import enviar_correo  # Importa la función genérica

@login_required
def ver_productos(request):
    if request.method == 'POST':
        # Manejo de adición de nuevos productos
        if 'nombre' in request.POST:
            form = ProductoForm(request.POST)
            if form.is_valid():
                producto = form.save(commit=False)
                producto.user = request.user
                producto.save()
                if producto.cantidad < producto.umbral:
                    enviar_alerta_producto(request, producto)
                enviar_alerta_expiracion(request, producto)  # Verificar y enviar alerta de expiración si aplica
                messages.success(request, 'Producto agregado con éxito.')
                return redirect('ver_productos')
        # Manejo de actualización de cantidad de productos
        else:
            for key, value in request.POST.items():
                if key.startswith('cantidad_'):
                    producto_id = key.split('_')[1]
                    try:
                        producto = Producto.objects.get(id=producto_id)
                        producto.cantidad = int(value)
                        producto.save()
                        if producto.cantidad < producto.umbral:
                            enviar_alerta_producto(request, producto)
                        enviar_alerta_expiracion(request, producto)  # Verificar y enviar alerta de expiración si aplica
                    except Producto.DoesNotExist:
                        messages.error(request, f"Producto con ID {producto_id} no encontrado.")
            messages.success(request, 'Cantidades de productos actualizadas con éxito.')
            return redirect('ver_productos')
    
    else:
        form = ProductoForm()

    productos = Producto.objects.filter(user=request.user)
    return render(request, 'inventario/ver_productos.html', {'productos': productos, 'form': form})

def enviar_alerta_producto(request, producto):
    if producto.user and producto.user.email:
        current_site = get_current_site(request)
        mail_subject = 'Alerta de Inventario: Cantidad Baja'
        mensaje = (
            f"Hola {producto.user.first_name},\n\n"
            f"El producto {producto.nombre} ha bajado del umbral de {producto.umbral} unidades.\n"
            f"La cantidad actual es de: {producto.cantidad} unidades.\n\n"
            "Por favor, revisa el inventario y realiza las compras necesarias.\n\n"
            "Le agradece,\n"
            "BeiDenti"
        )
        enviar_correo(mail_subject, mensaje, [producto.user.email])
    else:
        print(f"El producto {producto.nombre} no tiene un usuario asociado con un email válido.")

def enviar_alerta_expiracion(request, producto):
    if producto.user and producto.user.email:
        current_site = get_current_site(request)
        mail_subject = 'Alerta de Inventario: Fecha de Expiración Próxima'
        
        # Verifica si la fecha de expiración está a 3 días o menos
        hoy = datetime.today().date()
        if producto.fecha_expiracion and (producto.fecha_expiracion - hoy).days <= 3:
            mensaje = (
                f"Hola {producto.user.first_name},\n\n"
                f"El producto {producto.nombre} está próximo a expirar el {producto.fecha_expiracion}.\n"
                f"La cantidad actual es de: {producto.cantidad} unidades.\n\n"
                "Por favor, revisa el inventario y realiza las acciones necesarias.\n\n"
                "Le agradece,\n"
                "BeiDenti"
            )
            enviar_correo(mail_subject, mensaje, [producto.user.email])
        else:
            print(f"La fecha de expiración de {producto.nombre} no está dentro del rango de 3 días.")
    else:
        print(f"El producto {producto.nombre} no tiene un usuario asociado con un email válido.")

@login_required
def generar_reporte_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    productos = Producto.objects.filter(user=request.user)

    # Agregar título y fecha actual al PDF
    p.drawString(100, height - 50, "Reporte de Productos")
    p.drawString(100, height - 70, "Fecha: " + str(datetime.today().date()))  # Corrige la obtención de la fecha actual

    y = height - 100
    for producto in productos:
        p.drawString(100, y, f"Nombre: {producto.nombre}, Cantidad: {producto.cantidad}, Fecha de Expiración: {producto.fecha_expiracion}")
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()

    return response


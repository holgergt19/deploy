from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cita.models import Cita
from servicio.models import Servicio
from .models import  Cart, CartItem



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required
def add_cart(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request),
            user=request.user,
            idPaciente=request.user.paciente if hasattr(request.user, 'paciente') else None,
            idOdontologo=request.user.odontologo if hasattr(request.user, 'odontologo') else None
        )
        cart.save()

    cita_id = request.POST.get('cita')
    cita = get_object_or_404(Cita, id=cita_id)

    try:
        cart_item = CartItem.objects.get(servicio=servicio, cita=cita, cart=cart)
        cart_item.cantidad += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            servicio=servicio,
            cita=cita,
            cantidad=1,
            cart=cart
        )
        cart_item.save()

    messages.success(request, 'El servicio y la cita se han añadido al carrito.')
    return redirect('cart')

@login_required
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    except Cart.DoesNotExist:
        cart_items = []

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'servicio/carrito.html', context)

@login_required
def carttwo(request):
    if not hasattr(request.user, 'odontologo'):
        messages.error(request, 'Solo los odontólogos pueden acceder a esta página.')
        return redirect('home_paciente')

    if request.method == 'POST' and 'limpiar_carrito' in request.POST:
        try:
            cart_items = CartItem.objects.filter(cart__user__paciente__isnull=False, is_active=True)
            for item in cart_items:
                item.is_active = False
                item.save()
            messages.success(request, 'El carrito ha sido limpiado con éxito.')
        except Cart.DoesNotExist:
            messages.error(request, 'No se encontró el carrito.')
        return redirect('carttwo')

    try:
        cart_items = CartItem.objects.filter(cart__user__paciente__isnull=False, is_active=True)
    except Cart.DoesNotExist:
        cart_items = []

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'servicio/carrito2.html', context)

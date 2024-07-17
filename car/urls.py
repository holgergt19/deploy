from django.urls import path
from .views import add_cart, cart, carttwo


urlpatterns = [
    path('add_cart/<int:servicio_id>/', add_cart, name='add_cart'),
    path('cart/', cart, name='cart'),
    path('carttwo/', carttwo, name='carttwo'),
    path('ver-carrito/', cart, name='ver_carrito'),
    
    
]

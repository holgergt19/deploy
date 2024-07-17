from django.urls import path
from .views import actualizar_perfil

urlpatterns = [
    # otras rutas
    path('actualizar_perfil/', actualizar_perfil, name='actualizar_perfil'),
]

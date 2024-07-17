from django.urls import path
from .views import crear_hc, buscar_hc, generar_pdf

urlpatterns = [
    path('crear_hc/<int:paciente_id>/', crear_hc, name='crear_hc'),
    path('buscar_hc/', buscar_hc, name='buscar_hc'),
    path('generar_pdf/<int:historia_id>/', generar_pdf, name='generar_pdf'),
]

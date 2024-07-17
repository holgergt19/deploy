from django.urls import path
from .views import crear_cita, generar_reporte_citas, ver_citas, ver_citas_disponibles, ver_citas_odontologo

urlpatterns = [
    path('crear/', crear_cita, name='crear_cita'),
    path('ver/', ver_citas, name='ver_citas'),
    path('ver_citas_disponibles/', ver_citas_disponibles, name='ver_citas_disponibles'),
    path('ver_citas_odontologo/', ver_citas_odontologo, name='ver_citas_odontologo'),
    path('reporte-citas/', generar_reporte_citas, name='reporte_citas'),
    
    
    
    
]

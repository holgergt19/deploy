

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_productos, name='ver_productos'),
    
    path('reporte/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
]

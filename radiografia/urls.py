from django.urls import path

from radiografia.views import search, subir_radiografia

urlpatterns = [
    path('search/', search, name='search'),
    path('subir_radiografia/<int:paciente_id>/', subir_radiografia, name='subir_radiografia'),
    
]

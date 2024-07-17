from django.urls import path
from . import views

urlpatterns = [
    path('servicio/', views.servicio, name="servicio"),
    path('<slug:category_slug>/', views.servicio, name='servicios_by_category'),
    path('odontologo/servicios/', views.lista_servicios_odontologo, name='lista_servicios_odontologo'),
    path('odontologo/servicio/<int:servicio_id>/editar/', views.editar_servicio, name='editar_servicio'),
    path('<slug:category_slug>/<slug:nombre_servicio_slug>/', views.servicio_detalle, name='servicio_detalle'),
     
]

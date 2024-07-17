from django.contrib import admin
from .models import Servicio

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_servicio','descripcion','category','precio','created_date','is_available')
    prepopulated_fields = {'slug': ('nombre_servicio',)}
    
admin.site.register(Servicio, ServicioAdmin)
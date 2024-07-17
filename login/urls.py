from django.urls import path

from login.views import  activate, logout_odontologo, odontologo_register, paciente_login, paciente_register, role_selection, logout_paciente

from login.views import  odontologo_login


urlpatterns = [
    
    path('odontologo_login/', odontologo_login, name='odontologo_login'),
    path('role/', role_selection, name='role_selection'),
    path('odontologo_register/', odontologo_register, name='odontologo_register'),
    path('paciente_login/', paciente_login, name='paciente_login'),
    path('paciente_register/', paciente_register, name='paciente_register'),
    path('logout_odontologo/', logout_odontologo, name='logout_odontologo'),
    path('logout_paciente/', logout_paciente, name='logout_paciente'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
]
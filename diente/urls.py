
from django.urls import path
from . import views

urlpatterns = [
    path('upload_diente/', views.upload_diente, name='upload_diente'),
]

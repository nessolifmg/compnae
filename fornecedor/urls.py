from django.urls import path
from .views import *


urlpatterns = [
     path('', home_fornecedor, name='home'),
     path('fornecer_alimentos', fornecer_alimentos, name='fornecer_alimentos'),
     path('fornecer_alimentos/submit', submit_fornecer_alimentos, name='fornecer_alimentos_submit'),
     path('perfil', perfil, name='perfil'),
]

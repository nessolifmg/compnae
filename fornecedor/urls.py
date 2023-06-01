from django.contrib import admin
from django.urls import include, path
from fornecedor import views
from django.views.generic import RedirectView

urlpatterns = [
     path('', views.home_fornecedor, name='home'),
     path('fornecer_alimentos', views.fornecer_alimentos, name='fornecer_alimentos'),
     path('fornecer_alimentos/submit', views.submit_fornecer_alimentos, name='fornecer_alimentos_submit'),
     path('perfil', views.perfil, name = 'perfil' ),
    
]

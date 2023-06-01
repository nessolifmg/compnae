from django.contrib import admin
from django.urls import include, path
from servidor import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.home_servidor, name='home_servidor'),
    path('cadastro/alimentos/', views.cadastrar_alimento, name='cadastro_alimentos'), # cadastro de alimentos
    path('cadastro/alimentos/update/<int:alimento_id>/', views.atualizar_alimento, name='atualizar_alimentos'), # validação dos alimentos
   
    path('cadastro/editais/', views.cadastrar_edital, name='cadastro_editais'),
    path('cadastro/editais/update/<int:edital_id>/', views.atualizar_edital, name='atualizar_edital'),
   
    path('cadastro/alimentos_necessarios/', views.cadastrar_alimento_necessario, name='cadastrar_alimento_necessario'),
    path('cadastro/alimentos_necessarios/delete/<int:alimento_necessario_id>/', views.deletar_alimento_necessario, name='deletar_alimento_necessario'),
    
    path('media_alimentos/', views.media_alimentos, name='media'),
    path('fornecedores/', views.lista_fornecedores, name='fornecedores'),
    path('avisos/', views.gerenciar_avisos, name='avisos'),
]

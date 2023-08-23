from django.urls import path
from .views import *


urlpatterns = [
    path('', home_servidor, name='home_servidor'),
    # cadastro de alimentos
    path('cadastro/alimentos/', cadastrar_alimento, name='cadastro_alimentos'),
    path('cadastro/alimentos/update/<int:alimento_id>/', atualizar_alimento, name='atualizar_alimentos'),
   
    path('cadastro/editais/', cadastrar_edital, name='cadastro_editais'),
    path('cadastro/editais/update/<int:edital_id>/', atualizar_edital, name='atualizar_edital'),
   
    path('cadastro/alimentos_necessarios/', cadastrar_alimento_necessario, name='cadastrar_alimento_necessario'),
    path('cadastro/alimentos_necessarios/delete/<int:alimento_necessario_id>/',
         deletar_alimento_necessario, name='deletar_alimento_necessario'),
    
    path('media_alimentos/', media_alimentos, name='media'),
    path('fornecedores/', lista_fornecedores, name='fornecedores'),
    path('avisos/', gerenciar_avisos, name='avisos'),
]

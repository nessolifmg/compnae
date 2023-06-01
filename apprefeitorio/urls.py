from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls), # url para acessar o menu de administrador do django
    path('', include('core.urls')), # redirecionamento padrão
]

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # url para acessar o menu de administrador do django
    path('admin/', admin.site.urls),
    # redirecionamento padrão
    path('', include('core.urls')),
]

from django.contrib import admin
from .models import *

# Registro de tabelas existentes no Models, a fim de permitir sua visualização na área de admin

admin.site.register(Edital)
admin.site.register(Alimento)
admin.site.register(AlimentoNecessario)
admin.site.register(Avisos)

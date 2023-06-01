from django.db import models
from core.models import *
from servidor.models import *


class FornecedorEdital(models.Model):
    user = models.ForeignKey(to=Fornecedor, on_delete=models.PROTECT, related_name='usuarios')
    edital = models.ForeignKey(to=Edital, on_delete=models.PROTECT, blank=True, default = "", related_name='editais_fornecedor') 

    class Meta:
        db_table = 'fornecedor_por_edital'
    
    def __str__(self) -> str:
        return str(self.user)

class AlimentoFornecido(models.Model):
    fornecedor_edital = models.ForeignKey(to=FornecedorEdital, on_delete=models.PROTECT, blank=True, default = "", related_name='fornecedores_edital')
    alimento = models.ForeignKey(to=Alimento, on_delete=models.PROTECT, related_name='alimentos_fornecidos')
    preco = models.FloatField(max_length=15)

    class Meta:
        db_table = 'alimento_fornecido'
    
    def __str__(self) -> str:
        return str(self.alimento)

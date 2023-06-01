from django.db import models

        #--------------------Tabelas com relação aos editais---------------------------------------------
class Edital(models.Model):
    numero = models.CharField(unique=True, max_length=15)
    status = models.BooleanField(blank=True, default=False)
    data_inicio = models.DateField()
    data_final = models.DateField()
    
    class Meta:
        db_table = 'edital'

    def __str__(self) -> str:
        return self.numero

#---------------------Tabelas com relação aos Alimentos---------------------------------
class Alimento(models.Model):
    nome = models.CharField(max_length=15, unique=True)
    
    class Meta:
        db_table = 'alimento'

    def __str__(self) -> str:
        return self.nome

class AlimentoNecessario(models.Model):
    alimento = models.ForeignKey(to=Alimento, on_delete=models.PROTECT, related_name='alimentos_necessarios')
    edital = models.ForeignKey(to=Edital, on_delete=models.PROTECT, blank=True, default = "", related_name='editais_alimentos')
    quantidade = models.FloatField(max_length=15)

    class Meta:
        db_table = 'alimento_necessario'

    def __str__(self) -> str:
        return str(self.alimento)



class Avisos(models.Model):
    aviso = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'avisos'

    def __str__(self) -> str:
        return str(self.aviso)


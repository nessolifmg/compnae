from django.db import models
from django.contrib.auth.models import User

#---------------------Faz referência a classe Fornecedor--------------------------------
class Fornecedor(models.Model):
    ETNIA = (
        ('1', 'Quilombola'),
        ('2', 'Indigena'),
        ('3', 'Nenhum'),
    )
    user = models.OneToOneField(to=User, primary_key=True, unique=True, on_delete=models.CASCADE)
    cpf_cnpj = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15)
    cidade = models.CharField(max_length=150)
    estado = models.CharField(max_length=2)
    endereco = models.CharField(max_length=150)
    bairro = models.CharField(max_length=150)
    nascimento = models.DateField()
    dap = models.CharField(max_length=25)
    associacao = models.CharField(max_length=15, blank=True) 
    prioritario = models.CharField(
        max_length=1,
        choices=ETNIA,
        default='3',
        blank=True,
        null=False
    )
    class Meta:
        db_table = 'fornecedor'

    def __str__(self) -> str:
        return self.user.username

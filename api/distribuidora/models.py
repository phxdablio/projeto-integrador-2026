from django.db import models

# Create your models here.

class Vendedor(models.Model):
    id_vendedor = models.AutoField(primary_key=True)
    nome_vendedor = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_vendedor

class Cliente(models.Model):
    id_cliente = models.CharField(primary_key=True,max_length=50)
    razao_social = models.CharField(max_length=255)
    cnpj_normalizado = models.CharField(max_length=14)
    telefone_normalizado = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    bairro_normalizado = models.CharField(max_length=100)
    cep_normalizado = models.CharField(max_length=8)
    data_cadastro_normalizado = models.DateField()
    vendedor = models.ForeignKey(Vendedor,on_delete=models.PROTECT,related_name='clientes')

    def __str__(self):
        return self.razao_social

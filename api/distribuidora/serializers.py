from rest_framework import serializers  # ferramentas do DRF transformar a tabela em JSON
from .models import Cliente, Vendedor        # modelos usados pelos serializers

class ClienteSerializer(serializers.ModelSerializer):
   class Meta:
       model = Cliente
       fields = '__all__'  # expõe todos os campos da tabela Cliente

class VendedorSerializer(serializers.ModelSerializer):
   class Meta:
       model = Vendedor
       fields = '__all__'  # expõe todos os campos da tabela Vendedor

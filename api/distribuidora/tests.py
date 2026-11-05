from django.test import TestCase
from .serializers import VendedorSerializer
from .models import Vendedor
from .serializers import ClienteSerializer

class VendedorSerializerTest(TestCase):

    def test_vendedor_valido(self):
        dados = {
            "nome_vendedor": "Carlos Silva"
        }

        serializer = VendedorSerializer(data=dados)

        self.assertTrue(serializer.is_valid())

    def test_vendedor_sem_nome(self):
        dados = {}

        serializer = VendedorSerializer(data=dados)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "nome_vendedor",
            serializer.errors
        )

class ClienteSerializerTest(TestCase):

    def setUp(self):
        self.vendedor = Vendedor.objects.create(
            nome_vendedor="Carlos Silva"
        )

        self.dados = {
            "id_cliente": "CLI001",
            "razao_social": "Empresa Exemplo LTDA",
            "cnpj_normalizado": "12345678000195",
            "telefone_normalizado": "61999999999",
            "email": "empresa@exemplo.com",
            "bairro_normalizado": "Asa Norte",
            "cep_normalizado": "70000000",
            "data_cadastro_normalizado": "2026-11-04",
            "vendedor": self.vendedor.id_vendedor
        }

    def test_cliente_valido(self):
        serializer = ClienteSerializer(data=self.dados)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_cliente_email_invalido(self):
        dados = self.dados.copy()
        dados["email"] = "email_invalido"

        serializer = ClienteSerializer(data=dados)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "email",
            serializer.errors
        )

    def test_cliente_sem_razao_social(self):
        dados = self.dados.copy()
        dados.pop("razao_social")

        serializer = ClienteSerializer(data=dados)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "razao_social",
            serializer.errors
        )

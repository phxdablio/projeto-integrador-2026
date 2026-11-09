from rest_framework import viewsets, permissions  # Importa módulos de ViewSets e Permissões do DRF
from rest_framework.decorators import action  # Importa o decorator para criar rotas personalizadas
from rest_framework.response import Response  # Importa a classe Response para retornar os dados formatados em JSON
from django_filters.rest_framework import DjangoFilterBackend  # Importa o suporte a filtros do django-filter
from .models import Cliente, Vendedor  # Importa os modelos da aplicação
from .serializers import ClienteSerializer, VendedorSerializer  # Importa os serializers correspondentes


class VendedorViewSet(viewsets.ModelViewSet):
    "ViewSet responsável pelas operações do CRUD de Vendedor."
    
    queryset = Vendedor.objects.all()  # Consulta para listar todos os vendedores
    serializer_class = VendedorSerializer  # Serializer utilizado para validar e formatar dados do Vendedor
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Leitura pública, alterações apenas para autenticados

    # Rota extra: /api/vendedores/{id}/clientes/
    @action(detail=True, methods=['get'])  # detail=True indica que a rota precisa do ID do vendedor
    def clientes(self, request, pk=None):
        vendedor = self.get_object()  # Recupera o objeto do vendedor com base no ID da URL
        clientes = Cliente.objects.filter(vendedor=vendedor)  # Filtra os clientes associados a este vendedor
        serializer = ClienteSerializer(clientes, many=True)  # Serializa a lista de clientes encontrados
        return Response(serializer.data)  # Retorna a resposta HTTP com os dados serializados


class ClienteViewSet(viewsets.ModelViewSet):
    "ViewSet responsável pelas operações do CRUD de Cliente."

    queryset = Cliente.objects.select_related('vendedor').all()  # Otimiza a busca incluindo o JOIN com Vendedor
    serializer_class = ClienteSerializer  # Serializer utilizado para validar e formatar dados do Cliente
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Leitura pública, alterações apenas para autenticados
    
    # Configuração do django-filter para consultas na URL (ex: /api/clientes/?bairro_normalizado=Centro)
    filter_backends = [DjangoFilterBackend]  # Ativa o backend de filtros do django-filter
    filterset_fields = ['bairro_normalizado', 'vendedor']  # Define quais campos podem ser filtrados via query params

    # Rota extra: /api/clientes/bairro/{nome}/
    @action(detail=False, methods=['get'], url_path='bairro/(?P<nome>[^/.]+)')  # detail=False indica rota para a coleção inteira
    def por_bairro(self, request, nome=None):
        clientes = self.get_queryset().filter(bairro_normalizado__iexact=nome)  # Filtra clientes pelo bairro (case-insensitive)
        serializer = self.get_serializer(clientes, many=True)  # Serializa os clientes filtrados
        return Response(serializer.data)  # Retorna a resposta HTTP com os dados serializados

    # Rota extra: /api/clientes/vendedor/{id}/
    @action(detail=False, methods=['get'], url_path='vendedor/(?P<vendedor_id>\d+)')  # detail=False pois recebe o ID do Vendedor
    def por_vendedor(self, request, vendedor_id=None):
        clientes = self.get_queryset().filter(vendedor_id=vendedor_id)  # Filtra clientes associados ao ID do Vendedor
        serializer = self.get_serializer(clientes, many=True)  # Serializa os clientes filtrados
        return Response(serializer.data)  # Retorna a resposta HTTP com os dados serializados
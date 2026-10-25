from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
 
from .models import Cliente, Vendedor
from .serializers import ClienteSerializer, VendedorSerializer
 
 
class VendedorViewSet(viewsets.ModelViewSet):
    """
    CRUD de vendedores.
    Rotas geradas pelo router:
      GET/POST          /api/vendedores/
      GET/PUT/PATCH/DELETE  /api/vendedores/{id}/
    Rota extra (abaixo):
      GET               /api/vendedores/{id}/clientes/
    """
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    # Sem login: só GET. Com token: CRUD completo.
    permission_classes = [IsAuthenticatedOrReadOnly]
 
    # detail=True -> a rota trabalha com UM vendedor (usa o {id} da URL)
    @action(detail=True, methods=["get"])
    def clientes(self, request, pk=None):
        vendedor = self.get_object()  # busca o vendedor pelo id (404 se não existir)
        clientes = Cliente.objects.filter(vendedor=vendedor)
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)
 
 
class ClienteViewSet(viewsets.ModelViewSet):
    """
    CRUD de clientes.
    Rotas geradas pelo router:
      GET/POST          /api/clientes/
      GET/PUT/PATCH/DELETE  /api/clientes/{id}/
    Rotas extras (abaixo):
      GET               /api/clientes/bairro/{nome}/
      GET               /api/clientes/vendedor/{id}/
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
 
    # detail=False -> a rota trabalha com a LISTA de clientes (filtrada)
    @action(
        detail=False,
        methods=["get"],
        url_path=r"bairro/(?P<nome>[^/.]+)",
    )
    def por_bairro(self, request, nome=None):
        # iexact ignora maiúsculas/minúsculas
        clientes = Cliente.objects.filter(bairro_normalizado__iexact=nome)
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)
 
    @action(
        detail=False,
        methods=["get"],
        url_path=r"vendedor/(?P<vendedor_id>[0-9]+)",
    )
    def por_vendedor(self, request, vendedor_id=None):
        clientes = Cliente.objects.filter(vendedor_id=vendedor_id)
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)
 

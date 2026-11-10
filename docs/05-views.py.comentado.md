
# views.py — Arquivo Comentado

## 1. Importações

```python
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cliente, Vendedor
from .serializers import ClienteSerializer, VendedorSerializer
```

- `viewsets` → disponibiliza classes para implementar operações CRUD.
- `permissions` → controla as permissões de acesso aos endpoints.
- `action` → permite criar rotas personalizadas.
- `Response` → retorna respostas HTTP com dados serializados.
- `DjangoFilterBackend` → permite filtrar registros por parâmetros na URL.
- `models` e `serializers` → importam as entidades e seus respectivos serializers.

---

## 2. VendedorViewSet

```python
class VendedorViewSet(viewsets.ModelViewSet):
```

- Define o ViewSet responsável pelo gerenciamento de vendedores.
- `ModelViewSet` disponibiliza automaticamente as operações de listagem, consulta, criação, atualização e exclusão.

### Configurações principais

```python
queryset = Vendedor.objects.all()
serializer_class = VendedorSerializer
permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```

- `queryset` → consulta os vendedores cadastrados.
- `serializer_class` → define o serializer utilizado.
- `IsAuthenticatedOrReadOnly` → permite consultas públicas, mas exige autenticação para alterações.

### Rota personalizada — Clientes de um vendedor

**Endpoint:** `GET /api/vendedores/{id}/clientes/`

```python
@action(detail=True, methods=['get'])
def clientes(self, request, pk=None):
    vendedor = self.get_object()
    clientes = Cliente.objects.filter(vendedor=vendedor)
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)
```

- `@action(detail=True)` → cria uma rota associada a um vendedor específico.
- `self.get_object()` → recupera o vendedor pelo ID informado na URL.
- `filter(vendedor=vendedor)` → consulta os clientes vinculados ao vendedor.
- `many=True` → indica que serão serializados múltiplos registros.
- `Response(serializer.data)` → retorna a lista de clientes.

---

## 3. ClienteViewSet

```python
class ClienteViewSet(viewsets.ModelViewSet):
```

- Define o ViewSet responsável pelas operações CRUD de clientes.

### Configurações principais

```python
queryset = Cliente.objects.select_related('vendedor').all()
serializer_class = ClienteSerializer
permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```

- `select_related('vendedor')` → otimiza a consulta recuperando os dados do vendedor por meio de um JOIN.
- `serializer_class` → utiliza o `ClienteSerializer`.
- `IsAuthenticatedOrReadOnly` → permite leitura pública e restringe alterações a usuários autenticados.

### Filtros automáticos

```python
filter_backends = [DjangoFilterBackend]
filterset_fields = ['bairro_normalizado', 'vendedor']
```

- `DjangoFilterBackend` → habilita filtros por parâmetros de consulta.
- `filterset_fields` → define os campos disponíveis para filtragem.

## 4. Rota personalizada — Clientes por bairro

**Endpoint:** `GET /api/clientes/bairro/{nome}/`

```python
@action(
    detail=False,
    methods=['get'],
    url_path='bairro/(?P<nome>[^/.]+)'
)
def por_bairro(self, request, nome=None):
    clientes = self.get_queryset().filter(
        bairro_normalizado__iexact=nome
    )
    serializer = self.get_serializer(clientes, many=True)
    return Response(serializer.data)
```

- `detail=False` → cria uma rota de consulta à coleção de clientes.
- `url_path` → captura o nome do bairro informado na URL.
- `bairro_normalizado__iexact` → realiza uma comparação exata sem diferenciar letras maiúsculas e minúsculas.
- `self.get_serializer()` → serializa os clientes encontrados.
- `Response()` → retorna os resultados da consulta.

## 5. Rota personalizada — Clientes por vendedor

**Endpoint:** `GET /api/clientes/vendedor/{id}/`

```python
@action(
    detail=False,
    methods=['get'],
    url_path='vendedor/(?P<vendedor_id>\d+)'
)
def por_vendedor(self, request, vendedor_id=None):
    clientes = self.get_queryset().filter(
        vendedor_id=vendedor_id
    )
    serializer = self.get_serializer(clientes, many=True)
    return Response(serializer.data)
```

- `url_path` → captura o identificador numérico do vendedor.
- `filter(vendedor_id=vendedor_id)` → recupera os clientes associados ao vendedor informado.
- `self.get_serializer()` → converte os registros encontrados para uma representação serializável.
- `Response()` → retorna a lista de clientes.


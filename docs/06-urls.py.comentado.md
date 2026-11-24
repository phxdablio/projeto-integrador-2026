
# urls.py — Arquivo Comentado

## 1. Importações

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_views
from distribuidora.views import ClienteViewSet, VendedorViewSet
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
```

- `admin` → disponibiliza o painel administrativo do Django.
- `path` e `include` → definem e agrupam as rotas da aplicação.
- `DefaultRouter` → gera automaticamente os endpoints CRUD dos ViewSets.
- `token_views` → disponibiliza a autenticação por token do DRF.
- `ClienteViewSet` e `VendedorViewSet` → implementam as operações da API.
- `drf_spectacular` → gera o esquema OpenAPI e as interfaces de documentação Swagger e ReDoc.

---

## 2. Configuração do roteador

```python
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'vendedores', VendedorViewSet, basename='vendedor')
```

- `DefaultRouter()` → cria o roteador responsável por gerar as URLs automaticamente.
- `router.register()` → associa cada ViewSet a um prefixo de URL.
- `basename` → define o nome-base utilizado para identificar as rotas.

**Endpoints gerados:**

| Endpoint | Métodos | Funcionalidade |
|---|---|---|
| `/api/clientes/` | GET, POST | Listagem e cadastro de clientes |
| `/api/clientes/{id}/` | GET, PUT, PATCH, DELETE | Consulta, atualização e exclusão de clientes |
| `/api/vendedores/` | GET, POST | Listagem e cadastro de vendedores |
| `/api/vendedores/{id}/` | GET, PUT, PATCH, DELETE | Consulta, atualização e exclusão de vendedores |

O roteador também registra as rotas personalizadas definidas com `@action` nos ViewSets.

---

## 3. Definição das URLs

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
```

- `urlpatterns` → lista principal de rotas reconhecidas pelo Django.
- `/admin/` → permite acessar o painel administrativo.
- `/api/` → agrupa os endpoints de clientes e vendedores registrados no roteador.

---

## 4. Autenticação por token

**Endpoint:** `POST /api/auth/token/`

```python
path(
    "api/auth/token/",
    token_views.obtain_auth_token,
    name="api_token_auth"
)
```

- `obtain_auth_token` → recebe credenciais válidas e retorna um token de autenticação.
- `name="api_token_auth"` → identifica a rota internamente no Django.

## 5. Esquema OpenAPI

**Endpoint:** `GET /api/schema/`

```python
path(
    "api/schema/",
    SpectacularAPIView.as_view(),
    name="schema"
)
```

- `SpectacularAPIView` → gera o esquema OpenAPI da aplicação.
- O esquema descreve os endpoints, métodos HTTP, parâmetros e respostas da API.
- Pode ser utilizado por ferramentas de documentação e integração.

---

## 6. Documentação Swagger

**Endpoint:** `GET /api/docs/`

```python
path(
    "api/docs/",
    SpectacularSwaggerView.as_view(url_name="schema"),
    name="swagger-ui"
)
```

- `SpectacularSwaggerView` → disponibiliza a interface interativa Swagger UI.
- `url_name="schema"` → utiliza o esquema OpenAPI definido anteriormente.
- Permite visualizar os endpoints e realizar requisições de teste pela interface.

---

## 7. Documentação ReDoc

**Endpoint:** `GET /api/redoc/`

```python
path(
    "api/redoc/",
    SpectacularRedocView.as_view(url_name="schema"),
    name="redoc"
)
```

- `SpectacularRedocView` → disponibiliza uma interface alternativa de documentação da API.
- `url_name="schema"` → utiliza o mesmo esquema OpenAPI.
- Organiza os endpoints e seus detalhes para consulta.

---

## 8. Resumo das rotas principais

| Método | Endpoint | Funcionalidade |
|---|---|---|
| GET/POST | `/api/clientes/` | Listar e cadastrar clientes |
| GET/PUT/PATCH/DELETE | `/api/clientes/{id}/` | Gerenciar cliente específico |
| GET | `/api/clientes/bairro/{nome}/` | Filtrar clientes por bairro |
| GET | `/api/clientes/vendedor/{id}/` | Filtrar clientes por vendedor |
| GET/POST | `/api/vendedores/` | Listar e cadastrar vendedores |
| GET/PUT/PATCH/DELETE | `/api/vendedores/{id}/` | Gerenciar vendedor específico |
| GET | `/api/vendedores/{id}/clientes/` | Listar clientes de um vendedor |
| POST | `/api/auth/token/` | Obter token de autenticação |
| GET | `/api/schema/` | Consultar esquema OpenAPI |
| GET | `/api/docs/` | Acessar documentação Swagger |
| GET | `/api/redoc/` | Acessar documentação ReDoc |

---


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


# Criação e configuração do roteador do DRF
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'vendedores', VendedorViewSet, basename='vendedor')

urlpatterns = [
    path("admin/", admin.site.urls),

    # Endpoints da API (clientes e vendedores)
    path("api/", include(router.urls)),

    # Autenticação via Token
    path("api/auth/token/", token_views.obtain_auth_token, name="api_token_auth"),

    # Esquema OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # Documentação Swagger
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    # Documentação ReDoc
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
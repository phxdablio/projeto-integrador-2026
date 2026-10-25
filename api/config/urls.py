from rest_framework.routers import DefaultRouter
 
from .views import ClienteViewSet, VendedorViewSet
 
# O router cria sozinho as rotas de listar, criar, detalhar, editar e apagar,
# além das rotas extras definidas com @action nas views.
router = DefaultRouter()
router.register("clientes", ClienteViewSet, basename="cliente")
router.register("vendedores", VendedorViewSet, basename="vendedor")
 
urlpatterns = router.urls
 

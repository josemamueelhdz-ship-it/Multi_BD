# core/urls.py
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet

router = DefaultRouter()
# Esto creará los endpoints: /usuarios, /usuarios/{pk}, etc.
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = router.urls
# core/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, 
    ProductoViewSet,
    PedidoViewSet,
    NotificacionListCreateAPIView, 
    NotificacionRetrieveUpdateDestroyAPIView,
    LogListCreateAPIView,
    LogRetrieveDestroyAPIView,
    SesionCreateRetrieveDestroyAPIView
)

# Router para Modelos Relacionales (PostgreSQL)
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'pedidos', PedidoViewSet)

# URL patterns manuales para recursos NoSQL (MongoDB y Redis)
urlpatterns = [
    # Endpoints para Notificaciones (MongoDB)
    path('notificaciones/', NotificacionListCreateAPIView.as_view(), name='notificacion-list-create'),
    path('notificaciones/<str:pk>/', NotificacionRetrieveUpdateDestroyAPIView.as_view(), name='notificacion-detail'),
    
    # Endpoints para Logs (MongoDB)
    path('logs/', LogListCreateAPIView.as_view(), name='log-list-create'),
    path('logs/<str:pk>/', LogRetrieveDestroyAPIView.as_view(), name='log-detail'),
    
    # Endpoints para Sesiones (Redis)
    path('sesiones/', SesionCreateRetrieveDestroyAPIView.as_view(), name='sesion-create'),
    path('sesiones/<str:pk>/', SesionCreateRetrieveDestroyAPIView.as_view(), name='sesion-detail'),
]

# Unir las URLs del router con las URLs manuales
urlpatterns += router.urls
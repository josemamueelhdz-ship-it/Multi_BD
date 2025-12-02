# core/views.py

from rest_framework import viewsets, views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Usuario, Producto, Pedido 
from .serializers import (
    UsuarioSerializer, ProductoSerializer, PedidoSerializer, 
    NotificacionSerializer, LogSerializer, SesionSerializer
) 
from .services.mongo_service import mongo_service
from .services.redis_service import redis_service

# -------------------- Vistas Relacionales (PostgreSQL) --------------------

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------- Vistas NoSQL (MongoDB) --------------------

class NotificacionListCreateAPIView(views.APIView):
    def get(self, request, format=None):
        notificaciones = mongo_service.obtener_notificaciones()
        serializer = NotificacionSerializer(notificaciones, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificacionSerializer(data=request.data)
        if serializer.is_valid():
            mongo_id = mongo_service.crear_notificacion(serializer.validated_data)
            nueva_notificacion = mongo_service.obtener_notificaciones(notificacion_id=mongo_id)
            serializer_response = NotificacionSerializer(nueva_notificacion)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificacionRetrieveUpdateDestroyAPIView(views.APIView):
    def get(self, request, pk, format=None):
        notificacion = mongo_service.obtener_notificaciones(notificacion_id=pk)
        if notificacion:
            return Response(NotificacionSerializer(notificacion).data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk, format=None):
        existing_data = mongo_service.obtener_notificaciones(notificacion_id=pk)
        if not existing_data:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = NotificacionSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            modified_count = mongo_service.actualizar_notificacion(pk, serializer.validated_data)
            
            if modified_count > 0:
                updated_notif = mongo_service.obtener_notificaciones(notificacion_id=pk)
                return Response(NotificacionSerializer(updated_notif).data)
            
            return Response({'detail': 'No se encontró o no se pudo actualizar.'}, 
                            status=status.HTTP_404_NOT_FOUND)
                            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        modified_count = mongo_service.borrado_logico_notificacion(pk)
        if modified_count > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class LogListCreateAPIView(views.APIView):
    def get(self, request, format=None):
        logs = mongo_service.obtener_logs()
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            mongo_id = mongo_service.crear_log(serializer.validated_data)
            nuevo_log = mongo_service.obtener_logs(log_id=mongo_id)
            serializer_response = LogSerializer(nuevo_log)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogRetrieveDestroyAPIView(views.APIView):
    def get(self, request, pk, format=None):
        log = mongo_service.obtener_logs(log_id=pk)
        if log:
            return Response(LogSerializer(log).data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        modified_count = mongo_service.borrado_logico_log(pk)
        if modified_count > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

# -------------------- Vistas Clave-Valor (Redis) --------------------

class SesionCreateRetrieveDestroyAPIView(views.APIView):
    def post(self, request, format=None):
        serializer = SesionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            clave = data.pop('clave')
            ttl = data.pop('tiempo_expiracion_segundos', 3600)
            redis_service.crear_sesion(clave, data, ttl)
            response_data = {'clave': clave, **data}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        sesion_data = redis_service.obtener_sesion(pk)
        if sesion_data:
            response_data = {'clave': pk, **sesion_data}
            return Response(response_data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk, format=None):
        existing_data = redis_service.obtener_sesion(pk)
        if not existing_data:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        updated_data = existing_data.copy()
        updated_data.update(request.data)
        
        serializer = SesionSerializer(data=updated_data, partial=True)
        if serializer.is_valid():
            if redis_service.actualizar_sesion(pk, serializer.validated_data):
                response_data = {'clave': pk, **serializer.validated_data}
                return Response(response_data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if redis_service.borrado_logico_sesion(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
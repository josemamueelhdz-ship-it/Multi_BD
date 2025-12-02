# core/serializers.py

from rest_framework import serializers
from .models import Usuario, Producto, Pedido, PedidoDetalle

# -------------------- Serializadores Relacionales (PostgreSQL) --------------------

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'password_hash', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']
        extra_kwargs = {'password_hash': {'write_only': True}}

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']
        
# -------------------- Serializadores NoSQL (MongoDB) --------------------

class NotificacionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True) 
    usuario_id = serializers.IntegerField() 
    mensaje = serializers.CharField(max_length=500)
    tipo = serializers.CharField(max_length=50) 
    is_deleted = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return validated_data 

class LogSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True) 
    nivel = serializers.CharField(max_length=20) 
    mensaje_error = serializers.CharField(max_length=1024)
    recurso = serializers.CharField(max_length=100) 
    is_deleted = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return validated_data 

# -------------------- Serializador Clave-Valor (Redis) --------------------

class SesionSerializer(serializers.Serializer):
    clave = serializers.CharField(max_length=255) 
    user_id = serializers.IntegerField() 
    rol = serializers.CharField(max_length=50)
    tiempo_expiracion_segundos = serializers.IntegerField(default=3600, write_only=True) 
    
    def create(self, validated_data):
        return validated_data 

    def update(self, instance, validated_data):
        return validated_data
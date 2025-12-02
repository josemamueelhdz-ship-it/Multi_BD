# core/serializers.py
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Especifica todos los campos que deseas exponer en la API
        fields = ['id', 'nombre', 'email', 'created_at', 'updated_at', 'is_deleted']
        # El ID es de solo lectura, se genera automáticamente
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']
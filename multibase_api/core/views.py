from django.shortcuts import render

# Create your views here.
# core/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import Usuario, ActiveManager
from .serializers import UsuarioSerializer

# Sobrescribimos el ModelViewSet para garantizar el borrado lógico
class UsuarioViewSet(viewsets.ModelViewSet):
    # Consulta base: solo objetos activos (gracias al ActiveManager en el modelo)
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    # Sobrescribe el método destroy (DELETE) para aplicar el borrado lógico
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Llama al método de borrado lógico definido en core/models.py
        instance.delete() 
        
        # Devuelve un estado 204 No Content para indicar éxito
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Nota: El método list (GET /usuarios) ya usa el ActiveManager por defecto 
    # y no incluirá los usuarios borrados (is_deleted=True).
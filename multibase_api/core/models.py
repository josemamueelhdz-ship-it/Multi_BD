# core/models.py
from django.db import models

# ----------------- 1. Manager Personalizado para Borrado Lógico -----------------

class ActiveManager(models.Manager):
    """
    Manager que filtra automáticamente los objetos con is_deleted=False.
    Usado como el manager por defecto (objects).
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

# ----------------- 2. Modelo Base para Borrado Lógico y Timestamps -----------------

class BaseModel(models.Model):
    # Campo para el borrado lógico.
    is_deleted = models.BooleanField(default=False)
    
    # Campos de tiempo para tracking.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Managers:
    objects = ActiveManager()       # El manager por defecto (solo registros activos)
    all_objects = models.Manager()  # Manager para consultar TODOS los registros (incluidos borrados)
    
    class Meta:
        abstract = True
        
    def delete(self, *args, **kwargs):
        """Sobrescribe el método delete para marcar el registro como borrado (borrado lógico)."""
        self.is_deleted = True
        self.save()
        
    def hard_delete(self, *args, **kwargs):
        """Método opcional para eliminar físicamente el registro (uso interno)."""
        super().delete(*args, **kwargs)

# ----------------- 3. Recursos Relacionales (PostgreSQL) -----------------

# Recurso 1: Usuarios
class Usuario(BaseModel):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128) # Almacenar hash, no la contraseña
    
    def __str__(self):
        return f"Usuario: {self.nombre}"

# Recurso 2: Productos
class Producto(BaseModel):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre

# Recurso 3: Pedidos
class Pedido(BaseModel):
    # Relación uno-a-muchos con Usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING) 
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=50, 
        choices=[
            ('PENDIENTE', 'Pendiente'),
            ('PROCESO', 'En Proceso'),
            ('ENVIADO', 'Enviado'),
            ('ENTREGADO', 'Entregado'),
        ],
        default='PENDIENTE'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.nombre}"

# Recurso 4: Detalle del Pedido (Opcional, pero necesario para un Pedido funcional)
# Aunque tienes 6 recursos, este es un recurso relacionado esencial.
class PedidoDetalle(BaseModel):
    # Relación uno-a-muchos con Pedido
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE) 
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING) 
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id} en Pedido {self.pedido.id}"
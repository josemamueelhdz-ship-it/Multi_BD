# core/services/redis_service.py

import redis
import json
from django.conf import settings
from typing import Union

class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            db=settings.REDIS_DB, 
            decode_responses=True
        )

    # --------------------- CRUD para Sesiones (Clave-Valor) ---------------------
    
    def crear_sesion(self, clave: str, data: dict, tiempo_expiracion: int = 3600) -> bool:
        valor_json = json.dumps(data)
        self.client.set(clave, valor_json, ex=tiempo_expiracion)
        return True

    def obtener_sesion(self, clave: str) -> Union[dict, None]:
        valor_json = self.client.get(clave)
        if valor_json:
            return json.loads(valor_json)
        return None

    def actualizar_sesion(self, clave: str, data: dict) -> bool:
        if not self.client.exists(clave):
            return False
            
        ttl = self.client.ttl(clave)
        valor_json = json.dumps(data)
        self.client.set(clave, valor_json, ex=ttl)
        return True

    def borrado_logico_sesion(self, clave: str) -> bool:
        # En Redis, el borrado lógico es una eliminación física ya que los datos son volátiles
        return self.client.delete(clave) > 0

redis_service = RedisService()
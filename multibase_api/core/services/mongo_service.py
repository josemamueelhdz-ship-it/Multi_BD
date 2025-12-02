# core/services/mongo_service.py

from pymongo import MongoClient
from django.conf import settings
from bson.objectid import ObjectId
import datetime
from typing import Union

class MongoService:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DATABASE]

    def _get_collection(self, collection_name):
        return self.db[collection_name]

    # --------------------- CRUD para Notificaciones ---------------------
    
    def crear_notificacion(self, data: dict) -> str:
        data['is_deleted'] = False
        data['created_at'] = datetime.datetime.utcnow()
        collection = self._get_collection('notificaciones')
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def obtener_notificaciones(self, notificacion_id: str = None) -> Union[dict, list, None]:
        collection = self._get_collection('notificaciones')
        query = {'is_deleted': False}
        if notificacion_id:
            try:
                query['_id'] = ObjectId(notificacion_id)
                return collection.find_one(query) 
            except:
                return None
        return list(collection.find(query))

    def actualizar_notificacion(self, notificacion_id: str, data: dict) -> int:
        collection = self._get_collection('notificaciones')
        data['updated_at'] = datetime.datetime.utcnow()
        
        result = collection.update_one(
            {'_id': ObjectId(notificacion_id), 'is_deleted': False},
            {'$set': data}
        )
        return result.modified_count

    def borrado_logico_notificacion(self, notificacion_id: str) -> int:
        collection = self._get_collection('notificaciones')
        result = collection.update_one(
            {'_id': ObjectId(notificacion_id)},
            {'$set': {'is_deleted': True, 'deleted_at': datetime.datetime.utcnow()}}
        )
        return result.modified_count

    # --------------------- CRUD para Logs ---------------------
    
    def crear_log(self, data: dict) -> str:
        data['is_deleted'] = False
        data['created_at'] = datetime.datetime.utcnow()
        collection = self._get_collection('logs')
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def obtener_logs(self, log_id: str = None) -> Union[dict, list, None]:
        collection = self._get_collection('logs')
        query = {'is_deleted': False}
        
        if log_id:
            try:
                query['_id'] = ObjectId(log_id)
                return collection.find_one(query)
            except:
                return None
        
        return list(collection.find(query))

    def borrado_logico_log(self, log_id: str) -> int:
        collection = self._get_collection('logs')
        result = collection.update_one(
            {'_id': ObjectId(log_id)},
            {'$set': {'is_deleted': True, 'deleted_at': datetime.datetime.utcnow()}}
        )
        return result.modified_count

mongo_service = MongoService()
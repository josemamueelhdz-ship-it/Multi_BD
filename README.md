Esta aplicación implementa un servicio web (API REST) con Persistencia Políglota, utilizando Python y Django REST Framework para gestionar datos a través de tres tipos de bases de datos diferentes: PostgreSQL, MongoDB y Redis.

  Equipo de Desarrollo y Colaboración
Integrantes: Mario Angel Padilla Gonzalez - (MarioPadillaG)
Integrantes: Jose Manuel Soto Hernandez -   (JoseMamuel)

   Stack Tecnológico y Arquitectura
Motor de BD	   Tipo de Persistencia	       Recurso(s) Implementado(s)	  Borrado Aplicado
PostgreSQL	   Relacional (ORM de Django)	 Usuarios, Productos, Pedidos	Lógico (is_deleted = True)
MongoDB	       NoSQL (Documento)	         Notificaciones, Logs	        Lógico (is_deleted = True)
Redis	         Clave-Valor	               Sesiones	                    Físico (Eliminación de la clave)
Características de la Aplicación
API RESTful: Implementada con Django REST Framework (DRF) para crear endpoints (GET, POST, PATCH, DELETE).
Abstracción: Se utiliza la carpeta core/services/ para gestionar la lógica de conexión y operaciones de MongoDB y Redis.

1. Instalación y Configuración
A. Requisitos Previos
Asegúrese de que los siguientes servidores de bases de datos estén activos y accesibles antes de la instalación:
Servidor PostgreSQL (Puerto 5432).
Servidor MongoDB (Puerto 27017).
Servidor Redis (Puerto 6379).

B. Pasos de Instalación y Ejecución
Clonar el Repositorio:
git clone https://github.com/josemamueelhdz-ship-it/Multi_BD.gitcd Multi_BD

Crear Entorno Virtual e Instalar Dependencias:
python -m venv venvsource venv/bin/activate # o .\venv\Scripts\activate en Windows
pip install django djangorestframework psycopg2-binary pymongo redis

Configurar Conexiones:
PostgreSQL: Cree manualmente una base de datos vacía llamada db_relacional. Verifique las credenciales en multibase_api/settings.py.
Ejecutar Migraciones :
python manage.py makemigrations core
python manage.py migrate
Ejecutar el Servidor API:
python manage.py runserver
El API estará disponible en http://127.0.0.1:8000/.

2. Guía de Endpoints para Pruebas
Utilice una herramienta como Postman o cURL para probar las siguientes operaciones CRUD.
A. PostgreSQL (Relacional) - CRUD Lógico
Recurso	Método	URL de Prueba	Propósito
Usuarios	POST	/usuarios/	Crear un registro.
Productos	PATCH	/productos/{id}/	Editar parcialmente un registro
Pedidos	  DELETE	/pedidos/{id}/	Borrado Lógico (Marca is_deleted = true)
B. MongoDB (NoSQL Documento) - CRUD Lógico
Recurso	Método	URL de Prueba	Propósito
Logs	          POST	/logs/	Crear un documento 
Notificaciones	PATCH	/notificaciones/{id_mongo}/	Editar el campo mensaje 
Logs	          DELETE/logs/{id_mongo}/	Borrado Lógico (Marca is_deleted = true). Retorna 204.
C. Redis (Clave-Valor) 
Recurso	Método	URL de Prueba	Propósito
Sesiones	POST	/sesiones/	Crear una clave-valor (Ej: guardar un token).
Sesiones	PATCH	/sesiones/TOKEN_1/	Actualizar el valor de la clave (Ej: cambiar el rol).
Sesiones	DELETE	/sesiones/TOKEN_1/	Borrado Físico (Elimina la clave). Retorna 204.

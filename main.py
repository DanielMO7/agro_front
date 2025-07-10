from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.core.db.config import settings
from app.core.db.init_db import init_db
from app.core.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
)
from app.core.middlewares import catch_exceptions_middleware, timeout_middleware
from app.api.v1.router import api_v1_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200",  # URL del frontend Angular local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la base de datos
init_db()  # Inicializa la base de datos al arrancar la aplicación (puede incluir la creación de tablas, conexiones, etc.)

# Registrar el router para las rutas de la API versión 1
app.include_router(api_v1_router, prefix="/api/v1")  # Incluye las rutas del router `api_v1_router` bajo el prefijo `/api/v1`.

# Registrar Handlers de Excepciones
app.add_exception_handler(HTTPException, http_exception_handler)  # Maneja excepciones HTTP (por ejemplo, 404, 500, etc.)
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # Maneja excepciones de validación de datos (422).

# Registrar Middlewares
app.middleware("http")(catch_exceptions_middleware)  # Middleware para capturar y manejar excepciones no controladas.
app.middleware("http")(timeout_middleware)  # Middleware para manejar timeouts (limitar el tiempo de respuesta de las solicitudes).

# Endpoint raíz
@app.get("/")
def read_root():
    """Endpoint principal de bienvenida"""
    return {
        "success": True,
        "message": f"Bienvenido a agro-Backend, la API de Prueba Técnica. Base de Datos a Conectar: {settings.DB_NAME}",
    }

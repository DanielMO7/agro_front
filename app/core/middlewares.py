import asyncio
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

# Middleware para capturar excepciones globales
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Error interno del servidor",
                "details": str(e),
            },
        )

# Middleware para manejar timeouts
async def timeout_middleware(request: Request, call_next):
    try:
        return await asyncio.wait_for(call_next(request), timeout=5.0)
    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=408,
            content={
                "success": False,
                "error": "La solicitud tomó demasiado tiempo",
                "details": None,
            },
        )

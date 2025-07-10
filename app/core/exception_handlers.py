from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Handler para HTTPException
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail, "details": None},
    )

# Handler para errores de validación
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = []
    for error in exc.errors():
        error_details.append(
            {
                "type": error["type"],
                "loc": error["loc"],
                "msg": error["msg"].replace("Value error, ", ""),
                "input": error.get("input"),
                "ctx": error.get("ctx"),
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Error de validación en los datos de entrada",
            "details": jsonable_encoder(error_details),
        },
    )

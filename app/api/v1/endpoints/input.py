from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

# Core
from app.core.db.session import get_db
from app.core.security import get_current_user, bearer_scheme

# Schemas & CRUD
from app.schemas.input import InputCreate, InputUpdate, InputResponse
from app.crud.input import (
    get_inputs,
    get_input,
    create_input,
    update_input,
    delete_input
)

router = APIRouter(prefix="/inputs", tags=["Inputs"])

common_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "No autorizado - Token inválido o expirado",
        "headers": {"WWW-Authenticate": "Bearer"},
    },
    status.HTTP_403_FORBIDDEN: {"description": "Prohibido - No tienes permisos suficientes"},
    status.HTTP_404_NOT_FOUND: {"description": "Insumo no encontrado"},
}


def verify_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para esta acción",
        )


@router.get(
    "/",
    response_model=List[InputResponse],
    summary="Obtener todos los insumos",
    description="Lista todos los insumos registrados. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def read_inputs(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    return get_inputs(db)


@router.get(
    "/{input_id}",
    response_model=InputResponse,
    summary="Obtener un insumo por ID",
    description="Obtiene la información de un insumo específico. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def read_input(
    input_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    db_input = get_input(db, input_id)
    if not db_input:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return db_input


@router.post(
    "/",
    response_model=InputResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo insumo",
    description="Registra un nuevo insumo. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def create_input_endpoint(
    input_data: InputCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    return create_input(db, input_data)


@router.put(
    "/{input_id}",
    response_model=InputResponse,
    summary="Actualizar un insumo",
    description="Actualiza los datos de un insumo existente. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def update_input_endpoint(
    input_id: int,
    input_data: InputUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    updated_input = update_input(db, input_id, input_data)
    if not updated_input:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return updated_input


@router.delete(
    "/{input_id}",
    response_model=InputResponse,
    summary="Eliminar un insumo",
    description="Elimina un insumo existente. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def delete_input_endpoint(
    input_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    db_input = delete_input(db, input_id)
    if not db_input:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return db_input

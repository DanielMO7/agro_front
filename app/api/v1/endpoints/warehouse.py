from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

# Core
from app.core.db.session import get_db
from app.core.security import get_current_user, bearer_scheme

# Schemas & CRUD
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate, WarehouseResponse
from app.crud.warehouse import (
    get_warehouses,
    get_warehouse,
    create_warehouse,
    update_warehouse,
    delete_warehouse,
)

router = APIRouter(prefix="/warehouses", tags=["Warehouses"])

common_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "No autorizado - Token inválido o expirado",
        "headers": {"WWW-Authenticate": "Bearer"},
    },
    status.HTTP_403_FORBIDDEN: {"description": "Prohibido - No tienes permisos suficientes"},
    status.HTTP_404_NOT_FOUND: {"description": "Almacén no encontrado"},
}


def verify_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para esta acción",
        )


@router.get(
    "/",
    response_model=List[WarehouseResponse],
    summary="Obtener todos los almacenes",
    description="Lista todos los almacenes registrados. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def read_warehouses(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    return get_warehouses(db)


@router.get(
    "/{warehouse_id}",
    response_model=WarehouseResponse,
    summary="Obtener un almacén por ID",
    description="Obtiene la información de un almacén específico. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def read_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    warehouse = get_warehouse(db, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    return warehouse


@router.post(
    "/",
    response_model=WarehouseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo almacén",
    description="Registra un nuevo almacén. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def create_warehouse_endpoint(
    warehouse_data: WarehouseCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    return create_warehouse(db, warehouse_data)


@router.put(
    "/{warehouse_id}",
    response_model=WarehouseResponse,
    summary="Actualizar un almacén",
    description="Actualiza los datos de un almacén existente. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def update_warehouse_endpoint(
    warehouse_id: int,
    warehouse_data: WarehouseUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    updated_warehouse = update_warehouse(db, warehouse_id, warehouse_data)
    if not updated_warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    return updated_warehouse


@router.delete(
    "/{warehouse_id}",
    response_model=WarehouseResponse,
    summary="Eliminar un almacén",
    description="Elimina un almacén existente. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def delete_warehouse_endpoint(
    warehouse_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    warehouse = delete_warehouse(db, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    return warehouse

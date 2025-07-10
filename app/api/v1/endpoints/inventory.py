from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

# Core
from app.core.db.session import get_db
from app.core.security import get_current_user, bearer_scheme

# Schemas & CRUD
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.crud.inventory import (
    get_inventories,
    get_inventory,
    create_inventory,
    update_inventory,
    delete_inventory,
)

router = APIRouter(prefix="/inventories", tags=["Inventories"])

common_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "No autorizado - Token inválido o expirado",
        "headers": {"WWW-Authenticate": "Bearer"},
    },
    status.HTTP_403_FORBIDDEN: {"description": "Prohibido - No tienes permisos suficientes"},
    status.HTTP_404_NOT_FOUND: {"description": "Registro de inventario no encontrado"},
}


def verify_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para esta acción",
        )


@router.get(
    "/",
    response_model=List[InventoryResponse],
    summary="Obtener todo el inventario",
    description="Lista todos los registros de inventario. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def read_inventories(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    return get_inventories(db)


@router.get(
    "/{inventory_id}",
    response_model=InventoryResponse,
    summary="Obtener inventario por ID",
    description="Obtiene un registro de inventario por su ID. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def read_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    inventory = get_inventory(db, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")
    return inventory


@router.post(
    "/",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo registro de inventario",
    description="Crea un nuevo registro de inventario. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def create_inventory_endpoint(
    inventory_data: InventoryCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    return create_inventory(db, inventory_data)


@router.put(
    "/{inventory_id}",
    response_model=InventoryResponse,
    summary="Actualizar un registro de inventario",
    description="Actualiza un registro de inventario existente. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def update_inventory_endpoint(
    inventory_id: int,
    inventory_data: InventoryUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    updated_inventory = update_inventory(db, inventory_id, inventory_data)
    if not updated_inventory:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")
    return updated_inventory


@router.delete(
    "/{inventory_id}",
    response_model=InventoryResponse,
    summary="Eliminar registro de inventario",
    description="Elimina un registro de inventario existente. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={**common_responses},
)
async def delete_inventory_endpoint(
    inventory_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    verify_admin(current_user)
    inventory = delete_inventory(db, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")
    return inventory

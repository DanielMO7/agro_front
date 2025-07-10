# FastAPI Imports
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

# Importación de funciones de la base de datos y seguridad
from app.core.db.session import get_db
from app.core.security import get_current_user, bearer_scheme
from app.core.db.config import settings

# Importación de funciones de CRUD y esquemas
from app.crud.user import get_users, get_user, create_user, delete_user, update_user
from app.schemas.user import UserCreate, UserResponse, UserUpdate

from app.core.email import send_email

# Inicialización del router con el prefijo y las etiquetas correspondientes
router = APIRouter(prefix="/users", tags=["Users"])

# Documentación de respuestas comunes (errores de autenticación y autorización)
common_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "No autorizado - Token inválido o expirado",
        "headers": {"WWW-Authenticate": "Bearer"},
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Prohibido - No tienes permisos suficientes"
    },
    status.HTTP_404_NOT_FOUND: {"description": "Usuario no encontrado"},
}


# 🔹 Función para verificar si el usuario es administrador
def verify_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para esta acción",
        )


@router.get(
    "/",
    dependencies=[Depends(bearer_scheme)],
    response_model=List[UserResponse],
    summary="Obtener todos los usuarios",
    description="Retorna una lista de todos los usuarios registrados. Requiere autenticación JWT.",
    responses={  # Definimos las respuestas de la API
        **common_responses,
        status.HTTP_200_OK: {
            "description": "Lista de usuarios obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": [{"id": 1, "name": "user1"}, {"id": 2, "name": "user2"}]
                }
            },
        },
    },
)
async def read_users(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    """
    Obtiene todos los usuarios registrados en el sistema.

    Requiere:
    - Token JWT válido en el header Authorization

    Retorna:
    - Lista de usuarios en formato JSON
    """
    verify_admin(current_user)
    return get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener un usuario específico",
    description="Retorna los detalles de un usuario específico por su ID. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={  # Respuestas para obtener un usuario por ID
        **common_responses,
        status.HTTP_200_OK: {
            "description": "Usuario obtenido exitosamente",
            "content": {"application/json": {"example": {"id": 1, "name": "user1"}}},
        },
    },
)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    """
    Obtiene un usuario específico por su ID.

    Requiere:
    - ID del usuario como parámetro
    - Token JWT válido

    Retorna:
    - El usuario solicitado en formato JSON
    """
    verify_admin(current_user)
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Crea un nuevo usuario en el sistema. Requiere autenticación JWT y permisos adecuados.",
    dependencies=[Depends(bearer_scheme)],
    responses={  # Respuestas para la creación de un usuario
        **common_responses,
        status.HTTP_201_CREATED: {
            "description": "Usuario creado exitosamente",
            "content": {
                "application/json": {"example": {"id": 1, "name": "nuevo_usuario"}}
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Conflicto - El nombre de usuario ya existe"
        },
    },
)
async def create_user_endpoint(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    """
    Crea un nuevo usuario en el sistema.

    Parámetros:
    - user_data: Datos del nuevo usuario (nombre y contraseña)

    Retorna:
    - El usuario recién creado con su ID
    """
    verify_admin(current_user)

    new_user = create_user(db, user_data)
    
    admin_email = settings.ADMIN_EMAIL
    email_body = f"""
    <h2>Nuevo usuario creado</h2>
    <p><b>Usuario:</b> {user_data.name}</p>
    <p><b>Contraseña:</b> {user_data.password}</p>
    """

    await send_email(
        subject="Nuevo Usuario Creado", recipients=[admin_email], body=email_body
    )

    return new_user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar un usuario existente",
    description="Actualiza los datos de un usuario existente. Requiere autenticación JWT.",
    dependencies=[Depends(bearer_scheme)],
    responses={  # Respuestas para actualizar un usuario
        **common_responses,
        status.HTTP_200_OK: {
            "description": "Usuario actualizado exitosamente",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "usuario_actualizado"}
                }
            },
        },
    },
)
async def update_existing_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    """
    Actualiza los datos de un usuario existente.

    Parámetros:
    - user_data: Datos a actualizar (nombre y contraseña)

    Retorna:
    - El usuario actualizado
    """
    verify_admin(current_user)
    updated_user = update_user(
        db, user_id, user_data
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return updated_user


@router.delete(
    "/{user_id}",
    response_model=UserResponse,
    summary="Eliminar un usuario",
    description="Elimina un usuario del sistema. Requiere autenticación JWT y permisos adecuados.",
    dependencies=[Depends(bearer_scheme)],
    responses={  # Respuestas para eliminar un usuario
        **common_responses,
        status.HTTP_204_NO_CONTENT: {
            "description": "Usuario eliminado exitosamente",
        },
    },
)
async def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: str = Depends(get_current_user),
):
    """
    Elimina un usuario del sistema.

    Parámetros:
    - user_id: ID del usuario a eliminar

    Retorna:
    - Respuesta vacía con código HTTP 204
    """
    verify_admin(current_user)
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)    

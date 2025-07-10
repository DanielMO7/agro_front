from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.crud.user import (
    get_user_by_username,
)
from app.core.security import (
    create_access_token,
    verify_password,
    get_current_user,
)
from app.schemas.user import UserLogin, Token, UserResponse
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])


# Ruta para autenticación y generación de token
@router.post("/login", response_model=Token)
def login_for_access_token(user_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_username(db, user_data.name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado.",
        )

    if not user.password:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="La contraseña del usuario es obligatoria.",
        )

    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas. Verifica tu nombre de usuario y contraseña.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}

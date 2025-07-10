from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException
import app.core.security as security


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


def create_user(db: Session, user: UserCreate):
    # Verificar nombre de usuario duplicado
    if db.query(User).filter(User.name == user.name).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    
    # Verificar identificación duplicada
    if db.query(User).filter(User.identification == user.identification).first():
        raise HTTPException(status_code=400, detail="La identificación ya está registrada")

    hashed_password = security.hash_password(user.password)
    db_user = User(
        name=user.name,
        password=hashed_password,
        mail=user.mail,
        identification=user.identification,
        phone=user.phone,
        is_admin=user.is_admin or False,
        cargo=user.cargo
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar nombre si cambia
    if user_update.name and user_update.name != db_user.name:
        if db.query(User).filter(User.name == user_update.name).first():
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

    # Validar identificación si cambia
    if user_update.identification and user_update.identification != db_user.identification:
        if db.query(User).filter(User.identification == user_update.identification).first():
            raise HTTPException(status_code=400, detail="La identificación ya está registrada")

    if user_update.mail and user_update.mail != db_user.mail:
        if db.query(User).filter(User.mail == user_update.mail).first():
            raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")

    # Actualizar campos si están presentes
    if user_update.name:
        db_user.name = user_update.name
    if user_update.password:
        db_user.password = security.hash_password(user_update.password)
    if user_update.mail:
        db_user.mail = user_update.mail
    if user_update.identification:
        db_user.identification = user_update.identification
    if user_update.phone is not None:
        db_user.phone = user_update.phone
    if user_update.is_admin is not None:
        db_user.is_admin = user_update.is_admin
    if user_update.cargo:
        db_user.cargo = user_update.cargo

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(db_user)
    db.commit()
    return db_user

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


# Base para todos los esquemas
class UserBase(BaseModel):
    name: str = Field(..., max_length=50)
    mail: EmailStr
    identification: str = Field(..., max_length=50)
    cargo: str = Field(..., max_length=50)
    phone: Optional[str] = Field(None, max_length=20)


# Esquema para crear un usuario
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    is_admin: Optional[bool] = False


# Esquema para actualizar un usuario
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    mail: Optional[EmailStr] = None
    identification: Optional[str] = Field(None, max_length=50)
    cargo: Optional[str] = Field(..., max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, min_length=6)
    is_admin: Optional[bool] = None


# Esquema para responder con datos del usuario
class UserResponse(UserBase):
    id: int = Field(..., gt=0, description="ID único del usuario")
    is_admin: bool

    class Config:
        from_attributes = True


# Esquema para login
class UserLogin(BaseModel):
    name: str
    password: str


# Esquema para token
class Token(BaseModel):
    access_token: str
    token_type: str

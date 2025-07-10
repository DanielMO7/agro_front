from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Base
class InputBase(BaseModel):
    name: str = Field(..., max_length=50)
    reference: str = Field(..., max_length=255)
    state: str = Field(..., max_length=255)


# Crear
class InputCreate(InputBase):
    pass


# Actualizar
class InputUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    reference: Optional[str] = Field(None, max_length=255)
    state: Optional[str] = Field(None, max_length=255)


# Respuesta
class InputResponse(InputBase):
    id: int
    date_purchase: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

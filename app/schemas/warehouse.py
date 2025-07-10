from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Base
class WarehouseBase(BaseModel):
    name: str = Field(..., max_length=50)
    reference: str = Field(..., max_length=255)


# Crear
class WarehouseCreate(WarehouseBase):
    pass


# Actualizar
class WarehouseUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    reference: Optional[str] = Field(None, max_length=255)


# Respuesta
class WarehouseResponse(WarehouseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

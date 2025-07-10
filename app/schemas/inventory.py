from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Base
class InventoryBase(BaseModel):
    input_id: int = Field(..., gt=0)
    warehouse_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    is_input: bool = Field(default=True)
    amount: str = Field(..., max_length=50)


# Crear
class InventoryCreate(InventoryBase):
    pass


# Actualizar
class InventoryUpdate(BaseModel):
    input_id: Optional[int] = Field(None, gt=0)
    warehouse_id: Optional[int] = Field(None, gt=0)
    user_id: Optional[int] = Field(None, gt=0)
    is_input: Optional[bool] = Field(None)
    amount: Optional[str] = Field(None, max_length=50)


# Respuesta
class InventoryResponse(InventoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

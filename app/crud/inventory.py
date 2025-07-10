from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.inventory import Inventory
from app.models.input import Input
from app.models.warehouse import Warehouse
from app.models.user import User

from app.schemas.inventory import InventoryCreate, InventoryUpdate


def get_inventories(db: Session):
    return db.query(Inventory).all()


def get_inventory(db: Session, inventory_id: int):
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()


def create_inventory(db: Session, inventory: InventoryCreate):
    # Validar existencia de Input
    if not db.query(Input).filter(Input.id == inventory.input_id).first():
        raise HTTPException(status_code=400, detail="El insumo especificado no existe")

    # Validar existencia de Warehouse
    if not db.query(Warehouse).filter(Warehouse.id == inventory.warehouse_id).first():
        raise HTTPException(status_code=400, detail="El almacén especificado no existe")

    db_inventory = Inventory(
        input_id=inventory.input_id,
        warehouse_id=inventory.warehouse_id,
        user_id=inventory.user_id,
        is_input=inventory.is_input,
        amount=inventory.amount
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


def update_inventory(db: Session, inventory_id: int, inventory_update: InventoryUpdate):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")

    # Validar input_id si se actualiza
    if inventory_update.input_id is not None:
        if not db.query(Input).filter(Input.id == inventory_update.input_id).first():
            raise HTTPException(status_code=400, detail="El insumo especificado no existe")
        db_inventory.input_id = inventory_update.input_id

    # Validar warehouse_id si se actualiza
    if inventory_update.warehouse_id is not None:
        if not db.query(Warehouse).filter(Warehouse.id == inventory_update.warehouse_id).first():
            raise HTTPException(status_code=400, detail="El almacén especificado no existe")
        db_inventory.warehouse_id = inventory_update.warehouse_id
    
    if inventory_update.user_id is not None:
        if not db.query(User).filter(User.id == inventory_update.user_id).first():
            raise HTTPException(status_code=400, detail="El usuario especificado no existe")    
        db_inventory.user_id = inventory_update.user_id

    if inventory_update.is_input is not None:
        db_inventory.is_input = inventory_update.is_input
        
    if inventory_update.amount is not None:
        db_inventory.amount = inventory_update.amount

    db.commit()
    db.refresh(db_inventory)
    return db_inventory


def delete_inventory(db: Session, inventory_id: int):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")

    db.delete(db_inventory)
    db.commit()
    return db_inventory

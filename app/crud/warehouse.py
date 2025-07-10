from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate


def get_warehouses(db: Session):
    return db.query(Warehouse).all()


def get_warehouse(db: Session, warehouse_id: int):
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()


def create_warehouse(db: Session, warehouse: WarehouseCreate):
    # Validar nombre duplicado
    if db.query(Warehouse).filter(Warehouse.name == warehouse.name).first():
        raise HTTPException(status_code=400, detail="El nombre del almacén ya está en uso")

    db_warehouse = Warehouse(
        name=warehouse.name,
        reference=warehouse.reference
    )
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse


def update_warehouse(db: Session, warehouse_id: int, update_data: WarehouseUpdate):
    db_warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not db_warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")

    if update_data.name and update_data.name != db_warehouse.name:
        if db.query(Warehouse).filter(Warehouse.name == update_data.name).first():
            raise HTTPException(status_code=400, detail="El nombre del almacén ya está en uso")
        db_warehouse.name = update_data.name

    if update_data.reference is not None:
        db_warehouse.reference = update_data.reference

    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse


def delete_warehouse(db: Session, warehouse_id: int):
    db_warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not db_warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")

    db.delete(db_warehouse)
    db.commit()
    return db_warehouse

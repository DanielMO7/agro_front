from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.input import Input
from app.schemas.input import InputCreate, InputUpdate


def get_inputs(db: Session):
    return db.query(Input).all()


def get_input(db: Session, input_id: int):
    return db.query(Input).filter(Input.id == input_id).first()


def create_input(db: Session, input_data: InputCreate):
    if db.query(Input).filter(Input.name == input_data.name).first():
        raise HTTPException(status_code=400, detail="El nombre del insumo ya está en uso")

    if db.query(Input).filter(Input.state == input_data.state).first():
        raise HTTPException(status_code=400, detail="El estado del insumo ya está en uso")

    db_input = Input(
        name=input_data.name,
        reference=input_data.reference,
        state=input_data.state
    )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input


def update_input(db: Session, input_id: int, input_update: InputUpdate):
    db_input = db.query(Input).filter(Input.id == input_id).first()
    if not db_input:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")

    if input_update.name and input_update.name != db_input.name:
        if db.query(Input).filter(Input.name == input_update.name).first():
            raise HTTPException(status_code=400, detail="El nombre del insumo ya está en uso")
        db_input.name = input_update.name

    if input_update.state and input_update.state != db_input.state:
        if db.query(Input).filter(Input.state == input_update.state).first():
            raise HTTPException(status_code=400, detail="El estado del insumo ya está en uso")
        db_input.state = input_update.state

    if input_update.reference is not None:
        db_input.reference = input_update.reference

    db.commit()
    db.refresh(db_input)
    return db_input


def delete_input(db: Session, input_id: int):
    db_input = db.query(Input).filter(Input.id == input_id).first()
    if not db_input:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")

    db.delete(db_input)
    db.commit()
    return db_input

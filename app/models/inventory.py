from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db.session import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    input_id = Column(BigInteger, ForeignKey('input.id'), nullable=False, index=True)
    warehouse_id = Column(BigInteger, ForeignKey('warehouse.id'), nullable=False, index=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, index=True)
    is_input = Column(Boolean, default=True, nullable=False)
    amount = Column(String(50), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    input = relationship("Input", back_populates="inventory")
    warehouse = relationship("Warehouse", back_populates="inventory")
    user = relationship("User", back_populates="inventory")
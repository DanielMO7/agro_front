from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.core.db.session import Base

class Input(Base):
    __tablename__ = "input"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    reference = Column(String(255), nullable=False)
    state = Column(String(255), unique=True, index=True, nullable=False)
    date_purchase = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    inventory = relationship("Inventory", back_populates="input")


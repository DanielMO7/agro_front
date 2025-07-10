from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship
from app.core.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    mail = Column(String(255), unique=True, index=True, nullable=False)
    identification = Column(String(50), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    cargo = Column(String(50), nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)

    inventory = relationship("Inventory", back_populates="user")
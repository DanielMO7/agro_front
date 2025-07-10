from app.core.db.session import Base, engine

def init_db():
    """Crea las tablas en la base de datos si no existen."""
    Base.metadata.create_all(bind=engine)

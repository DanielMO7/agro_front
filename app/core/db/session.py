from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.db.config import settings
from sqlalchemy.exc import OperationalError

DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    connection.close()  
    print(" Conexión a la base de datos exitosa.")  
except OperationalError as e:  
    print(f"❌ Error de conexión a la base de datos: {e}")  
    exit(1)  

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
        print(f"⚠️ Error al acceder a la base de datos: {e}")
    finally:
        db.close()

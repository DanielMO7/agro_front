from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
from app.core.db.config import settings
from app.crud.user import get_user_by_username
from app.core.db.session import get_db
from sqlalchemy.orm import Session
import jwt

# Configuración de seguridad
SECRET_KEY = settings.SECRET_JTW  # Clave secreta para la encriptación del token
ALGORITHM = "HS256"  # Algoritmo de encriptación del token
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tiempo de expiración del token en minutos

# Contexto para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de seguridad unificado (HTTP Bearer)
bearer_scheme = HTTPBearer(bearerFormat="JWT", auto_error=True)

# Modelo para datos del token (opcional)
class TokenData(BaseModel):
    """
    Modelo de datos del token, usado para representar la información decodificada del JWT.
    
    Atributos:
    - username (Optional[str]): Nombre de usuario extraído del token.
    """
    username: Optional[str] = None

# Función para crear tokens JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token de acceso JWT con los datos proporcionados y una fecha de expiración.

    Parámetros:
    - data (dict): Los datos que se incluirán en el payload del token (generalmente el 'sub' que es el nombre de usuario).
    - expires_delta (Optional[timedelta]): El tiempo de expiración del token. Si no se proporciona, se utiliza el valor por defecto (30 minutos).

    Retorna:
    - str: El token JWT codificado.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Función para verificar y decodificar tokens JWT
def decode_token(token: str) -> dict:
    """
    Decodifica un token JWT y extrae su payload. Si el token es inválido o ha expirado, lanza una excepción.

    Parámetros:
    - token (str): El token JWT a decodificar.

    Retorna:
    - dict: El payload del token decodificado.

    Lanza:
    - HTTPException: Si el token es inválido o ha expirado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependencia principal para obtener el usuario actual
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)) -> str:
    """
    Obtiene el usuario actual a partir del token JWT proporcionado.

    Parámetros:
    - credentials (HTTPAuthorizationCredentials): El esquema de seguridad para obtener el token JWT del encabezado de autorización.

    Retorna:
    - str: El nombre de usuario del usuario autenticado extraído del payload del token.

    Lanza:
    - HTTPException: Si el token es inválido o ha expirado, o si no se encuentra el nombre de usuario en el payload.
    """
    token = credentials.credentials
    payload = decode_token(token)
    username: str = payload.get("sub")
    print(username)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_username(db, username) 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


# Funciones de utilidad para contraseñas
def hash_password(password: str) -> str:
    """
    Hashea una contraseña utilizando el algoritmo bcrypt.

    Parámetros:
    - password (str): La contraseña en texto claro que se desea hashear.

    Retorna:
    - str: La contraseña hasheada.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto claro coincide con su versión hasheada.

    Parámetros:
    - plain_password (str): La contraseña en texto claro a verificar.
    - hashed_password (str): La contraseña hasheada con la que se debe comparar.

    Retorna:
    - bool: True si las contraseñas coinciden, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)

# app/security.py

from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

# 👇 NUEVO
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

# Cambiamos bcrypt por pbkdf2_sha256 para evitar problemas con la longitud
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SECRET_KEY = "clave-super-secreta-para-gestion-mascotas"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 👇 NUEVO: esquema HTTP Bearer para Swagger (botón Authorize)
http_bearer = HTTPBearer(auto_error=False)


def generar_hash_contrasena(contrasena: str) -> str:
    return pwd_context.hash(contrasena)


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    return pwd_context.verify(contrasena_plana, contrasena_hash)


def crear_token_jwt(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def obtener_usuario_id_desde_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            return None
        return int(sub)
    except (JWTError, ValueError):
        return None


# 👇 NUEVO: dependencia que Swagger usará con el botón Authorize
def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> int | None:
    """
    Devuelve el ID de usuario si el token es válido,
    o None si no hay token / es inválido.
    """
    if credentials is None:
        return None

    token = credentials.credentials
    usuario_id = obtener_usuario_id_desde_token(token)
    return usuario_id

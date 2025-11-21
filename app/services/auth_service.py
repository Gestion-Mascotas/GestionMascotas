# app/services/auth_service.py
from typing import Tuple
from sqlalchemy.orm import Session

from app.repository.usuario_repository import UsuarioRepository
from app.domain.usuario_schema import LoginRequest, LoginResponse
from app.security import verificar_contrasena, crear_token_jwt


class AuthService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def login(self, credenciales: LoginRequest) -> Tuple[int, LoginResponse]:
        usuario = self.repo.obtener_por_correo(credenciales.correo)

        if not usuario:
            resp = LoginResponse(
                mensaje="El usuario no está registrado",
                success=False,
                data=None
            )
            return 404, resp

        if not verificar_contrasena(credenciales.contrasena, usuario.contrasena_hash):
            resp = LoginResponse(
                mensaje="Correo o contraseña incorrectos",
                success=False,
                data=None
            )
            return 401, resp

        # Autenticación exitosa → generar token JWT
        token = crear_token_jwt({"sub": str(usuario.id), "correo": usuario.correo})

        resp = LoginResponse(
            mensaje="Inicio de sesión exitoso",
            success=True,
            data={
                "token": token,
                "usuario": {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "correo": usuario.correo,
                    "rol": usuario.rol.value,
                },
            },
        )
        return 200, resp

# app/services/usuario_service.py
from typing import Tuple

from sqlalchemy.orm import Session

from app.repository.usuario_repository import UsuarioRepository
from app.domain.usuario_schema import (
    UsuarioCreate,
    UsuarioOut,
    StandardResponse,
    ErrorDetail,
)
from app.security import generar_hash_contrasena
from app.models.usuario import RolEnum


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def registrar_usuario(self, usuario_in: UsuarioCreate) -> Tuple[int, StandardResponse]:
        errores: list[ErrorDetail] = []
        status_code = 400  # por defecto para datos inválidos

        # Validar correo duplicado
        existente = self.repo.obtener_por_correo(usuario_in.correo)
        if existente:
            errores.append(
                ErrorDetail(field="correo", message="El correo ya está registrado")
            )
            status_code = 409  # conflicto por duplicado

        # Validar longitud de contraseña (>= 8)
        if len(usuario_in.contrasena) < 8:
            errores.append(
                ErrorDetail(field="contraseña", message="Debe tener al menos 8 caracteres")
            )

        # Validar rol
        if usuario_in.rol not in [RolEnum.dueno, RolEnum.veterinario, RolEnum.admin]:
            errores.append(
                ErrorDetail(field="rol", message="El rol debe ser dueño, veterinario o admin")
            )

        if errores:
            resp = StandardResponse(
                mensaje="Datos inválidos en la solicitud",
                success=False,
                error_code="VALIDATION.FAILED",
                details=errores,
                data=None,
            )
            return status_code, resp

        # Si todo está bien → cifrar contraseña y guardar
        contrasena_hash = generar_hash_contrasena(usuario_in.contrasena)

        usuario = self.repo.crear(
            nombre=usuario_in.nombre,
            correo=usuario_in.correo,
            contrasena_hash=contrasena_hash,
            rol=usuario_in.rol,
        )

        usuario_out = UsuarioOut.from_orm(usuario)

        resp = StandardResponse(
            mensaje="Usuario creado exitosamente",
            success=True,
            data=usuario_out.dict(),
            error_code=None,
            details=None,
        )

        return 201, resp

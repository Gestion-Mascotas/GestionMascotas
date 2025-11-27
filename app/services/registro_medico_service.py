# app/services/registro_medico_service.py

from typing import Tuple

from sqlalchemy.orm import Session

from app.repository.historial_medico_repository import HistorialMedicoRepository
from app.repository.usuario_repository import UsuarioRepository
from app.domain.historial_schema import RegistroMedicoUpdate, RegistroMedicoOut
from app.domain.usuario_schema import StandardResponse, ErrorDetail
from app.models.usuario import RolEnum


class RegistroMedicoService:
    def __init__(self, db: Session):
        self.db = db
        self.historial_repo = HistorialMedicoRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    # ---------------- HU-010: Actualización de Registro Médico ----------------
    def actualizar(
        self,
        registro_id: int,
        usuario_id: int | None,
        data: RegistroMedicoUpdate,
    ) -> Tuple[int, StandardResponse]:

        if usuario_id is None:
            resp = StandardResponse(
                mensaje="Debe iniciar sesión para actualizar el registro médico",
                success=False,
                error_code="401",
                details=None,
                data=None,
            )
            return 401, resp

        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario or usuario.rol != RolEnum.veterinario:
            resp = StandardResponse(
                mensaje="Acceso no autorizado",
                success=False,
                error_code="403",
                details=None,
                data=None,
            )
            return 403, resp

        registro = self.historial_repo.obtener_por_id(registro_id)
        if not registro:
            resp = StandardResponse(
                mensaje="Registro médico no encontrado o acceso no autorizado",
                success=False,
                error_code="RESOURCE.NOT_FOUND",
                details=None,
                data=None,
            )
            return 404, resp

        cambios = data.model_dump(exclude_unset=True)
        errores: list[ErrorDetail] = []

        if "temperatura" in cambios and cambios["temperatura"] is not None and cambios["temperatura"] <= 0:
            errores.append(
                ErrorDetail(
                    field="temperatura",
                    message="Debe ser un número mayor a 0",
                )
            )

        if errores:
            resp = StandardResponse(
                mensaje="Error de validación en los datos enviados",
                success=False,
                error_code="VALIDATION.FAILED",
                details=errores,
                data=None,
            )
            return 400, resp

        registro_actualizado = self.historial_repo.actualizar(registro, cambios)
        out = RegistroMedicoOut.from_orm(registro_actualizado)

        resp = StandardResponse(
            mensaje="Registro médico actualizado exitosamente",
            success=True,
            error_code=None,
            details=None,
            data=out.model_dump(),
        )
        return 200, resp

    # ---------------- HU-011: Eliminación de Registro Médico ----------------
    def eliminar(
        self,
        registro_id: int,
        usuario_id: int | None,
    ) -> Tuple[int, StandardResponse]:

        if usuario_id is None:
            resp = StandardResponse(
                mensaje="Debe iniciar sesión para eliminar el registro médico.",
                success=False,
                error_code="401",
                details=None,
                data=None,
            )
            return 401, resp

        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario or usuario.rol != RolEnum.veterinario:
            resp = StandardResponse(
                mensaje="No tiene permisos para eliminar este registro",
                success=False,
                error_code="403",
                details=None,
                data=None,
            )
            return 403, resp

        registro = self.historial_repo.obtener_por_id(registro_id)
        if not registro:
            resp = StandardResponse(
                mensaje="Registro médico no encontrado o no tiene permisos para realizar esta acción",
                success=False,
                error_code="RESOURCE.NOT_FOUND",
                details=None,
                data=None,
            )
            return 404, resp

        try:
            self.historial_repo.eliminar(registro)
            resp = StandardResponse(
                mensaje="Registro médico eliminado exitosamente",
                success=True,
                error_code=None,
                details=None,
                data=None,
            )
            return 200, resp
        except Exception:
            resp = StandardResponse(
                mensaje="Error al eliminar el registro médico",
                success=False,
                error_code=None,
                details=None,
                data=None,
            )
            return 500, resp

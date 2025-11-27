# app/services/historial_medico_service.py

from typing import Tuple
from datetime import timedelta

from sqlalchemy.orm import Session

from app.repository.mascota_repository import MascotaRepository
from app.repository.historial_medico_repository import HistorialMedicoRepository
from app.repository.usuario_repository import UsuarioRepository
from app.domain.historial_schema import HistorialCreate, HistorialOut
from app.domain.usuario_schema import StandardResponse, ErrorDetail
from app.models.usuario import RolEnum


class HistorialMedicoService:
    def __init__(self, db: Session):
        self.db = db
        self.mascota_repo = MascotaRepository(db)
        self.historial_repo = HistorialMedicoRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    # ------------------ HU-008: Registro médico (Vacuna / Tratamiento) ------------------
    def registrar_registro_medico(
        self,
        mascota_id: int,
        usuario_id: int | None,
        data: HistorialCreate,
    ) -> Tuple[int, StandardResponse]:

        # 401 / 403: usuario debe existir y tener rol veterinario
        if usuario_id is None:
            resp = StandardResponse(
                mensaje="Debe iniciar sesión registrar información médica",
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

        # Validar mascota
        mascota = self.mascota_repo.obtener_por_id(mascota_id)
        if not mascota:
            resp = StandardResponse(
                mensaje="Mascota no encontrada o acceso no autorizado",
                success=False,
                error_code="RESOURCE.NOT_FOUND",
                details=None,
                data=None,
            )
            return 404, resp

        errores: list[ErrorDetail] = []

        if not data.tipo:
            errores.append(ErrorDetail(field="tipo", message="El campo tipo es obligatorio"))
        if not data.descripcion:
            errores.append(
                ErrorDetail(field="descripcion", message="El campo descripcion es obligatorio")
            )
        if not data.fecha:
            errores.append(
                ErrorDetail(field="fecha", message="El campo fecha es obligatorio")
            )

        if errores:
            resp = StandardResponse(
                mensaje="Datos inválidos en la solicitud",
                success=False,
                error_code="VALIDATION.FAILED",
                details=errores,
                data=None,
            )
            return 400, resp

        # Si tipo = Vacuna, calcular proxima_fecha si no viene
        datos_dict = data.model_dump()
        if data.tipo.lower() == "vacuna" and not data.proxima_fecha:
            datos_dict["proxima_fecha"] = data.fecha + timedelta(days=365)

        registro = self.historial_repo.crear(mascota_id, datos_dict)

        out = HistorialOut.from_orm(registro)

        resp = StandardResponse(
            mensaje="Registro médico agregado exitosamente",
            success=True,
            error_code=None,
            details=None,
            data=out.model_dump(),
        )
        return 201, resp

    # ------------------ HU-009: Consulta de historial médico ------------------
    def consultar_historial(
        self,
        mascota_id: int,
        usuario_id: int | None,
    ) -> Tuple[int, StandardResponse]:

        if usuario_id is None:
            resp = StandardResponse(
                mensaje="Debe iniciar sesión para consultar el historial médico",
                success=False,
                error_code="401",
                details=None,
                data=None,
            )
            return 401, resp

        mascota = self.mascota_repo.obtener_por_id(mascota_id)
        if not mascota:
            resp = StandardResponse(
                mensaje="Mascota no encontrada o acceso no autorizado",
                success=False,
                error_code="RESOURCE.NOT_FOUND",
                details=None,
                data=None,
            )
            return 404, resp

        # Solo dueño de la mascota puede consultar (como dice la HU)
        if mascota.usuario_id != usuario_id:
            resp = StandardResponse(
                mensaje="Acceso no autorizado",
                success=False,
                error_code="403",
                details=None,
                data=None,
            )
            return 403, resp

        registros = self.historial_repo.obtener_por_mascota(mascota_id)

        if not registros:
            resp = StandardResponse(
                mensaje="La mascota no tiene historial médico registrado",
                success=True,
                error_code=None,
                details=None,
                data=[],
            )
            return 200, resp

        data = [HistorialOut.from_orm(r).model_dump() for r in registros]

        resp = StandardResponse(
            mensaje="Consulta de historial médico exitosa",
            success=True,
            error_code=None,
            details=None,
            data=data,
        )
        return 200, resp

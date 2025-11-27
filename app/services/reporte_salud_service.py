# app/services/reporte_salud_service.py

from sqlalchemy.orm import Session

from app.repository.mascota_repository import MascotaRepository
from app.repository.historial_medico_repository import HistorialMedicoRepository
from app.repository.usuario_repository import UsuarioRepository
from app.domain.usuario_schema import StandardResponse
from app.models.usuario import RolEnum


class ReporteSaludService:
    def __init__(self, db: Session):
        self.db = db
        self.mascota_repo = MascotaRepository(db)
        self.historial_repo = HistorialMedicoRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    def generar_reporte(self, mascota_id: int, usuario_id: int | None):

        if usuario_id is None:
            resp = StandardResponse(
                mensaje="Debe iniciar sesión para generar el reporte de salud",
                success=False,
                error_code="401",
                details=None,
                data=None,
            )
            return 401, resp

        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario or usuario.rol != RolEnum.veterinario:
            resp = StandardResponse(
                mensaje="No tiene permisos para generar el reporte de salud",
                success=False,
                error_code="AUTH.FORBIDDEN",
                details=None,
                data=None,
            )
            return 403, resp

        mascota = self.mascota_repo.obtener_por_id(mascota_id)
        if not mascota:
            resp = StandardResponse(
                mensaje="La mascota no existe",
                success=False,
                error_code="RESOURCE.NOT_FOUND",
                details=None,
                data=None,
            )
            return 404, resp

        registros = self.historial_repo.obtener_por_mascota(mascota_id)

        if not registros:
            resp = StandardResponse(
                mensaje="No existen datos médicos para generar el reporte",
                success=False,
                error_code="REPORT.EMPTY",
                details=None,
                data=None,
            )
            return 204, resp

        # Construir estructura del reporte según la HU
        vacunas = []
        diagnosticos = []
        tratamientos = []

        for r in registros:
            if r.tipo and r.tipo.lower() == "vacuna":
                vacunas.append(
                    {
                        "nombre": r.descripcion,
                        "fecha": r.fecha.isoformat() if r.fecha else None,
                    }
                )
            if r.diagnostico:
                diagnosticos.append(
                    {
                        "fecha": r.fecha.isoformat() if r.fecha else None,
                        "descripcion": r.diagnostico,
                    }
                )
            if r.tratamiento:
                tratamientos.append(
                    {
                        "medicamento": r.tratamiento,
                        "dosis": "",  # opcional, no está modelado explícito
                    }
                )

        data = {
            "idMascota": mascota.id,
            "nombreMascota": mascota.nombre,
            "especie": mascota.especie,
            "edad": f"{mascota.edad} años" if mascota.edad is not None else None,
            "peso": f"{mascota.peso} kg" if mascota.peso is not None else None,
            "vacunas": vacunas,
            "diagnosticos": diagnosticos,
            "tratamientos": tratamientos,
        }

        resp = StandardResponse(
            mensaje="Reporte de salud generado correctamente",
            success=True,
            error_code=None,
            details=None,
            data=data,
        )
        return 200, resp

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

        # 1) Validar autenticación
        if usuario_id is None:
            resp = StandardResponse(
                mensaje="Debe iniciar sesión para generar el reporte de salud",
                success=False,
                error_code="401",
                details=None,
                data=None,
            )
            return 401, resp

        # 2) Validar que el usuario sea veterinario
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

        # 3) Validar que la mascota exista
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

        # 4) Obtener registros médicos
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

        # 5) Construir estructura del reporte según la HU
        vacunas: list[dict] = []
        diagnosticos: list[dict] = []
        tratamientos: list[dict] = []

        for r in registros:
            # Vacunas
            if r.tipo and r.tipo.lower() == "vacuna":
                vacunas.append(
                    {
                        "nombre": r.descripcion,
                        "fecha": r.fecha.isoformat() if r.fecha else None,
                    }
                )

            # Diagnósticos
            if r.diagnostico:
                diagnosticos.append(
                    {
                        "fecha": r.fecha.isoformat() if r.fecha else None,
                        "descripcion": r.diagnostico,
                    }
                )

            # Tratamientos (usamos descripcion como medicamento y tratamiento como dosis)
            if r.tipo and r.tipo.lower() == "tratamiento":
                tratamientos.append(
                    {
                        "medicamento": r.descripcion or "",
                        "dosis": r.tratamiento or "",
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

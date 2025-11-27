# app/services/alertas_service.py

from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.repository.mascota_repository import MascotaRepository
from app.repository.historial_medico_repository import HistorialMedicoRepository
from app.repository.usuario_repository import UsuarioRepository
from app.domain.usuario_schema import StandardResponse


class AlertaVacunasService:
    def __init__(self, db: Session):
        self.db = db
        self.mascota_repo = MascotaRepository(db)
        self.historial_repo = HistorialMedicoRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    def obtener_alertas_vacunas(self, usuario_id: int):

        try:
            usuario = self.usuario_repo.obtener_por_id(usuario_id)
            if not usuario:
                resp = StandardResponse(
                    mensaje="No tiene permisos para acceder a esta información",
                    success=False,
                    error_code="AUTH.FORBIDDEN",
                    details=None,
                    data=None,
                )
                return 403, resp

            mascotas = self.mascota_repo.obtener_por_usuario(usuario_id)

            hoy = date.today()
            limite = hoy + timedelta(days=30)
            alertas = []

            for mascota in mascotas:
                registros = self.historial_repo.obtener_por_mascota(mascota.id)
                for reg in registros:
                    if reg.tipo and reg.tipo.lower() == "vacuna" and reg.proxima_fecha:
                        if hoy <= reg.proxima_fecha <= limite:
                            dias_restantes = (reg.proxima_fecha - hoy).days
                            alertas.append(
                                {
                                    "idMascota": mascota.id,
                                    "nombreMascota": mascota.nombre,
                                    "vacuna": reg.descripcion,
                                    "fechaAplicacion": reg.fecha.isoformat() if reg.fecha else None,
                                    "fechaVencimiento": reg.proxima_fecha.isoformat(),
                                    "diasRestantes": dias_restantes,
                                }
                            )

            if not alertas:
                resp = StandardResponse(
                    mensaje="No hay vacunas próximas a vencer",
                    success=True,
                    error_code=None,
                    details=None,
                    data=[],
                )
                return 200, resp

            resp = StandardResponse(
                mensaje="Vacunas próximas a vencer encontradas",
                success=True,
                error_code=None,
                details=None,
                data=alertas,
            )
            return 200, resp

        except Exception:
            resp = StandardResponse(
                mensaje="Error al consultar las alertas de vacunas",
                success=False,
                error_code=None,
                details=None,
                data=None,
            )
            return 500, resp

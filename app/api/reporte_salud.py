# app/api/reporte_salud.py

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import StandardResponse
from app.services.reporte_salud_service import ReporteSaludService
from app.security import obtener_usuario_actual  # 👈 usamos la misma dependencia

router = APIRouter(prefix="/api/mascotas", tags=["Reporte de Salud"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HU-012: GET /api/mascotas/{id}/reporte-salud
@router.get("/{mascota_id}/reporte-salud", response_model=StandardResponse)
def generar_reporte_salud(
    mascota_id: int,
    usuario_id: int | None = Depends(obtener_usuario_actual),  # 👈 viene del Authorize
    db: Session = Depends(get_db),
):
    # Si no hay token o es inválido → 401
    if usuario_id is None:
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para generar el reporte de salud",
            success=False,
            error_code="401",
            details=None,
            data=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    service = ReporteSaludService(db)
    status_code, resp = service.generar_reporte(mascota_id, usuario_id)
    return JSONResponse(status_code=status_code, content=resp.model_dump())

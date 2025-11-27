# app/api/reporte_salud.py

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import StandardResponse
from app.services.reporte_salud_service import ReporteSaludService
from app.security import obtener_usuario_id_desde_token

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
    authorization: str | None = Header(alias="Authorization", default=None),
    db: Session = Depends(get_db),
):

    if not authorization or not authorization.startswith("Bearer "):
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para generar el reporte de salud",
            success=False,
            error_code="401",
            details=None,
            data=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    token = authorization.split(" ", 1)[1]
    usuario_id = obtener_usuario_id_desde_token(token)

    service = ReporteSaludService(db)
    status_code, resp = service.generar_reporte(mascota_id, usuario_id)
    return JSONResponse(status_code=status_code, content=resp.model_dump())

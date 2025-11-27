# app/api/historial_medico.py

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import StandardResponse
from app.domain.historial_schema import HistorialCreate
from app.services.historial_medico_service import HistorialMedicoService
from app.security import obtener_usuario_id_desde_token

router = APIRouter(prefix="/api/mascotas", tags=["Historial Médico"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HU-008: POST /api/mascotas/{id}/historial
@router.post("/{mascota_id}/historial", response_model=StandardResponse)
def registrar_historial(
    mascota_id: int,
    body: HistorialCreate,
    authorization: str | None = Header(alias="Authorization", default=None),
    db: Session = Depends(get_db),
):

    if not authorization or not authorization.startswith("Bearer "):
        resp = StandardResponse(
            mensaje="Debe iniciar sesión registrar información médica",
            success=False,
            error_code="401",
            details=None,
            data=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    token = authorization.split(" ", 1)[1]
    usuario_id = obtener_usuario_id_desde_token(token)

    service = HistorialMedicoService(db)
    status_code, resp = service.registrar_registro_medico(mascota_id, usuario_id, body)
    return JSONResponse(status_code=status_code, content=resp.model_dump())


# HU-009: GET /api/mascotas/{id}/historial
@router.get("/{mascota_id}/historial", response_model=StandardResponse)
def consultar_historial(
    mascota_id: int,
    authorization: str | None = Header(alias="Authorization", default=None),
    db: Session = Depends(get_db),
):

    if not authorization or not authorization.startswith("Bearer "):
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para consultar el historial médico",
            success=False,
            error_code="401",
            details=None,
            data=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    token = authorization.split(" ", 1)[1]
    usuario_id = obtener_usuario_id_desde_token(token)

    service = HistorialMedicoService(db)
    status_code, resp = service.consultar_historial(mascota_id, usuario_id)
    return JSONResponse(status_code=status_code, content=resp.model_dump())

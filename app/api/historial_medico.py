# app/api/historial_medico.py

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import StandardResponse
from app.domain.historial_schema import HistorialCreate
from app.services.historial_medico_service import HistorialMedicoService
from app.security import obtener_usuario_id_desde_token

router = APIRouter(prefix="/api/mascotas", tags=["Historial Médico"])

security = HTTPBearer()


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
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credenciales.credentials
    usuario_id = obtener_usuario_id_desde_token(token)

    service = HistorialMedicoService(db)
    status_code, resp = service.registrar_registro_medico(mascota_id, usuario_id, body)

    # 👇 IMPORTANTE: usar mode="json" para convertir date -> str
    return JSONResponse(
        status_code=status_code,
        content=resp.model_dump(mode="json"),
    )


# HU-009: GET /api/mascotas/{id}/historial
@router.get("/{mascota_id}/historial", response_model=StandardResponse)
def consultar_historial(
    mascota_id: int,
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credenciales.credentials
    usuario_id = obtener_usuario_id_desde_token(token)

    service = HistorialMedicoService(db)
    status_code, resp = service.consultar_historial(mascota_id, usuario_id)

    # 👇 Igual aquí
    return JSONResponse(
        status_code=status_code,
        content=resp.model_dump(mode="json"),
    )

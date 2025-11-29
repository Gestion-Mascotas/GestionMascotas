# app/api/registro_medico.py

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import StandardResponse
from app.domain.historial_schema import RegistroMedicoUpdate
from app.services.registro_medico_service import RegistroMedicoService
from app.security import obtener_usuario_id_desde_token

router = APIRouter(prefix="/api/registro-medico", tags=["Registro Médico"])

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HU-010: PUT /api/registro-medico/{id}
@router.put("/{registro_id}", response_model=StandardResponse)
def actualizar_registro(
    registro_id: int,
    body: RegistroMedicoUpdate,
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credenciales.credentials
    usuario_id = obtener_usuario_id_desde_token(token)

    service = RegistroMedicoService(db)
    status_code, resp = service.actualizar(registro_id, usuario_id, body)

    # 👇 IMPORTANTE: modo JSON para serializar datetime
    return JSONResponse(
        status_code=status_code,
        content=resp.model_dump(mode="json"),
    )


# HU-011: DELETE /api/registro-medico/{id}
@router.delete("/{registro_id}", response_model=StandardResponse)
def eliminar_registro(
    registro_id: int,
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credenciales.credentials
    usuario_id = obtener_usuario_id_desde_token(token)

    service = RegistroMedicoService(db)
    status_code, resp = service.eliminar(registro_id, usuario_id)

    # Por consistencia, también en modo JSON (por si en el futuro agregas fechas)
    return JSONResponse(
        status_code=status_code,
        content=resp.model_dump(mode="json"),
    )

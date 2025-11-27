# app/api/registro_medico.py

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import StandardResponse
from app.domain.historial_schema import RegistroMedicoUpdate
from app.services.registro_medico_service import RegistroMedicoService
from app.security import obtener_usuario_id_desde_token

router = APIRouter(prefix="/api/registro-medico", tags=["Registro Médico"])


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
    authorization: str | None = Header(alias="Authorization", default=None),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.startswith("Bearer "):
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para actualizar el registro médico",
            success=False,
            error_code="401",
            details=None,
            data=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    token = authorization.split(" ", 1)[1]
    usuario_id = obtener_usuario_id_desde_token(token)

    service = RegistroMedicoService(db)
    status_code, resp = service.actualizar(registro_id, usuario_id, body)
    return JSONResponse(status_code=status_code, content=resp.model_dump())


# HU-011: DELETE /api/registro-medico/{id}
@router.delete("/{registro_id}", response_model=StandardResponse)
def eliminar_registro(
    registro_id: int,
    authorization: str | None = Header(alias="Authorization", default=None),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.startswith("Bearer "):
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para eliminar el registro médico.",
            success=False,
            error_code="401",
            details=None,
            data=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    token = authorization.split(" ", 1)[1]
    usuario_id = obtener_usuario_id_desde_token(token)

    service = RegistroMedicoService(db)
    status_code, resp = service.eliminar(registro_id, usuario_id)
    return JSONResponse(status_code=status_code, content=resp.model_dump())

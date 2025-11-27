# app/api/alertas.py

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import StandardResponse
from app.services.alertas_service import AlertaVacunasService
from app.security import obtener_usuario_id_desde_token

router = APIRouter(prefix="/api/alertas", tags=["Alertas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HU-013: GET /api/alertas/vacunas-proximas
@router.get("/vacunas-proximas", response_model=StandardResponse)
def vacunas_proximas(
    authorization: str | None = Header(alias="Authorization", default=None),
    db: Session = Depends(get_db),
):

    if not authorization or not authorization.startswith("Bearer "):
        resp = StandardResponse(
            mensaje="No tiene permisos para acceder a esta información",
            success=False,
            error_code="AUTH.FORBIDDEN",
            details=None,
            data=None,
        )
        return JSONResponse(status_code=403, content=resp.model_dump())

    token = authorization.split(" ", 1)[1]
    usuario_id = obtener_usuario_id_desde_token(token)

    if not usuario_id:
        resp = StandardResponse(
            mensaje="No tiene permisos para acceder a esta información",
            success=False,
            error_code="AUTH.FORBIDDEN",
            details=None,
            data=None,
        )
        return JSONResponse(status_code=403, content=resp.model_dump())

    service = AlertaVacunasService(db)
    status_code, resp = service.obtener_alertas_vacunas(usuario_id)
    return JSONResponse(status_code=status_code, content=resp.model_dump())

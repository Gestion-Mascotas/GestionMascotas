# app/api/alertas.py

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import StandardResponse
from app.services.alertas_service import AlertaVacunasService
from app.security import obtener_usuario_actual  # 👈 dependencia centralizada

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
    usuario_id: int | None = Depends(obtener_usuario_actual),  # 👈 valida token automáticamente
    db: Session = Depends(get_db),
):

    # Si Swagger no pasó token → 401
    if usuario_id is None:
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para consultar alertas de vacunas",
            success=False,
            error_code="401",
            details=None,
            data=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    # Llamamos al servicio
    service = AlertaVacunasService(db)
    status_code, resp = service.obtener_alertas_vacunas(usuario_id)
    return JSONResponse(status_code=status_code, content=resp.model_dump())

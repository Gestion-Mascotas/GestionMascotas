# app/api/mascotas.py

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.mascota_schema import MascotaUpdate
from app.domain.usuario_schema import StandardResponse
from app.domain.mascota_schema import MascotaCreate
from app.services.mascota_service import MascotaService
from app.security import obtener_usuario_id_desde_token

router = APIRouter(prefix="/api/mascotas", tags=["Mascotas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------- HU-003: Creación de Mascota --------------
@router.post("/", response_model=StandardResponse)
def crear_mascota(
    datos: MascotaCreate,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    # Validar token presente
    if not authorization or not authorization.startswith("Bearer "):
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para registrar una mascota.",
            success=False,
            data=None,
            error_code="401",
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    # Extraer token
    token = authorization.split(" ", 1)[1]
    usuario_id = obtener_usuario_id_desde_token(token)

    # Token inválido o expirado
    if not usuario_id:
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para registrar una mascota.",
            success=False,
            data=None,
            error_code="401",
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    # Ejecutar servicio
    service = MascotaService(db)
    status_code, resp = service.crear_mascota(usuario_id, datos)
    
    return JSONResponse(status_code=status_code, content=resp.model_dump())

# ---------- HU-005: Actualización de Mascota ----------
@router.put("/{mascota_id}", response_model=StandardResponse)
def actualizar_mascota(
    mascota_id: int,
    datos: MascotaUpdate,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    # Validar token presente
    if not authorization or not authorization.startswith("Bearer "):
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para actualizar la mascota",
            success=False,
            data=None,
            error_code=None,
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.dict())

    token = authorization.split(" ", 1)[1]
    usuario_id = obtener_usuario_id_desde_token(token)

    if not usuario_id:
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para actualizar la mascota",
            success=False,
            data=None,
            error_code=None,
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.dict())

    service = MascotaService(db)
    status_code, resp = service.actualizar_mascota(mascota_id, usuario_id, datos)
    return JSONResponse(status_code=status_code, content=resp.dict())


# ---------- HU-006: Eliminación de Mascota ----------
@router.delete("/{mascota_id}", response_model=StandardResponse)
def eliminar_mascota(
    mascota_id: int,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    # Validar token presente
    if not authorization or not authorization.startswith("Bearer "):
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para eliminar la mascota",
            success=False,
            data=None,
            error_code=None,
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.dict())

    token = authorization.split(" ", 1)[1]
    usuario_id = obtener_usuario_id_desde_token(token)

    if not usuario_id:
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para eliminar la mascota",
            success=False,
            data=None,
            error_code=None,
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.dict())

    service = MascotaService(db)
    status_code, resp = service.eliminar_mascota(mascota_id, usuario_id)
    return JSONResponse(status_code=status_code, content=resp.dict())

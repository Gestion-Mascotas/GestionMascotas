# app/api/mascotas.py

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.mascota_schema import MascotaCreate, MascotaUpdate
from app.domain.usuario_schema import StandardResponse
from app.services.mascota_service import MascotaService
from app.security import obtener_usuario_actual  # 👈 usamos la dependencia global

router = APIRouter(prefix="/api/mascotas", tags=["Mascotas"])


# -----------------------
# Obtener sesión de BD
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------
# HU-003: Creación de Mascota
# ---------------------------------------------------
@router.post("/", response_model=StandardResponse)
def crear_mascota(
    datos: MascotaCreate,
    db: Session = Depends(get_db),
    usuario_id: int | None = Depends(obtener_usuario_actual),
):

    # Sin token o token inválido
    if usuario_id is None:
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para registrar una mascota.",
            success=False,
            data=None,
            error_code="401",
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    service = MascotaService(db)
    status_code, resp = service.crear_mascota(usuario_id, datos)
    return JSONResponse(status_code=status_code, content=resp.model_dump())


# ---------------------------------------------------
# HU-004: Consulta de Mascota
# ---------------------------------------------------
@router.get("/{mascota_id}", response_model=StandardResponse)
def consultar_mascota(
    mascota_id: int,
    db: Session = Depends(get_db),
    usuario_id: int | None = Depends(obtener_usuario_actual),
):

    if usuario_id is None:
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para consultar la mascota.",
            success=False,
            data=None,
            error_code="401",
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    service = MascotaService(db)
    status_code, resp = service.consultar_mascota(mascota_id, usuario_id)
    return JSONResponse(status_code=status_code, content=resp.model_dump())


# ---------------------------------------------------
# HU-005: Actualización de Mascota
# ---------------------------------------------------
@router.put("/{mascota_id}", response_model=StandardResponse)
def actualizar_mascota(
    mascota_id: int,
    datos: MascotaUpdate,
    db: Session = Depends(get_db),
    usuario_id: int | None = Depends(obtener_usuario_actual),
):

    if usuario_id is None:
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para actualizar la mascota.",
            success=False,
            data=None,
            error_code="401",
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    service = MascotaService(db)
    status_code, resp = service.actualizar_mascota(mascota_id, usuario_id, datos)
    return JSONResponse(status_code=status_code, content=resp.model_dump())


# ---------------------------------------------------
# HU-006: Eliminación de Mascota
# ---------------------------------------------------
@router.delete("/{mascota_id}", response_model=StandardResponse)
def eliminar_mascota(
    mascota_id: int,
    db: Session = Depends(get_db),
    usuario_id: int | None = Depends(obtener_usuario_actual),
):

    if usuario_id is None:
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para eliminar la mascota.",
            success=False,
            data=None,
            error_code="401",
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.model_dump())

    service = MascotaService(db)
    status_code, resp = service.eliminar_mascota(mascota_id, usuario_id)
    return JSONResponse(status_code=status_code, content=resp.model_dump())

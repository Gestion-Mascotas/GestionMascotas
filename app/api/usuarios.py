# app/api/usuarios.py
from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import UsuarioCreate, StandardResponse
from app.services.usuario_service import UsuarioService
from app.services.mascota_service import MascotaService
from app.security import obtener_usuario_id_desde_token

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=StandardResponse,
    summary="Registro de usuario (HU-001)",
)
def registrar_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    status_code, resp = service.registrar_usuario(usuario_in)
    return JSONResponse(status_code=status_code, content=resp.dict())


# ---------------- HU-007: Consulta de mascotas del usuario ----------------
@router.get(
    "/{usuario_id}/mascotas",
    response_model=StandardResponse,
    summary="Consulta de Mascotas del Usuario (HU-007)",
)
def listar_mascotas_usuario(
    usuario_id: int,
    authorization: str | None = Header(alias="Authorization", default=None),
    db: Session = Depends(get_db),
):
    # 401/403 según HU
    if not authorization or not authorization.startswith("Bearer "):
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para consultar las mascotas",
            success=False,
            data=None,
            error_code="401",
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.dict())

    token = authorization.split(" ", 1)[1]
    usuario_id_token = obtener_usuario_id_desde_token(token)

    if not usuario_id_token:
        resp = StandardResponse(
            mensaje="Debe iniciar sesión para consultar las mascotas",
            success=False,
            data=None,
            error_code="401",
            details=None,
        )
        return JSONResponse(status_code=401, content=resp.dict())

    # 403 si el id consultado no coincide con el usuario autenticado
    if usuario_id_token != usuario_id:
        resp = StandardResponse(
            mensaje="Acceso no autorizado",
            success=False,
            data=None,
            error_code="403",
            details=None,
        )
        return JSONResponse(status_code=403, content=resp.dict())

    service = MascotaService(db)
    status_code, resp = service.listar_mascotas_usuario(usuario_id)

    return JSONResponse(status_code=status_code, content=resp.dict())

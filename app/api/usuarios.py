# app/routers/usuarios.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import UsuarioCreate, StandardResponse
from app.services.usuario_service import UsuarioService

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

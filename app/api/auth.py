# app/routers/auth.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.usuario_schema import LoginRequest, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api", tags=["Autenticación"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Autenticación de usuario (HU-002)",
)
def login(credenciales: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    status_code, resp = service.login(credenciales)
    return JSONResponse(status_code=status_code, content=resp.dict())

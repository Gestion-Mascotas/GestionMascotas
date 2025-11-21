# app/schemas/usuario_schema.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from app.models.usuario import RolEnum


# --------- Modelos de entrada / salida ---------

class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    # En JSON el campo se llama "contraseña"
    contrasena: str = Field(..., alias="contraseña")
    rol: RolEnum

    class Config:
        # Permite usar alias "contraseña" en el body
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "nombre": "Juan Pérez",
                "correo": "juan@example.com",
                "contraseña": "12345678",
                "rol": "dueño"
            }
        }


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: RolEnum

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str = Field(..., alias="contraseña")


# --------- Estructuras de respuesta ---------

class ErrorDetail(BaseModel):
    field: str
    message: str


class StandardResponse(BaseModel):
    mensaje: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None
    details: Optional[List[ErrorDetail]] = None


class LoginResponse(BaseModel):
    mensaje: str
    success: bool
    data: Optional[Dict[str, Any]] = None

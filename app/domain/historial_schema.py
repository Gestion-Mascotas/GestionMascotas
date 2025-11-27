# app/domain/historial_schema.py

from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


# ------------- HU-008: Registro médico (Vacuna / Tratamiento) -------------

class HistorialCreate(BaseModel):
    tipo: str = Field(..., description="Vacuna o Tratamiento")
    descripcion: str
    fecha: date
    proxima_fecha: Optional[date] = None


class HistorialOut(BaseModel):
    id: int
    mascota_id: int
    tipo: str
    descripcion: str
    fecha: date
    proxima_fecha: Optional[date] = None

    class Config:
        from_attributes = True


# ------------- HU-010: Actualización de registro médico -------------

class RegistroMedicoUpdate(BaseModel):
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    peso: Optional[float] = None
    temperatura: Optional[float] = None


class RegistroMedicoOut(BaseModel):
    id: int
    mascota_id: int
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    peso: Optional[float] = None
    temperatura: Optional[float] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

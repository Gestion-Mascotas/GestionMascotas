# app/domain/mascota_schema.py

from pydantic import BaseModel
from typing import Optional


class MascotaUpdate(BaseModel):
    """
    Modelo para actualización parcial de mascota (HU-005).
    Todos los campos son opcionales, solo se actualiza lo que venga en la petición.
    """
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    edad: Optional[int] = None
    peso: Optional[float] = None
    sexo: Optional[str] = None


class MascotaOut(BaseModel):
    """
    Modelo de salida para respuestas de mascota.
    """
    id: int
    nombre: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[int] = None
    peso: Optional[float] = None
    sexo: Optional[str] = None
    usuario_id: int

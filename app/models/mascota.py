# app/models/mascota.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(100), nullable=True)
    edad = Column(Integer, nullable=True)
    peso = Column(Float, nullable=True)
    sexo = Column(String(20), nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

# app/models/usuario.py
from sqlalchemy import Column, Integer, String, Enum
import enum
from app.database import Base

class RolEnum(str, enum.Enum):
    dueno = "dueño"
    veterinario = "veterinario"
    admin = "admin"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(255), unique=True, index=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), nullable=False)

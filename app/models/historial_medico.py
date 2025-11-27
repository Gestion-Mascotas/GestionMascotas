# app/models/historial_medico.py

from sqlalchemy import Column, Integer, String, Date, Float, DateTime, ForeignKey
from datetime import datetime

from app.database import Base


class HistorialMedico(Base):
    __tablename__ = "historial_medico"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=False)

    # HU-008 / 009 (tipo, descripcion, fecha, proxima_fecha)
    tipo = Column(String(50), nullable=True)          # "Vacuna" | "Tratamiento" ...
    descripcion = Column(String(255), nullable=True)
    fecha = Column(Date, nullable=True)
    proxima_fecha = Column(Date, nullable=True)

    # HU-010 / 011 (diagnostico, tratamiento, peso, temperatura)
    diagnostico = Column(String(255), nullable=True)
    tratamiento = Column(String(255), nullable=True)
    peso = Column(Float, nullable=True)
    temperatura = Column(Float, nullable=True)

    fecha_actualizacion = Column(
        DateTime,
        nullable=True,
        default=datetime.utcnow
    )

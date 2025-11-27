# app/repository/historial_medico_repository.py

from sqlalchemy.orm import Session
from app.models.historial_medico import HistorialMedico


class HistorialMedicoRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = HistorialMedico

    def crear(self, mascota_id: int, datos: dict) -> HistorialMedico:
        registro = HistorialMedico(
            mascota_id=mascota_id,
            tipo=datos.get("tipo"),
            descripcion=datos.get("descripcion"),
            fecha=datos.get("fecha"),
            proxima_fecha=datos.get("proxima_fecha"),
            diagnostico=datos.get("diagnostico"),
            tratamiento=datos.get("tratamiento"),
            peso=datos.get("peso"),
            temperatura=datos.get("temperatura"),
        )
        self.db.add(registro)
        self.db.commit()
        self.db.refresh(registro)
        return registro

    def obtener_por_id(self, registro_id: int) -> HistorialMedico | None:
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.id == registro_id)
            .first()
        )

    def obtener_por_mascota(self, mascota_id: int) -> list[HistorialMedico]:
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.mascota_id == mascota_id)
            .order_by(HistorialMedico.fecha.desc())
            .all()
        )

    def actualizar(self, registro: HistorialMedico, campos: dict) -> HistorialMedico:
        from datetime import datetime

        for key, value in campos.items():
            setattr(registro, key, value)
        registro.fecha_actualizacion = datetime.utcnow()
        self.db.commit()
        self.db.refresh(registro)
        return registro

    def eliminar(self, registro: HistorialMedico) -> None:
        self.db.delete(registro)
        self.db.commit()

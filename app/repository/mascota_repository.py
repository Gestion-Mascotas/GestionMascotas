# app/repository/mascota_repository.py

from sqlalchemy.orm import Session
from app.models.mascota import Mascota


class MascotaRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, mascota_id: int) -> Mascota | None:
        return self.db.query(Mascota).filter(Mascota.id == mascota_id).first()

    def actualizar(self, mascota: Mascota, campos: dict) -> Mascota:
        for key, value in campos.items():
            setattr(mascota, key, value)
        self.db.commit()
        self.db.refresh(mascota)
        return mascota

    def eliminar(self, mascota: Mascota) -> None:
        self.db.delete(mascota)
        self.db.commit()

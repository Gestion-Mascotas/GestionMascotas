# app/repository/usuario_repository.py
from sqlalchemy.orm import Session
from app.models.usuario import Usuario, RolEnum


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_correo(self, correo: str):
        return self.db.query(Usuario).filter(Usuario.correo == correo).first()

    def crear(self, nombre: str, correo: str, contrasena_hash: str, rol: RolEnum) -> Usuario:
        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            contrasena_hash=contrasena_hash,
            rol=rol
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

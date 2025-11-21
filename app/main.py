from fastapi import FastAPI

from app.database import Base, engine
from app.models import usuario  # importa el modelo para crear la tabla

from app.api.usuarios import router as usuarios_router
from app.api.auth import router as auth_router
from app.api.mascotas import router as mascotas_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestión de Mascotas",
    version="1.0.0"
)

app.include_router(usuarios_router)
app.include_router(auth_router)
app.include_router(mascotas_router) 

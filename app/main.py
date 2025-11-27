# app/main.py

from fastapi import FastAPI

from app.database import Base, engine
from app.config.routers import ROUTERS  # ← aquí usamos la lista de routers

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestión de Mascotas",
    version="1.0.0",
)

# Registrar TODOS los routers definidos en config/routers.py
for router in ROUTERS:
    app.include_router(router)


@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

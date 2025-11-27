# app/config/routers.py

from app.api import usuarios
from app.api import auth
from app.api import mascotas
from app.api import historial_medico
from app.api import registro_medico
from app.api import reporte_salud
from app.api import alertas

ROUTERS = [
    usuarios.router,
    auth.router,
    mascotas.router,
    historial_medico.router,
    registro_medico.router,
    reporte_salud.router,
    alertas.router,
]

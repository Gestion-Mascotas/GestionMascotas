from app.api import usuarios
from app.api import auth
from app.api import mascotas

ROUTERS = [
    usuarios.router,
    auth.router,
    mascotas.router
]

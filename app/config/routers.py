from app.api import usuarios
from app.api import auth

ROUTERS = [
    usuarios.router,
    auth.router
]

from flask import Blueprint

api = Blueprint("api", __name__)

from .routes import *  # Importa las rutas desde routes.py

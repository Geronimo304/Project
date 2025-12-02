from flask import Flask
from flask_restx import Api

from app.api.v1.users import api as users_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Marcador de posición para los espacios de nombres de la API (los endpoints se añadirán más adelante)
    # Espacios de nombres adicionales para places, reviews y amenities se añadirán más adelante

    api.add_namespace(users_ns, path='/api/v1/users')
    return app
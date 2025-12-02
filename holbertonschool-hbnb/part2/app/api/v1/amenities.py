from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Operaciones de amenidades')

# Define el modelo de amenidad para validación de entrada y documentación
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Nombre de la amenidad')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenidad creada exitosamente')
    @api.response(400, 'Datos de entrada inválidos')
    def post(self):
        """Registrar una nueva amenidad"""
        # Marcador de posición para la lógica de registrar una nueva amenidad
        pass

    @api.response(200, 'Lista de amenidades obtenida exitosamente')
    def get(self):
        """Obtener una lista de todas las amenidades"""
        # Marcador de posición para la lógica de devolver una lista de todas las amenidades
        pass

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Detalles de amenidad obtenidos exitosamente')
    @api.response(404, 'Amenidad no encontrada')
    def get(self, amenity_id):
        """Obtener detalles de amenidad por ID"""
        # Marcador de posición para la lógica de obtener una amenidad por ID
        pass

    @api.expect(amenity_model)
    @api.response(200, 'Amenidad actualizada exitosamente')
    @api.response(404, 'Amenidad no encontrada')
    @api.response(400, 'Datos de entrada inválidos')
    def put(self, amenity_id):
        """Actualizar la información de una amenidad"""
        # Marcador de posición para la lógica de actualizar una amenidad por ID
        pass
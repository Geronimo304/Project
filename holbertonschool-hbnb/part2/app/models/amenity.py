from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Operaciones de amenidades')

# Define el modelo de amenidad para validación de entrada y documentación
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Nombre de la amenidad')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenidad creada exitosamente')
    @api.response(400, 'Datos de entrada inválidos')
    def post(self):
        """Registrar una nueva amenidad"""
        amenity_data = api.payload
        
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Lista de amenidades obtenida exitosamente')
    def get(self):
        """Obtener una lista de todas las amenidades"""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name
            } for amenity in amenities
        ], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Detalles de amenidad obtenidos exitosamente')
    @api.response(404, 'Amenidad no encontrada')
    def get(self, amenity_id):
        """Obtener detalles de amenidad por ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenidad no encontrada'}, 404
        
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenidad actualizada exitosamente')
    @api.response(404, 'Amenidad no encontrada')
    @api.response(400, 'Datos de entrada inválidos')
    def put(self, amenity_id):
        """Actualizar la información de una amenidad"""
        amenity_data = api.payload
        
        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
            if not amenity:
                return {'error': 'Amenidad no encontrada'}, 404
            
            return {
                'message': 'Amenidad actualizada exitosamente'
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
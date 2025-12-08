from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace('users', description='Operaciones de usuarios')

                                                                        
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Nombre del usuario'),
    'last_name': fields.String(required=True, description='Apellido del usuario'),
    'email': fields.String(required=True, description='Correo del usuario'),
    'password': fields.String(required=True, description='Password del usuario')
})

@api.route('/', methods=['GET', 'POST'])                                            
class UserList(Resource):
    @api.response(200, 'Lista de usuarios obtenida exitosamente')
    def get(self):         
        """Obtener todos los usuarios"""
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'Usuario creado exitosamente')
    @api.response(400, 'Correo ya registrado')
    @api.response(400, 'Datos de entrada inválidos')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Registrar un nuevo usuario - requires admin"""
        jwt_data = get_jwt()
        is_admin = jwt_data.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Correo ya registrado'}, 400
        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
    
@api.route('/<user_id>', methods=['GET', 'PUT'])                                           
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'Usuario actualizado exitosamente')
    @api.response(404, 'Usuario no encontrado')
    @api.response(400, 'Correo ya registrado')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'You cannot modify email or password')
    @jwt_required()
    def put(self, user_id):         
        """Actualizar usuario por ID - user can only modify own data; admin can modify any"""
        current_user = get_jwt_identity()
        jwt_data = get_jwt()
        is_admin = jwt_data.get('is_admin', False)
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Usuario no encontrado'}, 404

        # check if user is updating own data or is admin
        if current_user != user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload
        
        # regular users cannot modify email or password
        if not is_admin:
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'You cannot modify email or password'}, 400
        
        # check email uniqueness if modified
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Correo ya registrado'}, 400

        facade.update_user(user_id, user_data)
        updated_user = facade.get_user(user_id)
        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace('users', description='Operaciones de usuarios')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Nombre del usuario'),
    'last_name': fields.String(required=True, description='Apellido del usuario'),
    'email': fields.String(required=True, description='Correo del usuario')
})

# Include password as optional in the shared model; POST will require it explicitly
user_model['password'] = fields.String(required=False, description='Password del usuario')

@api.route('/', methods=['GET', 'POST'])  #cambio: permite explícitamente GET y POST
class UserList(Resource):
    @api.response(200, 'Lista de usuarios obtenida exitosamente')
    def get(self):  #cambio
        """Obtener todos los usuarios"""
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'Usuario creado exitosamente')
    @api.response(400, 'Correo ya registrado')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Registrar un nuevo usuario (admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        if 'password' not in user_data or not user_data.get('password'):
            return {'error': 'password is required'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
    
@api.route('/<user_id>', methods=['GET', 'PUT'])  #cambio: permite explícitamente GET y PUT
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
    @api.response(400, 'Email already in use')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Actualizar usuario (propietario o admin). Admins pueden cambiar email/password."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Usuario no encontrado'}, 404

        current_user = get_jwt_identity()
        current_user_claims = get_jwt()
        is_admin = current_user_claims.get('is_admin', False)

        if current_user != user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload or {}

        # Regular users cannot modify email or password
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password.'}, 400

        # Check email uniqueness
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already in use'}, 400

        # Admin can change password
        if is_admin and 'password' in user_data:
            password = user_data.pop('password')
            facade.update_user(user_id, user_data)
            updated_user = facade.get_user(user_id)
            if password:
                updated_user.hash_password(password)
        else:
            facade.update_user(user_id, user_data)

        updated_user = facade.get_user(user_id)
        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200

from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('protected', description='Protected endpoints')


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_identity = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        return {'message': f'Hello, user {current_identity}', 'is_admin': is_admin}, 200

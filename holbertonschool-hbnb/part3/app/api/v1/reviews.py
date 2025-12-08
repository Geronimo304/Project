from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Model for updates (no place_id required)
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Text of the review'),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review (authenticated users only)"""
        payload = api.payload
        current_user = get_jwt_identity()
        
        review_data = {
            'place_id': payload.get('place_id'),
            'text': payload.get('text'),
            'rating': payload.get('rating'),
            'user_id': current_user
        }

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user,
                'place_id': new_review.place
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews (public)"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            } for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (public)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user,
            'place_id': review.place
        }, 200

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information (creator or admin)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        current_user = get_jwt_identity()
        current_user_claims = get_jwt()
        is_admin = current_user_claims.get('is_admin', False)

        # Allow creator or admin to update
        if review.user != current_user and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload or {}
        # Prevent changing user or place via update
        data.pop('user_id', None)
        data.pop('place_id', None)
        data.pop('user', None)
        data.pop('place', None)

        try:
            facade.update_review(review_id, data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review (creator or admin)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        current_user = get_jwt_identity()
        current_user_claims = get_jwt()
        is_admin = current_user_claims.get('is_admin', False)

        # Allow creator or admin to delete
        if review.user != current_user and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=False, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner or amenity not found')
    @jwt_required()
    def post(self):
        """Register a new place (authenticated users only). Owner_id will be set to the authenticated user."""
        place_data = api.payload or {}
        try:
            current_user = get_jwt_identity()
            # enforce owner to be the authenticated user
            place_data['owner_id'] = current_user
            new_place = facade.create_place(place_data)

            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        
        return [
            {
                'id': place.id,
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude
            } for place in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Get owner details
        owner = facade.get_user(place.owner_id)
        owner_data = {
            'id': owner.id,
            'first_name': owner.first_name,
            'last_name': owner.last_name,
            'email': owner.email
        } if owner else None
        
        # Get amenities details
        amenities_data = []
        for amenity_id in place.amenities:
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenities_data.append({
                    'id': amenity.id,
                    'name': amenity.name
                })
        
        # Get reviews details
        reviews_data = []
        for review_id in place.reviews:
            review = facade.get_review(review_id)
            if review:
                reviews_data.append({
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user
                })
        
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_data,
            'amenities': amenities_data,
            'reviews': reviews_data
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (owner or admin)"""
        place_data = api.payload or {}
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        current_user = get_jwt_identity()
        current_user_claims = get_jwt()
        is_admin = current_user_claims.get('is_admin', False)

        # Allow owner or admin to update
        if place.owner_id != current_user and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        # Prevent changing owner (unless admin is explicitly setting it, but generally prevent)
        if 'owner_id' in place_data and place_data.get('owner_id') != current_user and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_place = facade.update_place(place_id, place_data)

            if not updated_place:
                return {'error': 'Place not found'}, 404

            return {'message': 'Place updated successfully'}, 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Invalid input data'}, 400


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            } for review in reviews
        ], 200
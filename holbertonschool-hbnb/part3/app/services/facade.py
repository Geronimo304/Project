from app.persistence.repository import InMemoryRepository
from app.services.user_repository import UserRepository
from app.services.place_repository import PlaceRepository
from app.services.review_repository import ReviewRepository
from app.services.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.amenity_repo = AmenityRepository()
        self.review_repo = ReviewRepository()

    # ===== USER METHODS =====
    def create_user(self, user_data):
        # Accepts an optional 'password' in user_data; hash it using the model helper
        password = None
        if 'password' in user_data:
            password = user_data.pop('password')

        user = User(**user_data)
        if password:
            user.hash_password(password)

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    # ===== PLACE METHODS =====
    def create_place(self, place_data):
        """Create a new place with validation"""
        # Validate that the owner exists
        owner_id = place_data.get('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        
        # Validate amenities if provided
        amenity_ids = place_data.get('amenities', [])
        validated_amenities = []
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            validated_amenities.append(amenity_id)
        
        # Create the place
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=owner_id,
            amenities=validated_amenities
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places"""
        return self.place_repo.get_all()

    # ===== REVIEW METHODS =====
    def create_review(self, review_data):
        """Create a new review with validation
        review_data must include: text, rating (int), place_id, user_id
        """
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')
        text = review_data.get('text')
        rating = review_data.get('rating')

        place = self.get_place(place_id)
        if not place:
            raise ValueError('Place not found')

        # User cannot review own place
        if place.owner_id == user_id:
            raise ValueError('You cannot review your own place')

        # Ensure user hasn't already reviewed this place
        existing = self.review_repo.get_review_by_place_and_user(place_id, user_id)
        if existing:
            raise ValueError('You have already reviewed this place')

        review = Review(text=text, rating=rating, place_id=place_id, user_id=user_id)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if review:
            self.review_repo.delete(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        place = self.get_place(place_id)
        if not place:
            return None
        return self.review_repo.get_reviews_by_place(place_id)

    def update_place(self, place_id, place_data):
        """Update a place's information"""
        place = self.get_place(place_id)
        if not place:
            return None
        
        # Validate owner if being updated
        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
        
        # Validate amenities if being updated
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        # Update the place
        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

    # ===== AMENITY METHODS =====
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        return self.amenity_repo.update(amenity_id, amenity_data)
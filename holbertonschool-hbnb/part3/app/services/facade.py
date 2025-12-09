from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.services.repositories.user_repository import UserRepository
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.review_repo = SQLAlchemyRepository(Review)

                              
    def create_user(self, user_data):
        password = user_data.pop('password', None)
        user = User(**user_data, password=password)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        try:
            return self.user_repo.get_user_by_email(email)
        except Exception:
            return None

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

                               
    def create_place(self, place_data):                                        
        owner_id = place_data.get('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        
                                        
        amenity_ids = place_data.get('amenities', [])
        validated_amenities = []
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            validated_amenities.append(amenity_id)
        
                          
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
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        
                                         
        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
        
                                             
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
        
                          
        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

                                 
    def create_amenity(self, amenity_data):
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    def create_review(self, review_data):
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')
        
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Place not found')
        
        user = self.get_user(user_id)
        if not user:
            raise ValueError('User not found')
        
        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place_id=place_id,
            user_id=user_id
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews = self.get_all_reviews()
        return [review for review in reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
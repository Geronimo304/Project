from app.models.Base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        if not hasattr(self, 'reviews') or self.reviews is None:
            self.reviews = []
        if not hasattr(self, 'amenities') or self.amenities is None:
            self.amenities = []

    def verify(self):
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Title is required and must be a string")
        if len(self.title) > 100:
            raise ValueError("Title must be less than 100 characters")

        if not self.description or not isinstance(self.description, str):
            raise ValueError("Description is required and must be a string")

        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be a non-negative number")

        if not isinstance(self.latitude, float) or not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be a float between -90 and 90")

        if not isinstance(self.longitude, float) or not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be a float between -180 and 180")

        if not self.owner or not isinstance(self.owner, str):
            raise ValueError("Owner is required and must be a string")
        
            
    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

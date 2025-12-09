from app.models.Base_model import BaseModel
from app import db

# Association table for Place-Amenity many-to-many relationship
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    _title = db.Column('title', db.String(100), nullable=False)
    _description = db.Column('description', db.String(500), nullable=False)
    _price = db.Column('price', db.Float, nullable=False)
    _latitude = db.Column('latitude', db.Float, nullable=False)
    _longitude = db.Column('longitude', db.Float, nullable=False)
    _owner_id = db.Column('owner_id', db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None):
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
    
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title is required and must be a string")
        if len(value) > 100:
            raise ValueError("Title must be less than 100 characters")
        if not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value
    
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Description is required and must be a string")
        if not value.strip():
            raise ValueError("Description cannot be empty")
        self._description = value
    
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)
    
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Owner ID is required and must be a string")
        self._owner_id = value
        
    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)
    
    def delete_review(self, review):
        if review in self.reviews:
            self.reviews.remove(review)
    
    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def delete_amenity(self, amenity):
        if amenity in self.amenities:
            self.amenities.remove(amenity)
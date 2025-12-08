from app.models.Base_model import BaseModel
from app import db


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='place', lazy=True, foreign_keys='Review.place_id')

    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None):
        super().__init__()
        self._validate_title(title)
        self._validate_description(description)
        self._validate_price(price)
        self._validate_latitude(latitude)
        self._validate_longitude(longitude)
        self._validate_owner_id(owner_id)
        
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id

    @staticmethod
    def _validate_title(value):
        if not isinstance(value, str):
            raise TypeError("Title is required and must be a string")
        if len(value) > 100:
            raise ValueError("Title must be less than 100 characters")
        if not value.strip():
            raise ValueError("Title cannot be empty")

    @staticmethod
    def _validate_description(value):
        if not value or not isinstance(value, str):
            raise ValueError("Description is required and must be a string")
        if not value.strip():
            raise ValueError("Description cannot be empty")

    @staticmethod
    def _validate_price(value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")

    @staticmethod
    def _validate_latitude(value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")

    @staticmethod
    def _validate_longitude(value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")

    @staticmethod
    def _validate_owner_id(value):
        if not value or not isinstance(value, str):
            raise ValueError("Owner ID is required and must be a string")

    def update(self, data):
        if 'title' in data:
            self._validate_title(data['title'])
            self.title = data['title']
        if 'description' in data:
            self._validate_description(data['description'])
            self.description = data['description']
        if 'price' in data:
            self._validate_price(data['price'])
            self.price = float(data['price'])
        if 'latitude' in data:
            self._validate_latitude(data['latitude'])
            self.latitude = float(data['latitude'])
        if 'longitude' in data:
            self._validate_longitude(data['longitude'])
            self.longitude = float(data['longitude'])
        if 'owner_id' in data:
            self._validate_owner_id(data['owner_id'])
            self.owner_id = data['owner_id']
        self.save()

    def add_review(self, review):
        """Add a review to the place"""
        pass
    
    def delete_review(self, review):
        """Remove a review from the place"""
        pass
    
    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        pass

    def delete_amenity(self, amenity):
        """Remove an amenity from the place"""
        pass
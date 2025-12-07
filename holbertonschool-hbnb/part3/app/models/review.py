from app.models.Base_model import BaseModel
from app import db


class Review(BaseModel):
    """Review model mapped to SQLAlchemy"""
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self._validate_text(text)
        self._validate_rating(rating)
        self._validate_place_id(place_id)
        self._validate_user_id(user_id)
        
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @staticmethod
    def _validate_text(value):
        if not isinstance(value, str):
            raise TypeError("The text is required and must contain only characters")

    @staticmethod
    def _validate_rating(value):
        if not isinstance(value, int):
            raise TypeError("The rating must be an int")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

    @staticmethod
    def _validate_place_id(value):
        if not isinstance(value, str):
            raise TypeError("The place_id is required and must be a string")

    @staticmethod
    def _validate_user_id(value):
        if not value or not isinstance(value, str):
            raise TypeError("User_id is required and must be a string")

    def update(self, data):
        if 'text' in data:
            self._validate_text(data['text'])
            self.text = data['text']
        if 'rating' in data:
            self._validate_rating(data['rating'])
            self.rating = data['rating']
        if 'place_id' in data:
            self._validate_place_id(data['place_id'])
            self.place_id = data['place_id']
        if 'user_id' in data:
            self._validate_user_id(data['user_id'])
            self.user_id = data['user_id']
        self.save()
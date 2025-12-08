from app.models.Base_model import BaseModel
from app import db


place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    places = db.relationship('Place', secondary=place_amenity, backref=db.backref('amenities', lazy=True))

    def __init__(self, name):
        super().__init__()
        self._validate_name(name)
        self.name = name

    @staticmethod
    def _validate_name(value):
        if not isinstance(value, str):
            raise TypeError("Name is required and must be a string")
        if len(value) > 50:
            raise ValueError("Name must be less than 50 characters")

    def update(self, data):
        if 'name' in data:
            self._validate_name(data['name'])
            self.name = data['name']
        self.save()
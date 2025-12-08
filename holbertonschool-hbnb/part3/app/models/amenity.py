from app.models.Base_model import BaseModel
from app import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    _name = db.Column('name', db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name is required and must be a string")
        if len(value) > 50:
            raise ValueError("Name must be less than 50 characters")
        self._name = value
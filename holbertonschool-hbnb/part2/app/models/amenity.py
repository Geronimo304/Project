from app.models.Base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name is required and must be a string")
        if len(self.name) > 50:
            raise ValueError("Name must be less than 50 characters")
        self._name = value

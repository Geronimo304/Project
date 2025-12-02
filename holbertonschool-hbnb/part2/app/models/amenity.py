from app.models.Base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def verify(self):
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name is required and must be a string")
        if len(self.name) > 50:
            raise ValueError("Name must be less than 50 characters")
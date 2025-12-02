from app.models.Base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def verify(self):
        if not self.text or not isinstance(self.text, str):
            raise ValueError("The text is required and must contain only characters")

        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        if not self.place or not isinstance(self.place, str):
            raise ValueError("The place is required and must contain only characters")

        if not self.user or not isinstance(self.user, str):
            raise ValueError("User is required and must contain characters")

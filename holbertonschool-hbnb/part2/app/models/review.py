from app.models.Base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("The text is required and must contain only characters")
        self._text = value
    
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("The rating must be an int")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        self._rating = value

    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, value):
        if not isinstance(value, str):
            raise TypeError("The place is required and must contain only characters")
        self._place = value
    
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not value or not isinstance(value, str):
            raise TypeError("User is required and must contain characters")
        self._user = value
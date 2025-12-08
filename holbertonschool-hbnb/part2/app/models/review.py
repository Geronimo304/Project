from app.models.Base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

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
    def place_id(self):
        return self._place_id
    
    @place_id.setter
    def place_id(self, value):
        if not isinstance(value, str):
            raise TypeError("The place_id is required and must be a string")
        self._place_id = value
    
    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not value or not isinstance(value, str):
            raise TypeError("User_id is required and must be a string")
        self._user_id = value
        self._user = value
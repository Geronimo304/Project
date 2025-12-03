from app.models.Base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
    
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
            raise ValueError("The price cannot be a negative number.")
        self._price = value


    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, float) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be a float between -90 and 90")
        self._latitude = value

    
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, float) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be a float between -180 and 180")
        self._longitude = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Owner is required and must be a string")
        self._owner = value
        
            
    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)
    
    def delate_review(self):
        if review 
    
    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def delete_amenity(self):

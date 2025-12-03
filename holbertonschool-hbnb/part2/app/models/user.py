from app.models.Base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
    
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("The name must be a string")
        if len(value) > 50:
            raise ValueError("Your name must be less than 50 characters")
        self._first_name = value


    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("The last name must be a string")
        if len(value) > 50:
            raise ValueError("Your last name must be less than 50 characters")
        self._last_name = value


    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not value
            raise ValueError("email is required")
        if "@" not value:
            raise ValueError("Invalid email format")
        self._email = value


    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value): 
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean value")

    def update(self, data):  #cambio
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'email' in data:
            self.email = data['email']
        if 'is_admin' in data:
            self.is_admin = data['is_admin']
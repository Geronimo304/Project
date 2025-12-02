from app.models.Base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def verify(self,):
        if not self.first_name or isinstance(self.first_name, str):
            raise ValueError("name is required")
        if len(self.first_name) > 50:
            raise ValueError("Your name must be less than 50 characters")
        
        if not self.last_name or isinstance(self.last_name, str):
            raise ValueError("last name is required")
        if len(self.last_name) > 50:
            raise ValueError("Your last name must be less than 50 characters")

        if not self.email:
            raise ValueError("email is required")
        if "@" not in self.email or "." not in self.email:
            raise ValueError("Invalid email format")
        
        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be a boolean value")

    def update(self, data):  #cambio
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'email' in data:
            self.email = data['email']
        if 'is_admin' in data:
            self.is_admin = data['is_admin']
from app.models.Base_model import BaseModel
from app import db, bcrypt


class User(BaseModel):
    __tablename__ = 'users'

    _first_name = db.Column('first_name', db.String(50), nullable=False)
    _last_name = db.Column('last_name', db.String(50), nullable=False)
    _email = db.Column('email', db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    _is_admin = db.Column('is_admin', db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        # keep constructor simple (student style)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
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
        if not value:
            raise ValueError("email is required")
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._email = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value): 
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean value")
        self._is_admin = value

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
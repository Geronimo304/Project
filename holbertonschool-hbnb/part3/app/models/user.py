from app.models.Base_model import BaseModel
from app import bcrypt, db


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='owner', lazy=True, foreign_keys='Place.owner_id')
    reviews = db.relationship('Review', backref='user', lazy=True, foreign_keys='Review.user_id')

    def __init__(self, first_name, last_name, email, is_admin=False, password=None):
        super().__init__()
        self._validate_first_name(first_name)
        self._validate_last_name(last_name)
        self._validate_email(email)
        self._validate_is_admin(is_admin)
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    @staticmethod
    def _validate_first_name(value):
        if not isinstance(value, str):
            raise TypeError("The name must be a string")
        if len(value) > 50:
            raise ValueError("Your name must be less than 50 characters")

    @staticmethod
    def _validate_last_name(value):
        if not isinstance(value, str):
            raise TypeError("The last name must be a string")
        if len(value) > 50:
            raise ValueError("Your last name must be less than 50 characters")

    @staticmethod
    def _validate_email(value):
        if not value:
            raise ValueError("email is required")
        if "@" not in value:
            raise ValueError("Invalid email format")

    @staticmethod
    def _validate_is_admin(value):
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean value")

    def hash_password(self, password):
        if password is None:
            self.password = None
            return
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def update(self, data):
        if 'first_name' in data:
            self._validate_first_name(data['first_name'])
            self.first_name = data['first_name']
        if 'last_name' in data:
            self._validate_last_name(data['last_name'])
            self.last_name = data['last_name']
        if 'email' in data:
            self._validate_email(data['email'])
            self.email = data['email']
        if 'is_admin' in data:
            self._validate_is_admin(data['is_admin'])
            self.is_admin = data['is_admin']
        self.save()
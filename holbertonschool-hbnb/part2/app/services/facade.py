from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity  # Agregar esta importación

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()  # Agregar repositorio de amenities

    # === Métodos de Usuario (existentes) ===
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    # === Métodos de Amenity (nuevos) ===
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        amenity.verify()  # Validar antes de guardar
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        
        amenity.update(amenity_data)
        amenity.verify()  # Validar después de actualizar
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity
from app.persistence.repository import SQLAlchemyRepository
from app.models.amenity import Amenity


class AmenityRepository(SQLAlchemyRepository):
    """Amenity-specific repository extending SQLAlchemyRepository"""
    
    def __init__(self):
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """Retrieve an amenity by its name"""
        return self.model.query.filter_by(name=name).first()

from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place


class PlaceRepository(SQLAlchemyRepository):
    """Place-specific repository extending SQLAlchemyRepository"""
    
    def __init__(self):
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        """Retrieve all places owned by a specific user"""
        return self.model.query.filter_by(owner_id=owner_id).all()

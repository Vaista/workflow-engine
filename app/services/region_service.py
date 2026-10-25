from sqlalchemy.orm import Session

from app.repositories.region_repository import RegionRepository
from app.schemas.auth import CurrentUser



class RegionService:
    def __init__ (
            self, 
            region_repository: RegionRepository,
            session: Session
    ):
        self.region_repository = region_repository
        self.session = session


    def get_all_regions(self, current_user: CurrentUser):
        """Get all regions"""
        return self.region_repository.get_all_regions()
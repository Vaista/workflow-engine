from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.region import Regions
from app.exceptions.exceptions.regions import InvalidRegionCodeException


class RegionRepository:
    """Region Repository"""
    
    def __init__(self, session: Session):
        self.session = session

    def get_by_codes(self, codes: list[str]):
        # Fetch the region by list of codes
    
        stmt = select(Regions).where(Regions.code.in_(codes))

        regions = self.session.execute(stmt)

        requested = set(codes)
        found = {region.code for region in regions}
        missing = requested - found

        if missing:
            raise InvalidRegionCodeException(missing)
        
        return regions
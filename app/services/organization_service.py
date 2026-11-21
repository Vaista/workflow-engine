from sqlalchemy.orm import Session

from app.exceptions.exceptions.regions import RegionNotFoundException
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.region_repository import RegionRepository
from app.schemas.organizations import OrganizationCreate, OrganizationUnitCreate
from app.exceptions.exceptions.organizations import OrganizationAlreadyExistsException, OrganizationNotFoundException, OrganizationUnitAlreadyExistsException


class OrganizationService:
    def __init__(
            self, 
            organization_repository: OrganizationRepository,
            region_repository: RegionRepository, 
            session: Session):
        self.session = session
        self.organization_repository = organization_repository
        self.region_repository = region_repository

    def get_organization(self, organization_id: int):
        return self.organization_repository.get_organization(organization_id)

    def create_organization(self, organization: OrganizationCreate):
        try:
            name = organization.name
            if self.organization_repository.get_organization_by_name(name):
                raise OrganizationAlreadyExistsException()
            org = self.organization_repository.create_organization(organization)
            self.session.commit()
            return org
        except Exception as e:
            self.session.rollback()
            raise e

    def create_organization_unit(self, organization_id: int, unit: OrganizationUnitCreate):
        try:
            org = self.organization_repository.get_organization(organization_id)
            region_code = unit.region_code
            region = self.region_repository.get_region_by_code(region_code)
            if not region: 
                raise RegionNotFoundException(region_code)
            name = unit.name
            address = unit.address
            if not org:
                raise OrganizationNotFoundException()
            unit_name = self.organization_repository.get_organization_unit_by_name(organization_id, region.region_id, name)
            if unit_name:
                raise OrganizationUnitAlreadyExistsException()
            unit = self.organization_repository.create_organization_unit(organization_id, unit, region.region_id)
            self.session.commit()
            return unit
        except Exception as e:
            self.session.rollback()
            raise e
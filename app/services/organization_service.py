from sqlalchemy.orm import Session

from app.repositories.organization_repository import OrganizationRepository
from app.schemas.organizations import OrganizationCreate
from app.exceptions.exceptions.organizations import OrganizationAlreadyExistsException


class OrganizationService:
    def __init__(
            self, 
            organization_repository: OrganizationRepository,
            session: Session):
        self.session = session
        self.organization_repository = organization_repository

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
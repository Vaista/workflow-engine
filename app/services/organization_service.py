from sqlalchemy.orm import Session

from app.repositories.organization_repository import OrganizationRepository


class OrganizationService:
    def __init__(
            self, 
            organization_repository: OrganizationRepository,
            session: Session):
        self.session = session
        self.organization_repository = organization_repository

    def get_organization(self, organization_id: int):
        # Placeholder for actual database retrieval logic
        return self.organization_repository.get_organization(organization_id)
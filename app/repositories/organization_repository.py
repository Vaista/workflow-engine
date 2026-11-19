from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.organization import Organizations
from app.schemas.organizations import OrganizationCreate


class OrganizationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_organization(self, organization_id: int):
        # Fetch the organization from the database using the provided organization_id

        stmt = select(Organizations).where(
            Organizations.org_id == organization_id
        )

        return self.session.execute(stmt).scalar_one_or_none()

    def get_organization_by_name(self, name: str):
        print(name)
        stmt = select(Organizations).where(
            Organizations.name == name.lower()
        )

        result =  self.session.execute(stmt).scalar_one_or_none()
        print(result)
        return result

    def create_organization(self, organization: OrganizationCreate):
        # Create a new organization in the database using the provided organization data
        name = organization.name.lower()
        new_organization = Organizations(
            name=name,
            address=organization.address
        )
        self.session.add(new_organization)
        self.session.flush()
        return new_organization
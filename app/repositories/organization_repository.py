from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.organization import Organizations, OrganizationUnits
from app.schemas.organizations import OrganizationCreate, OrganizationUnitCreate


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

    def create_organization_unit(self, organization_id: int, unit: OrganizationUnitCreate, region_id: int):
        # Create a new organization unit in the database using the provided unit data
        name = unit.name.lower()
        new_unit = OrganizationUnits(
            org_id=organization_id,
            name=name,
            address=unit.address,
            region_id=region_id
        )
        self.session.add(new_unit)
        self.session.flush()
        return new_unit

    def get_organization_unit_by_name(self, organization_id: int, region_id: int, name: str):
        # Fetch the organization unit from the database using the provided organization_id and unit name
        stmt = select(OrganizationUnits).where(
            OrganizationUnits.org_id == organization_id,
            OrganizationUnits.name == name.lower(),
            OrganizationUnits.region_id == region_id
        )

        return self.session.execute(stmt).scalar_one_or_none()

    def get_organization_unit_by_id(self, organization_id: int, unit_id: int):
        # Fetch the organization unit from the database using the provided organization_id and unit_id
        stmt = select(OrganizationUnits).where(
            OrganizationUnits.org_id == organization_id,
            OrganizationUnits.org_unit_id == unit_id
        )

        return self.session.execute(stmt).scalar_one_or_none()
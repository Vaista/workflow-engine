from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.organization import Organizations


class OrganizationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_organization(self, organization_id: int):
        # Fetch the organization from the database using the provided organization_id

        stmt = select(Organizations).where(
            Organizations.org_id == organization_id
        )

        return self.session.execute(stmt).scalar_one_or_none()
from sqlalchemy.orm import Session

from app.exceptions.exceptions.organizations import OrganizationNotFoundException, OrganizationUnitNotFoundException
from app.exceptions.exceptions.users import UserAlreadyExistsException
from app.repositories.user_repository import UserRepository
from app.repositories.organization_repository import OrganizationRepository
from app.schemas.users import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository, organization_repository: OrganizationRepository, session: Session):
        self.user_repository = user_repository
        self.organization_repository = organization_repository
        self.session = session

    def create_user(self, user_data: UserCreate):
        try:
            # Check if the user already exists
            existing_user = self.user_repository.get_user_by_email(user_data.email)
            if existing_user:
                raise UserAlreadyExistsException()
            # Check if valid organization_id is provided
            if user_data.org_id is not None:
                organization = self.organization_repository.get_organization(user_data.org_id)
                if not organization:
                    raise OrganizationNotFoundException("Invalid organization_id provided.")
            # Check if valid organization_unit_id is provided
            if user_data.org_unit_id is not None:
                organization_unit = self.organization_repository.get_organization_unit_by_id(user_data.org_id, user_data.org_unit_id)
                if not organization_unit:
                    raise OrganizationUnitNotFoundException()
            new_user = self.user_repository.create_user(user_data)
            self.session.commit()
            return new_user
        except Exception as e:
            self.session.rollback()
            raise e
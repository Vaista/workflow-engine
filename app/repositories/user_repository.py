from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import Users
from app.schemas.users import UserCreate
from app.core.security import hash_password


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str):
        stmt = select(Users).where(Users.email == email.strip().lower())
        result = self.session.execute(stmt).scalar_one_or_none()
        return result

    def create_user(self, user_data: UserCreate):
        user_data = user_data.model_dump()
        user_data['email'] = user_data['email'].strip().lower()
        password = user_data.pop('password')
        user_data['password_hash'] = hash_password(password)
        user = Users(**user_data)
        self.session.add(user)
        self.session.flush()
        return user
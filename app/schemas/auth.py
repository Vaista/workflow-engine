from pydantic import BaseModel, EmailStr
from uuid import UUID


class CurrentUser(BaseModel):
    user_id: UUID
    org_unit_id: int
    name: str
    email: EmailStr
    is_active: bool
    
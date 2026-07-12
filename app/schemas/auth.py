from pydantic import BaseModel, EmailStr
from uuid import UUID


class CurrentUser(BaseModel):
    user_id: UUID

    org_id: int
    org_unit_id: int

    name: str
    email: EmailStr

    roles: list[str]

    permissions: set[str]

    is_active: bool
    
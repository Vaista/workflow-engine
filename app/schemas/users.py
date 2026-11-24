from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Annotated
from uuid import UUID


class UserCreate(BaseModel):
    org_id: Annotated[int, Field(gt=0)]
    org_unit_id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(min_length=1, max_length=60)]
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=255)]
    contact: Annotated[str, Field(min_length=1, max_length=20)]
    country: Annotated[str, Field(min_length=1, max_length=20)]


class UserResponse(BaseModel):
    user_id: UUID
    org_id: int
    org_unit_id: int
    name: str
    email: EmailStr
    contact: str | None
    country: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
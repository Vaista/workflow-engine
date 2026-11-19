from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class OrganizationResponse(BaseModel):
    org_id: int
    name: str
    address: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)]
    address: str | None = Field(default=None, max_length=255)

    model_config = ConfigDict(from_attributes=True)
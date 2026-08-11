from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Annotated
from uuid import UUID

from app.utils.pagination import OrderBy


class WorkflowCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)]
    description: str | None = Field(default=None, max_length=255)
    region_codes: Annotated[list[str], Field(min_length=1)]


class WorkflowFetch(BaseModel):
    org_id: int
    org_unit_id: int | None = None
    name: str | None = None
    region: list[str] = None
    created_by: UUID | None = None
    order_by: list[OrderBy] = None
    limit: int = 25
    offset: int = 0


class FetchWorkflowResponse(BaseModel):
    id: int
    org_id: int | None = None
    org_name: str
    org_unit_id: int | None = None
    org_unit_name: str | None = None
    name: str | None = None
    description: str | None
    created_on: datetime | None = None
    created_by_name: str | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class WorkflowResponse(BaseModel):
    name: str
    description: str | None
    is_active: bool
    created_on: datetime
    region_codes: list[str]

    model_config = ConfigDict(from_attributes=True)


class WorkflowUpdateResponse(BaseModel):
    name: str
    description: str | None
    is_active: bool
    updated_on: datetime
    region_codes: list[str]

    model_config = ConfigDict(from_attributes=True)
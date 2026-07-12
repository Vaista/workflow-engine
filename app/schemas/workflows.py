from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated


class WorkflowCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)]
    description: str | None = Field(default=None, max_length=255)
    region_codes: Annotated[list[str], Field(min_length=1)]


class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool
    created_on: datetime
    region_codes: list[str]
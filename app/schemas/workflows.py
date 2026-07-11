from pydantic import BaseModel, Field
from typing import Annotated


class WorkflowCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)]
    description: str | None = Field(default=None, max_length=255)

from pydantic import BaseModel, Field
from typing import Annotated


class WorkflowStepCreate(BaseModel):
    step_number: int = Field(gt=0)
    step_name: Annotated[str, Field(min_length=3, max_length=30)]
    step_description: str | None = Field(default=None, max_length=255)
    step_config: dict
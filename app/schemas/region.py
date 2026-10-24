from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated


class RegionCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=10)]
    code: Annotated[str, Field(min_length=2, max_length=5)]


class RegionResponse(BaseModel):
    region_id: int
    name: str
    code: str

    model_config = ConfigDict(from_attributes=True)
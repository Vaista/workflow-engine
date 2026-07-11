from pydantic import BaseModel, Field
from typing import Annotated


class RegionCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=10)]
    code: Annotated[str, Field(min_length=2, max_length=5)]
    
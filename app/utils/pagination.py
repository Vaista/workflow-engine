from enum import Enum
from pydantic import BaseModel


class SortField(str, Enum):
    NAME = "name"
    CREATED_ON = "created_on"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class OrderBy(BaseModel):
    field: SortField
    order: SortOrder | None = None

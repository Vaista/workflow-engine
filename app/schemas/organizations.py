from pydantic import BaseModel, Field, ConfigDict


class OrganizationResponse(BaseModel):
    org_id: int
    name: str
    address: str

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    is_active: bool


class UserResponse(BaseModel):
    name: str
    email: EmailStr
    is_active: bool
from fastapi import APIRouter
from app.schemas.users import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}


@router.get("/")
async def list_users(page: int = 1, limit: int = 20):
    return {"page": page, "limit": limit}


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    return user

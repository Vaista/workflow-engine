from fastapi import APIRouter, status, Depends
from app.schemas.users import UserCreate, UserResponse
from app.services.user_service import UserService
from app.provider.services import get_user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@router.get("/")
def list_users(page: int = 1, limit: int = 20):
    return {"page": page, "limit": limit}


@router.post("/",  response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service)
    ):
    return user_service.create_user(user)

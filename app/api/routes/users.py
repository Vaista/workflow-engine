from fastapi import APIRouter, status, Depends
from app.schemas.users import UserCreate, UserResponse
from app.services.user_service import UserService
from app.provider.services import get_user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_email}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_email: str, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user_by_email(user_email)
    return user


@router.get("/")
def list_users(page: int = 1, limit: int = 20):
    return {"page": page, "limit": limit}


@router.post("/",  response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service)
    ):
    return user_service.create_user(user)

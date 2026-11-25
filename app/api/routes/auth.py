from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.deps import get_db
from app.provider.auth import get_current_user
from app.schemas.auth import CurrentUser, LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.provider.services import get_auth_service
from app.core.security import create_access_token
from app.core.config import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/me", response_model=CurrentUser)
def me(
    user: Annotated[CurrentUser, Depends(get_current_user)],
):
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.authenticate_user(
        credentials.email,
        credentials.password,
    )

    token = create_access_token(
        user_id=str(user.user_id),
        secret_key=settings.JWT_SECRET,
    )

    return TokenResponse(access_token=token)
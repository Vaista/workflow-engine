from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt


from app.repositories.user_repository import UserRepository
from app.provider.services import get_user_repository
from app.core.security import decode_access_token
from app.core.config import settings


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
):
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(
            credentials.credentials,
            settings.JWT_SECRET,
        )

        if payload.get("type") != "access":
            raise unauthorized

        user_id = UUID(payload["sub"])

    except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
        raise unauthorized

    user = user_repository.get_by_id(user_id)

    if user is None or not user.is_active:
        raise unauthorized

    return user


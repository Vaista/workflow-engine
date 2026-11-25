from fastapi import HTTPException, status

from app.core.security import verify_password


class AuthService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def authenticate_user(self, email: str, password: str):
        user = self.user_repository.get_user_by_email(
            email.strip().lower()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )

        return user
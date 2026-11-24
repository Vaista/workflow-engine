from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions.users import UserAlreadyExistsException


def register_user_handlers(app: FastAPI):

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "code": "USER_ALREADY_EXISTS",
                    "message": "User with this email already exists."
                }
            },
        )
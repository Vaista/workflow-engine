from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions.users import UserAlreadyExistsException, UserNotFoundException


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

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "USER_NOT_FOUND",
                    "message": "User not found."
                }
            },
        )
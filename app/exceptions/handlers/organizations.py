from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions.organizations import (
    OrganizationAlreadyExistsException
)


def register_organization_handlers(app: FastAPI):

    @app.exception_handler(OrganizationAlreadyExistsException)
    async def organization_exists(
        request: Request,
        exc: OrganizationAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "code": "ORGANIZATION_ALREADY_EXISTS",
                    "message": "Organization already exists.",
                }
            },
        )
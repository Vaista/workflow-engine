from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions.organizations import (
    OrganizationAlreadyExistsException,
    OrganizationNotFoundException,
    OrganizationUnitAlreadyExistsException
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

    @app.exception_handler(OrganizationNotFoundException)
    async def organization_not_found(
        request: Request,
        exc: OrganizationNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "ORGANIZATION_NOT_FOUND",
                    "message": "Organization not found.",
                }
            },
        )

    @app.exception_handler(OrganizationUnitAlreadyExistsException)
    async def organization_unit_exists(
        request: Request,
        exc: OrganizationUnitAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "code": "ORGANIZATION_UNIT_ALREADY_EXISTS",
                    "message": "Organization unit already exists.",
                }
            },
        )
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions.regions import InvalidRegionCodeException, RegionNotFoundException


def register_region_handler(app: FastAPI):
    
    @app.exception_handler(InvalidRegionCodeException)
    async def region_exists(
        request: Request,
        exc: InvalidRegionCodeException,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "code": "INVALID_REGION_CODE",
                    "message": "Invalid Region provided.",
                    "regions": f"{exc.region_codes}"
                }
            },
        )

    @app.exception_handler(RegionNotFoundException)
    async def region_not_found(
        request: Request,
        exc: RegionNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "REGION_NOT_FOUND",
                    "message": f"Region with code '{exc.region_code}' not found."
                }
            },
        )
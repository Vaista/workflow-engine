from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions.regions import InvalidRegionCodeException


def register_region_handler(app: FastAPI):
    
    @app.exception_handler(InvalidRegionCodeException)
    async def workflow_exists(
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
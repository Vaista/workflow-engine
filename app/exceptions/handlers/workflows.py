from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions.workflows import (
    WorkflowAlreadyExists,
    WorkflowNotFound,
    WorkflowCreationFailed
)


def register_workflow_handlers(app: FastAPI):

    @app.exception_handler(WorkflowAlreadyExists)
    async def workflow_exists(
        request: Request,
        exc: WorkflowAlreadyExists,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "code": "WORKFLOW_ALREADY_EXISTS",
                    "message": "Workflow already exists.",
                }
            },
        )

    @app.exception_handler(WorkflowNotFound)
    async def workflow_not_found(
        request: Request,
        exc: WorkflowNotFound,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "WORKFLOW_NOT_FOUND",
                    "message": "Workflow not found.",
                }
            },
        )
        
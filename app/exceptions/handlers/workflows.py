from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions.workflows import (
    WorkflowAlreadyExists,
    WorkflowNotFound,
    DuplicateWorkflowStepNumber,
    InvalidWorkflowStepNumber
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
        
    @app.exception_handler(DuplicateWorkflowStepNumber)
    async def duplicate_workflow_step_number(
        request: Request,
        exc: DuplicateWorkflowStepNumber,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "code": "DUPLICATE_WORKFLOW_STEP_NUMBER",
                    "message": "Duplicate workflow step number.",
                }
            },
        )

    @app.exception_handler(InvalidWorkflowStepNumber)
    async def invalid_workflow_step_number(
        request: Request,
        exc: InvalidWorkflowStepNumber,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": "INVALID_WORKFLOW_STEP_NUMBER",
                    "message": "Invalid workflow step number. The step number must be greater than the last step number for the given workflow.",
                }
            },
        )

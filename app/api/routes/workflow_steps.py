from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user
from app.provider.services import get_workflow_step_service
from app.provider.services import get_workflow_step_service
from app.schemas.auth import CurrentUser
from app.schemas.workflow_steps import WorkflowStepCreate, WorkflowStepResult
from app.services.workflow_step_service import WorkflowStepService


workflow_steps_router = APIRouter(prefix="/workflow", tags=["Workflow Steps"])


@workflow_steps_router.post(
        "/steps",
        response_model=WorkflowStepResult,
        status_code=status.HTTP_200_OK
    )
async def create_workflow_steps(
    workflow_id: int, 
    step: WorkflowStepCreate,
    current_user: CurrentUser = Depends(get_current_user),
    workflow_step_service: WorkflowStepService = Depends(get_workflow_step_service)
    ):

    result = workflow_step_service.create_workflow_step(workflow_id, step)

    response = {"message": "Workflow step created successfully", "data": result}

    return response


@workflow_steps_router.post(
    "/steps/update", 
    response_model=WorkflowStepResult, 
    status_code=status.HTTP_200_OK
    )
def update_workflow_steps(
    workflow_id: int,
    step: WorkflowStepCreate,
    current_user: CurrentUser = Depends(get_current_user),
    workflow_step_service: WorkflowStepService = Depends(get_workflow_step_service)
    ):

    result = workflow_step_service.update_workflow_step(workflow_id, step)

    response = {"message": "Workflow step updated successfully", "data": result}

    return response


@workflow_steps_router.delete(
    "/steps", 
    response_model=WorkflowStepResult,
    status_code=status.HTTP_200_OK
    )
def delete_workflow_steps(
    workflow_id: int,
    step_number: int,
    current_user: CurrentUser = Depends(get_current_user),
    workflow_step_service: WorkflowStepService = Depends(get_workflow_step_service)
    ):

    result = workflow_step_service.delete_workflow_step(workflow_id, step_number)

    response = {"message": "Workflow step deleted successfully", "data": result}

    return response
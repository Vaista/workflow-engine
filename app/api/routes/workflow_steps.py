from fastapi import APIRouter, Depends, status

from app.provider.services import get_workflow_step_service
from app.provider.services import get_workflow_step_service
from app.schemas.workflow_steps import WorkflowStepCreate, WorkflowStepResponse
from app.services.workflow_step_service import WorkflowStepService


workflow_steps_router = APIRouter(prefix="/workflow", tags=["Workflow Steps"])


@workflow_steps_router.post(
        "/steps",
        response_model=WorkflowStepResponse,
        status_code=status.HTTP_200_OK
    )
async def create_workflow_steps(
    workflow_id: int, 
    step: WorkflowStepCreate,
    workflow_step_service: WorkflowStepService = Depends(get_workflow_step_service)
    ):

    response = workflow_step_service.create_workflow_step(workflow_id, step)
    return response
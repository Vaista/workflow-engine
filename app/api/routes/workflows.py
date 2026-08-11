from fastapi import APIRouter, Depends, status


from app.services.workflow_service import WorkflowService
from app.schemas.workflows import WorkflowResponse, WorkflowCreate, WorkflowFetch, FetchWorkflowResponse, WorkflowUpdateResponse
from app.schemas.auth import CurrentUser
from app.api.deps import get_current_user
from app.provider.services import get_workflow_service


router = APIRouter(prefix="/workflows", tags=["Workflows"])



@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=list[FetchWorkflowResponse]
)
async def fetch_workflows(
    workflow: WorkflowFetch,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    
    return workflow_service.fetch_workflow(workflow)


@router.post(
    "/", 
    response_model=WorkflowResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_workflow(
    workflow: WorkflowCreate,
    current_user: CurrentUser = Depends(get_current_user),
    workflow_service: WorkflowService = Depends(get_workflow_service)
):

    created_workflow = workflow_service.create_workflow(workflow, current_user)

    response = WorkflowResponse(
        name=created_workflow.name,
        description=created_workflow.description,
        is_active=created_workflow.is_active,
        created_on=created_workflow.created_on,
        region_codes=workflow.region_codes
    )

    return response


@router.post(
    "/{workflow_id}/update",
    response_model=WorkflowUpdateResponse,
    status_code=status.HTTP_200_OK
)
async def update_workflow(
    workflow_id: int,
    workflow: WorkflowCreate,
    current_user: CurrentUser = Depends(get_current_user),
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    updated_workflow = workflow_service.update_workflow(workflow_id, workflow, current_user)

    response = WorkflowUpdateResponse(
        name=updated_workflow.name,
        description=updated_workflow.description,
        is_active=updated_workflow.is_active,
        updated_on=updated_workflow.updated_on,
        region_codes=workflow.region_codes
    )

    return response


@router.delete(
    "/{workflow_id}",
    status_code=status.HTTP_200_OK
)
async def delete_workflow(
    workflow_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    result = workflow_service.delete_workflow(workflow_id, current_user)

    return result
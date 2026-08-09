from app.schemas.workflows import WorkflowResponse, FetchWorkflowResponse

from datetime import datetime
from uuid import UUID


def workflow_response(**kwargs):

    response = WorkflowResponse(
        name="Leave Approval",
        description="Leave workflow",
        is_active=True,
        created_on=datetime.now(),
        region_codes=["APAC"],
    )

    return response.model_copy(
        update=kwargs
    )


def fetch_workflow_response(**kwargs):

    response = FetchWorkflowResponse(
        id=1,
        org_id=1,
        org_name='Organization Name',
        org_unit_id=1,
        org_unit_name="Organization Unit",
        name="Test Workflow",
        description='Test Description',
        created_on=datetime.now(),
        created_by_name="Test User",
        created_by=UUID("123e4567-e89b-12d3-a456-426614174000"),
        is_active=True
    )

    return response.model_copy(
        update=kwargs
    )
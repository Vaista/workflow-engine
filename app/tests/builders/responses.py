from app.schemas.workflows import WorkflowResponse

from datetime import datetime


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
import pytest

from app.models.workflow import Workflow, WorkflowRegion


@pytest.fixture
def workflow_factory(db_session, current_user):
    """
    Factory for creating Workflow model instances.

    Usage:
        workflow = workflow_factory()
        workflow = workflow_factory(name="Expense Approval")
        workflow = workflow_factory(is_deleted=True)
    """

    def create_workflow(**kwargs):

        regions = kwargs.pop("regions", [])

        data = {
            "org_id": current_user.org_id,
            "org_unit_id": current_user.org_unit_id,
            "name": "Test Workflow",
            "description": "Test Description",
            "created_by": current_user.user_id,
        }

        data.update(kwargs)

        workflow = Workflow(**data)

        db_session.add(workflow)

        # Writes to DB without committing.
        db_session.flush()

        # Populates generated fields like id.
        db_session.refresh(workflow)

        for region in regions:
            workflow_region = WorkflowRegion(workflow_id = workflow.id, region_id=region.region_id)
            db_session.add(workflow_region)

        # Writes to DB without committing.
        db_session.flush()

        return workflow

    return create_workflow
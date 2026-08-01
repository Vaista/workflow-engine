import pytest

from app.models.workflow import Workflow


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

        return workflow

    return create_workflow
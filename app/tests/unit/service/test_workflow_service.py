from app.schemas.workflows import WorkflowCreate
from app.schemas.auth import CurrentUser
from app.models.workflow import Workflow

from unittest.mock import Mock
import uuid


def test_create_workflow_success(
    workflow_service,
    workflow_repo,
    region_repo, 
    workflow_region_repo, 
    session        
):
    # Test the happy path

    # Arrange
    workflow_repo.get_workflow_by_name_and_org_unit.return_value = None
    
    workflow_to_create = WorkflowCreate(
        name='Test Workflow',
        description='Test Description',
        region_codes=['IND', 'UK']
    )

    created_workflow = Workflow(
        id=1,
        org_id=123,
        org_unit_id=123456,
        name='Test Workflow',
        description='Test Description',
        created_by='12345'
    )

    user_id = str(uuid.uuid4())

    current_user = CurrentUser(
        user_id=user_id,
        org_id=123,
        org_unit_id=123456,
        name="Vaibhav",
        email="test@test.com",
        is_active=True,
        roles=[],
        permissions=[]
    )

    regions = [
        Mock(id=1),
        Mock(id=2)
    ]

    region_repo.get_by_codes.return_value = regions

    workflow_repo.create_new_workflow.return_value = created_workflow

    result = workflow_service.create_workflow(workflow_to_create, current_user)

    workflow_repo.get_workflow_by_name_and_org_unit.assert_called_once()
    workflow_repo.create_new_workflow.assert_called_once()

    region_repo.get_by_codes.assert_called_once()

    workflow_region_repo.create_workflow_region_mapping.assert_called_once_with(
        created_workflow,
        regions
    )

    session.commit.assert_called_once()
    session.rollback.assert_not_called()

    assert result == created_workflow
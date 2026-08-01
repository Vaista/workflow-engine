from app.schemas.workflows import WorkflowCreate
from app.schemas.auth import CurrentUser
from app.models.workflow import Workflow
from app.exceptions.exceptions.workflows import WorkflowAlreadyExists
from app.exceptions.exceptions.regions import InvalidRegionCodeException

from unittest.mock import Mock
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
import uuid
import pytest


def test_create_workflow_success(
    mock_workflow_service,
    mock_workflow_repo,
    mock_region_repo, 
    mock_workflow_region_repo, 
    mock_session        
):

    mock_workflow_repo.get_workflow_by_name_and_org_unit.return_value = None
    
    workflow_to_create = WorkflowCreate(
        name='Test Workflow',
        description='Test Description',
        region_codes=['IND', 'UK']
    )

    user_id = str(uuid.uuid4())

    created_workflow = Workflow(
        id=1,
        org_id=123,
        org_unit_id=123456,
        name='Test Workflow',
        description='Test Description',
        created_by=user_id
    )

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

    mock_region_repo.get_by_codes.return_value = regions

    mock_workflow_repo.create_new_workflow.return_value = created_workflow

    result = mock_workflow_service.create_workflow(workflow_to_create, current_user)

    mock_workflow_repo.get_workflow_by_name_and_org_unit.assert_called_once()
    mock_workflow_repo.create_new_workflow.assert_called_once()

    mock_region_repo.get_by_codes.assert_called_once()

    mock_workflow_region_repo.create_workflow_region_mapping.assert_called_once_with(
        created_workflow,
        regions
    )

    mock_session.commit.assert_called_once()
    mock_session.rollback.assert_not_called()

    assert result == created_workflow


def test_create_workflow_returns_WorkflowAlreadyExists_Exception(
    mock_workflow_service,
    mock_workflow_repo
):

    user_id = str(uuid.uuid4())

    workflow = Workflow(
        id=1,
        org_id=123,
        org_unit_id=123456,
        name='Test Workflow',
        description='Test Description',
        created_by=user_id
    )

    mock_workflow_repo.get_workflow_by_name_and_org_unit.return_value = workflow

    workflow_to_create = WorkflowCreate(
        name='Test Workflow',
        description='Test Description',
        region_codes=['IND', 'UK']
    )

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

    with pytest.raises(WorkflowAlreadyExists) as exc_info:
        mock_workflow_service.create_workflow(workflow_to_create, current_user)

    assert exc_info.type is WorkflowAlreadyExists


def test_create_workflow_empty_region_Exception():

    with pytest.raises(ValidationError) as exc_info:
        WorkflowCreate(
            name="Test Workflow",
            description="Test Description",
            region_codes=[]
        )

    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("region_codes",)
    assert errors[0]["type"] == "too_short"


def test_create_workflow_invalid_region_return_Exception(
    mock_workflow_service,
    mock_workflow_repo,
    mock_region_repo
):
    mock_workflow_repo.get_workflow_by_name_and_org_unit.return_value = None
        
    workflow_to_create = WorkflowCreate(
        name='Test Workflow',
        description='Test Description',
        region_codes=['IND', 'UK']
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

    mock_region_repo.get_by_codes.side_effect = InvalidRegionCodeException(workflow_to_create.region_codes)

    with pytest.raises(InvalidRegionCodeException) as exc_info:
        mock_workflow_service.create_workflow(workflow_to_create, current_user)

    assert exc_info.type == InvalidRegionCodeException


def test_create_workflow_SQLAlchemy_Exception(
    mock_workflow_service,
    mock_workflow_repo,
    mock_region_repo, 
    mock_session
):
    mock_workflow_repo.get_workflow_by_name_and_org_unit.return_value = None
        
    workflow_to_create = WorkflowCreate(
        name='Test Workflow',
        description='Test Description',
        region_codes=['IND', 'UK']
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

    mock_region_repo.get_by_codes.return_value = regions
    mock_session.commit.side_effect = SQLAlchemyError("Database error")

    with pytest.raises(SQLAlchemyError):
        mock_workflow_service.create_workflow(workflow_to_create, current_user)

    mock_session.rollback.assert_called_once()
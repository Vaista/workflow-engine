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
    workflow_service,
    workflow_repo,
    region_repo, 
    workflow_region_repo, 
    session        
):

    workflow_repo.get_workflow_by_name_and_org_unit.return_value = None
    
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


def test_create_workflow_returns_WorkflowAlreadyExists_Exception(
    workflow_service,
    workflow_repo
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

    workflow_repo.get_workflow_by_name_and_org_unit.return_value = workflow

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
        workflow_service.create_workflow(workflow_to_create, current_user)

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
    workflow_service,
    workflow_repo,
    region_repo
):
    workflow_repo.get_workflow_by_name_and_org_unit.return_value = None
        
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

    region_repo.get_by_codes.side_effect = InvalidRegionCodeException(workflow_to_create.region_codes)

    with pytest.raises(InvalidRegionCodeException) as exc_info:
        workflow_service.create_workflow(workflow_to_create, current_user)

    assert exc_info.type == InvalidRegionCodeException


def test_create_workflow_SQLAlchemy_Exception(
    workflow_service,
    workflow_repo,
    region_repo, 
    session
):
    workflow_repo.get_workflow_by_name_and_org_unit.return_value = None
        
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

    region_repo.get_by_codes.return_value = regions
    session.commit.side_effect = SQLAlchemyError("Database error")

    with pytest.raises(SQLAlchemyError):
        workflow_service.create_workflow(workflow_to_create, current_user)

    session.rollback.assert_called_once()
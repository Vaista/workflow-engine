from app.repositories.workflow_repository import WorkflowRepository, WorkflowRegionRepository
from app.models.workflow import Workflow

from sqlalchemy import select


def test_create_workflow_generates_id(db_session, workflow_factory):

    # Create workflow
    new_workflow = workflow_factory()

    # Act
    repo = WorkflowRepository(db_session)
    created = repo.create_new_workflow(new_workflow)

    # Assert
    assert created.id is not None


def test_get_workflow_by_id_fetch_workflow(db_session, workflow_factory):

    # Create workflow
    new_workflow = workflow_factory()

    # Act
    repo = WorkflowRepository(db_session)
    created = repo.create_new_workflow(new_workflow)
    created_workflow_id = int(created.id)

    # Act
    fetched_workflow = repo.get_workflow_by_id(created_workflow_id)

    # Assert
    assert fetched_workflow.id == created_workflow_id


def test_get_workflow_by_id_fetch_None(db_session):

    repo = WorkflowRepository(db_session)

    fetched_workflow = repo.get_workflow_by_id(99999)

    assert fetched_workflow is None


def test_get_workflow_by_id_fetch_deleted_workflow_returns_None(db_session, workflow_factory):

    repo = WorkflowRepository(db_session)

    new_workflow = workflow_factory(is_deleted=True)

    created = repo.create_new_workflow(new_workflow)
    workflow_id = int(created.id)

    fetched_workflow = repo.get_workflow_by_id(workflow_id)

    assert fetched_workflow is None


def test_list_all_workflows_return_list_of_workflows(db_session, workflow_factory):
    
    repo = WorkflowRepository(db_session)

    # Arrange
    for i in range(1, 4):
        # Create workflow
        new_workflow = workflow_factory(name=f"Test Workflow - {i}", description=f"Test Workflow Description - {i}")

        created = repo.create_new_workflow(new_workflow)

    # Act
    workflow_list = repo.list_all_workflows()

    # Assert
    assert len(workflow_list) == 3


def test_list_all_workflows_returns_None(db_session):
    
    # Arrange
    repo = WorkflowRepository(db_session)

    # Act
    workflow_list = repo.list_all_workflows()

    # Assert
    assert len(workflow_list) == 0


def test_list_all_workflows_returns_active_workflows(db_session, workflow_factory):
    
    # Arrange
    repo = WorkflowRepository(db_session)

    for i in range(1, 4):
        is_deleted = False
        if i == 2:
            is_deleted = True
        # Create workflow
        new_workflow = workflow_factory(name=f"Test Workflow - {i}", description=f"Test Workflow Description - {i}", is_deleted=is_deleted)

        created = repo.create_new_workflow(new_workflow)

    # Act
    workflow_list = repo.list_all_workflows()

    # Assert
    assert len(workflow_list) == 2


def test_get_workflow_by_name_and_org_unit_return_workflow(db_session, workflow_factory):

    # Create workflow
    new_workflow = workflow_factory()

    repo = WorkflowRepository(db_session)
    created = repo.create_new_workflow(new_workflow)
    
    workflow_id = created.id

    # Act
    returned_workflow = repo.get_workflow_by_name_and_org_unit(name=created.name, org_unit_id=created.org_unit_id)

    # Assert
    assert workflow_id == returned_workflow.id


def test_get_workflow_by_name_and_org_unit_returns_None(db_session, workflow_factory):

    # Create workflow
    new_workflow = workflow_factory()

    repo = WorkflowRepository(db_session)
    created = repo.create_new_workflow(new_workflow)
    
    workflow_id = created.id

    # Act
    returned_workflow = repo.get_workflow_by_name_and_org_unit(name='Workflow 2', org_unit_id=created.org_unit_id)

    # Assert
    assert returned_workflow is None


def test_get_workflow_by_name_and_org_unit_fetch_deleted_workflow_returns_None(db_session, workflow_factory):

    # Create workflow
    new_workflow = workflow_factory(is_deleted=True)

    repo = WorkflowRepository(db_session)
    created = repo.create_new_workflow(new_workflow)

    # Act
    returned_workflow = repo.get_workflow_by_name_and_org_unit(name=created.name, org_unit_id=created.org_unit_id)

    # Assert
    assert returned_workflow is None

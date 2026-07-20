import pytest
from unittest.mock import Mock

from app.services.workflow_service import WorkflowService


@pytest.fixture
def workflow_repo():
    return Mock()


@pytest.fixture
def region_repo():
    return Mock()


@pytest.fixture
def workflow_region_repo():
    return Mock()


@pytest.fixture
def session():
    return Mock()


@pytest.fixture
def workflow_service(workflow_repo,
    region_repo,
    workflow_region_repo,
    session
):
    return WorkflowService(
        workflow_repo,
        region_repo,
        workflow_region_repo,
        session,
    )
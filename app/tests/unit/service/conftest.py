import pytest
from unittest.mock import Mock

from app.services.workflow_service import WorkflowService


@pytest.fixture
def mock_workflow_repo():
    return Mock()


@pytest.fixture
def mock_region_repo():
    return Mock()


@pytest.fixture
def mock_workflow_region_repo():
    return Mock()


@pytest.fixture
def mock_session():
    return Mock()


@pytest.fixture
def mock_workflow_service(
    mock_workflow_repo,
    mock_region_repo,
    mock_workflow_region_repo,
    mock_session
):
    return WorkflowService(
        mock_workflow_repo,
        mock_region_repo,
        mock_workflow_region_repo,
        mock_session,
    )
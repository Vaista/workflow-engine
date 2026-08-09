import pytest
from fastapi.testclient import TestClient
from uuid import UUID

from app.provider.services import get_workflow_service
from app.schemas.auth import CurrentUser
from app.api.deps import get_current_user
from app.main import app


fake_user = CurrentUser(
    user_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
    org_id=1,
    org_unit_id=1,
    name="John Doe",
    email="john@example.com",
    is_active=True,
    roles=[],
    permissions=[],
)

async def override_current_user():
    return fake_user


class FakeWorkflowService:

    def __init__(self):
        self.result = None
        self.exception = None

    def create_workflow(self, workflow, current_user):

        if self.exception:
            raise self.exception

        return self.result

    def fetch_workflow(self, workflow):

        if self.exception:
            raise self.exception

        return self.result


@pytest.fixture
def fake_workflow_service():
    fake_service = FakeWorkflowService()
    return fake_service


@pytest.fixture
def mock_client(fake_workflow_service):

    app.dependency_overrides[get_workflow_service] = lambda: fake_workflow_service
    app.dependency_overrides[get_current_user] = override_current_user

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
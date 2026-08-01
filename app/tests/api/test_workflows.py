from fastapi.testclient import TestClient
from uuid import UUID
from datetime import datetime

from app.main import app

from app.provider.services import get_workflow_service
from app.exceptions.exceptions.workflows import WorkflowAlreadyExists
from app.exceptions.exceptions.regions import InvalidRegionCodeException
from app.api.deps import get_current_user
from app.schemas.auth import CurrentUser
from app.schemas.workflows import WorkflowResponse


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


class FakeWorkflowService():

    def __init__(self, result=None, exception=None):
        self.result = result
        self.exception = exception

    def create_workflow(self, workflow, current_user):

        if self.exception:
            raise self.exception

        return self.result


client = TestClient(app)


def test_create_workflow_returns_201_success():

    response = WorkflowResponse(
        name="Leave Approval",
        description="Leave Workflow",
        is_active=True,
        created_on=datetime.now(),
        region_codes=["APAC"]
    )

    fake_service = FakeWorkflowService(result=response)

    app.dependency_overrides[get_workflow_service] = lambda: fake_service
    app.dependency_overrides[get_current_user] = override_current_user

    payload = {
        "name": "Leave Approval",
        "description": "Leave workflow",
        "region_codes": ["APAC"]
    }

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 201

    app.dependency_overrides.clear()


def test_create_workflow_returns_409_when_duplicate():

    fake_service = FakeWorkflowService(exception=WorkflowAlreadyExists)

    app.dependency_overrides[get_workflow_service] = lambda: fake_service
    app.dependency_overrides[get_current_user] = override_current_user

    payload = {
        "name": "Leave Approval",
        "description": "Leave workflow",
        "region_codes": ["APAC"]
    }

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 409

    assert response.json() == {
        "error": {
            "code": "WORKFLOW_ALREADY_EXISTS",
            "message": "Workflow already exists."
        }
    }

    app.dependency_overrides.clear()


def test_create_workflow_returns_409_invalid_regions():

    regions = ["APAC", "APAC2"]

    payload = {
        "name": "Leave Approval",
        "description": "Leave workflow",
        "region_codes": regions
    }

    fake_service = FakeWorkflowService(exception=InvalidRegionCodeException(payload['region_codes']))

    app.dependency_overrides[get_workflow_service] = lambda: fake_service
    app.dependency_overrides[get_current_user] = override_current_user

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 409

    assert response.json() == {
        "error": {
            "code": "INVALID_REGION_CODE",
            "message": "Invalid Region provided.",
            "regions": f"{sorted(regions)}"
        }
    }

    app.dependency_overrides.clear()


def test_create_workflow_returns_423_missing_regions():

    fake_service = FakeWorkflowService()

    app.dependency_overrides[get_workflow_service] = lambda: fake_service
    app.dependency_overrides[get_current_user] = override_current_user

    payload = {
        "name": "Leave Approval",
        "description": "Leave workflow",
        "region_codes": []
    }

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 422

    app.dependency_overrides.clear()
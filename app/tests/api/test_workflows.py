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
from app.tests.builders.responses import workflow_response
from app.tests.builders.workflow_payload import workflow_payload


def test_create_workflow_returns_201_success(fake_workflow_service, mock_client):

    payload = workflow_payload()

    response = workflow_response(name=payload['name'], description=payload['description'], region_codes=payload['region_codes'])

    fake_workflow_service.result = response

    response = mock_client.post("/workflows/", json=payload)

    assert response.status_code == 201


def test_create_workflow_returns_409_when_duplicate(fake_workflow_service, mock_client):

    payload = workflow_payload()

    fake_workflow_service.exception = WorkflowAlreadyExists()

    response = mock_client.post("/workflows/", json=payload)

    assert response.status_code == 409

    assert response.json() == {
        "error": {
            "code": "WORKFLOW_ALREADY_EXISTS",
            "message": "Workflow already exists."
        }
    }


def test_create_workflow_returns_409_invalid_regions(fake_workflow_service, mock_client):

    regions = ["APAC", "APAC2"]

    payload = workflow_payload(region_codes=["APAC", "APAC2"])

    fake_workflow_service.exception = InvalidRegionCodeException(payload['region_codes'])

    response = mock_client.post("/workflows/", json=payload)

    assert response.status_code == 409

    assert response.json() == {
        "error": {
            "code": "INVALID_REGION_CODE",
            "message": "Invalid Region provided.",
            "regions": f"{sorted(regions)}"
        }
    }


def test_create_workflow_returns_423_missing_regions(mock_client):

    payload = workflow_payload(region_codes=[])

    response = mock_client.post("/workflows/", json=payload)

    assert response.status_code == 422
    
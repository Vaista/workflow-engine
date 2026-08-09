from app.exceptions.exceptions.workflows import WorkflowAlreadyExists
from app.exceptions.exceptions.regions import InvalidRegionCodeException
from app.tests.builders.responses import workflow_response, fetch_workflow_response
from app.tests.builders.workflow_payload import create_workflow_payload, search_workflow_payload


def test_create_workflow_returns_201_success(fake_workflow_service, mock_client):

    payload = create_workflow_payload()

    response = workflow_response(name=payload['name'], description=payload['description'], region_codes=payload['region_codes'])

    fake_workflow_service.result = response

    response = mock_client.post("/workflows/", json=payload)

    assert response.status_code == 201


def test_create_workflow_returns_409_when_duplicate(fake_workflow_service, mock_client):

    payload = create_workflow_payload()

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

    payload = create_workflow_payload(region_codes=["APAC", "APAC2"])

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

    payload = create_workflow_payload(region_codes=[])

    response = mock_client.post("/workflows/", json=payload)

    assert response.status_code == 422


def test_fetch_workflow_returns_workflow(fake_workflow_service, mock_client):

    response = fetch_workflow_response(org_id=1, name='Workflow')

    fake_workflow_service.result = [response]

    payload = search_workflow_payload(org_id=1, name='Workflow', region=['R1'])

    response = mock_client.post("/workflows/search", json=payload)

    assert response.status_code == 200


def test_fetch_workflow_returns_ValidationError(fake_workflow_service, mock_client):

    payload = search_workflow_payload(org_id=1, name='Workflow', region='R1')

    response = mock_client.post("/workflows/search", json=payload)

    assert response.status_code == 422
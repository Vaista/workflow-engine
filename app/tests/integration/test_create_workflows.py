from sqlalchemy import select

from app.models.workflow import Workflow


def test_create_workflow_success(db_session, client):

    payload = {
        "name": "Leave Approval",
        "description": "Leave workflow",
        "region_codes": ["APAC"],
    }

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 201

    workflow = db_session.scalar(
        select(Workflow).where(Workflow.name == "Leave Approval")
    )

    assert workflow is not None
    assert workflow.description == "Leave workflow"
    assert workflow.org_id == 1



def test_create_workflow_missing_regions(client):

    payload = {
        "name": "Leave Approval",
        "description": "Leave workflow",
        "region_codes": [],
    }

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 422


def test_create_workflow_duplicate_workflow(client):

    payload = {
        "name": "Test Workflow",
        "description": "Leave workflow",
        "region_codes": [],
    }

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 422
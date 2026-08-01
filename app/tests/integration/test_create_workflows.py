from sqlalchemy import select

from app.models.workflow import Workflow
from app.tests.builders.workflow_payload import workflow_payload


def test_create_workflow_success(db_session, client):

    payload = workflow_payload()

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 201

    workflow = db_session.scalar(
        select(Workflow).where(Workflow.name == "Leave Approval")
    )

    assert workflow is not None
    assert workflow.description == "Leave workflow"
    assert workflow.org_id == 1



def test_create_workflow_missing_regions(client):

    payload = workflow_payload(region_codes=[])

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 422


def test_create_workflow_duplicate_workflow(client, db_session, workflow_factory):

    payload = workflow_payload(name="Test Workflow")

    new_workflow = workflow_factory(name="Test Workflow", description="Test Workflow Description")

    db_session.add(new_workflow)
    db_session.commit()

    db_session.refresh(new_workflow)

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 409
from sqlalchemy import select

from app.models.workflow import Workflow
from app.tests.builders.workflow_payload import create_workflow_payload


def test_create_workflow_success(db_session, client):

    payload = create_workflow_payload()

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 201

    workflow = db_session.scalar(
        select(Workflow).where(Workflow.name == "Leave Approval")
    )

    assert workflow is not None
    assert workflow.description == "Leave workflow"
    assert workflow.org_id == 1



def test_create_workflow_missing_regions(client):

    payload = create_workflow_payload(region_codes=[])

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 422


def test_create_workflow_duplicate_workflow(client, db_session, workflow_factory):

    payload = create_workflow_payload(name="Test Workflow")

    new_workflow = workflow_factory(name="Test Workflow", description="Test Workflow Description")

    db_session.add(new_workflow)
    db_session.commit()

    db_session.refresh(new_workflow)

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 409


def test_create_workflow_invalid_regions(client):

    payload = create_workflow_payload(region_codes=["INVALID_REGION"])

    response = client.post("/workflows/", json=payload)

    assert response.status_code == 409


def test_delete_workflow_success(client, db_session, workflow_factory):

    # Create a workflow to delete
    new_workflow = workflow_factory(name="Workflow to Delete", description="Workflow Description")
    db_session.add(new_workflow)
    db_session.commit()
    db_session.refresh(new_workflow)

    workflow_id = new_workflow.id

    response = client.delete(f"/workflows/{workflow_id}")

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": f"Workflow with ID {workflow_id} has been deleted."
    }

    # Verify that the workflow is marked as deleted in the database
    deleted_workflow = db_session.get(Workflow, workflow_id)
    assert deleted_workflow.is_deleted is True


def test_delete_workflow_not_found(client):

    workflow_id = 99999  # Assuming this ID does not exist or is already deleted

    response = client.delete(f"/workflows/{workflow_id}")

    assert response.status_code == 404
    assert response.json()['error']['code'] == "WORKFLOW_NOT_FOUND"


def test_update_workflow_success(client, db_session, workflow_factory):

    # Create a workflow to update
    new_workflow = workflow_factory(name="Workflow to Update", description="Workflow Description")
    db_session.add(new_workflow)
    db_session.commit()
    db_session.refresh(new_workflow)

    workflow_id = new_workflow.id

    payload = create_workflow_payload(name="Updated Workflow Name", description="Updated Description")

    response = client.post(f"/workflows/{workflow_id}/update", json=payload)

    assert response.status_code == 200
    assert response.json()['name'] == "Updated Workflow Name"
    assert response.json()['description'] == "Updated Description"

    # Verify that the workflow is updated in the database
    updated_workflow = db_session.get(Workflow, workflow_id)
    assert updated_workflow.name == "Updated Workflow Name"
    assert updated_workflow.description == "Updated Description"


def test_update_workflow_not_found(client):

    workflow_id = 99999  # Assuming this ID does not exist or is already deleted

    payload = create_workflow_payload(name="Updated Workflow Name", description="Updated Description")

    response = client.post(f"/workflows/{workflow_id}/update", json=payload)

    assert response.status_code == 404
    assert response.json()['error']['code'] == "WORKFLOW_NOT_FOUND"
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.workflow import Workflow


class WorkflowRepository:
    """Workflow repository logic"""

    def __init__(self, session: Session):
        self.session = session

    def create_new_workflow(self, workflow: Workflow):
        # Create a new workflow
        self.session.add(workflow)
        self.session.flush()
        return workflow

    def get_workflow_by_id(self, workflow_id: int):
        # Retrieve a workflow by its ID
        stmt = select(Workflow).where(Workflow.id == workflow_id)
        result = self.session.execute(stmt).scalar_one_or_none()
        return result

    def list_all_workflows(self):
        "Fetch all the workflows"
        stmt = select(Workflow)
        result = self.session.execute(stmt).scalars().all()
        return result

    def update(self):
        pass

    def get_workflow_by_name_and_org_unit(self, name: str, org_unit_id: int):
        "Retrieve the workflow by name and org_unit_id"
        stmt = (
            select(Workflow)
            .where(
                Workflow.name == name,
                Workflow.org_unit_id == org_unit_id, 
                Workflow.is_deleted == False
            )
        )
        result = self.session.execute(stmt).scalar_one_or_none()
        return result

    def delete_workflow(self, workflow_id: int):
        pass
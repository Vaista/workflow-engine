from app.repositories.workflow_repository import WorkflowRepository
from app.schemas.workflows import WorkflowCreate
from app.schemas.auth import CurrentUser
from app.models.workflow import Workflow
from app.api.deps import get_db
from fastapi import Depends
from app.exceptions.exceptions.workflows import WorkflowAlreadyExists


class WorkflowService:
    def __init__(self, workflow_repository: WorkflowRepository, session = Depends(get_db)):
        self.workflow = workflow_repository
        self.session = session

    def create_workflow(self, workflow: WorkflowCreate, current_user: CurrentUser):
        """Create a new workflow"""

        try:
            # Check if the workflow already exists
            existing_workflow = self.workflow.get_workflow_by_name_and_org_unit(workflow, current_user.org_unit_id)

            if existing_workflow:
                raise WorkflowAlreadyExists()
            
            # Create a workflow model
            new_workflow = Workflow(
                org_id = current_user.org_id,
                org_unit_id = current_user.org_unit_id,
                name = workflow.name,
                description = workflow.description,
                created_by = current_user.user_id
            )

            # Create the workflow
            created = self.workflow.create_new_workflow(new_workflow)
            self.session.refresh(created)

            # Add workflow regions


            self.session.commit()

        except:
            self.session.rollback()
            raise
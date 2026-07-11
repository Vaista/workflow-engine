from app.repositories.workflow_repository import WorkflowRepository
from app.schemas.workflows import WorkflowCreate
from app.schemas.auth import CurrentUser


class WorkflowService:
    def __init__(self, workflow_repository: WorkflowRepository):
        self.workflow = workflow_repository

    def create_workflow(self, workflow: WorkflowCreate, current_user: CurrentUser):
        """Create a new workflow"""

        try:
            # Begin a transaction (if using a database transaction)

            # Check if the workflow already exists
            existing_workflow = self.workflow.get_by_name_and_org_unit(workflow, current_user.org_unit_id)

            if existing_workflow:
                raise ValueError("Workflow already exists")

            # Create the workflow
            created = self.workflow.create(workflow.name, current_user)

        except Exception as e:
            # Rollback any changes if necessary (if using a database transaction)
            raise ValueError(f"Error creating workflow: {str(e)}")
        else:
            # Commit the transaction if everything is successful (if using a database transaction)
            return created
    
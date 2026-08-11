from sqlalchemy.orm import Session

from app.repositories.workflow_repository import WorkflowRepository, WorkflowRegionRepository
from app.repositories.region_repository import RegionRepository
from app.schemas.workflows import WorkflowCreate, WorkflowFetch, FetchWorkflowResponse
from app.schemas.auth import CurrentUser
from app.models.workflow import Workflow
from app.exceptions.exceptions.workflows import WorkflowAlreadyExists, WorkflowNotFound


class WorkflowService:
    def __init__(
            self, 
            workflow_repository: WorkflowRepository, 
            region_repository: RegionRepository, 
            workflow_region_repository: WorkflowRegionRepository, 
            session: Session
        ):
        
        self.workflow_repository = workflow_repository
        self.region_repository = region_repository
        self.workflow_region_repository = workflow_region_repository
        self.session = session

    def create_workflow(self, workflow: WorkflowCreate, current_user: CurrentUser):
        """Create a new workflow"""

        try:
            # Check if the workflow already exists
            existing_workflow = self.workflow_repository.get_workflow_by_name_and_org_unit(workflow.name, current_user.org_unit_id)

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
            created_workflow = self.workflow_repository.create_new_workflow(new_workflow)

            # Add workflow regions
            region_codes = workflow.region_codes
            
            regions = self.region_repository.get_by_codes(region_codes)

            # Create workflow regions
            self.workflow_region_repository.create_workflow_region_mapping(created_workflow, regions)

            self.session.commit()

            self.session.refresh(created_workflow)

            return created_workflow
        
        except Exception:
            self.session.rollback()
            raise


    def update_workflow(self, workflow_id: int, workflow: WorkflowCreate, current_user: CurrentUser):
        """Update an existing workflow"""

        existing_workflow = self.workflow_repository.get_workflow_by_id(workflow_id)

        if not existing_workflow:
            raise WorkflowNotFound()

        # Update the workflow details
        existing_workflow.name = workflow.name
        existing_workflow.description = workflow.description
        existing_workflow.updated_by = current_user.user_id

        # Update the workflow
        updated_workflow = self.workflow_repository.update(existing_workflow)

        # Update workflow regions
        region_codes = workflow.region_codes
        
        regions = self.region_repository.get_by_codes(region_codes)

        # Update workflow regions
        self.workflow_region_repository.update_workflow_region_mapping(updated_workflow, regions)

        self.session.commit()

        self.session.refresh(updated_workflow)

        return updated_workflow
    

    def fetch_workflow(self, workflow: WorkflowFetch):

        rows = self.workflow_repository.fetch_workflow_by_search_criteria(workflow)

        return [
            FetchWorkflowResponse(
                id=workflow.id,
                org_id=workflow.org_id,
                org_name=org_name,
                org_unit_id=workflow.org_unit_id,
                org_unit_name=org_unit_name,
                name=workflow.name,
                description=workflow.description,
                is_active=workflow.is_active,
                created_on=workflow.created_on,
                created_by=workflow.created_by,
                created_by_name=created_by_name,
            )
            for workflow, created_by_name, org_name, org_unit_name in rows
        ]


    def delete_workflow(self, workflow_id: int, current_user: CurrentUser):
        """Delete a workflow by its ID"""

        self.workflow_repository.delete(workflow_id, current_user.user_id)

        return {"status": "success", "message": f"Workflow with ID {workflow_id} has been deleted."}
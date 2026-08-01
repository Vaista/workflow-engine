from fastapi import Depends
from sqlalchemy.orm import Session

from app.repositories.workflow_repository import WorkflowRepository, WorkflowRegionRepository
from app.repositories.region_repository import RegionRepository
from app.schemas.workflows import WorkflowCreate
from app.schemas.auth import CurrentUser
from app.models.workflow import Workflow
from app.exceptions.exceptions.workflows import WorkflowAlreadyExists


class WorkflowService:
    def __init__(
            self, 
            workflow_repository: WorkflowRepository, 
            region_repository: RegionRepository, 
            workflow_region_repository: WorkflowRegionRepository, 
            session: Session
        ):
        
        self.workflow = workflow_repository
        self.regions = region_repository
        self.workflow_regions = workflow_region_repository
        self.session = session

    def create_workflow(self, workflow: WorkflowCreate, current_user: CurrentUser):
        """Create a new workflow"""

        try:
            # Check if the workflow already exists
            existing_workflow = self.workflow.get_workflow_by_name_and_org_unit(workflow.name, current_user.org_unit_id)

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
            created_workflow = self.workflow.create_new_workflow(new_workflow)

            # Add workflow regions
            region_codes = workflow.region_codes
            
            regions = self.regions.get_by_codes(region_codes)

            # Create workflow regions
            self.workflow_regions.create_workflow_region_mapping(created_workflow, regions)

            self.session.commit()

            self.session.refresh(created_workflow)

            return created_workflow
        
        except Exception:
            self.session.rollback()
            raise
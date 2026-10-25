from sqlalchemy.orm import Session

from app.exceptions.exceptions.workflows import DuplicateWorkflowStepNumber, InvalidWorkflowStepNumber, WorkflowNotFound, WorkflowStepNotFound
from app.repositories.workflow_step_repository import WorkflowStepRepository
from app.repositories.workflow_repository import WorkflowRepository
from app.schemas.workflow_steps import WorkflowStepCreate


class WorkflowStepService:
    def __init__(
            self, 
            workflow_repository: WorkflowRepository,
            workflow_step_repository: WorkflowStepRepository,
            session: Session):
        self.session = session
        self.workflow_repository = workflow_repository
        self.workflow_step_repository = workflow_step_repository


    def create_workflow_step(self, workflow_id: int, step: WorkflowStepCreate):
        try:
            # Check if the workflow exists
            workflow = self.workflow_repository.get_workflow_by_id(workflow_id)
            if not workflow:
                 raise WorkflowNotFound()

            # Check if the step number already exists for the given workflow
            existing_step = self.workflow_step_repository.get_workflow_step_by_number(workflow_id, step.step_number)
            if existing_step:
                raise DuplicateWorkflowStepNumber()

            # Check if the step number is just greater than the last step number for the given workflow
            last_step = self.workflow_step_repository.get_last_workflow_step(workflow_id)
            if last_step and step.step_number != last_step.step_number + 1:
                raise InvalidWorkflowStepNumber()

            # Create the workflow step
            new_step = self.workflow_step_repository.create_workflow_step(workflow_id, step)

            self.session.commit()

            return new_step
        
        except Exception as e:
            self.session.rollback()
            raise e

    def update_workflow_step(self, workflow_id: int, step: WorkflowStepCreate):
        try:
            # Check if the workflow exists
            workflow = self.workflow_repository.get_workflow_by_id(workflow_id)
            if not workflow:
                raise WorkflowNotFound()

            # Check if the step number already exists for the given workflow (excluding the current step)
            existing_step = self.workflow_step_repository.get_workflow_step_by_number(workflow_id, step.step_number)
            if not existing_step:
                raise WorkflowStepNotFound()

            # Update the workflow step
            updated_step = self.workflow_step_repository.update_workflow_step(workflow_id, step)

            self.session.commit()

            return updated_step
        
        except Exception as e:
            self.session.rollback()
            raise e


    def delete_workflow_step(self, workflow_id: int, step_number: int):
        try:
            # Check if the workflow exists
            workflow = self.workflow_repository.get_workflow_by_id(workflow_id)
            if not workflow:
                raise WorkflowNotFound()

            # Check if the step number exists for the given workflow
            existing_step = self.workflow_step_repository.get_workflow_step_by_number(workflow_id, step_number)
            if not existing_step:
                raise WorkflowStepNotFound()

            # Delete the workflow step
            self.workflow_step_repository.delete_workflow_step(workflow_id, step_number)
            
            self.session.commit()

            return existing_step
        
        except Exception as e:
            self.session.rollback()
            raise e
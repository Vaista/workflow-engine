from sqlalchemy.orm import Session

from app.models.workflow import WorkflowStep
from app.schemas.workflow_steps import WorkflowStepCreate


class WorkflowStepRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_workflow_step(self, workflow_id: int, step: WorkflowStepCreate):

        new_step = WorkflowStep(
            workflow_id=workflow_id,
            step_number=step.step_number,
            step_name=step.step_name,
            step_description=step.step_description,
            step_config=step.step_config
        )
        self.session.add(new_step)
        self.session.flush()

        return new_step

    def update_workflow_step(self, workflow_id: int, step: WorkflowStepCreate):
        existing_step = self.session.query(WorkflowStep).filter_by(workflow_id=workflow_id, step_number=step.step_number).first()
        if existing_step:
            existing_step.step_number = step.step_number
            existing_step.step_name = step.step_name
            existing_step.step_description = step.step_description
            existing_step.step_config = step.step_config

            self.session.flush()

        return existing_step

    def get_workflow_step_by_number(self, workflow_id: int, step_number: int):
        return self.session.query(WorkflowStep).filter_by(workflow_id=workflow_id, step_number=step_number).first()

    def get_last_workflow_step(self, workflow_id: int):
        return self.session.query(WorkflowStep).filter_by(workflow_id=workflow_id).order_by(WorkflowStep.step_number.desc()).first()

    def delete_workflow_step(self, workflow_id: int, step_number: int):
        step = self.get_workflow_step_by_number(workflow_id, step_number)
        if step:
            self.session.delete(step)
            self.session.flush()
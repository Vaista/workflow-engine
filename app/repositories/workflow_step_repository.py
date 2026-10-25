from sqlalchemy.orm import Session

from app.models.workflow import WorkflowStep


class WorkflowStepRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_workflow_step(self, workflow_id: int, step):

        new_step = WorkflowStep(
            workflow_id=workflow_id,
            step_number=step.step_number,
            step_name=step.step_name,
            step_description=step.step_description,
            step_config=step.step_config
        )
        self.session.add(new_step)
        self.session.commit()
        self.session.refresh(new_step)
        return new_step

    def get_workflow_step_by_number(self, workflow_id: int, step_number: int):
        return self.session.query(WorkflowStep).filter_by(workflow_id=workflow_id, step_number=step_number).first()

    def get_last_workflow_step(self, workflow_id: int):
        return self.session.query(WorkflowStep).filter_by(workflow_id=workflow_id).order_by(WorkflowStep.step_number.desc()).first()
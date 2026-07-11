from app.schemas.workflows import WorkflowCreate
from app.schemas.auth import CurrentUser


class WorkflowRepository:
    """Workflow repository logic"""
    def __init__(self):
        pass

    def create(self, workflow: WorkflowCreate, current_user: CurrentUser):
        pass

    def get_by_id(self):
        pass

    def list(self):
        pass

    def update(self):
        pass

    def get_by_name_and_org_unit(self, name: str, org_unit_id: int):
        pass